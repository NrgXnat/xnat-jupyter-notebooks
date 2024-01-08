import panel as pn

def hello_world():
    return "Hello, World! This is a Panel app."

app = pn.Column(hello_world)

app.servable()
