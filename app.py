from os import name
from full_stack import create_app
# from pyfladesk import init_gui

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    # init_gui(app, window_title="UIISS", icon="logo.png")
