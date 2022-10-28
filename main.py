import os
from time import sleep
import datetime
import requests
import json
import discord
from discord.ext import commands
from discord.ext import tasks
from server import keep_alive

my_secret = os.environ['TOKEN']
CHANNEL_ID = 1035060199305793567  #チャンネルID

discord_intents = discord.Intents.all()
discord_intents.typing = False
discord_intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord_intents)
# p1: {regular|bankara-challenge|bankara-open|fest|coop-grouping-regular}
# p2: {now|next|schedule}


@bot.event
# Botの準備完了時に呼び出されるイベント
async def on_ready():
  print('We have logged in as {0}'.format(bot.user))


@bot.command()
async def now(ctx):
  apiurl = 'https://spla3.yuu26.com/api/schedule/'
  r = requests.get(apiurl)
  result = r.json()["result"]

  print(result["bankara_open"][0]["stages"][0]["name"],
        result["bankara_open"][0]["stages"][1]["name"])

  str_time_start = result["regular"][0]["start_time"][11:]
  str_time_end = result["regular"][0]["end_time"][11:]

  str_bankara_challenge_rule = result["bankara_challenge"][0]["rule"]["name"]
  str_bankara_open_rule = result["bankara_open"][0]["rule"]["name"]

  str_regular_a = result["regular"][0]["stages"][0]["name"]
  str_bankara_challenge_a = result["bankara_challenge"][0]["stages"][0]["name"]
  str_bankara_open_a = result["bankara_open"][0]["stages"][0]["name"]
  str_regular_b = result["regular"][0]["stages"][1]["name"]
  str_bankara_challenge_b = result["bankara_challenge"][0]["stages"][1]["name"]
  str_bankara_open_b = result["bankara_open"][0]["stages"][1]["name"]

  str_regular = str_regular_a + "," + str_regular_b
  str_bankara_challenge = str_bankara_challenge_a + "," + str_bankara_challenge_b
  str_bankara_open = str_bankara_open_a + "," + str_bankara_open_b

  if ctx.author == bot.user:
    return

  await ctx.send(
    '''\
```asciidoc
%s 〜 %s
[ナワバリ]
%s
[バンカラ(チャレンジ)(%s)]
%s
[バンカラ(オープン)(%s)]
%s
```\
        ''' %
    (str_time_start, str_time_end, str_regular, str_bankara_challenge_rule,
     str_bankara_challenge, str_bankara_open_rule, str_bankara_open))


@bot.command()
async def next(ctx):
  apiurl = 'https://spla3.yuu26.com/api/schedule/'
  r = requests.get(apiurl)
  result = r.json()["result"]

  print(result["bankara_open"][1]["stages"][0]["name"],
        result["bankara_open"][0]["stages"][1]["name"])

  str_time_start = result["regular"][1]["start_time"][11:]
  str_time_end = result["regular"][1]["end_time"][11:]

  str_bankara_challenge_rule = result["bankara_challenge"][1]["rule"]["name"]
  str_bankara_open_rule = result["bankara_open"][1]["rule"]["name"]

  str_regular_a = result["regular"][1]["stages"][0]["name"]
  str_bankara_challenge_a = result["bankara_challenge"][1]["stages"][0]["name"]
  str_bankara_open_a = result["bankara_open"][1]["stages"][0]["name"]
  str_regular_b = result["regular"][1]["stages"][1]["name"]
  str_bankara_challenge_b = result["bankara_challenge"][1]["stages"][1]["name"]
  str_bankara_open_b = result["bankara_open"][1]["stages"][1]["name"]

  str_regular = str_regular_a + "," + str_regular_b
  str_bankara_challenge = str_bankara_challenge_a + "," + str_bankara_challenge_b
  str_bankara_open = str_bankara_open_a + "," + str_bankara_open_b

  if ctx.author == bot.user:
    return

  await ctx.send(
    '''\
```asciidoc
%s 〜 %s
[ナワバリ]
%s
[バンカラ(チャレンジ)(%s)]
%s
[バンカラ(オープン)(%s)]
%s
```\
        ''' %
    (str_time_start, str_time_end, str_regular, str_bankara_challenge_rule,
     str_bankara_challenge, str_bankara_open_rule, str_bankara_open))


@tasks.loop(seconds=60)
async def loop():
  t_delta = datetime.timedelta(hours=9)
  JST = datetime.timezone(t_delta, 'JST')
  now = datetime.datetime.now(JST).strftime('%H:%M')
  #print(now)
  if now == '07:00' or now == '07:00' or now == '09:00' or now == '11:00' or now == '13:00' or now == '15:00' or now == '17:00' or now == '19:00' or now == '21:00' or now == '23:00' or now == '01:00' or now == '03:00' or now == '05:00':
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    apiurl = 'https://spla3.yuu26.com/api/schedule/'
    r = requests.get(apiurl)
    result = r.json()["result"]

    print(result["bankara_open"][0]["stages"][0]["name"],
          result["bankara_open"][0]["stages"][1]["name"])

    str_time_start = result["regular"][0]["start_time"][11:]
    str_time_end = result["regular"][0]["end_time"][11:]

    str_bankara_challenge_rule = result["bankara_challenge"][0]["rule"]["name"]
    str_bankara_open_rule = result["bankara_open"][0]["rule"]["name"]

    str_regular_a = result["regular"][0]["stages"][0]["name"]
    str_bankara_challenge_a = result["bankara_challenge"][0]["stages"][0][
      "name"]
    str_bankara_open_a = result["bankara_open"][0]["stages"][0]["name"]
    str_regular_b = result["regular"][0]["stages"][1]["name"]
    str_bankara_challenge_b = result["bankara_challenge"][0]["stages"][1][
      "name"]
    str_bankara_open_b = result["bankara_open"][0]["stages"][1]["name"]

    str_regular = str_regular_a + "," + str_regular_b
    str_bankara_challenge = str_bankara_challenge_a + "," + str_bankara_challenge_b
    str_bankara_open = str_bankara_open_a + "," + str_bankara_open_b

    await channel.send(
      '''\
```asciidoc
%s 〜 %s
[ナワバリ]
%s
[バンカラ(チャレンジ)(%s)]
%s
[バンカラ(オープン)(%s)]
%s
```\
        ''' %
      (str_time_start, str_time_end, str_regular, str_bankara_challenge_rule,
       str_bankara_challenge, str_bankara_open_rule, str_bankara_open))


@bot.listen()
async def on_ready():
  loop.start()  # important to start the loop


keep_alive()
try:
  bot.run(my_secret)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  os.system("python restarter.py")
  os.system('kill 1')
