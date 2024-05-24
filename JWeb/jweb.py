import socket
import signal
import sys
import os
import re
from .response import Response

class Config:
    showPoweredBy = True
    codeDir = "src"

class JWebApp:
    def __init__(self, host="127.0.0.1", port=8080, config=""):
        self.config = Config()
        if config: pass

        self.host = host
        self.port = port
        self.routes = {}

        self.serverSocket = None

        self.frameworkName = "JWeb"

        self.LoadFiles()
    
    def _interpret(self, line):
        return eval(line)
    
    def _exec(self, jwebCode):
        lines = jwebCode.split('\n')
        output = ""
        for line in lines:
            res = self._interpret(line)
            if res: output += res
        return output

    def _run(self, code):
        pattern = r"<\?jweb(.*?)\?>"
        if "<?jweb" in code:
            scripts = re.findall(pattern, code)
            for script in scripts:
                res = self._exec(script)
                code.replace(f"<?jweb {script} ?>", res if res else '', 1)
        return code

    def LoadFiles(self, path=""):
        for item in os.listdir(os.path.join(self.config.codeDir, path)):
            fullPath = os.path.join(self.config.codeDir, path, item)

            if os.path.isdir(fullPath):
                self.LoadFiles(os.path.join(path, item))
            elif os.path.isfile(fullPath):
                with open(fullPath, 'r') as file:
                    content = file.read()
                
                print("Setting up an endpoint", os.path.join(path, item))

                def func(): return Response(200, self._run(content), contentType="text/html; charset=utf-8")

                # WARNING: saving functions from local LoadFiles might not be
                # a good idea. Also, adding '/' + ... could be a mistake

                self.routes['/' + os.path.join(path, item)] = func
                if item == "index.jweb":
                    self.routes['/' + path] = func
                
        
    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def _middleware(self, response):
        if self.config.showPoweredBy:
            response.AddHeaders({"X-Powered-By": self.frameworkName})
        
        return response
    
    def ShutdownHandler(self, signum, frame):
        print("Shutting down server...")
        if self.serverSocket:
            self.serverSocket.close()
        sys.exit(0)

    def Run(self):
        signal.signal(signal.SIGINT, self.ShutdownHandler)
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.host, self.port))
        serverSocket.listen(5)

        print(f"Listening on {self.host}:{self.port}")
        print("Loaded routes:")
        for route in self.routes:
            print(f" \"{route}\" =>", self.routes[route])
        print()

        while True:
            clientSocket, clientAddress = serverSocket.accept()
            requestData = clientSocket.recv(1024).decode()

            if requestData:
                method, path, *_ = requestData.split("\r\n")[0].split()
                handler = self.routes.get(path)

                if handler:
                    response = handler()
                else:
                    response = Response(404, "Not found")
                
                if isinstance(response, str):
                    response = Response(200, response)
                
                response = self._middleware(response)
                print(f"{method} {path} - {response.status}")
                clientSocket.sendall(response.Raw())

                clientSocket.close()
