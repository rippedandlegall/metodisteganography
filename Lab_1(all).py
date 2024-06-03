from bs4 import BeautifulSoup
import re

ArrayBytesCodRule = ["11111", "00000", "11011", "00100", "00010", "01000"]
ArrayBytesCod = ["11000", "10011", "01110", "10010", "10000", "10110", "01011", "00101", "01100",
                 "11010", "11110", "01001", "00111", "00110", "00011", "01101", "11101", "01010",
                 "10100", "00001", "11100", "01111", "11001", "10111", "10101", "10001"]
ArrayLatinUp = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
ArrayLatinLow = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ArrayRussianUp = ['А', 'Б', 'Ц', 'Д', 'Е', 'Ф', 'Г', 'Х', 'И', 'Й', 'К', 'Л', 'М',
                  'Н', 'О', 'П', 'Я', 'Р', 'С', 'Т', 'У', 'Ж', 'В', 'Ь', 'Ы', 'З']
ArrayRussianLow = ['а', 'б', 'ц', 'д', 'е', 'ф', 'г', 'х', 'и', 'й', 'к', 'л', 'м',
                   'н', 'о', 'п', 'я', 'р', 'с', 'т', 'у', 'ж', 'в', 'ь', 'ы', 'з']
ArraySpecialUp = ['-', '?', ':', '', '3', 'Э', 'Ш', 'Щ', '8', 'Ю', '(', ')', '.', ',',
                  '9', '0', '1', '4', '\'', '5', '7', '=', '2', '/', '6', '+']
ArraySpecialLow = ['-', '?', ':', '', '3', 'э', 'ш', 'щ', '8', 'ю', '(', ')', '.', ',',
                   '9', '0', '1', '4', '\'', '5', '7', '=', '2', '/', '6', '+']

results = []


def MTK2_decode(bytes_mass):
    text = ""
    while len(bytes_mass) % 5 != 0:
        bytes_mass += ' '

    flag = 0
    for i in range(0, len(bytes_mass), 5):
        char_kod = bytes_mass[i:i + 5]
        if char_kod == ArrayBytesCodRule[0]:
            flag = 0
        elif char_kod == ArrayBytesCodRule[1]:
            flag = 1
        elif char_kod == ArrayBytesCodRule[2]:
            flag = 2
        elif char_kod == ArrayBytesCodRule[3]:
            text += ' '
        elif char_kod == ArrayBytesCodRule[4]:
            text += '\r'
        elif char_kod == ArrayBytesCodRule[5]:
            text += '\n'

        else:
            for i in range(len(ArrayBytesCod)):
                if char_kod == ArrayBytesCod[i]:
                    if flag == 0:
                        text += ArrayLatinUp[i]
                    elif flag == 1:
                        text += ArrayRussianUp[i]
                    elif flag == 2:
                        text += ArraySpecialUp[i]

    return text


def bits_to_text(bits):
    # Преобразование битов в байты
    bytes_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        byte_value = int(byte, 2).to_bytes(1, byteorder='big')
        bytes_array.extend(byte_value)

    # Декодирование с использованием кодировки Windows-1251
    try:
        text = bytes_array.decode('cp1251')
        return text
    except UnicodeDecodeError:
        print("Ошибка декодирования. Проверьте правильность входных данных.")
        return None


def bits_to_text(bits):
    # Преобразование битов в байты
    bytes_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        byte_value = int(byte, 2).to_bytes(1, byteorder='big')
        bytes_array.extend(byte_value)

    # Декодирование с использованием кодировки cp866
    try:
        text2 = bytes_array.decode('cp866')
        return text2

    except UnicodeDecodeError:
        print("Ошибка декодирования. Проверьте правильность входных данных.")
        return None


def bits_to_text(bits):
    # Преобразование битов в байты
    bytes_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        byte_value = int(byte, 2).to_bytes(1, byteorder='big')
        bytes_array.extend(byte_value)

    # Декодирование с использованием кодировки KOI8-R
    try:
        text3 = bytes_array.decode('koi8-r')
        return text3
    except UnicodeDecodeError:
        print("Ошибка декодирования. Проверьте правильность входных данных.")
        return None


