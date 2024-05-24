from JWeb import *

app = JWebApp("0.0.0.0", 1337)

@app.route("/")
def index():
    return Response(200, "<h1>Hello world!</h1>")

@app.route("/test.abc")
def index():
    return Response(200, "<h1>Hi world!</h1>")

app.Run()
