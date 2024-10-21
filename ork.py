import sys
import ssl
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
        # print(request)
        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True: 
            line = response.readline()
            if line == "\r\n": break 
            print(line)
            print("test", line.split(":" , 1))
            try: 
                header, value = line.split(":", 1)
                response_headers[header.casefold()] = value.strip()
                assert "transfer-encoding" not in response_headers 
                assert "content-encoding" not in response_headers
                content = response.read()
                s.close()
                return content 
            except ValueError: 
                print("ValueError: Some line in the response not the right length")
        
    def show(self, body):
        in_tag = False 
        for c in body: 
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False 
            elif not in_tag: 
                print(c, end="")
    
    def load(self): 
       body = self.request()
       self.show(body)

if __name__ == "__main__": 
    url = URL(sys.argv[1])
    url.load()



