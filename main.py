import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement


def setting():
    try:
        with open("setting.txt") as file:
            return False
    except FileNotFoundError:
        with open("setting.txt") as file:
            file.write("training_completed:1")
            return True


def create_bot():
    return ChatBot("Bot")


def training_2(chatbot, file_with_data_train="data\\dialogs.json"):
    trainer = ListTrainer(chatbot)

    training_data = []

    with open(file_with_data_train) as file:
        training_data_json = json.load(file)
        for key in training_data_json.keys():
            for i in range(len(training_data_json[key])):
                training_data_json[key][i] = training_data_json[key][i].strip("\n")

            training_data += [training_data_json[key]]

    for dialog in training_data:
        trainer.train(dialog)


def get_feedback():
    text = input('"Yes" or "No": ')

    if 'yes' in text.lower():
        return False  # or True?
    elif 'no' in text.lower():
        return True  # or False?
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


if __name__ == '__main__':
    bot = create_bot()
    if setting():
        training_2(chatbot=bot)

    while True:
        input_statement = Statement(text=input("Вы: "))
        bot_response = bot.generate_response(input_statement)
        # or
        # bot_response = bot.get_response(input_statement)
        print("Бот: ", bot_response)
        print(10*"#", 'Is "{}" a coherent response to "{}"?'.format(bot_response.text, input_statement.text), 10*'#', sep='\n')

        if get_feedback():
            print("Please input the correct one:", end='')
            correct_response = Statement(text=input())
            bot.learn_response(correct_response, input_statement)  # разобраться как работает
            print('\nResponses added to bot')

