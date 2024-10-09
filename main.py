import flet as ft
from pythonosc import udp_client


def main(page: ft.Page):
    page.title = "OSC Test Sender"
    page.window_width = 700
    page.window_height = 300
    def sender(e):
        ip = ip_portField.controls[0].value
        port = int(ip_portField.controls[1].value)
        address = "/value"
        message = int(numberField.value)
        if message == "":
            return
        client = udp_client.SimpleUDPClient(ip, port)
        client.send_message(address, message)
        
        print(f"OSC message sent to {ip}:{port} - Address: {address}, Message: {message}")    

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
    label="OSC Command  ( Only numbers are allowed )",
    input_filter=ft.NumbersOnlyInputFilter()
    )

    btn = ft.ElevatedButton(text="Send",on_click=sender)
    
    page.add(t1,ip_portField,numberField,btn)


ft.app(main)
