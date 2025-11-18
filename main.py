import json
import csv
import argparse
import sys


def json_to_csv(json_file, csv_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл {json_file} не найден.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка: файл {json_file} не является корректным JSON.")
        sys.exit(1)

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
                print("Ошибка: JSON-массив должен содержать объекты.")
                sys.exit(1)
        elif isinstance(data, dict):
            # Одиночный объект
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(data.keys())
                writer.writerow(data.values())
        else:
            print("Ошибка: неподдерживаемая структура JSON. Ожидается массив объектов или объект.")
            sys.exit(1)
    except Exception as e:
        print(f"Ошибка при записи CSV: {e}")
        sys.exit(1)

    print(f"Конвертация завершена. CSV сохранен в {csv_file}")


def main():
    parser = argparse.ArgumentParser(description='Конвертирует JSON-файл в CSV.')
    parser.add_argument('json_file', help='Путь к JSON-файлу')
    parser.add_argument('--output', '-o', help='Путь к выходному CSV-файлу (по умолчанию: имя JSON-файла с расширением .csv)')

    args = parser.parse_args()

    if args.output is None:
        args.output = args.json_file.rsplit('.', 1)[0] + '.csv'

    json_to_csv(args.json_file, args.output)


if __name__ == "__main__":
    main()
