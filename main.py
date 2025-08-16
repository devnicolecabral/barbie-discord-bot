import os 
import json5
import discord 
from discord.ext import commands 
from dotenv import load_dotenv

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Carregando as configurações do arquivo jsonc
with open('config.jsonc', 'r', encoding='utf-8') as f:
    config = json5.load(f)

# Definindo as intenções do bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Criando a instância do bot
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

# Evento que é acionado quando a barbie está pronta e conectada ao Discord 
@bot.event
async def on_ready():
    print(f'Logado como: {bot.user.name}')
    print(f'ID do Bot: {bot.user.id}')
    print('--------------')

    # Carregando todos os cogs 
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Carregando o cog: {filename}')
            except Exception as e:
                print(f'Falha ao carregar o cog: {filename}: {e}')
    
    print('--------------')
    print(f'Barbie está online e pronta para brilhar! ✨ - {discord.utils.utcnow().strftime("%d/%m/%Y %H:%M:%S")}')

# Iniciando o bot com o TOKEN
bot.run(TOKEN)