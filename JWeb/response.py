statusNames = {200: "OK", 404: "Not found"}

class Response:
    def __init__(self, status:int, body="", headers={}, contentType="text/plain", version="1.0") -> None:
        self.version = version
        self.status = status
        self.body = body
        self.contentType = contentType

        self.encoding = "utf-8"
        self.headers = headers

        try:
            self.statusName = statusNames[status]
        except IndexError:
            self.statusName = "Unknown"
    
    def AddHeaders(self, headers):
        self.headers += headers
    
    def Raw(self):
        lines = [
            f"HTTP/{self.version} {self.status} {self.statusName}",
            f"Content-Type: {self.contentType}",
            f"Content-Length: {len(self.body)}", # what if body is None?
            f"Connection: close"
        ]

        for header in self.headers:
            lines += [f"{header}: {self.headers[header]}"]
        
        if self.body: lines += [f"\n{self.body}"]

        return "\n".join(lines).encode(self.encoding)
    
    def __repr__(self):
        return f"<Response {self.status} {self.contentType}>"