def check_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            spans = soup.find_all('span')
            for span in spans:
                style = span.get('style', '')
                match style:
                    case 'letter-spacing:1.0pt;':
                        for i in spans:
                            # Получаем стиль элемента
                            style = span.get('style', '')
                            # Проверяем наличие letter-spacing:1.0pt; в стиле
                            if 'letter-spacing:1.0pt;' in style:
                                # Если присутствует, добавляем 1 за каждый символ
                                results.extend([1] * len(span.text))
                            else:
                                # Если отсутствует, добавляем 0 за каждый символ
                                results.extend([0] * len(span.text))
                            print("Способ форматирования -> межсимвольный интервал")
                            print(results)
                            results_str = ''.join(map(str, results))

                            text = bits_to_text(results_str)
                            if text:
                                print("(Windows-1251):", text)

                            text2 = bits_to_text(results_str)
                            if text2:
                                print("(cp866):", text2)

                            text3 = bits_to_text(results_str)
                            if text3:
                                print("(koi8-r):", text3)

                            text4 = MTK2_decode(results_str)
                            if text4:
                                print("(код Бодо(МТК-2)):", text4)

                    case 'color:#010101;':
                        for i in spans:
                            # Получаем стиль элемента
                            style = span.get('style', '')
                            # Проверяем наличие letter-spacing:1.0pt; в стиле
                            if 'color:#010101;' in style:
                                # Если присутствует, добавляем 1 за каждый символ
                                results.extend([1] * len(span.text))
                            # if 'color:#010101;' in style:
                            #     # Если присутствует, добавляем 1 за каждый символ
                            #     results.extend([1] * len(span.text))
                            else:
                                # Если отсутствует, добавляем 0 за каждый символ
                                results.extend([0] * len(span.text))
                        print("Способ форматирования -> цвет символов")
                        # Выводим результат
                        print(results)

                        results_str = ''.join(map(str, results))
                        text = bits_to_text(results_str)
                        if text:
                            print("(Windows-1251):", text)

                        text2 = bits_to_text(results_str)
                        if text2:
                            print("(cp866):", text2)

                        text3 = bits_to_text(results_str)
                        if text3:
                            print("(koi8-r):", text3)

                        text4 = MTK2_decode(results_str)
                        if text4:
                            print("(код Бодо(МТК-2)):", text4)

                    case 'mso-font-width:99%;':
                        for i in spans:
                            # Получаем стиль элемента
                            style = span.get('style', '')
                            # Проверяем наличие letter-spacing:1.0pt; в стиле
                            if 'mso-font-width:99%' in style:
                                # Если присутствует, добавляем 1 за каждый символ
                                results.extend([1] * len(span.text))
                            # if 'color:#010101;' in style:
                            #     # Если присутствует, добавляем 1 за каждый символ
                            #     results.extend([1] * len(span.text))
                            else:
                                # Если отсутствует, добавляем 0 за каждый символ
                                results.extend([0] * len(span.text))
                                print("Способ форматирования -> масштаб шрифта")
                                # Выводим результат
                                print(results)

                            results_str = ''.join(map(str, results))
                            if text:
                                print("(Windows-1251):", text)

                            text2 = bits_to_text(results_str)
                            if text2:
                                print("(cp866):", text2)

                            text3 = bits_to_text(results_str)
                            if text3:
                                print("(koi8-r):", text3)

                            text4 = MTK2_decode(results_str)
                            if text4:
                                print("(код Бодо(МТК-2)):", text4)

                    case 'font-size:11.5pt;':
                        for i in spans:
                            # Получаем стиль элемента
                            style = span.get('style', '')
                            # Проверяем наличие letter-spacing:1.0pt; в стиле
                            if 'font-size:11.5pt;' in style:
                                # Если присутствует, добавляем 1 за каждый символ
                                results.extend([1] * len(span.text))
                            # if 'font-size:12.0pt;' in style:
                            #     # Если присутствует, добавляем 1 за каждый символ
                            #     results.extend([0] * len(span.text))
                            else:
                                # Если отсутствует, добавляем 0 за каждый символ
                                results.extend([0] * len(span.text))

                            # Выводим результат
                            print("Способ форматирования -> размер шрифта")
                            print(results)

                            results_str = ''.join(map(str, results))
                            if text:
                                print("(Windows-1251):", text)

                            text2 = bits_to_text(results_str)
                            if text2:
                                print("(cp866):", text2)

                            text3 = bits_to_text(results_str)
                            if text3:
                                print("(koi8-r):", text3)

                            text4 = MTK2_decode(results_str)
                            if text4:
                                print("(код Бодо(МТК-2)):", text4)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


file_path = "variant05.html"
check_html_file(file_path)
