from api import PetFriends
from settings import *
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=my_email, password=my_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(my_email, my_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(my_email, my_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

    '''
           Дополнительные 10 тестов REST API-интерфейса apy.py (вторая часть практического задания 24.7.2):
            А) Позитивные:
                (01) - Проверка возможности добавления информации о новом питомце без фотографии;
                (02) - Проверка возможности добавления фотографии питомца в существующую запись;
                (03) - Проверяем, что запрос питомцев со значением параметра filter = 'my_pets' 
                    возвращает не пустой список.
            
            Б) Негативные:
                (04) - Проверка что запрос API-ключа возвращает статус 403 при некорректных или "пустых" email и
                    password, а в результате содержится сообщение об ошибке;
                (05) - Проверка, что запрос питомцев с некорректным значением параметра filter выдаёт статус 
                    ошибки 500, а также - некорректным или "пустым" значением параметра auth_key выдаёт 
                    статус ошибки 403, в результате содержится сообщение об ошибке;
                (06) - Проверка возможности удаления питомца с некорректным и "пустым" auth_key, "пустым" pet_id;
                (07) - Проверяем возможность обновления информации о питомце с некорректным (тип: строка)
                    значением параметра age;
                (08) Проверка возможности добавления изображения в формате bmp вместо допускаемых в 
                    форматах jpg, jpeg, png;                    
                (09) - Проверка возможности добавления файла в формате txt вместо допускаемых в 
                    форматах jpg, jpeg, png";
                (10) Проверяем возможность использования в качестве строкового параметра, например - name, строки 
                длиной более 255 символов (500 символов)
                
                
                
    '''

def test_add_new_pet_without_photo(name='Kurz2', animal_type='mongrel', age='4'):
    """ (01) Проверяем что можно добавить питомца с данными без фотографии"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(my_email, my_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_wh_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_pet_photo(pet_photo='images/cat1.jpg'):
    """(02) Проверяем что можно добавить фотографию питомца в существующую запись"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    len_my_pet = len(my_pets['pets'])
    pet_id = ""

    # Если список не пустой, то пробуем найти запись питомца без фотографии
    if len_my_pet > 0:

        for i in range(len_my_pet):
            if my_pets['pets'][i]['pet_photo'] == "":
                pet_id = my_pets['pets'][i]['id']
                break

    # Если список пустой или запись питомца без фотографии не найдена, добавляем такую запись
    if pet_id == "":

        _, result = pf.add_new_pet_wh_photo(auth_key, name='Kurz1', animal_type='mongrel', age='2')
        pet_id = result['id']

    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа = 200 и в запись питомца добавлена фотография
    assert status == 200
    assert result['pet_photo'] != ""


def test_get_list_pets_with_valid_key(filter='my_pets'):
    """(03) - Проверяем что запрос питомцев со значением параметра filter = 'my_pets' возвращает не пустой список."""

    _, auth_key = pf.get_api_key(my_email, my_password)

    # Принудительно добавляем запись о питомце, чтобы иметь хотя бы одну в разделе "my_pets"
    pf.add_new_pet_wh_photo(auth_key, name='Kurz_test', animal_type='mongrel', age='10')

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_get_api_key_negative():
    """ (04) - Проверяем что запрос API-ключа возвращает статус 403 при некорректных или "пустых" email и
        password, а в результате содержится сообщение об ошибке"""

    # Отправляем запрос с некорректным паролем
    status, result = pf.get_api_key(my_email, my_password_neg)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result

    # Отправляем запрос с некорректным email
    status, result = pf.get_api_key(my_email_neg, my_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result

    # Отправляем запрос с "пустым" паролем
    status, result = pf.get_api_key(my_email, my_password_null)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result

    # Отправляем запрос с некорректным email
    status, result = pf.get_api_key(my_email_null, my_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result


def test_get_list_pets_negative():
    """(05) - Проверяем что запрос питомцев с некорректным значением параметра filter выдаёт статус ошибки 500,
        а также - некорректным или "пустым" значением параметра auth_key выдаёт статус ошибки 403"""

    # Корректный auth_key и некорректный filter
    _, auth_key = pf.get_api_key(my_email, my_password)
    filter = 'pet'
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 500
    assert 'Filter value is incorrect' in result

    # Некорректный auth_key
    auth_key ['key'] = str(auth_key.values()) + 'a'
    filter = ''
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result

    # "Пустой" auth_key
    auth_key ['key']= ''
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result


def test_delete_pet_negative():
    """(06) - Проверяем возможность удаления питомца с некорректным или "пустым" auth_key, "пустым" pet_id"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Формируем список ID питомцев и берём ID первого питомца из списка
    my_list_id = [my_pets['pets'][i]['id'] for i in range(len(my_pets['pets']))]
    pet_id = my_pets['pets'][0]['id']

    # Формируем некорректный auth_key
    auth_key['key'] = str(auth_key.values()) + 'a'

    # Пробуем удалить запись о питомце с некорректным auth_key
    status, result = pf.delete_pet(auth_key, pet_id)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert pet_id in my_list_id

    # Формируем "пустой" auth_key
    auth_key['key'] = ''

    # Пробуем удалить запись о питомце с 'пустым' auth_key
    status, result = pf.delete_pet(auth_key, pet_id)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert pet_id in my_list_id

    # Повторно получаем корректный auth_key
    _, auth_key = pf.get_api_key(my_email, my_password)

    # Формируем "пустой" pet_id
    pet_id = ''

    # Пробуем удалить запись о питомце с "пустым" pet_id
    status, result = pf.delete_pet(auth_key, pet_id)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 404
    assert 'Not Found' in result


def test_update_pet_negative(name='Kurz_ren', animal_type='kat'):
    """(07) - Проверяем возможность обновления информации о питомце с некорректным (тип-строка)
        значением параметра age"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

    # Присваиваем параметру age значение типа string
    age = 'asd'

    status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    # Если статус ответа сервера равен 200, то выкидываем исключение
    if status == 200:
        raise Exception("Параметр 'age' типа 'string' не должен корректно обрабатываться сервером")
    else:
        assert status == 400


def test_add_pet_photo_negative_bmp():
    """(08) Проверка возможности добавления изображения в формате bmp вместо допускаемых в форматах jpg, jpeg, png"""

    # Выбираем в качестве фотографии файл bmp
    pet_photo = 'images/cat.bmp'

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    len_my_pet = len(my_pets['pets'])
    pet_id = ""

    # Если список не пустой, то пробуем найти запись питомца без фотографии
    if len_my_pet > 0:

        for i in range(len_my_pet):
            if my_pets['pets'][i]['pet_photo'] == "":
                pet_id = my_pets['pets'][i]['id']
                break

    # Если список пустой или запись питомца без фотографии не найдена, добавляем такую запись
    if pet_id == "":

        _, result = pf.add_new_pet_wh_photo(auth_key, name='Kurz1', animal_type='mongrel', age='2')
        pet_id = result['id']

    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа и в запись питомца не добавлена фотография
    if status == 200:
        raise Exception("Сервисом должны поддерживаться файлы только форматов jpg, jpeg, png")
    else:
        assert status == 400
        assert result['pet_photo'] == ""

    # Выбираем в качестве фотографии файл txt
    pet_photo = 'images/tex.txt'

    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа и в запись питомца не добавлена фотография
    if status == 200:
        raise Exception("Сервисом должны поддерживаться файлы только форматов jpg, jpeg, png")
    else:
        assert status == 400


def test_add_pet_photo_negative_txt():
    """(09) Проверка возможности добавления файла в формате txt вместо допускаемых в форматах jpg, jpeg, png"""

    # Выбираем в качестве фотографии файл bmp
    pet_photo = 'images/tex.txt'

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    len_my_pet = len(my_pets['pets'])
    pet_id = ""

    # Если список не пустой, то пробуем найти запись питомца без фотографии
    if len_my_pet > 0:

        for i in range(len_my_pet):
            if my_pets['pets'][i]['pet_photo'] == "":
                pet_id = my_pets['pets'][i]['id']
                break

    # Если список пустой или запись питомца без фотографии не найдена, добавляем такую запись
    if pet_id == "":

        _, result = pf.add_new_pet_wh_photo(auth_key, name='Kurz1', animal_type='mongrel', age='2')
        pet_id = result['id']

    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа
    if status == 200:
        raise Exception("Сервисом должны поддерживаться файлы только форматов jpg, jpeg, png")
    else:
        assert status == 500


def test_add_new_pet_without_photo_negative(animal_type='mongrel', age='4'):
    """ (10) Проверяем возможность использования в качестве строкового параметра, например - name, строки длинной
    более 255 символов (500 символов)"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(my_email, my_password)

    # Определяем name строкой в 500 символов
    name = '''
            14jYuZsGlJjYxOYdPTJebhuJgGgWuaYBpUbxEtxKEhGtXiuBkyCIufWQqTAbaXlAQzaZOEvvxRgGaMKTFLduRaouihOuXjxHqPXq
            bjzkjPSCYbtFaqiDBnzNcJymvCsPTAEWlFBofUqdhmSpOihjBumquPfqWXkmEUSvsXGQAVBwZZsSXsXQYnYPrCbCGoZRoJIBOgSRJp
            ePQWGBlPCnrIlkOdYobRLcXFgbwxRmwySAvfHLiBVyhIudSNenbvyjzZxraJzMKupefOTeKoNiIiAfiEKIejvoABMdFYcUWsibgfmc
            sDnExHGpozUFTetzoCTSdTGckvgJicwngwV7EKIoBeGuYLCouOGOSZWMSPpPFCVSagjiXZIayxvZVWkdomVwMjxvOxpCotcTxAsVdQ
            STEujFqccMxVtWQayFdFDrDOrWMsRLymSNYgVyCLuIPMlcxhzFVFhMgpRwhHYfjQVWsLpaOpkhEnkflRtqkZQgFeOeLm21
            '''

    # Добавляем питомца
    status, _ = pf.add_new_pet_wh_photo(auth_key, name, animal_type, age)

    # Проверяем что статус ответа
    if status == 200:
        raise Exception("Сервисом не должны поддерживаться строки более 255 символов")
    else:
        assert status == 400

