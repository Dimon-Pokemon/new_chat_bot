import chatterbot
# import chatterbot_corpus
from chatterbot.trainers import ListTrainer


def create_bot():
    return chatterbot.ChatBot("Bot")


def training_2(chatbot, file_with_data_train=None):
    trainer = ListTrainer(chatbot)

    if file_with_data_train:
        with open(file_with_data_train) as file:
            training_data = file.readlines()
            for i in range(len(training_data)):
                training_data[i] = training_data[i].strip("\n")
    else:
        for number_film in range(617):
            with open(f"data\\m{number_film}.txt") as file:
                training_data = file.readlines()
                for i in range(len(training_data)):
                    training_data[i] = training_data[i].strip("\n")

            trainer.train(training_data)


if __name__ == '__main__':
    bot = create_bot()
    training_2(chatbot=bot, file_with_data_train="F:\\project\\bot\\new_movie_lines.txt")

    while True:
        bot_input = bot.get_response(input("Вы: "))
        print("Бот: ", bot_input)
