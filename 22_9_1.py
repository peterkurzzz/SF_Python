"""
    Решение задания 22.9.1 (HW-03)
"""


#   Ввод и проверка соответствия вводимых данных (вводимые данные - целое число, последовательность целых чисел)
def check_data(param):
    any_data = None
    alarm_text = ''

    while True:
        try:
            if param == 'list':
                any_data = list(map(int, input('Введите последовательность целых чисел через пробел:').split()))
                print('Введённая последовательность - ', any_data)

            if param == 'digital':
                any_data = int(input('Введите любое целое число:'))
                print('Введённое число - ', any_data)

        except ValueError:
            if param == 'list':
                alarm_text = 'В введённой последовательности не все элементы являются ЦЕЛЫМИ числами'

            if param == 'digital':
                alarm_text = 'Введённое значение не является ЦЕЛЫМ числом'

            print('%s\nБудьте внимательнее!!!' % alarm_text)

        else:
            return any_data


#   Сортировка списка по возрастанию (сортировка вставками)
def sort_max(array):
    for i in range(1, len(array)):
        tmp = array[i]
        index = i - 1
        while index >= 0 and tmp < array[index]:
            array[index + 1] = array[index]
            index -= 1
        array[index + 1] = tmp
    return array


#   Итерационный бинарный поиск
def binary_search_iter(array, digital):

    #   Проверка - входит ли введённое число в интервал последовательности
    if digital < array[0] or digital > array[-1]:
        return False  # Если число не входит в интервал последовательности (списка) - результат "FALSE"

    #   Бинарный поиск
    minimum = 0
    maximum = len(array)

    while minimum < maximum - 1:

        middle = (minimum + maximum) // 2

        if array[middle] < digital:
            minimum = middle

        else:
            maximum = middle

    return minimum


any_list = check_data('list')
any_digital = check_data('digital')

any_list = sort_max(any_list)
print('Список, отсортированный по возрастанию (сортировка вставками):', any_list)

print('Индекс числа, которое меньше введённого, а следующее за введённым - равно или больше введённого:',
      binary_search_iter(any_list, any_digital))
