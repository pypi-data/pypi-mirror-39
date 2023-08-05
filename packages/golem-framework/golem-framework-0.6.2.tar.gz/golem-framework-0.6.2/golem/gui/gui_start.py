"""A function to start the GUI application."""
from golem.core import test_execution
from golem import gui


def run_gui(port):
    host = '0.0.0.0'
    gui.root_path = test_execution.root_path
    # Note, some features won't work if the golem gui is not
    # started with debug = True
    gui.app.run(debug=True, host=host, port=port)
