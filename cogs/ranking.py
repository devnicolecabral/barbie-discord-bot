import discord
from discord.ext import commands
import json
import json5
import os
from datetime import datetime

# Caminho pro arquivo de dados de verificação
VERIFICATIONS_FILE = 'data/verifications.json'

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config.jsonc', 'r', encoding='utf-8') as f:
            self.config = json5.load(f)

    def _load_verifications_data(self):
        """Carrega os dados de verificação do arquivo JSON."""
        if not os.path.exists(VERIFICATIONS_FILE):
            return {}
        try:
            with open(VERIFICATIONS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            return {}

    @commands.command(name='rankingverificacoes')
    async def ranking_verificacoes(self, ctx):
        """Mostra o ranking de quem mais verificou membras."""

        # 1. Checagem: O comando só pode ser usado no servidor da staff
        if ctx.guild.id != int(self.config['staff_server_id']):
            await ctx.send("Este comando só pode ser usado no servidor da Staff.", delete_after=10)
            return

        # 2. Carregar os dados
        verifications_data = self._load_verifications_data()

        if not verifications_data:
            await ctx.send("Ainda não há nenhuma verificação registrada para criar um ranking.")
            return

        # 3. Organizar os dados
        # O 'key=lambda item: item[1]' diz para ordenar pela contagem (o segundo valor)
        # 'reverse=True' faz ser do maior para o menor
        sorted_staff = sorted(verifications_data.items(), key=lambda item: item[1], reverse=True)

        # 4. Montar a mensagem (Embed)
        embed = discord.Embed(
            title="🏆 Ranking de Verificações da Staff",
            description="Quem mais ajudou a casa a crescer! 💖",
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )

        description_text = ""
        rank_emojis = {1: "🥇", 2: "🥈", 3: "🥉"}

        for i, (staff_id, count) in enumerate(sorted_staff[:10]): # Pega só o top 10
            rank = i + 1
            try:
                # Tenta buscar o nome da membra no servidor da staff
                staff_member = await self.bot.fetch_user(int(staff_id))
                staff_name = staff_member.display_name
            except discord.NotFound:
                staff_name = f"ID Desconhecido ({staff_id})"

            emoji = rank_emojis.get(rank, f"**{rank}.**")
            description_text += f"{emoji} {staff_name} - `{count}` verificações\n"

        embed.description = description_text
        embed.set_footer(text="DreamHouse Staff DRH")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Ranking(bot))