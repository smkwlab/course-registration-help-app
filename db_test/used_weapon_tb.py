import mysql.connector
import configparser

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

db=mysql.connector.connect(host=config_ini.get('MYSQL', 'host'), user=config_ini.get('MYSQL', 'user'), password=config_ini.get('MYSQL', 'pass'))
cursor=db.cursor()

db_name = 'slum_spla_draft_cup_db'

tb_name = 'used_weapon_tb'

def create_db(cursor, db):
    cursor.execute("CREATE DATABASE slum_spla_draft_cup_db;")
    db.commit()
    print('dbをクリエイトしました')

def use_db(cursor, db):
    cursor.execute("USE slum_spla_draft_cup_db")
    db.commit()
    print('dbをユーズしました')

def create_used_weapon_tb(cursor, db):
    cursor.execute("""CREATE TABLE IF NOT EXISTS used_weapon_tb(
                    used_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    p_id INT,
                    wp_id INT);""")
    db.commit()
    print('used_weapon_tbをクリエイトしました')

def drop_tb(cursor, db, tb_name):
    # tbの削除
    cursor.execute(f"DROP TABLE {tb_name}")
    db.commit()
    print(f'{tb_name}をドロップしました')

# create_db(cursor, db)
use_db(cursor, db)

drop_tb(cursor, db, tb_name)
create_used_weapon_tb(cursor, db)

# データを取得
cursor.execute('SELECT * FROM used_weapon_tb')
rows = cursor.fetchall()

# 出力
for i in rows:
    print(i)

# 接続をクローズする
cursor.close()
db.close()
