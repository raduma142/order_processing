from tkinter import *
import socket, time
from threading import Thread
from functools import partial

# Encrypt message
def message_encrypt(msg):
    msg_coded = bytes(msg, encoding="utf-8")
    return msg_coded

# Decrypt messages
def message_descrypt(msg_coded):
    msg = msg_coded.decode('utf-8', 'replace')
    return msg   

# Sending a socket
class socket_sending():    
    def socket_send(self):
        HOST = self.server_host  # The server's hostname or IP address
        PORT = self.server_port  # The port used by the server
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        while True:
            if (self.data_send != None):
                self.message_encrypt()
                s.sendall(self.data_send)
                self.data_send = None
    
    # Request a product
    def make_request(self):
        self.data_send = self.buttons_info[0]
    
    # Encrypt message
    def message_encrypt(self):
        self.data_send = bytes(self.data_send , encoding="utf-8")
    
    # Decrypt messages
    def message_descrypt(self, msg_coded):
        msg = msg_coded.decode('utf-8', 'replace')
        return msg
    
    def __init__(self, a, b):
        self.data_send = ""
        self.server_host = a
        self.server_port = b
        
        self.th_socket_send = Thread(target=self.socket_send, args=())
        self.th_socket_send.start()        

# Receive a socket
class socket_receiving():
    
    # Encrypt message
    def message_encrypt(msg):
        msg_coded = bytes(msg, encoding="utf-8")
        return msg_coded
    
    # Decrypt messages
    def message_descrypt(msg_coded):
        msg = msg_coded.decode('utf-8', 'replace')
        return msg    
    
    def socket_receive(self):
        HOST = self.server_host  # The server's hostname or IP address
        PORT = self.server_port  # The port used by the server
    
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
                        print(msg)
                        self.data.append(data)
                        data = None
            finally:
                conn.close()
        finally:
            s.close()
    
    def __init__(self, a, b):
        self.data_send = ""
        self.server_host = a
        self.server_port = b
        
        self.data = []
        
        self.th_socket_recv = Thread(target=self.socket_receive, args=())
        self.th_socket_recv.start()      

class worker_window():
    def __init__(self):
        #Init data
        self.server_host = "127.0.0.1"
        self.server_port = 9091
        self.client_host = ""
        self.client_port = 9090
        self.button_number = 0
        self.buttons_info = []
        self.password = ""
        
        self.init_data()
        self.sending_agent = socket_sending(self.server_host, self.server_port)
        time.sleep(1)
        self.receiving_agent = socket_receiving(self.server_host, self.server_port)
        
        self.sending_agent.data_send = "password"
        
        self.main_window = None
        self.login_window = None
        self.settings_window = None
        
        self.show_login_window()
        
        self.login_window.mainloop()
    
    def init_data(self):
        f = open("settings.txt")
        
        text = f.read()
        text = text.split('\n')
        
        self.server_host = text[0]
        self.server_port = int(text[1])
        self.client_host = text[2]
        self.client_port = int(text[3])
        self.button_number = int(text[4])
        
        n = 5
        self.buttons_info = []
        for i in range(self.button_number):
            self.buttons_info.append(text[n])
            n += 1
        self.password = text[n]
        print(text)
        f.close()        
    
    def show_main_window(self):
        try: self.login_window.destroy()
        except: pass
        try: self.settings_window.destroy()
        except: pass
        
        self.main_window = Tk()
        self.main_window.title("Подтверждение заказов")
        self.main_window.geometry('800x600')
        self.main_window["bg"] = "gray99"
        
        btn_password = Button(self.main_window, text="Обновить", bg="light gray", command=self.show_login_window)
        btn_password.pack(side=TOP, fill=X)
    
        btn_settings = Button(self.main_window, text="Настройки", bg="light gray", command=self.show_settings_window)
        btn_settings.pack(side=RIGHT, fill=Y)
    
        btn_password = Button(self.main_window, text="Выход", bg="light gray", command=self.show_login_window)
        btn_password.pack(side=LEFT, fill=Y)
        
        for i in range(self.button_number):
            temp = self.buttons_info[i].split(";")
            entryText = StringVar()
            entryText.set(temp)  
            ent_order = Entry(self.settings_window, textvariable=entryText, width=50)          
            ent_order.pack(fill=X)            
            btn_order = Button(self.main_window, text='Подтвердить', bg="SteelBlue1", command=partial(self.btn_click, i))
            btn_order.pack(fill=X)
    
    def show_settings_window(self):
        try: self.main_window.destroy()
        except: pass
        self.settings_window = Tk()
        self.settings_window.title("Настройки")
        self.settings_window.geometry('800x600')
        self.settings_window["bg"] = "gray99"
    
        lbl_host = Label(self.settings_window, text="Сервер: ХОСТ")
        lbl_host.pack(fill=X)
        enter_host = Entry(self.settings_window, width=50)
        enter_host.pack(fill=X)
    
        lbl_port = Label(self.settings_window, text="Сервер: ПОРТ")
        lbl_port.pack(fill=X)
        enter_port = Entry(self.settings_window, width=50)
        enter_port.pack(fill=X)
        
        btn_close = Button(self.settings_window, bg="SteelBlue1", text="Сохранить", command=self.show_main_window)
        btn_close.pack(fill=X)
        
        self.settings_window.protocol("WM_DELETE_WINDOW", self.main_window)
    
    def show_login_window(self):
        try: self.main_window.destroy()
        except: pass
        try: self.settings_window.destroy()
        except: pass
        
        self.login_window = Tk()
        self.login_window.title("Авторизация")
        self.login_window.geometry('800x600')
        self.login_window["bg"] = "light yellow"
        
        lbl_user = Label(self.login_window, text=" ", height=2)
        lbl_user.pack(fill=X)
        
        lbl_user = Label(self.login_window, text="Поставщик")
        lbl_user.pack(fill=X)
        
        self.enter_user = Entry(self.login_window, width=50)
        self.enter_user.pack(fill=X)        
        
        lbl_user = Label(self.login_window, text="Пароль")
        lbl_user.pack(fill=X)
        
        self.enter_password = Entry(self.login_window, width=50)
        self.enter_password.pack(fill=X)
        
        btn_login = Button(self.login_window, text="Войти", bg="sky blue", command=self.check_password)
        btn_login.pack(fill=X)
    
    def btn_click(self, i):
        self.sending_agent.data_send = "CONFIRM;" + self.buttons_info[i]
    
    def check_password(self):
        password = self.enter_password.get()
        if (password == self.password):
            self.show_main_window()

def main():
    worker_window()
main()