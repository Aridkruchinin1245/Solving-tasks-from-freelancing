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

def add_number(number,id):
    try:
        cursor.execute(f"""
UPDATE users SET "Телефон" = %s WHERE "Telegram ID" = %s 
""", (number,id))
        conn.commit()
        logger.info("Телефон записан")
    except Exception as e:
        logger.critical(f"Ошибка записи телефона {e}")

def add_promo_data(promo, discount, date, id):
    try:
        cursor.execute("""
UPDATE users SET "Промокод отправленный" = %s,
                "Размер скидки обещанный" = %s,
                "Дата отправки промокода" = %s
WHERE "Telegram ID" = %s
""", (promo,discount,date,id))
        conn.commit() 
    except Exception as e:
        logger.critical(f"Ошибка записи данных о промокоде {e}")
         
if __name__ == '__main__':
    get_database()