from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_app.auth import login_required
from flask_app.db import get_db

from third_party.cube_main.rubik.cube import Cube
from third_party.cube_main.rubik.solve import Solver

bp = Blueprint('cube', __name__)


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
    flat_string = request.args.get('flat_string')
    solution = None
    if flat_string:
        cube = Cube(flat_string)
        solver = Solver(cube)
        solver.solve()
        solution = solver.moves

    return render_template('cube/flat_string.html', flat_string=flat_string, solution=solution)


@bp.route('/pics')
def pics():
    return render_template('cube/pic.html')