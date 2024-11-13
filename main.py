import flet as ft
from pythonosc import udp_client
from socket import socket, AF_INET, SOCK_DGRAM


def main(page: ft.Page):
    page.title = "UDP/OSC Test SENDER"
    page.window.width = 700
    page.window.height = 300
    def on_mode_change(e):
        if send_mode.value == "osc":
            numberField.input_filter = ft.NumbersOnlyInputFilter()
            numberField.label = "OSC Command (Only numbers are allowed)"
            t2.value = "OSC Command (Only numbers are allowed :))"
        else:
            numberField.input_filter = None
            numberField.label = "UDP Message"
            t2.value = "UDP Message (Any text allowed)"
        page.update()

    def sender(e):
        ip = ip_portField.controls[0].value
        port = int(ip_portField.controls[1].value)
        message = numberField.value
        if message == "":
            return

        if send_mode.value == "osc":
            message = int(message)  # OSCの場合のみ数値に変換
            address = "/value"
            client = udp_client.SimpleUDPClient(ip, port)
            client.send_message(address, message)
            print(f"OSC message sent to {ip}:{port} - Address: {address}, Message: {message}")
        else:
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.sendto(message.encode(), (ip, port))
            print(f"UDP message sent to {ip}:{port} - Message: {message}")
            sock.close()

    t1 = ft.Text(value="", size=12)

    ip_portField = ft.Row([
        ft.TextField(
            label="IP",
            value="127.0.0.1"
        ),
        ft.TextField(
            label="PORT",
            value="7000",
            input_filter=ft.NumbersOnlyInputFilter()
        ),
    ]) 

    t2 = ft.Text(value="OSC Command (Only numbers are allowed :))", size=12)

    numberField = ft.TextField(
        label="UDP Message",
        input_filter=None
    )

    btn = ft.ElevatedButton(text="Send",on_click=sender)

    send_mode = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="udp", label="UDP"),
            ft.Radio(value="osc", label="OSC"),
        ]),
        value="udp",
        on_change=on_mode_change
    )

    page.add(t1, ip_portField, send_mode, numberField, btn)


ft.app(main)
