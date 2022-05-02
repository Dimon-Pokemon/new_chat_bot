import json  # библиотека для работы с json файлами
from chatterbot import ChatBot  # основной класс для чат-бота
from chatterbot.trainers import ListTrainer  # класс для обучения
from chatterbot.conversation import Statement  # хз, что это, но нада
from chatterbot.response_selection import get_random_response

#эти импорты нужны для обработки исключений
import traceback
import sys

print(10*"#", "БИБЛИОТЕКИ ПОДКЛЮЧЕНЫ", 10*"#", '\n', sep='\n')

def read_settings(file_name: str = "setting.json", user: str = "user_id_localuser", user_lang: str = "ru") -> dict:
    """Возвращает словарь с настройками пользователя, если файл с настройками существует, иначе - инициализирует его"""
    try:
        with open(file_name, "r") as file:
            settings_from_a_file = json.load(file)
            return settings_from_a_file
    except FileNotFoundError:
        with open(file_name, "w") as file:
            json.dump({user: {"training_completed": 1, "lang": user_lang}}, file, indent=4)


def save_settings(settings_from_a_file: dict, file_name: str = "setting.json") -> None:
    with open(file_name, "w") as file:
        json.dump(settings_from_a_file, file, indent=4)


def show_settings(settings_from_a_file, user: str = "user_id_localuser") -> None:
    print(settings_from_a_file)
    for setting_item in settings_from_a_file[user]:
        print(setting_item)


def change_settings(settings_from_a_file, user: str = "user_id_localuser") -> dict:
    """Возвращает измененные настройки"""

    while True:
        command = input("Введите 0, чтобы выйти из настроек, иначе укажите пункт настроек, который хотите изменить, в виде <настройка>: новое_значение")
        if command == "0":
            break

        else:
            command_ref = command.replace(" ", "").split(":")
            settings_from_a_file[user][command_ref[0]] = command_ref[1]

    return settings_from_a_file


def create_bot():
    """Инициализирует бота"""
    return ChatBot("Bot", response_selection_method=get_random_response, logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path':'chatterbot.logic.BestMatch',
            'default_response':'I am sorry, I do not understand',
            'maximum_similarity_threshold':0.8
        }
    ])


def training_1(trainer, chatbot: "<class 'chatterbot.chatterbot.ChatBot'>", file_with_data_train: "path to file" = "data\\lang\\en\\dialogs_en.json"):
    """Функция тренировки бота"""
    #trainer = ListTrainer(chatbot)

    training_data = []  # массив диалогов

    with open(file_with_data_train, encoding="utf-8") as file:  # открытие json-файла с диалогами
        training_data_json = json.load(file)  # чтение json-файла с диалогами в словарь диалогов
        for key in training_data_json.keys():  # перебираем ключи словаря(key имеет вид 'u1+u2', где u1 и u2 - идентификаторы говорящих актеров, т.е. между кем идет текущий диалог)
            for i in range(len(training_data_json[key])):  # перебираем высказывания текущего диалога
                training_data_json[key][i] = training_data_json[key][i].strip("\n")  # убираем управляющий символ(он лишний)

            training_data += [training_data_json[key]]  # добавляем массив выражений текущего диалога(т.е. диалог) в массив диалогов

    for dialog in training_data:  # перебираем диалоги в массиве диалогов
        trainer.train(dialog)  # обучаем бота на каждом цельном диалоге


def get_feedback() -> "return bool or get_feedback()":
    """Функция определитель - устраивает ли пользователя высказывание бота"""
    text = input('"Yes" or "No": ')

    if 'yes' in text.lower():
        return False  # or True?
    elif 'no' in text.lower():
        return True  # or False?
    """
    else:  # выполняется блок else, если пользователь сморозил хуйню
        print('Please type either "Yes" or "No"')  # просьба не морозить хуйню, а ответить 'да' или 'нет'
        return get_feedback()  # повторный запуск функции
    """


def user_dictionary(user_id: str, statements: "Список с двумя утверждениями", path="dict_%s.txt") -> None:
    """
        Функция заполняет индивидуальный словарь пользователя.

        Параметр path должен иметь вид path_to_file\\dict_%s.txt, где:
            -path_to_file - путь до файла
            -dict_%s.txt - название файла, %s - user_id(id пользователя)
    """
    try:  # ставим под сомнение следующий блок кода:
        with open(path % user_id, "a") as file:  # открываем файл в режиме дозаписи
            for statement in statements:
                file.write(statement)
    except FileNotFoundError:  # если файл не найден
        with open(path % user_id, "w") as file:  # создаем файл
            for statement in statements:
                file.write(statement+'\n')


def learning_based_on_user_input(user_input_statement, correct_response, trainer):
    last_statement_answer = [user_input_statement, correct_response]
    try:
        # trainer = ListTrainer(bot)  # создаем экземпляр 'тренера'
        trainer.train(last_statement_answer)  # тренируем бота
        user_dictionary("user_id_localuser", last_statement_answer)
        # bot.learn_response(correct_response, input_statement)  # разобраться как работает
        print('\nResponses added to bot')
    except:
        print('\nПроизошла ошибка. Бот не учел вашу корректировку. Подробности смотрите ниже')
        exception_information = sys.exc_info()
        exception_type, exception_value, traceback_obj = exception_information

        traceback_info = traceback.format_tb(traceback_obj)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + traceback_info + "\nError Info:\n" + str(sys.exc_info()[1])
        print(pymsg)

        try:
            with open("error.txt", "a") as file:
                traceback.print_exception(etype=exception_type, value=exception_value, tb=traceback_obj, file=file)
        except FileNotFoundError:
            with open("error.txt", "w") as file:
                traceback.print_exception(etype=exception_type, value=exception_value, tb=traceback_obj, file=file)

def dialog(user_input_statement, bot, trainer):

    input_statement = Statement(text=user_input_statement)  # утверждение пользователя
    bot_response = bot.generate_response(input_statement)  # генерируем ответ бота
    return bot_response.text


def main(user_input_statement, bot, trainer, client):
    settings = read_settings(user=client, user_lang="eg")
    dialog(user_input_statement, bot, trainer)

'''def main(user_input_statement):
    bot = create_bot()
    trainer = ListTrainer(bot)
    dialog(user_input_statement, bot=bot, trainer=trainer)
'''


if __name__ == '__main__':
    pass
   # main()
