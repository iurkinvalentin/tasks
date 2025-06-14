Решение задач

Python 3.8+: Убедитесь, что Python установлен в вашей системе. Проверить версию можно командой:python3 --version

Инструкции по настройке
1. Склонируйте или скачайте проект
Если проект находится в репозитории, склонируйте его:
git clone https://github.com/iurkinvalentin/tasks
cd tasks

Или скачайте файлы проекта (например, solution.py) и перейдите в директорию проекта.
2. Создание виртуального окружения
Для изоляции зависимостей создайте виртуальное окружение:
python3 -m venv venv

Активируйте виртуальное окружение:

На macOS/Linux:source venv/bin/activate


На Windows:venv\Scripts\activate


3. Установка зависимостей
pip install -r requirements
4. Проверка файлов проекта
Убедитесь, что в директории проекта присутствует файл:

solution.py: Содержит решения

Тестирование кода
Файл solution.py и test.py включает набор тестов

Запуск тестов:В активированном виртуальном окружении выполните:
python3 solution.py


Ожидаемый результат task3:Если все тесты пройдены успешно, вы увидите:
Test 0 passed: got 3117, expected 3117
Test 1 passed: got 3577, expected 3577
Test 2 passed: got 3565, expected 3565

Если тест не пройден, будет выведена ошибка AssertionError с указанием, какой тест провалился и какие значения получены.


Устранение неполадок

Версия Python: Убедитесь, что используется Python 3.8 или выше.
Файл не найден: Проверьте, что solution.py находится в текущей директории.
Ошибки в тестах: Если тесты не проходят, изучите сообщение об ошибке. Предоставленный код solution.py протестирован и должен успешно проходить все тесты.

Структура проекта

solution.py: Основной скрипт с функцией appearance и тестами.
README.md: Этот файл с инструкциями по настройке и тестированию.
test.py: Дополнительные тесты

Примечания

Решение task3 использует событийный алгоритм (sweep line) для эффективного вычисления пересечения интервалов ученика и учителя в пределах урока.
Внешние библиотеки не требуются, что упрощает настройку.

