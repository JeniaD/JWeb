# JWeb microframework
A minimal microframework for creating simple web applications with ease.

### Build  
You can build and install JWeb yourself. Here's how:  

```bash
# Optional: Use a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the package
pip install -e .

# Verify the installation
pip list
```

## Usage

Using JWeb is straightforward. Here’s an example project structure:
```
Project Name/
    main.py
    src/
        index.jweb
```

The `main.py` file:
```python
from JWeb import JWebApp

app = JWebApp()

@app.route("/hello")
def hello():
    return "hi"

app.Run()
```

Run the application:
```bash
python3 main.py
```

Expected output:
```
Setting up an endpoint index.jweb
Listening on 127.0.0.1:8080
Loaded routes:
 "/index.jweb" => <function JWebApp.LoadFiles.<locals>.func at 0x...>
 "/" => <function JWebApp.LoadFiles.<locals>.func at 0x...>
 "/hello" => <function hello at 0x...>
```

Your app should be running on http://127.0.0.1:8080.