# res_text - словарь, содержащий диалоги для каждого из фильмов. Ключ - фильм, значение - диалог
dialog_dict = {}  # m{номер_фильма}:диалог

with open("movie_lines.txt") as file:

    lines = file.readlines()  # lines - массив строк текстового файла. Каждая строка файла - элемент массива.
    for line in lines:  # перебираем все элементы массива(строки файла). Можно заменить на for line in file:

        '''
        Чтобы из строки текстового файла получить строку диалога без дополнительных данных,
        можно взять срез строки line[первый_символ_текста_диалога:].
        Т.е. если line="+++$+++ abc", то line[8:] -> abc (под индексом 8 находится "a").
        '''
        text_of_the_statement = line[line.rfind("+") + 2:]  # из элемента массива(строки файла) выбираем текст персонажа

        '''
        str.rfind(arg_str) - ищет первое С КОНЦА вхождение подстроки arg_str в строке str. Возвращает индекс arg_str
        прибавляем 2 к line.rfind("+"), т.к. после разделителя +++$+++ идет пробел.
        Нижняя граница среза УЧИТЫВАЕТСЯ. Т.е. "abc"[1:2] -> "b". "+++$+++ abc"[8:] -> "abc".
        '''

        line_split = line.split(" +++$+++ ")  # разбиваем очередной элемент массива(строку файла) по разделителю " +++$+++ "
        dialog_dict[line_split[2]] = dialog_dict[line_split[2]]+text_of_the_statement if line_split[2] in dialog_dict else text_of_the_statement

# перебираем ключи словаря dialog_dict
for number_films in dialog_dict.keys():
    # создаем файлы(имя каждого файла - идентификатор фильма)
    # записываем в каждый файл соответствующий фильму диалог
    with open(f"data\\{number_films}.txt", "w") as file:
        file.write(dialog_dict[number_films])
