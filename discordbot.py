# インストールした discord.py を読み込む
import discord
import operator as op
import json

# アクセストークン
TOKEN = 'ODYxMTA4NDk5OTMzNDI5Nzgx.YOE_yQ.KM0Mroai-aK7TJRshqJr6lmXrKc'

# 接続に必要なオブジェクトを生成
client = discord.Client()

userlist = [[0 for _ in range(2)] for _ in range(0)]
#firstcheck = True


@client.event
async def on_raw_reaction_add(payload):
    #emojiIDが51スタンプ以外の際はやらない
    if payload.emoji.id != 861122962006867988:
        print("b")
        return
    # 絵文字を返信
    msgID = payload.message_id
    #チャンネル取得
    Channel = client.get_channel(payload.channel_id)
    #メッセージ取得
    message = await Channel.fetch_message(msgID)
    authorID = message.author.id
    user = await client.fetch_user(authorID)
    author = user.name
    
    # jsonファイル取得とリストに代入
    json_open= open("userlist.json","r")
    json_load = json.load(json_open)

    userlist = list(json_load)

    result = False
    for i in userlist:
        if author in i:
            result = True
            break
    result
    
    if result == False:
        add = [author,0]
        userlist.append(add)
        print("初回追加")

    for i in userlist:
        if author in i:
            j = userlist.index(i)
            userlist[j][1] = userlist[j][1]+1
            break
    await Channel.send(author)
    userlist.sort(reverse = True,key=op.itemgetter(1))
    print(*userlist, sep='\n')
    #jsonファイル用に辞書変換・書き出し
    f= open("userlist.json","w")
    json.dump(userlist,f,ensure_ascii=False)


@client.event
async def on_raw_reaction_remove(payload):
    #jsonファイル取得用に辞書変換
    json_open= open("userlist.json","r")
    json_load = json.load(json_open)
    userlist = list(json_load)

    if payload.emoji.id != 861122962006867988:
        print("b")
        return
    #メッセージID取得
    msgID = payload.message_id
    #チャンネル取得
    Channel = channel = client.get_channel(payload.channel_id)
    #メッセージ取得
    message = await Channel.fetch_message(msgID)
    #メッセージ送信者ID取得
    authorID = message.author.id
    #メッセージ送信者取得
    user = await client.fetch_user(authorID)
    author = user.name

    #ユーザーの有無チェック
    result = False
    for i in userlist:
        if author in i:
            result = True
            break
    result
    
    if result == False:
        return

    for i in userlist:
        if author in i:
            j = userlist.index(i)
            if userlist[j][1]>0:
                userlist[j][1] -= 1
            else:
                userlist[j][1]=0
            break
    await Channel.send(author)
    userlist.sort(reverse = True,key=op.itemgetter(1))
    print(*userlist, sep='\n')

    #jsonファイル用に辞書変換・書き出し
    f= open("userlist.json","w")
    json.dump(userlist,f,ensure_ascii=False)




@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    #jsonファイル取得用に辞書変換
    json_open= open("userlist.json","r")
    json_load = json.load(json_open)
    userlist = list(json_load)

    #個人順位の取得
    if message.content == '!search':
        authorID = message.author.id
        user = await client.fetch_user(authorID)
        author = user.name
        for i in userlist:
            if author in i:
                result_search = True
                j = userlist.index(i)
                print(j)
                break
        result_search

        for i in userlist:
            if author in i:
                j = userlist.index(i)
                text = "あなたの51ポイントは"+str(userlist[j][1])+"、現在順位は"+str(j+1)+ "位です"
                break
        await message.channel.send(text)

    if message.content == '!list':
        #全体順位の取得
        j=0
        for i in userlist:
            text = str(j+1)+"位:"+userlist[j][0]+":"+str(userlist[j][1])+ "pt"
            await message.channel.send(text)
            j+=1

client.run(TOKEN)