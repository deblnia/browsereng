import socket 

class URL: 
    def __init__(self, url): 
        self.scheme, url = url.split("://", 1)
        assert self.scheme == "http"
        if "/" not in url: 
            url += "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url
        
    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, 80))
        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host} \r\n"
        request += "\r\n"
        print(request)
        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

ex = URL("http://www.google.com")
ex.request()