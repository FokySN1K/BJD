import json
import platform
import urllib
from pathlib import Path

import easyocr
import os
import webbrowser



def getPathFilesFromDirectory(directory: str) -> list:
    return [os.path.join(os.path.basename(directory), f)
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))]

def getTextFromFile(filePath: str) -> str:
    try:
        reader = easyocr.Reader(['ru', 'en'], gpu=True)
        results = reader.readtext(filePath, detail=1, paragraph=True)

        texts = [result[1] for result in results]

        return str.lower(' '.join(texts))
    except:
        print("Название файлов должно содержать только латинские буквы или цифры")

def createTextFromFiles(directoryPath: str) -> list:

    result = []
    for file in getPathFilesFromDirectory(directoryPath):

        text = getTextFromFile(file)
        result.append([text, file])

    return result

def getFileUrl(path: str) -> str:

    abs_path = os.path.abspath(path)
    fileurl = ""

    if platform.system() == 'Windows':
        win_path = abs_path.replace('\\', '/')
        file_url = "file:///" + urllib.parse.quote(win_path, safe='/:')
    else:
        file_url = "file://" + urllib.parse.quote(abs_path)

    return file_url

def start():
    # Если хотите добавить к новые данные, то просто сгенерьте новый файл json
    # и добавьте результат к старому (не забудьте заменить директорию поиска)
    jsonFileDumpPath = "example.json"
    jsonFile = Path(jsonFileDumpPath)
    directoryPath = "./BJD"

    data = []

    if jsonFile.is_file():
        print("Загрузка данных из json")

        with open(jsonFile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("Загрузка завершена")

    else:
        print("Обработка фотографий")
        results = createTextFromFiles(directoryPath)
        print("Загрузка завершена")

        for result in results:
            data.append(dict())
            data[-1]["text"] = result[0]
            data[-1]["filepath"] = result[1]

        with open(jsonFile, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    while True:

        find = str.lower(input("Введите вопрос(лучше его часть):"))

        for res in data:
            if find in res["text"]:
                print(f"Ссылка: {getFileUrl(res['filepath'])}")
                #webbrowser.open(res['filepath'])

def rename():
    directory = "./21"
    index = 54

    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            new_filename = str(index) + ".png"
            index += 1
            os.rename(
                os.path.join(directory, filename),
                os.path.join(directory, new_filename)
            )
            print(f'Переименован: {filename} -> {new_filename}')


if __name__ == '__main__':

    start()