from discord.ext import commands
from database.banco import Banco
from dotenv import load_dotenv
from pathlib import Path
import os

if __name__ == '__main__':
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    TOKEN = os.getenv("TOKEN")
    bot = commands.Bot(command_prefix='$')
    db = Banco()
    db.iniciar()
    bot.load_extension("cogs.dev_commands")
    bot.load_extension("cogs.management")
    bot.load_extension("cogs.moves")
    bot.run(TOKEN)