import socket

class JWebApp:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.routes = {}
    
    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def Run(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.host, self.port))
        serverSocket.listen(5)

        while True:
            clientSocket, clientAddress = serverSocket.accept()
            requestData = clientSocket.recv(1024).decode()

            if requestData:
                method, path, *_ = requestData.split("\r\n")[0].split()
                handler = self.routes.get(path)
                if handler:
                    response = handler()
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"
                clientSocket.sendall(response.encode())

            clientSocket.close()
