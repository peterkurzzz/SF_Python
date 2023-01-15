def check_input(notif):
    # Счётчик количества повторов ввода
    count = 0

    # Запуск цикла проверки корректного ввода числа
    while True:

        # Ввод строки (числа)
        input_digital = input(notif)

        # Увеличение счётчика
        count += 1

        # Критическая проверка количества попыток ввода и длины вводимой строки
        if count > 20 or len(input_digital) > 7:
            print('Вы не серьёзный человек. До следующей встречи!!!')
            exit()  # При количестве попыток больше 20-ти и длине строки более 7 работа программы заканчивается

        # Проверка на наличие в водимом числе только символов цифр
        if input_digital.isdigit():
            input_digital = int(input_digital)  # Преобразование введённой строки в целое число

            # Проверка положительной полярности числа
            if input_digital > 0:
                return input_digital  # Если число целое и положительное - проверка заканчивается
            else:
                print('Вы ввели не положительное целое число. Повторите ввод')
                continue  # Повтор ввода если число отрицательное
        else:
            print('Вы ввели не целое число. Повторите ввод')
            continue  # Повтор ввода если строка содержит не только символы цифр


# Ввод и проверка ввода количества билетов
quan_tick = check_input('Введите количество билетов - ')

# Начальная стоимость билетов
price = 0

# Ввод возраста зрителей и подсчёт общей суммы стоимости билетов
for num in range(1, quan_tick + 1):
    age_viewer = check_input('Введите возраст %d зрителя - ' % num)

    # Вычисление суммарной стоимости билетов
    if 18 <= age_viewer < 25:  # Добавление стоимости для зрителей от 18 до 25 лет
        print('Стоимость билета %d зрителя равна 990 рублей' % num)
        price += 990
    elif age_viewer >= 25:  # Добавление стоимости для зрителей от 25 лет
        print('Стоимость билета %d зрителя равна 1390 рублей' % num)
        price += 1390
    else:
        print('Для %d зрителя билет бесплатный' % num)

# Учёт скидки при покупке более 3-х билетов
if quan_tick > 3:
    price *= 0.9

# Вывод итоговой стоимости билетов
print('\nОбщая стоимость билетов - {0:.2f} руб.'.format(price))

