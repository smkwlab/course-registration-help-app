import mysql.connector
import configparser

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

db=mysql.connector.connect(host=config_ini.get('MYSQL', 'host'), user=config_ini.get('MYSQL', 'user'), password=config_ini.get('MYSQL', 'pass'))
cursor=db.cursor()

db_name = config_ini.get('MYSQL', 'db_name')

def create_db(cursor, db):
    cursor.execute(f"CREATE DATABASE {db_name};")
    db.commit()
    print('DBをクリエイトしました')

def use_db(cursor, db):
    cursor.execute(f"USE {db_name}")
    db.commit()
    print('DBをUSEしました')

def create_player_tb(cursor, db):

    cursor.execute("""CREATE TABLE IF NOT EXISTS player_tb(
                    p_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    p_name VARCHAR(32),
                    d_id BIGINT,
                    color INT);""")
    db.commit()
    print('player_tbをクリエイトしました')

def drop_player_tb(cursor, db):
    cursor.execute("DROP TABLE player_tb")
    db.commit()
    
# create_db(cursor, db)
# use_db(cursor, db)
# create_player_tb(cursor, db)

# データを挿入
# insert_player = "INSERT INTO player_tb (p_name, d_id, color) VALUES (%s, %s, %s);"
 
# player_list = [
#     ("apple", 100, 1),
#     ("orange", 80, 2),
#     ("melon", 500, 3),
#     ("pineapple", 700, 4) 
# ]
 
# for player in player_list:
#     cursor.execute(insert_player, player)
 
# db.commit()
 
# # データを取得
# cursor.execute('SELECT * FROM player_tb')
# rows = cursor.fetchall()
 
# # 出力
# for i in rows:
#     print(i)


# # 接続をクローズする
# cursor.close()
# db.close()
# 
# # # tbの削除
# cursor.execute("DROP TABLE player_tb")
# db.commit()