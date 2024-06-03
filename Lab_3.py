from typing import List

def convert_to_decimal_codes(text: str) -> List[int]:
    return [ord(char) for char in text]

file_path = 'lab3.txt'

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines_array = [line.strip() for line in file.readlines()]

    even_odd_array = []
    for line in lines_array:
        decimal_codes_sum = sum(convert_to_decimal_codes(line))
        if decimal_codes_sum % 2 == 0:
            even_odd_array.append(1)
        else:
            even_odd_array.append(0)

    print("Decimal Character Codes:")
    for line in lines_array:
        print(convert_to_decimal_codes(line))

    print("Суммы Decimal Character Codes:")
    for line in lines_array:
        decimal_codes_sum = sum(convert_to_decimal_codes(line))
        print(decimal_codes_sum)

    print("Вывод:")
    for i in range(len(lines_array)):
        if (even_odd_array[i] == 0):
            print(f"{lines_array[i]} --> {even_odd_array[i]} | НЕТ")
        else:
            print(f"{lines_array[i]} --> {even_odd_array[i]} | ДА")

except FileNotFoundError:
    print(f"Файл {file_path} не найден.")
except Exception as e:
    print(f"Произошла ошибка: {e}")