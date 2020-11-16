# -*- coding: utf8 -*-

import socket

HOST        = '10.0.0.86'
PORT        = 51000

def com_send(mess):
    while True:
        try:
            # 通信の確立
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))

            # メッセージ送信
            sock.send(mess.encode('utf-8'))

            # 通信の終了
            sock.close()
            break

        except:
            print ('retry: ' + mess)

if __name__ == "__main__":
    com_send("temp=50.8\n")
