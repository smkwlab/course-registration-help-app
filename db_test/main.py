import discord
from discord import app_commands # coding: utf-8
import get_weapon_list
import mysql.connector
import configparser
from enum import Enum 
import player_tb
import random

intents = discord.Intents.all()
intents.members = True
intents.message_content = True  # メッセージコンテントのintentはオンにする
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

db=mysql.connector.connect(host=config_ini.get('MYSQL', 'host'), user=config_ini.get('MYSQL', 'user'), password=config_ini.get('MYSQL', 'pass'))
cursor=db.cursor()
print('MySQLにCONNECTしました')

player_tb.use_db(cursor, db)
# player_tb.create_player_tb(cursor, db)
# player_tb.drop_player_tb(cursor, db)

def show_tb_data(cursor, tb_name):
    # データを取得
    cursor.execute(f'SELECT * FROM {tb_name}')
    rows = cursor.fetchall()
    
    # 出力
    for i in rows:
        print(i)

def create_embed_send_weapon_successed(msg, w_list):
    desc = f'{msg}\n 以下申請済みブキ一覧です。\n'
    for i in range(len(w_list)):
        desc += f'{str(i+1)}  {w_list[i]}\n'

    embed = discord.Embed(title='ブキ申請完了',
                          description=desc,
                          color=0xdddddd, 
                          )
    return embed

def create_embed_send_weapon_failed(msg, w_list):
    desc = f'{msg}\n 以下申請済みブキ一覧です。\n'
    for i in range(len(w_list)):
        desc += f'{str(i+1)}  {w_list[i]}\n'

    embed = discord.Embed(title='警告',
                          description=desc,
                          color=0xff0000, 
                          )
    return embed

def create_embed_used_weapon(p_name, w_list, icon_url):
    desc = ''
    for i in range(len(w_list)):
        desc += f'{str(i+1)}  {w_list[i]}\n'

    embed = discord.Embed(title='申請済みブキ一覧',
                          description=desc,
                          color=0xffffff, 
                          )
    embed.set_author(name=p_name, 
                     icon_url=icon_url 
                     )
    return embed

def create_embed_roll_dies(name, num, icon_url):
    rolled_num =  random.randint(1, num)
    desc = f'You rolled **{rolled_num}**' 
    embed = discord.Embed(title='',
                          description=desc,
                          color=0xffffff, 
                          )
    embed.set_author(name=name, 
                     icon_url=icon_url 
                     )
    return embed

# show_tb_data(cursor, 'player_tb')
# show_tb_data(cursor, 'weapon_tb')

guild_id = config_ini.getint('GUILD', 'guild_id')

MY_GUILDS = [discord.Object(id=guild_id)]

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self) 
    async def setup_hook(self):
        for id in MY_GUILDS:
            self.tree.copy_global_to(guild=id)
            await self.tree.sync(guild=id)

client = MyClient(intents=intents)

@client.event
async def on_ready():   
    print('on_ready')
    guild = client.get_guild(guild_id)
    role_entry = discord.utils.get(guild.roles, name='エントリー済')
    R = 0
    Y = 1
    G = 2
    B = 3
    # role_entryがついてる人一覧
    member_entry    = [member for member in guild.members if role_entry in member.roles]
    role_red_members = [(member.display_name, member.id, 1) for member in member_entry if discord.utils.get(member.roles, name='red')]
    role_yellow_members = [(member.display_name, member.id, 2) for member in member_entry if discord.utils.get(member.roles, name='yellow')]
    role_green_members = [(member.display_name, member.id, 3) for member in member_entry if discord.utils.get(member.roles, name='green')]
    role_blue_members = [(member.display_name, member.id, 4) for member in member_entry if discord.utils.get(member.roles, name='blue')]

class weapon_category(Enum):
    シューター1 = 'shooter1'
    シューター2 = 'shooter2'
    ローラー = 'roller'
    チャージャー = 'charger'
    スロッシャー = 'slosher'
    スピナー = 'spiner'
    マニューバー = 'maneuver'
    シェルター = 'shelter'
    ブラスター = 'blaster'
    フデ = 'brush'
    ストリンガー = 'stringer'
    ワイパー = 'wiper'

