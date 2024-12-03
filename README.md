# UDPとOSCのテスター

## 使い方
IPアドレスとポートを入力して、メッセージを送信します。
ウィンドウを閉じると設定が保存されます。

## 注意
OSCの場合は数値のみ送信できます。

## EXE化
```
pyinstaller --onefile main.spec
```

または
```
pyinstaller commandTester.spec
```