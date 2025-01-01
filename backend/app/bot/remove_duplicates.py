def remove_duplicates(filename: str):
    """
    Удаляет дубликаты из файла и сохраняет уникальные значения
    
    Args:
        filename (str): Имя файла для обработки
    """
    try:
        # Читаем все строки из файла
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Убираем пробелы и пустые строки, создаем множество уникальных значений
        unique_lines = set(line.strip() for line in lines if line.strip())
        
        # Сортируем строки для удобства чтения
        sorted_lines = sorted(unique_lines)
        
        # Записываем уникальные значения обратно в файл
        with open(filename, 'w', encoding='utf-8') as file:
            for line in sorted_lines:
                file.write(f"{line}\n")
        
        print(f"Обработка завершена:")
        print(f"Было строк: {len(lines)}")
        print(f"Стало строк: {len(sorted_lines)}")
        print(f"Удалено дубликатов: {len(lines) - len(sorted_lines)}")
        
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    remove_duplicates('userai.txt') 