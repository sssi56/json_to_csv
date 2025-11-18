import json
import csv
import os
import sys

def json_to_csv(json_file, csv_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл {json_file} не найден.")
        return False
    except json.JSONDecodeError:
        print(f"Ошибка: файл {json_file} не является корректным JSON.")
        return False

    try:
        if isinstance(data, list) and data:
            if isinstance(data[0], dict):
                # Массив объектов
                keys = list(data[0].keys())
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys, delimiter=';')
                    writer.writeheader()
                    writer.writerows(data)
            else:
                print(f"Ошибка: JSON-массив в {json_file} должен содержать объекты.")
                return False
        elif isinstance(data, dict):
            # Одиночный объект
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(data.keys())
                writer.writerow(data.values())
        else:
            print(f"Ошибка: неподдерживаемая структура JSON в {json_file}. Ожидается массив объектов или объект.")
            return False
    except Exception as e:
        print(f"Ошибка при записи CSV для {json_file}: {e}")
        return False

    print(f"Конвертация завершена. CSV сохранен в {csv_file}")
    return True

def main():
    # Получить список всех .json файлов в текущей директории
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not json_files:
        print("В текущей директории нет JSON-файлов для конвертации.")
        sys.exit(0)
    
    converted_count = 0
    for json_file in json_files:
        csv_file = json_file.rsplit('.', 1)[0] + '.csv'
        if json_to_csv(json_file, csv_file):
            converted_count += 1
    
    print(f"Всего конвертировано файлов: {converted_count}")

if __name__ == "__main__":
    main()
