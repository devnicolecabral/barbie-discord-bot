import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone
import json5
import asyncio

class TicketManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config.jsonc', 'r', encoding='utf-8') as f:
            self.config = json5.load(f)
        self.close_old_tickets.start()

    @tasks.loop(hours=1)
    async def close_old_tickets(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(int(self.config['dreamhouse_server_id']))
        if not guild: return

        ticket_category_id = self.config.get('ticket_category_id')
        if not ticket_category_id: return

        ticket_category = guild.get_channel(int(ticket_category_id))
        if not ticket_category or not isinstance(ticket_category, discord.CategoryChannel): return

        limit_seconds = self.config.get("ticket_close_after_hours", 48) * 3600
        now = datetime.now(timezone.utc)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] TICKET_MANAGER: Verificando tickets antigos...")
        for channel in ticket_category.text_channels:
            
            # TRAVA DE SEGURANÇA ADICIONAL POR CONTA DO BUG QUE APAGOU TUDO
            # Se o nome do canal contiver "verifique-se", PULAR IMEDIATAMENTE.
            # Isso protege o canal principal, não importa os símbolos ou emojis
            if "verifique-se" in channel.name:
                continue
            # FIM DA TRAVA DE SEGURANÇA

            # Checagem original
            # Só considera canais que começam com 'ticket-' ou 'verificacao-'.
            if not channel.name.startswith(('ticket-', 'verificacao-')):
                continue
            
            age = now - channel.created_at
            
            if age.total_seconds() > limit_seconds:
                print(f"TICKET_MANAGER: O canal de ticket '{channel.name}' é antigo. Fechando.")
                try:
                    await channel.send("> 自動閉鎖\n> Este ticket está sendo fechado automaticamente por inatividade.")
                    await asyncio.sleep(10)
                    await channel.delete(reason="Fechado automaticamente por inatividade")
                except Exception as e:
                    print(f"TICKET_MANAGER: Erro ao fechar o canal {channel.name}: {e}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] TICKET_MANAGER: Verificação concluída.")


async def setup(bot):
    await bot.add_cog(TicketManager(bot))