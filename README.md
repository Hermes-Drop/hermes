# Hermes - Python server for Hermes control systems

## Getting Started with Backend

The Hermes server will be handled with python websockets to send and receive instructions; which works with OpenCV for object detection.

- `main.py` will be the main backend code (abstracting python files makes it easier to make modular).

### Directory Structure
```
hermes
├── venv        # Activate virtual python environment (make sure to activate this before starting to code)
└── servo_control               # Arduino code directory
    ├── servos.py               # arduino code here
└── camera_control              # OpenCV code directory
    ├── camera.py               # camera code here
├── main.py                     # main parent source code
├── Requirements.txt            # install the requirements AFTER initalizing the venv
└── .gitignore          # Ensure node_modules is ignored
```

### How to Get It Running

1. If you do not have Python and pip installed, install them first.

2. Initialize the virtual environment
    ```bash
    python3 (or python) -m venv venv
    source ./venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r Requirements.txt
    ```

3. Start the hermes server:
    ```bash
    python main.py
    ```