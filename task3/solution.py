def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']
    
    # Получить интервалы, обрезанные по границам урока
    def get_pairs(lst):
        return [(max(start, lesson_start), min(end, lesson_end)) 
                for start, end in zip(lst[::2], lst[1::2]) 
                if max(start, lesson_start) < min(end, lesson_end)]
    
    pupil_intervals = get_pairs(intervals['pupil'])
    tutor_intervals = get_pairs(intervals['tutor'])
    
    # Создаем список событий: (время, тип_события, кто)
    events = []
    for start, end in pupil_intervals:
        events.append((start, 1, 'pupil'))  # Начало интервала ученика
        events.append((end, -1, 'pupil'))   # Конец интервала ученика
    for start, end in tutor_intervals:
        events.append((start, 1, 'tutor'))  # Начало интервала учителя
        events.append((end, -1, 'tutor'))   # Конец интервала учителя
    
    # Сортируем события по времени
    events.sort()
    
    total_time = 0
    pupil_count = 0
    tutor_count = 0
    last_time = lesson_start
    
    # Обрабатываем события
    for time, event_type, who in events:
        # Если оба присутствуют, добавляем время до текущего события
        if pupil_count > 0 and tutor_count > 0:
            total_time += time - last_time
        
        # Обновляем счетчики
        if who == 'pupil':
            pupil_count += event_type
        else:
            tutor_count += event_type
        
        last_time = time
    
    return total_time


# Тесты
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117},
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577},
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565},
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
        print(f'Test {i} passed: got {test_answer}, expected {test["answer"]}')