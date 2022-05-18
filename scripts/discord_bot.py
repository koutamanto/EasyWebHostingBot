from datetime import datetime
import json
import os
import discord
from zipfile import ZipFile

client = discord.Client()

is_one_directory = True

host = "http://127.0.0.1"

def _write(wait):
    with open("json/discord_bot_wait.json", "w") as f:
        json.dump(wait, f)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global is_one_directory
    global host
    if message.author == client.user:
        return
    with open("json/discord_bot_wait.json", "r") as f:
        wait = json.load(f)
    if message.content in ["start", "s", "開始"]:
        wait[str(message.author.id)] = {}
        wait[str(message.author.id)]["next"] = "subdomain"
        # with open("json/discord_bot_wait.json", "w") as f:
        #     json.dump(wait, f)
        _write(wait)
        await message.channel.send("公開に使用したいサブドメインを英数字で入力してください。")
        return
    if wait[str(message.author.id)]["next"] == "subdomain":
        wait[str(message.author.id)]["next"] = "save"
        wait[str(message.author.id)]["subdomain"] = message.content
        _write(wait)
        await message.channel.send("サブドメインを設定しました。\n公開したいファイル(HTML/CSS/JavaScript/Fontなど)の入ったフォルダをzip形式に圧縮してアップロードしてください。")
    if wait[str(message.author.id)]["next"] == "save":
        await message.attachments[0].save(f'scripts/tmp/{wait[str(message.author.id)]["subdomain"]}.zip')
        wait[str(message.author.id)]["next"] = "saved"
        path = f'scripts/tmp/{wait[str(message.author.id)]["subdomain"]}.zip'
        with ZipFile(path, 'r') as zip:
            zip.extractall(f'templates/datas/{wait[str(message.author.id)]["subdomain"]}/')
        items = os.listdir(f'templates/datas/{wait[str(message.author.id)]["subdomain"]}/')
        j = 0
        for item in items:
            j = j + 1
            one_directory_path = os.path.join(f'templates/datas/{wait[str(message.author.id)]["subdomain"]}/', item)
            if j == 1:         
                if not os.path.isfile(path):
                    is_one_directory = True
                    break
            else:
                is_one_directory = False
        if is_one_directory:
            os.system(f'move {one_directory_path} templates\\datas\\')
            print(f'move {one_directory_path} templates\\datas\\')
            os.system(f'rd /s /q templates\\datas\\{wait[str(message.author.id)]["subdomain"]}')
            print(f'rd /s /q templates\\datas\\{wait[str(message.author.id)]["subdomain"]}')
            os.system(f'ren templates\\datas\\{item} {wait[str(message.author.id)]["subdomain"]}')
            print(f'ren templates\\datas\\{item} {wait[str(message.author.id)]["subdomain"]}')
        # items = os.listdir(".")
        # for item in items:
        #     path = os.path.join(path, item)
        #     if ".html" in item:
        #         break
        #     else:
        #         path = os.path.join(path, item)
        #         if not os.path.isfile():
        #             items = os.listdir(path)
        #             for item in items:
        #                 if ".html" in item:
        #                     break
        with open("json/infos.json", "r") as f:
            infos = json.load(f)
        datetime.now().day
        infos[wait[str(message.author.id)]["subdomain"]] = {
            "user_id": str(message.author.id),
            "subdomain": wait[str(message.author.id)]["subdomain"],
            "path": f'templates/datas/{wait[str(message.author.id)]["subdomain"]}'
        }
        with open("json/infos.json", "w") as f:
            json.dump(infos, f)
        _write(wait)
        await message.channel.send("アップロードが完了しました。")
        await message.channel.send(f'URL: {host}/{wait[str(message.author.id)]["subdomain"]}\nトップページのURL: {host}/{wait[str(message.author.id)]["subdomain"]}/index.html')
        
        
client.run('OTc2NDAwMjcxNTY1NTQxMzc3.GHUSKi.dtke3efdgtQTg02c6b9eCiDQOvIwqWaNrhZtqw')