@client.tree.command(name="ssd使用ブキ申請", 
                     description="使うブキを試合前に申請するコマンド")
@app_commands.describe(
    ブキカテゴリ='ブキのカテゴリを選んでください',
)
async def test_command2(interaction: discord.Interaction,  ブキカテゴリ: weapon_category):
    weapon_num_dict = {
        weapon_category.シューター1 : 0,
        weapon_category.シューター2 : 1,
        weapon_category.ブラスター : 2,
        weapon_category.ローラー : 3,
        weapon_category.フデ : 4,
        weapon_category.チャージャー : 5,
        weapon_category.スロッシャー : 6,
        weapon_category.スピナー : 7,
        weapon_category.マニューバー : 8,
        weapon_category.シェルター : 9,
        weapon_category.ストリンガー : 10,
        weapon_category.ワイパー : 11,
    }
    wepon_list = get_weapon_list.wepon_list_for_drop_down()
    select = []
    for i in range(len(wepon_list[weapon_num_dict[ブキカテゴリ]])):
        weapon_name = wepon_list[weapon_num_dict[ブキカテゴリ]][i]
        select.append(discord.SelectOption(label=weapon_name,value=weapon_name))
    view = discord.ui.View()
    view.add_item(discord.ui.Select(custom_id='iii',options=select))
    await interaction.response.send_message(view=view, ephemeral=True)

#全てのインタラクションを取得
@client.event
async def on_interaction(inter:discord.Interaction):
    try:
        if inter.data['component_type'] == 3:
            await on_dropdown(inter)
    except KeyError:
        pass

async def on_dropdown(inter:discord.Interaction):
    custom_id = inter.data["custom_id"]
    select_value = inter.data["values"][0]
    player_name = inter.user.display_name
    player_d_id = inter.user.id

    cursor.execute(f"SELECT wp_id FROM weapon_tb WHERE wp_name = '{select_value}'")
    rows = cursor.fetchall()
    wp_id = '' # 使ったブキのw_id
    for row in rows:
        wp_id = row[0]
    print(wp_id)

    cursor.execute(f"SELECT p_id FROM player_tb WHERE d_id = '{player_d_id}'")
    rows = cursor.fetchall()
    p_id = '' # 使った人のd_id
    for row in rows:
        p_id = row[0]
    print(p_id)

    cursor.execute(f"SELECT color FROM player_tb WHERE d_id = '{player_d_id}'")
    rows = cursor.fetchall()
    color = '' # 使った人の色コード color
    for row in rows:
        color = row[0]
    print(color)

    cursor.execute(f"SELECT wp_id FROM used_weapon_tb WHERE p_id = '{p_id}'")
    rows = cursor.fetchall()
    # 出力
    used_weapon_id_list = []
    # 結果を表示する
    for row in rows:
        used_weapon_id_list.append(row[0])
    print('インサート前')
    print(used_weapon_id_list)

    exceeded_usage_count = False
     
    if color==1: # 赤のとき
        if used_weapon_id_list.count(wp_id) >= color:
            exceeded_usage_count = True
    elif color==2:
        if used_weapon_id_list.count(wp_id) >= color:
            exceeded_usage_count = True
    
    if exceeded_usage_count:
        msg = f'{select_value}は既に{color}回使用しています。別のブキを選んでください。'
        used_weapon_name_list = []
        for weapon_id in used_weapon_id_list:
            cursor.execute(f"SELECT wp_name FROM weapon_tb WHERE wp_id = '{weapon_id}'")
            rows = cursor.fetchall()
            # 結果を表示する
            for row in rows:
                used_weapon_name_list.append(row[0])
            
            embed = create_embed_send_weapon_failed(msg, used_weapon_name_list)
        await inter.response.send_message(embed=embed, ephemeral=True)
    else:
        wp_id_p_id_color_tuple = (p_id, wp_id) # プレイヤーID, ブキID, 色 
        # データを挿入
        insert_used_weapon = "INSERT INTO used_weapon_tb (p_id, wp_id) VALUES (%s, %s);"
        cursor.execute(insert_used_weapon, wp_id_p_id_color_tuple)
        db.commit()
        # used_weapon_tbの中で、この人のp_idがある全てのローのwidを出す
        msg = f'{select_value}を申請しました。'
        cursor.execute(f"SELECT wp_id FROM used_weapon_tb WHERE p_id = '{p_id}'")
        rows = cursor.fetchall()
        # 出力
        used_weapon_id_list = []
        # 結果を表示する
        for row in rows:
            used_weapon_id_list.append(row[0])
        print('インサート後')
        print(used_weapon_id_list)
        used_weapon_name_list = []
        for weapon_id in used_weapon_id_list:
            cursor.execute(f"SELECT wp_name FROM weapon_tb WHERE wp_id = '{weapon_id}'")
            rows = cursor.fetchall()
            # 結果を表示する
            for row in rows:
                used_weapon_name_list.append(row[0])
        embed = create_embed_send_weapon_successed(msg, used_weapon_name_list)
        await inter.response.send_message(embed=embed, ephemeral=True)
    
