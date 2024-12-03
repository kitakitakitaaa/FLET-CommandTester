import flet as ft
from pythonosc import udp_client
from socket import socket, AF_INET, SOCK_DGRAM
import json
import os


def main(page: ft.Page):
    page.title = "UDP/OSC Test SENDER"
    page.window.width = 700
    page.window.height = 300
    # 設定ファイルのパスを定義
    CONFIG_FILE = "app_settings.json"
    
    # 設定を読み込む関数
    def load_settings():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    settings = json.load(f)
                    return settings
            except:
                return get_default_settings()
        return get_default_settings()
    
    # デフォルト設定を取得する関数
    def get_default_settings():
        return {
            "ip": "127.0.0.1",
            "port": "7000",
            "mode": "udp",
            "message": ""
        }
    
    # 設定を保存する関数
    def save_settings():
        try:
            settings = {
                "ip": ip_portField.controls[0].value,
                "port": ip_portField.controls[1].value,
                "mode": send_mode.value,
                "message": numberField.value
            }
            print(f"Saving settings: {settings}")  # デバッグ用
            with open(CONFIG_FILE, "w", encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            print(f"Settings saved to {CONFIG_FILE}")  # デバッグ用
        except Exception as e:
            print(f"Error saving settings: {e}")  # エラーメッセージを表示
    
    def window_event_handler(e):
        print("Window event triggered:", e.data)  # デバッグ用
        if e.data == "close":
            print("Close event detected")  # デバッグ用
            save_settings()
            page.window.prevent_close = False  # prevent_closeをFalseに設定
            page.update()  # ページを更新
            page.window.destroy()  # ウィンドウを強制的に破棄
    
    # ページを閉じる時のイベントハンドラを設定
    page.window.prevent_close = True
    page.window.on_event = window_event_handler

    # 保存された設定を読み込む
    settings = load_settings()

    def on_mode_change(e):
        if send_mode.value == "osc":
            numberField.input_filter = None  # 数値制限を解除
            numberField.label = "OSC Message"
            t2.value = "OSC Message (Any text allowed)"
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
            address = "/value"
            client = udp_client.SimpleUDPClient(ip, port)
            # メッセージが数値の場合は数値に変換、そうでない場合は文字列として送信
            try:
                # 整数の場合
                if message.isdigit():
                    message = int(message)
                # 小数の場合
                elif message.replace(".", "", 1).isdigit() and message.count(".") < 2:
                    message = float(message)
            except ValueError:
                # 数値変換できない場合は文字列のまま
                pass
            
            client.send_message(address, message)
            print(f"OSC message sent to {ip}:{port} - Address: {address}, Message: {message} (Type: {type(message)})")
        else:
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.sendto(message.encode(), (ip, port))
            print(f"UDP message sent to {ip}:{port} - Message: {message}")
            sock.close()

    t1 = ft.Text(value="", size=12)

    ip_portField = ft.Row([
        ft.TextField(
            label="IP",
            value=settings["ip"]  # 保存された値を使用
        ),
        ft.TextField(
            label="PORT",
            value=settings["port"],  # 保存された値を使用
            input_filter=ft.NumbersOnlyInputFilter()
        ),
    ]) 

    t2 = ft.Text(value="OSC Command (Only numbers are allowed :))", size=12)

    numberField = ft.TextField(
        label="UDP Message",
        value=settings["message"],  # 保存された値を使用
        input_filter=None,
        on_submit=sender  # エンターキーでの送信を有効にする
    )

    btn = ft.ElevatedButton(text="Send",on_click=sender)

    send_mode = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="udp", label="UDP"),
            ft.Radio(value="osc", label="OSC"),
        ]),
        value=settings["mode"],  # 保存された値を使用
        on_change=on_mode_change
    )

    page.add(t1, ip_portField, send_mode, numberField, btn)


ft.app(main)
