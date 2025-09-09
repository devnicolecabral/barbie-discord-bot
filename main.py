import os
import json5
import discord
from discord.ext import commands

# Inicio da lógica de configuração para hospedagem discloud
# Construi o dicionario de config a partir das variáveis de ambiente que serão definidas no painel da discloud

config = {
    "prefix": os.getenv('prefix'),
    "dreamhouse_server_id": os.getenv('dreamhouse_server_id'),
    "staff_server_id": os.getenv('staff_server_id'),
    "unverified_role_id": os.getenv('unverified_role_id'),
    "diva_role_id": os.getenv('diva_role_id'),
    "verifier_role_id": os.getenv('verifier_role_id'),
    "verifier_role_id_preparation_heart": os.getenv('verifier_role_id_preparation_heart'),
    "preparation_heart_log_channel_id":os.getenv('preparation_heart_log_channel_id'),
    "ticket_category_id": os.getenv('ticket_category_id'),
    "ticket_close_after_hours" : int(os.getenv('ticket_close_after_hours', 48)),
    "staff_diares": json5.loads(os.getenv('staff_diares', '{}'))
}
# Fim da lógica de config pro discloud

# Pegando o token diretamente das variáveis de ambiente 
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("ERRO CRÍTICO: DISCORD_TOKEN não foi encontrado nas variáveis de ambiente.")
    exit()

# Definindo as intenções do BOT 
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Criando a instância 
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

# Anexando a config construída à instância do bot 
# Agora, qualquer Cog poderá acessar as configs com `self.bot.config`
bot.config = config

# Evento que é acionado quando o bot está pronto
@bot.event
async def on_ready():
    print(f'Logado como {bot.user.name}')
    print(f'ID do Bot: {bot.user.id}')
    print('------')
    # Carregando os cogs da pasta /cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Carregado o cog: {filename}')
            except Exception as e:
                print(f'Falha ao carregar o cog {filename}: {e}')
    print('------')
    print(f'Barbie está online e pronta para brilhar! ✨')


# Inicia o bot
bot.run(TOKEN)