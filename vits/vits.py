import socket

class vits():

    def __init__(self) -> None:
        
        self.s=socket.socket()
        self.host = socket.gethostname()
        self.port = 9000
        self.s.connect(('127.0.0.1',9001))
    def sendmsg(self,ques) -> str:
        self.s.send(ques.encode())
        response=self.s.recv(1024)
        dirn=response.decode()
        print(dirn)
        return dirn
    def change(self,ques:str):
        self.s.send(ques.encode())
        return


