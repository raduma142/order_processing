import socket, time
from threading import Thread

server_host = "127.0.0.1"
server_port = 9091
client_host = ""
client_port = 9090
button_number = 0
buttons_info = []
# Вид Наименование Кол-во Пункт Адрес
password = ""

data_send = ""
stop_send = False

# Initialization
def init():
    global server_host, server_port, client_host, client_port
    global button_number, buttons_info, password
    
    f = open("settings.dat")
    
    f.readline()
    int(f.readline())
    f.readline()
    int(f.readline())
    button_number = int(f.readline())
    buttons_info = []
    for i in range(button_number):
        buttons_info.append(f.readline())
    password = f.readline()
    f.close()

# Encrypt message
def message_encrypt(msg):
    msg_coded = bytes(msg, encoding="utf-8")
    return msg_coded

# Decrypt messages
def message_descrypt(msg_coded):
    msg = msg_coded.decode('utf-8', 'replace')
    return msg

# Sending a socket
def socket_send():
    global data_send
    HOST = server_host  # The server's hostname or IP address
    PORT = server_port  # The port used by the server

    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while True:
        if (data_send != None) and (len(data_send) > 5):
            msg = message_encrypt(data_send)
            s.sendall(msg)
            data_send = None


# Getting a socket
def soket_receive():
    HOST = client_host  # The server's hostname or IP address
    PORT = client_port  # The port used by the server

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        data = None
        while data == None:
            data = conn.recv(1024)
    conn.close()
    msg = message_descrypt(data)
    return msg

# Request a product
def make_request():
    global data_send
    data_send = buttons_info[0]