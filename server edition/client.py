import socket
import multiprocessing


def client(message, client_sock):
    '''client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 53210))
    '''
    client_sock.sendall(bytes(message, encoding="utf-8"))
    data = client_sock.recv(1024)
    print('Bot:',  data.decode("utf-8"))


'''client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 53210))
client_sock.sendall(bytes(input("Вы"), encoding="utf-8"))
data = client_sock.recv(1024)
client_sock.close()'''
if __name__ == "__main__":
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 53210))
    while True:
        msg = input().lower()
        if msg == "0" or msg == "exit":
            client_sock.close()
            break
        elif msg == "настройки" or msg == "setting":
            pass
        client(msg, client_sock)
    '''msg = [["hello", "hi"], ["what are you doing?", "Weeee"]]
    multiprocessing.freeze_support()
    for m in msg:
        print(1)
        multiprocessing.Process(target=client, args=(m,)).start()
        print(0)'''
