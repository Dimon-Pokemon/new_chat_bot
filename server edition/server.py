import multiprocessing
import second_main
import time
import socket

bot = second_main.create_bot()
trainer = second_main.ListTrainer(bot)

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('', 53210))
serv_sock.listen(10)
print("Сервер работает. Ожидание подключения пользователя")

while True:
    # Бесконечно обрабатываем входящие подключения
    client_sock, client_addr = serv_sock.accept()
    print('Connected by', client_addr)

    while True:
        # Пока клиент не отключился, читаем передаваемые
        # им данные и отправляем их обратно
        data = client_sock.recv(1024)
        data = data.decode("utf-8")
        print(client_addr, data)
        answer = second_main.main(data, bot=bot, trainer=trainer, client=client_addr[0]+":"+client_addr[1])
        if not data:
            # Клиент отключился
            break
        client_sock.sendall(bytes(answer+"\nОтвет корректный? 'Да' или 'Нет':", encoding="utf-8"))
        question_correct_answer = client_sock.recv(1024)
        question_correct_answer_data = question_correct_answer.decode("utf-8")
        if question_correct_answer_data=="нет":
            client_sock.sendall(bytes("Введите корреткный ответ:", encoding="utf-8"))
            correct_answer = client_sock.recv(1024)
            correct_answer = correct_answer.decode("utf-8")
            second_main.learning_based_on_user_input(data, correct_answer, trainer=trainer)

    client_sock.close()
#multiprocessing.freeze_support()
