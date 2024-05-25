import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import asyncio
from itertools import cycle

# 設置intents
intents = discord.Intents.default()
intents.message_content = True  # 啟用 message_content intent 以便bot能夠讀取消息內容
status = cycle(['分科倒數{remaining_days}天', '剩下{remaining_days}天還不去讀書?'])
TARGET_DATE = datetime(2024, 7, 13, 8, 0, 0)  #目標日期，可以自己改 年/月/日/時/分/秒

# 創建一個機器人的實例
bot = commands.Bot(command_prefix='!', intents=intents)

async def send_days_left(channel):
    target_date = datetime(2024, 7, 13)
    current_date = datetime.now()
    days_remaining = (target_date - current_date).days
    await channel.send(f'**距離分科測驗還有 {days_remaining} 天**')

@tasks.loop(seconds=10)  # 每隔10秒更換一次機器人個人狀態
async def change_status():
    if bot.is_ready():  
        now = datetime.now()
        remaining_days = (TARGET_DATE - now).days
        activity = discord.Game(next(status).format(remaining_days=remaining_days))
        await bot.change_presence(activity=activity)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # 獲取特定頻道
    channel = bot.get_channel(YOUR_CHANNEL_ID)  # 替換 YOUR_CHANNEL_ID 為你指定的頻道ID
    if channel is not None:
        daily_task.start(channel)  # 啟動每日任務
        change_status.start()
@tasks.loop(seconds=10)
async def daily_task(channel):
    now = datetime.now()
    if now.time() >= time(8, 0) and now.time() < time(8, 0, 10):
        await send_days_left(channel)

@bot.command()
async def days_left(ctx):
    await send_days_left(ctx.channel)

bot.run('YOUR_BOT_TOKEN')  # 替換 YOUR_BOT_TOKEN 為你的機器人token
