import requests
import time
import csv
import random
from urllib.parse import quote

BASE_URL = 'https://ru.wikipedia.org'
API_URL = 'https://ru.wikipedia.org/w/api.php'
CATEGORY_TITLE = 'Категория:Животные_по_алфавиту'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; Bot/1.0)'
}

RUSSIAN_ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

def get_animals(session):
    """Получаем список всех животных через MediaWiki API"""
    animals = []
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': CATEGORY_TITLE,
        'format': 'json',
        'cmlimit': 500,  # Максимум 500 записей за запрос
        'cmcontinue': ''
    }
    request_count = 0
    max_requests = 50  # Ограничение на количество запросов

    while True:
        try:
            print(f"Отправка запроса {request_count + 1} к API: {API_URL}")
            resp = session.get(API_URL, headers=HEADERS, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"Ошибка при получении данных API: {e}")
            break

        cmembers = data.get('query', {}).get('categorymembers', [])
        page_animals = [member['title'] for member in cmembers if member['title']]
        animals.extend(page_animals)
        print(f"Найдено {len(page_animals)} животных в текущем запросе. Всего собрано: {len(animals)}")

        if 'continue' not in data:
            print("Достигнута последняя страница.")
            break

        params['cmcontinue'] = data['continue']['cmcontinue']
        request_count += 1
        if request_count >= max_requests:
            print(f"Достигнуто максимальное количество запросов ({max_requests}). Прерываем.")
            break

        time.sleep(random.uniform(1, 3))  # Задержка 1–3 секунды

    return animals

def count_animals_by_letter(animals):
    """Подсчитываем количество животных для каждой буквы"""
    counts = {letter: 0 for letter in RUSSIAN_ALPHABET}
    
    for animal in animals:
        first_letter = animal[0].upper() if animal else None
        if first_letter in counts:
            counts[first_letter] += 1
    
    return [(letter, counts[letter]) for letter in RUSSIAN_ALPHABET]

def main():
    session = requests.Session()
    print("Получаем список животных...")
    start_time = time.time()
    animals = get_animals(session)
    print(f"Время выполнения: {time.time() - start_time:.2f} секунд")
    
    if not animals:
        print("Не удалось получить список животных. Завершение работы.")
        return

    print(f"Найдено {len(animals)} животных.")
    result = count_animals_by_letter(animals)

    try:
        with open('beasts.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Буква', 'Количество'])  # Заголовок для CSV
            for letter, count in result:
                writer.writerow([letter, count])
        print("Данные успешно записаны в beasts.csv")
    except IOError as e:
        print(f"Ошибка при записи в файл: {e}")

if __name__ == '__main__':
    main()