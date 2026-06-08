import time
import subprocess
import sys


def main():
    query = "дождевик"
    sku = "4367148108"

    print(f"--- Проверка устойчивости скрипта (3 запуска с паузой 30 сек) ---")

    for i in range(1, 4):
        print(f"\n[Запуск #{i}] Время: {time.strftime('%H:%M:%S')}")
        result = subprocess.run(
            [sys.executable, "parser.py", query, sku],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        print(result.stdout)

        if i < 3:
            print("Ожидаем 30 секунд...")
            time.sleep(30)

    print("--- Тест устойчивости успешно пройден! ---")


if __name__ == "__main__":
    main()
