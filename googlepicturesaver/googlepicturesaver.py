import re
import requests
import string
from typing import List
import os
from bs4 import BeautifulSoup
from textwrap import shorten

ENGINE = 'GoogleEngine'
NUMBER_OF_PICTURES = 15
PATH_TO_SAVE = ''


class ConsoleApp(object):
    def __init__(self) -> None:
        self.engine: Engine = globals()[ENGINE]()
        self.numbers_of_pictures: int = NUMBER_OF_PICTURES
        self.string_for_search: str = ""
        self.files: List[str] = []
        self.linque: str = 'ru'

    @staticmethod
    def start_message() -> None:
        print('Введите слово для поиска и сохранения картинок.')
        print('Используемый поиск: {}'.format(ENGINE))
        print('Для выхода наберите #exit')

    @staticmethod
    def close_app() -> None:
        print('Закрываем приложение')
        raise SystemExit

    def run(self):
        while True:
            self.start_message()
            self.get_string()
            if len(self.string_for_search) == 0:

                continue
            validator = Validator(self.string_for_search)
            if (validator.result_validation_query and
                    validator.result_validation_path):
                self.files = self.engine.get_images(validator.query_string)
            else:
                print("Некорректный запрос. Невозожно сделать поиск или создать папку")
                return None
            falisaver = FileSaver(validator.path_string, self.files, self)
            falisaver.save_files()

    def get_string(self) -> None:
        self.string_for_search = input()
        if self.string_for_search == '#exit':
            self.close_app()


class Engine(object):

    def __init__(self):
        pass

    def get_search_page(self, string_for_search):
        pass

    def parse_links(self):
        pass

    def download_files(self):
        pass

    def get_images(self, search_string):
        pass


class GoogleEngine(Engine):
    def __init__(self):
        super().__init__()
        self.file_links = []
        self.files = []
        self.answer = None
        self.successful_request = False
        self.successful_parse = False
        self.successful_download = False

    def get_search_page(self, string_for_search) -> None:
        headers = {"content-type": "image/jpg"}
        params = {'q': string_for_search, 'source': 'lnms', 'tbm': 'isch'}
        try:
            self.answer = requests.get('https://google.com/search', headers=headers,
                                       params=params)
            if self.answer.status_code == 200:
                self.successful_request = True
            else:
                self.successful_request = False
        except requests.exceptions.RequestException as e:
            print(e)
            self.successful_request = False

    def parse_links(self):
        try:
            soup = BeautifulSoup(self.answer.content, 'html.parser')

            imgs = soup.findAll('img')
            for img in imgs:
                if img['src'][:5] == 'https':
                    self.file_links.append(img['src'])
            self.successful_parse = True
        except Exception:
            print('Parsing Error')
            raise SystemExit

    def download_files(self):
        try:
            for link in self.file_links:
                img_file = requests.get(link)
                self.files.append(img_file.content)
            self.successful_download = True

        except requests.exceptions.RequestException as e:
            self.successful_download = False
            print('Download files error!')
            print(e)
            raise SystemExit

    def get_images(self, search_string):
        """Base logic for engine"""
        self.get_search_page(search_string)
        if self.successful_request:
            self.parse_links()
        if self.successful_parse:
            self.download_files()
        if self.successful_download:
            return self.files


class Validator(object):
    """This class validate query string - len, correct symbols, and return correct folder name,
       and correct query string. If string is empty, the app will be restarted"""

    def __init__(self, query_string: str):

        self.query_string = query_string
        self.path_string = ""
        self.result_validation_query = self.validate_query_string()
        self.result_validation_path = self.validate_path_string()

    def validate_query_string(self) -> bool:
        character_map = {
            ord('\n'): ' ',
            ord('\t'): ' ',
            ord('\r'): None
        }

        self.query_string = self.query_string.lower()
        self.query_string = self.query_string.strip()
        self.query_string = self.query_string.translate(character_map)
        self.query_string = re.sub(" +", " ", self.query_string)
        if self.query_string.isspace():
            return False
        if len(self.query_string) == 0:
            return False
        return True

    def validate_path_string(self):
        alp = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        valid_chars = "-_() {}{}{}".format(string.ascii_letters, string.digits, alp)
        self.path_string = re.sub('', '', self.query_string)
        self.path_string = re.sub(r"[^{}]".format(valid_chars),
                                  "-", self.path_string)
        self.path_string = shorten(self.path_string, width=20, placeholder="")
        self.path_string = self.path_string.lstrip()
        self.path_string = self.path_string.rstrip()
        if len(self.path_string) == 0:
            return False
        return True


class FileSaver(object):
    """This class create base folder for saved files and save files in the target folder"""

    def __init__(self, folder_name, files, applicat):
        self.files = files
        self.folder_name = folder_name
        self.app = applicat
        self.path_for_save: str = ""
        try:
            if not os.path.exists('SavedFiles'):
                os.mkdir('SavedFiles')
        except Exception as e:

            print("Не могу создать целевую папку")
            print(e)
            self.app.close_app()

    def validate_path_exist(self):
        return os.path.exists(os.path.join('SavedFiles', self.folder_name))

    def save_files(self):

        try:
            os.mkdir(os.path.join('SavedFiles', self.folder_name))
            for num, file in enumerate(self.files):
                if num < NUMBER_OF_PICTURES:
                    with open(os.path.join('SavedFiles', self.folder_name, str(num) + ".jpg"), 'wb') as f:
                        f.write(file)
            print("Файлы сохранены в папке: {}".format(self.folder_name))

        except Exception as e:
            print(e)
            self.app.close_app()


if __name__ == '__main__':

    while True:
        app = ConsoleApp()
        app.run()
