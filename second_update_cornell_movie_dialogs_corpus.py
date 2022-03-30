import json
dialog_dict = {}  # m{номер_фильма}:диалог

def write_in_dialog_dict(dialog_dict_in_func: dict, first_line: list, second_line: list):
    dialog_dict_in_func[f"{first_line[1]}+{second_line[1]}"] = dialog_dict[f"{first_line[1]}+{second_line[1]}"] + [first_line[-1], second_line[-1]] if f"{first_line[1]}+{second_line[1]}" in dialog_dict_in_func else [first_line[-1], second_line[-1]]


with open("movie_lines_short.txt") as file:

    lines = file.readlines()  # lines - массив строк текстового файла. Каждая строка файла - элемент массива.
    for index_line in range(len(lines)):  # перебираем все элементы массива(строки файла). Можно заменить на for line in file:
        lines[index_line] = lines[index_line].split(" +++$+++ ")

    for index_line in range(len(lines)-1):
        if lines[index_line][1] == lines[index_line+1][1]:
            lines[index_line+1][-1] = lines[index_line][-1].rstrip("\n") + " " + lines[index_line+1][-1]
            lines[index_line] = ''

    lines_2 = []
    for line in lines:
        if line != '':
            lines_2 += [line]

    first_and_second_actor = [lines_2[0][1], lines_2[1][1]]
    for index_line in range(0, len(lines_2)-1, 2):
        if lines_2[index_line][1] in first_and_second_actor:
            if lines_2[index_line+1][1] in first_and_second_actor:
                write_in_dialog_dict(dialog_dict, lines_2[index_line], lines_2[index_line+1])
            elif lines_2[index_line+2][1] in first_and_second_actor:
                first_and_second_actor[1] = lines_2[index_line+1][1]
                write_in_dialog_dict(dialog_dict, lines_2[index_line], lines_2[index_line + 1])
        else:
            first_and_second_actor = [lines_2[index_line][1], lines_2[index_line+1][1]]
            write_in_dialog_dict(dialog_dict, lines_2[index_line], lines_2[index_line + 1])


with open(f"data\\dialogs.json", "w") as file:
    json.dump(dialog_dict, file, indent=4)
