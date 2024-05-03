import discord
from datetime import datetime
from itertools import cycle
from discord.ext import commands, tasks

TOKEN = '輸入你自己的機器人token'
CHANNEL_ID = '輸入你自己的channel_id'
TARGET_DATE = datetime(2024, 7, 12, 8, 0, 0)  #目標日期，可以自己改 年/月/日/時/分/秒

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="*", intents=intents) 
status = cycle(['分科倒數{remaining_days}天', '剩下{remaining_days}天還不去讀書?']) #能自己更改機器人狀態，10秒一循環

@bot.event
async def on_ready():
    print(f'機器人已上線：{bot.user}')
    change_status.start()

@tasks.loop(seconds=10)  # 每隔10秒更換一次機器人個人狀態
async def change_status():
    if bot.is_ready():  
        now = datetime.now()
        remaining_days = (TARGET_DATE - now).days
        activity = discord.Game(next(status).format(remaining_days=remaining_days))
        await bot.change_presence(activity=activity)

@tasks.loop(seconds=10)  # 每十秒確認時間
async def check_time():
    if bot.is_ready():  
        now = datetime.now().time()
        if now.hour == TARGET_DATE.hour and now.minute == TARGET_DATE.minute:
            channel = bot.get_channel(int(CHANNEL_ID))
            remaining_days = (TARGET_DATE - datetime.now()).days
        await channel.send(f'**距離分科測驗還有 {remaining_days} 天**') # 這邊也都可以自己更改傳送訊息內容


bot.run(TOKEN)
