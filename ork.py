import sys
import ssl
import socket 
import tkinter 

WIDTH, HEIGHT = 800, 600

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

class Browser: 
    def __init__(self): 
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window, 
            width=WIDTH, 
            height=HEIGHT
        )
        self.canvas.pack()

    def load(self, url):
        body = self.request()
        self.show(body)
        self.canvas.create_rectangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150) 
        self.canvas.create_text(200, 150, text="Hi!")

 

if __name__ == "__main__": 
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
    # url.load()



