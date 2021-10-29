
import discord, asyncio, os, platform, sys
from discord.ext.commands import Bot
from discord.ext import commands
if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config
  
intents = discord.Intents.all()

bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents)


@bot.event
async def on_ready():
	bot.loop.create_task(status_task())
	print(f"Logged in as {bot.user.name}")
	print(f"Discord.py API version: {discord.__version__}")
	print(f"Python version: {platform.python_version()}")
	print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
	print("---NOVA-BOT---")








async def status_task():
	while True:
		await bot.change_presence(activity=discord.Game("lucid dreams"))      

bot.remove_command("help")

if __name__ == "__main__":
	for file in os.listdir("./cogs"):
		if file.endswith(".py"):
			extension = file[:-3]
			try:
				bot.load_extension(f"cogs.{extension}")
				print(f"Loaded extension '{extension}'")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				print(f"Failed to load extension {extension}\n{exception}")


@bot.event
async def on_message(message):

	if message.author == bot.user or message.author.bot:
		return

	if message.author.id in config.BLACKLIST:
		return
	await bot.process_commands(message)


@bot.event
async def on_command_completion(ctx):
	fullCommandName = ctx.command.qualified_name
	split = fullCommandName.split(" ")
	executedCommand = str(split[0])
	print(f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


@bot.event
async def on_command_error(context, error):
	if isinstance(error, commands.CommandOnCooldown):
		embed = discord.Embed(
			title="Error!",
			description="This command is on a %.2fs cool down" % error.retry_after,
			color=config.error
		)
		await context.send(embed=embed)
	raise error


bot.run(config.TOKEN)