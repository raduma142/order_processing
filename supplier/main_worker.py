from tkinter import *
from client_worker import *

def main_window():
    init()

    th_socket_send = Thread(target=socket_send, args=())
    th_socket_send.start()

    window = Tk()
    window.title("Обработка заказов")
    window.geometry('400x250')

    btn_settings = Button(window, text="Настройки", command=clicked_settings)
    btn_settings.grid(column=0, row=0)

    btn_password = Button(window, text="Вход", command=clicked_password)
    btn_password.grid(column=1, row=0)

    btn_order = Button(window, text="Заказать", command=make_request)
    btn_order.grid(column=2, row=0)


    window.mainloop()


def clicked_settings():
    settings = Tk()

    lbl_org = Label(settings, text="Наименование пункта")
    lbl_org.grid(column=0, row=0)
    enter_org = Entry(settings, width=50)
    enter_org.grid(column=1, row=0)

    lbl_adress = Label(settings, text="Адрес")
    lbl_adress.grid(column=0, row=1)
    enter_adress = Entry(settings, width=50)
    enter_adress.grid(column=1, row=1)

    lbl_host = Label(settings, text="Сервер: ХОСТ")
    lbl_host.grid(column=0, row=2)
    enter_host = Entry(settings, width=50)
    enter_host.grid(column=1, row=2)

    lbl_port = Label(settings, text="Сервер: ПОРТ")
    lbl_port.grid(column=0, row=3)
    enter_port = Entry(settings, width=50)
    enter_port.grid(column=1, row=3)

    btn_minus = Button(settings, text="-")
    btn_minus.grid(column=0, row=4)

    lbl_number = Label(settings, text="0")
    lbl_number.grid(column=1, row=4)

    btn_plus = Button(settings, text="+")
    btn_plus.grid(column=2, row=4)




def clicked_password():
    password = Tk()



def main():
    main_window()

main()