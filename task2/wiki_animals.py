import requests
from bs4 import BeautifulSoup
import csv

# Константа русского алфавита
RUSSIAN_ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

def get_letters():
    """Получает буквы с категориями животных с Википедии."""
    url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        category_div = soup.find('div', class_='mw-category')
        if not category_div:
            return list(RUSSIAN_ALPHABET)
        letters = [h3.text.strip() for h3 in category_div.find_all('h3') if h3.text.strip() in RUSSIAN_ALPHABET]
        return letters if letters else list(RUSSIAN_ALPHABET)
    except requests.RequestException:
        return list(RUSSIAN_ALPHABET)

def get_animals_count_by_letter(letter, session):
    """Подсчитывает количество животных на заданной букве с учётом пагинации."""
    count = 0
    url = f'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту_({letter})'
    try:
        while url:
            response = session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            pages_div = soup.find('div', id='mw-pages')
            if pages_div:
                animals = pages_div.find_all('li')
                count += len(animals)
            next_page = soup.find('a', string='следующая страница')
            url = f"https://ru.wikipedia.org{next_page['href']}" if next_page else None
    except requests.RequestException:
        return 0
    return count

def main():
    """Основная функция для сбора данных и записи в CSV."""
    letters = get_letters()
    result = []
    with requests.Session() as session:
        for letter in RUSSIAN_ALPHABET:
            count = get_animals_count_by_letter(letter, session) if letter in letters else 0
            result.append([letter, str(count)])
    
    try:
        with open('beasts.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for row in result:
                writer.writerow(row)
    except IOError as e:
        print(f"Ошибка при записи в файл: {e}")