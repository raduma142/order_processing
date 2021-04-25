import socket, time
from threading import Thread

server_host = ""
server_port = 9090
client_host = "127.0.0.1"
client_port = 9091
orders_info = []
password = ""

data_send = ""

# Encrypt message
def message_encrypt(msg):
  msg_coded = bytes(msg, encoding = "utf-8")
  return msg_coded

# Decrypt messages
def message_descrypt(msg_coded):
  msg = msg_coded.decode("utf-8", 'replace')
  return msg

# Sending a socket
def soсket_send():
    HOST = client_host  # The server's hostname or IP address
    PORT = client_port  # The port used by the server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        while True:
            if (data_send != None) and (len(data_send) > 5):
                print("RETURN:")
                print(data_send)
                data = message_encrypt(data_send)
                s.sendall(data)
    finally:
        s.close()

# Getting a socket
def soсket_receive():
    HOST = server_host  # The server's hostname or IP address
    PORT = server_port  # The port used by the server
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen()
        try:
            conn, addr = s.accept()
            print('Connected by', addr)
            data = None
            while (True):
                data = conn.recv(1024)
                if (data != None) and (len(data) > 5):
                    msg = message_descrypt(data)
                    orders_info.append(msg)
                    print("REQUEST:")
                    print(msg)
                    if (msg == "password"):
                        #th_socket_send = Thread(target=soсket_send, args=())
                        #th_socket_send.start()
                        data_send = "12345"
                    data = None
        finally:
            conn.close()
    finally:
        s.close()

def main():
  th_socket_receive = Thread(target=soсket_receive, args=())
  th_socket_receive.start()
  input()
  
  
main()