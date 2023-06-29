import mysql.connector
import configparser
import get_weapon_list

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

db=mysql.connector.connect(host=config_ini.get('MYSQL', 'host'), user=config_ini.get('MYSQL', 'user'), password=config_ini.get('MYSQL', 'pass'))
cursor=db.cursor()

db_name = config_ini.get('MYSQL', 'db_name')

tb_name = 'weapon_tb'



def create_db(cursor, db):
    cursor.execute(f"CREATE DATABASE {db_name};")
    db.commit()
    print('dbをクリエイトしました')

def use_db(cursor, db):
    cursor.execute(f"USE {db_name}")
    db.commit()
    print('dbをユーズしました')

def create_weapon_tb(cursor, db):

    cursor.execute("""CREATE TABLE IF NOT EXISTS weapon_tb(
                    wp_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    wp_name VARCHAR(32));""")
    db.commit()
    print('weapon_tbをクリエイトしました。。。')

def drop_tb(cursor, db, tb_name):
    # tbの削除
    cursor.execute(f"DROP TABLE {tb_name}")
    db.commit()

# create_db(cursor, db)
use_db(cursor, db)

drop_tb(cursor, db, tb_name)

create_weapon_tb(cursor, db)


# データを挿入
insert_weapon = "INSERT INTO weapon_tb (wp_name) VALUES (%s);"
weapon_list = get_weapon_list.get_weapon_list_for_insert()
for weapon in weapon_list:
    cursor.execute(insert_weapon, weapon)
db.commit()
 
# データを取得
cursor.execute('SELECT * FROM weapon_tb')
rows = cursor.fetchall()
 
# 出力
for i in rows:
    print(i)

# # SQLクエリを実行する
# cursor.execute("SELECT wp_id FROM weapon_tb WHERE wp_name = 'ケルビン525'")

# # 結果を取得する
# rows = cursor.fetchall()

# # 結果を表示する
# for row in rows:
#     print(row[0])

# 接続をクローズする
cursor.close()
db.close()