@client.tree.command(name="ssd申請済ブキ表示", 
                     description="申請済みのブキを表示します。")
async def test_command2(interaction: discord.Interaction):
    d_id = interaction.user.id
    p_name = interaction.user.display_name
    cursor.execute(f"SELECT p_id FROM player_tb WHERE d_id = '{d_id}'")
    rows = cursor.fetchall()
    # 出力
    p_id = ''
    # 結果を表示する
    for row in rows:
        p_id = row[0]

    cursor.execute(f"SELECT wp_id FROM used_weapon_tb WHERE p_id = '{p_id}'")
    rows = cursor.fetchall()
    # 出力
    used_weapon_id_list = []
    # 結果を表示する
    for row in rows:
        used_weapon_id_list.append(row[0])
    print(used_weapon_id_list)
    used_weapon_name_list = []
    for wp_id in used_weapon_id_list:
        cursor.execute(f"SELECT wp_name FROM weapon_tb WHERE wp_id = '{wp_id}'")
        rows = cursor.fetchall()
        # 結果を表示する
        for row in rows:
            used_weapon_name_list.append(row[0])
    avatar = interaction.user.display_avatar
    embed = create_embed_used_weapon(p_name, used_weapon_name_list, avatar)

    await interaction.response.send_message(embed=embed, ephemeral=False)

@client.event
async def on_message(message):
    if message.author == client.user: 
        return
    if message.content.startswith('?roll'):
        r = '?roll d'
        num_list = [4, 6, 8, 10, 12, 20, 100]
        avatar = message.author.display_avatar
        name = message.author.display_name
        try :
            if message.content.startswith(r):
                num = int(message.content.split()[1][1:])
                if num in num_list:
                    embed = create_embed_roll_dies(name, num, avatar)
                    print(f'{name}ダイスロール')
                else :
                    embed = discord.Embed(title='?roll について',
                                description='',
                                color=0xffffff, 
                                )
                    embed.add_field(name="説明",value="ダイスを振ります。\n [ダイスの目の数]は、d4, d6, d8, d10, d12, d20, d100 から選べます。")
                    embed.add_field(name="使い方",value="?roll [ダイスの目の数]")
                    embed.add_field(name="使用例",value="?roll d4 \n ?roll d20 \n ?roll d100")   
        except :
            embed = discord.Embed(title='?roll について',
                                description='',
                                color=0xffffff, 
                                )
            embed.add_field(name="説明",value="ダイスを振ります。\n [ダイスの目の数]は、d4, d6, d8, d10, d12, d20, d100 から選べます。")
            embed.add_field(name="使い方",value="?roll [ダイスの目の数]")
            embed.add_field(name="使用例",value="?roll d4 \n ?roll d20 \n ?roll d100")
        finally:
            await message.channel.send(embed=embed)
            



client.run(config_ini.get('TOKEN', 'token'))