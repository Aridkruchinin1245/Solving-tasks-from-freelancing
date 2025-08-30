import psycopg2
import subprocess
from config import DBNAME,HOST,PASSWORD,DBUSER
from logger import logger


try:
    conn = psycopg2.connect(dbname=DBNAME, user=DBUSER, password=PASSWORD, host=HOST)
    cursor = conn.cursor()

except:
    logger.critical('Ошибка подключения к базе данных')

def clear():
    try:
        cursor.execute("TRUNCATE TABLE users")
        conn.commit()
        logger.warning("База данных очищена")

    except Exception as e:
        logger.critical(f'Ошибка очистки базы данных {e}')

def get_database():
    try:
        command = [
            '/opt/homebrew/bin/pg_dump',
            '-h', HOST,
            '-U', DBUSER,
            '-F', 'p', #формат plain
            '-f', 'copies/backup.sql',
            DBNAME
        ]
        env = {'PGPASSWORD':PASSWORD} # защита пароля 
        subprocess.run(command,env=env,check=True)
        logger.info('База данных скопирована')

    except Exception as e:
        logger.critical(f'Ошибка копирования базы данных {e}')

def start_data(id,username,firstDate):
    try:
        cursor.execute(f"""
INSERT INTO users ("Telegram ID", "Username", "Дата первого захода")
                        VALUES (%s,%s,%s)
""", (id,username,firstDate))
        conn.commit()
        logger.info("Запись в базу данных")
        
    except Exception as e:
        logger.critical(f"Ошибка записи данных {e}")

def add_number(number):
    try:
        cursor.execute(f"""
INSERT INTO users ("Телефон") VALUES (%s) 
""", (number))
        conn.commit()
        logger.info("Телефон записан")
    except Exception as e:
        logger.critical(f"Ошибка записи телефона {e}")
        
if __name__ == '__main__':
    get_database()