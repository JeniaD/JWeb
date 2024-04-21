import socket
import signal
import sys
from .response import Response

class Config:
    showPoweredBy = True

class JWebApp:
    def __init__(self, host="127.0.0.1", port=8080, config=""):
        self.config = Config()
        if config: pass

        self.host = host
        self.port = port
        self.routes = {}

        self.serverSocket = None

        self.frameworkName = "JWeb"
        
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

        clientSocket = None
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
                
                print(f"{method} {path} - {response.status}")
                clientSocket.sendall(response.Raw())

                clientSocket.close()
