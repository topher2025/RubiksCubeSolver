# RubiksCubeSolver
It solves Rubiks Cubes

## Target Project Structure
```
project/
│
├── cube/                     # Core Rubik’s Cube logic
│   ├── __init__.py
│   ├── cube.py               # Cube class
│   ├── solver.py             # Solver class
│   └── algorithms/           # Optional: Kociemba, A*, IDA*, etc.
│
├── vision/                   # CV model for cube color extraction
│   ├── __init__.py
│   ├── model.py              # ML model loading + inference
│   ├── preprocessing.py
│   └── utils.py
│
├── api/                      # Flask backend (Blueprints recommended)
│   ├── __init__.py           # create_app(), register blueprints
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── cube_routes.py    # endpoints: /solve, /state, /upload
│   │   └── vision_routes.py  # endpoints: /detect
│   ├── services/
│   │   ├── cube_service.py   # orchestrates Cube + Solver
│   │   └── vision_service.py # orchestrates CV model
│   └── config.py
│
├── frontend/                 # Website UI
│   ├── static/               # JS, CSS, images
│   └── templates/            # HTML (Jinja2)
│
├── tests/                    # Unit tests
│   ├── test_cube.py
│   ├── test_solver.py
│   ├── test_api.py
│   └── test_vision.py
│
├── run.py                    # Entry point for Flask
├── requirements.txt
└── README.md

```

df
