from telethon import TelegramClient
from telethon.tl.types import User, Channel
import asyncio
import os
from typing import List, Set
import time

# Открытые чаты (можно получить список участников)
OPEN_CHATS = [
    'https://t.me/imichatchallenge',
    'https://t.me/neironutii',
    'https://t.me/forgetmeai_chat',
    'https://t.me/incubeaichat',
    'https://t.me/neyrodev'
]

# Закрытые чаты (получаем через сообщения)
CLOSED_CHATS = [
    'https://t.me/neuroart0',
    'https://t.me/+szDfPREr1rpjMWRi',
    'https://t.me/saburov_chat',
    'https://t.me/integromat_russia',
    'https://t.me/+V2toPTWQB4RkYWRi'
]

def remove_duplicates_from_file(filename: str) -> None:
    """
    Удаляет дубликаты строк из файла и сохраняет только уникальные значения
    
    Args:
        filename (str): Имя файла для обработки
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден")
            return

        # Читаем все строки из файла
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Подсчитываем начальное количество строк
        initial_count = len(lines)

        # Создаем множество уникальных строк (удаляем пробелы и пустые строки)
        unique_lines = set(line.strip() for line in lines if line.strip())

        # Сортируем строки
        sorted_lines = sorted(unique_lines)

        # Записываем уникальные значения обратно в файл
        with open(filename, 'w', encoding='utf-8') as file:
            for line in sorted_lines:
                file.write(f"{line}\n")

        # Выводим статистику
        final_count = len(sorted_lines)
        removed_count = initial_count - final_count
        print(f"\nУдаление дубликатов из файла {filename}:")
        print(f"Было строк: {initial_count}")
        print(f"Стало строк: {final_count}")
        print(f"Удалено дубликатов: {removed_count}")

    except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {str(e)}")

async def get_users_from_participants(client: TelegramClient, chat_link: str) -> Set[str]:
    """
    Получает список пользователей из участников чата (для открытых чатов)
    """
    try:
        chat = await client.get_entity(chat_link)
        unique_usernames = set()
        
        print(f"Получаю список участников из открытого чата {chat_link}...")
        async for participant in client.iter_participants(chat):
            if isinstance(participant, User) and not participant.bot and participant.username:
                unique_usernames.add(f"@{participant.username}")
        
        print(f"Собрано {len(unique_usernames)} уникальных пользователей из {chat_link}")
        return unique_usernames
    
    except Exception as e:
        print(f"Ошибка при обработке открытого чата {chat_link}: {str(e)}")
        return set()

async def get_users_from_messages(client: TelegramClient, chat_link: str) -> Set[str]:
    """
    Получает список пользователей из истории сообщений (для закрытых чатов)
    """
    try:
        chat = await client.get_entity(chat_link)
        unique_usernames = set()
        
        print(f"Получаю сообщения из закрытого чата {chat_link}...")
        async for message in client.iter_messages(chat, limit=None):
            if message.sender and isinstance(message.sender, User) and not message.sender.bot:
                if message.sender.username:
                    unique_usernames.add(f"@{message.sender.username}")
        
        print(f"Собрано {len(unique_usernames)} уникальных пользователей из {chat_link}")
        return unique_usernames
    
    except Exception as e:
        print(f"Ошибка при обработке закрытого чата {chat_link}: {str(e)}")
        return set()

async def main():
    # Инициализация клиента с заданными параметрами
    client = TelegramClient(
        session='anon15',
        api_id=22454710,
        api_hash='4eb535b17a9b8b832d985d269944b184',
        proxy=None,
        device_model='PC',
        system_version='1.0',
        app_version='1.0',
        lang_code='en',
        system_lang_code='en',
        connection_retries=5,
        auto_reconnect=True,
        timeout=10
    )
    
    await client.start()
    
    try:
        all_usernames = set()
        
        # Обрабатываем открытые чаты
        print("\nОбработка открытых чатов...")
        for chat in OPEN_CHATS:
            try:
                usernames = await get_users_from_participants(client, chat)
                all_usernames.update(usernames)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Не удалось обработать открытый чат {chat}: {str(e)}")
        
        # Обрабатываем закрытые чаты
        print("\nОбработка закрытых чатов...")
        for chat in CLOSED_CHATS:
            try:
                usernames = await get_users_from_messages(client, chat)
                all_usernames.update(usernames)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Не удалось обработать закрытый чат {chat}: {str(e)}")
        
        # Сохраняем результаты в файл
        print(f"\nВсего найдено {len(all_usernames)} уникальных пользователей")
        with open('bigparsing', 'w', encoding='utf-8') as file:
            for username in sorted(all_usernames):
                file.write(f"{username}\n")
        
        print(f"Результаты сохранены в файл 'bigparsing'")
        
        # Удаляем дубликаты из файла
        remove_duplicates_from_file('bigparsing')
        
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main()) 