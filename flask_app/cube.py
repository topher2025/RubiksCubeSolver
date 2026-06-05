from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_app.auth import login_required
from flask_app.db import get_db

from third_party.cube_main.rubik.cube import Cube
from third_party.cube_main.rubik.solve import Solver

from vision.rubiks import solve

bp = Blueprint('cube', __name__)

MAX_FILES = 3
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_MIME = {'image/jpeg', 'image/png'}
ALLOWED_EXT = {'.jpg', '.jpeg', '.png'}


def _validate_uploaded_files(files):
    errors = []

    if not files:
        errors.append('Please select at least one image.')
        return errors

    if len(files) > MAX_FILES:
        errors.append(f'Maximum {MAX_FILES} files allowed. You selected {len(files)}.')

    for file in files:
        filename = (file.filename or '').strip()
        if not filename:
            errors.append('Each uploaded file must have a filename.')
            continue

        lower_name = filename.lower()
        if not any(lower_name.endswith(ext) for ext in ALLOWED_EXT):
            errors.append(f'File "{filename}" has unsupported extension.')

        if file.mimetype and file.mimetype not in ALLOWED_MIME:
            errors.append(f'File "{filename}" has unsupported type {file.mimetype}.')

        file.stream.seek(0, 2)
        size = file.stream.tell()
        file.stream.seek(0)
        if size > MAX_FILE_SIZE:
            errors.append(f'File "{filename}" exceeds 5.0 MB limit.')

    return errors


@bp.route('/')
def index():
    cubes = None
    if g.user:
        db = get_db()
        cubes = db.execute(
            'SELECT c.flat_string, uc.last_used'
            ' FROM cubes AS c'
            ' JOIN user_cubes AS uc ON uc.cube_id = c.id'
            ' WHERE uc.user_id = ?'
            ' ORDER BY uc.last_used DESC;',
            (g.user['id'],)
        ).fetchall()
    return render_template('cube/index.html', cubes=cubes)


@bp.route('/flat_string')
def flat_string():
    flat_string = request.args.get('fs')
    if flat_string:
        return redirect(url_for('cube.solution', fs=flat_string))
        
    return render_template('cube/flat_string.html')


@bp.route('/pics', methods=('GET', 'POST'))
def pics():
    if request.method == 'POST':
        files = request.files.getlist('images')
        errors = _validate_uploaded_files(files)
        if errors:
            for error in errors:
                flash(error)
            return render_template('cube/pics.html')

        cube = solve(*files)
        flat_string = cube.flat_str()
        return redirect(url_for('cube.solution', fs=flat_string))
    
    return render_template('cube/pics.html')


@bp.route('/solution')
def solution():
    error = None
    try:
        flat_string = request.args.get('fs')
        cube = Cube(flat_string)
        solver = Solver(cube)
        solver.solve()
        solution = solver.moves
        return render_template('cube/solution.html', solution=solution, fs=flat_string)
    except:
        error = "The cube you entered is invalid"
        flash(error)
        return render_template('cube/solution.html', e=error)
    

@bp.route('/save')
@login_required
def save():    
    db = get_db()
    flat_string = request.args.get('fs')
    if not flat_string:
        flash("No cube provided")
        return redirect(request.referrer or url_for('cube.index'))

    cube = db.execute(
        'SELECT id FROM cubes WHERE flat_string = ?',
        (flat_string,)
    ).fetchone()
    if cube is None:
        cur = db.execute(
            'INSERT INTO cubes (flat_string) VALUES (?)',
            (flat_string,)
        )
        cube_id = cur.lastrowid
    else:
        cube_id = cube['id']

    already_saved = db.execute(
        'SELECT 1 FROM user_cubes WHERE user_id = ? AND cube_id = ?',
        (g.user['id'], cube_id)
    ).fetchone()
    if already_saved:
        flash('You already saved this cube')
        return redirect(request.referrer or url_for('cube.index'))

    db.execute(
        'INSERT INTO user_cubes (user_id, cube_id, last_used) VALUES (?, ?, CURRENT_TIMESTAMP);',
        (g.user['id'], cube_id)
    )
    db.commit()

    flash('Cube saved')
    return redirect(request.referrer or url_for('cube.index'))