import asyncio
from secrets import choice
from pagermaid import Config, log
from pagermaid.listener import listener
from pagermaid.config import config
from pagermaid.enums import Message
from pagermaid.utils import alias_command, client, edit_delete
try:
	upstream_url = config["ericdress_upstream_url"]
except KeyError:
	try:
		from .upstream import upstream_url
	except ModuleNotFoundError:
		from .upstream_default import upstream_url

ericliu_said = []

async def init():
	response = await client.get(upstream_url)
	response.raise_for_status()
	ericliu_said = str(response.text).split(",\n")

@listener(command="updateericdress",
          description="抓取刘酱女装语料")
async def ericdress(message: Message):
	if not Config.SILENT:
		message = await message.edit("正在抓取刘酱女装语料...")
	try:
		init()
	except Exception as e:
		await edit_delete(message, f"抓取刘酱女装语料失败：{type(e).__name__}: {str(e)}")
	else:
		await edit_delete(message, f"抓取刘酱女装语料成功，快使用{alias_command('ericdress')}来催促刘酱女装吧！")

@listener(command="ericdress",
          description="刘酱快女装！")
async def ericdress(message: Message):
	if len(ericliu_said) == 0:
		await edit_delete(message, f"语料库是空的，请使用{alias_command('updateericdress')}抓取语料。")
	else:
		await message.edit(choice(ericliu_said))
		
async def safe_init():
	try:
		await init()
	except Exception as e:
		log.exception(f"{type(e).__name__}: {str(e)}")

asyncio.run(safe_init())
