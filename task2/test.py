import unittest
from unittest.mock import patch, MagicMock
import requests
from bs4 import BeautifulSoup
import csv
import os
from io import StringIO
import sys


from wiki_animals import get_letters, get_animals_count_by_letter, main, RUSSIAN_ALPHABET

class TestWikiAnimals(unittest.TestCase):
    def setUp(self):
        # Пример HTML для тестирования get_letters
        self.letters_html = """
        <div class="mw-category">
            <div class="mw-category-group"><h3>А</h3><ul><li><a href="/wiki/Категория:Животные_по_алфавиту_(А)">А</a></li></ul></div>
            <div class="mw-category-group"><h3>Б</h3><ul><li><a href="/wiki/Категория:Животные_по_алфавиту_(Б)">Б</a></li></ul></div>
        </div>
        """
        # Пример HTML для страницы с животными (одна страница)
        self.animals_html = """
        <div id="mw-pages">
            <ul>
                <li><a href="/wiki/Антилопа">Антилопа</a></li>
                <li><a href="/wiki/Агути">Агути</a></li>
            </ul>
        </div>
        """
        # Пример HTML для страницы с пагинацией
        self.animals_paginated_html = """
        <div id="mw-pages">
            <ul>
                <li><a href="/wiki/Барсук">Барсук</a></li>
                <li><a href="/wiki/Бегемот">Бегемот</a></li>
                <li><a href="/wiki/Белка">Белка</a></li>
            </ul>
            <a href="/wiki/Категория:Животные_по_алфавиту_(Б)?from=Белка">следующая страница</a>
        </div>
        """

    @patch('requests.get')
    def test_get_letters_success(self, mock_get):
        # Тестируем успешное получение букв
        mock_response = MagicMock()
        mock_response.text = self.letters_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        letters = get_letters()
        self.assertEqual(letters, ['А', 'Б'])

    @patch('requests.get')
    def test_get_letters_empty_page(self, mock_get):
        # Тестируем случай, когда блок с буквами отсутствует
        mock_response = MagicMock()
        mock_response.text = "<div>No letters here</div>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        letters = get_letters()
        self.assertEqual(letters, list(RUSSIAN_ALPHABET))

    @patch('requests.get')
    def test_get_letters_request_error(self, mock_get):
        # Тестируем ошибку HTTP-запроса
        mock_get.side_effect = requests.RequestException("Network error")
        letters = get_letters()
        self.assertEqual(letters, list(RUSSIAN_ALPHABET))

    @patch('requests.Session.get')
    def test_get_animals_count_single_page(self, mock_get):
        # Тестируем подсчёт животных на одной странице
        mock_response = MagicMock()
        mock_response.text = self.animals_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        session = requests.Session()
        count = get_animals_count_by_letter('А', session)
        self.assertEqual(count, 2)  # Антилопа, Агути

    @patch('requests.Session.get')
    def test_get_animals_count_paginated(self, mock_get):
        # Тестируем подсчёт с пагинацией
        mock_response1 = MagicMock()
        mock_response1.text = self.animals_paginated_html
        mock_response1.raise_for_status.return_value = None

        mock_response2 = MagicMock()
        mock_response2.text = self.animals_html  # Вторая страница
        mock_response2.raise_for_status.return_value = None

        mock_get.side_effect = [mock_response1, mock_response2]

        session = requests.Session()
        count = get_animals_count_by_letter('Б', session)
        self.assertEqual(count, 5)  # 3 (Барсук, Бегемот, Белка) + 2 (Антилопа, Агути)

    @patch('requests.Session.get')
    def test_get_animals_count_request_error(self, mock_get):
        # Тестируем ошибку запроса в get_animals_count_by_letter
        mock_get.side_effect = requests.RequestException("Network error")
        session = requests.Session()
        count = get_animals_count_by_letter('А', session)
        self.assertEqual(count, 0)

    @patch('requests.get')
    @patch('requests.Session.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output_file(self, mock_stdout, mock_session_get, mock_get):
        # Тестируем основную функцию и создание файла
        # Мокаем get_letters
        mock_response_letters = MagicMock()
        mock_response_letters.text = self.letters_html
        mock_response_letters.raise_for_status.return_value = None
        mock_get.return_value = mock_response_letters

        # Мокаем get_animals_count_by_letter
        mock_response_animals = MagicMock()
        mock_response_animals.text = self.animals_html
        mock_response_animals.raise_for_status.return_value = None
        mock_session_get.return_value = mock_response_animals

        # Запускаем main
        main()

        # Проверяем, что файл создан и содержит правильные данные
        self.assertTrue(os.path.exists('beasts.csv'))
        with open('beasts.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            expected = [
                ['А', '2'],
                ['Б', '2'],
            ] + [[letter, '0'] for letter in RUSSIAN_ALPHABET if letter not in ['А', 'Б']]
            self.assertEqual(rows, expected)

        # Удаляем тестовый файл
        os.remove('beasts.csv')

    @patch('requests.get')
    @patch('requests.Session.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_file_write_error(self, mock_stdout, mock_session_get, mock_get):
        # Тестируем ошибку записи в файл
        mock_response_letters = MagicMock()
        mock_response_letters.text = self.letters_html
        mock_response_letters.raise_for_status.return_value = None
        mock_get.return_value = mock_response_letters

        mock_response_animals = MagicMock()
        mock_response_animals.text = self.animals_html
        mock_response_animals.raise_for_status.return_value = None
        mock_session_get.return_value = mock_response_animals

        # Мокаем open для имитации ошибки записи
        with patch('builtins.open', side_effect=IOError("Write error")):
            main()
            self.assertIn("Ошибка при записи в файл", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()