import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime, timezone
import json5
import asyncio

# Caminhos para os arquivos de dados
VERIFICATIONS_FILE = 'data/verifications.json'
UNVERIFIED_USERS_FILE = 'data/unverified_users.json'


class Verificacao(commands.Cog):
    # MÉTODO __INIT__ CORRIGIDO 
    def __init__(self, bot):
        self.bot = bot
        # Pega a config diretamente do bot, que foi carregada no main.py a partir das Secrets/Variables. É mais eficiente e funciona online.
        self.config = bot.config 
        self.check_unverified_members.start()
    # FIM DA CORREÇÃO 

    # Funções Auxiliares
    def _load_data(self, file_path):
        if not os.path.exists(file_path): return {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return json.loads(content) if content else {}
        except json.JSONDecodeError: return {}

    def _save_data(self, data, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    # COMANDO !VERIFICAR
    @commands.command(name='verificar')
    async def verificar(self, ctx, membra: discord.Member):
        if not isinstance(ctx.author, discord.Member): return
        staff_id_str = str(ctx.author.id)
        main_verifier_role_id = int(self.config.get('verifier_role_id', 0))
        prep_heart_role_id = int(self.config.get('verifier_role_id_preparation_heart', 0))
        main_verifier_role = ctx.guild.get_role(main_verifier_role_id)
        prep_heart_role = ctx.guild.get_role(prep_heart_role_id)
        has_main_role = main_verifier_role in ctx.author.roles if main_verifier_role else False
        has_prep_heart_role = prep_heart_role in ctx.author.roles if prep_heart_role else False
        is_in_diary_list = staff_id_str in self.config['staff_diaries']
        is_main_staff = has_main_role and is_in_diary_list
        is_prep_heart_staff = has_prep_heart_role
        if not (is_main_staff or is_prep_heart_staff):
            await ctx.send(f"{ctx.author.mention}, você não tem permissão para usar este comando.", delete_after=10)
            return
        unverified_role = ctx.guild.get_role(int(self.config['unverified_role_id']))
        diva_role = ctx.guild.get_role(int(self.config['diva_role_id']))
        if not unverified_role or not diva_role: return await ctx.send("Erro: Cargos de verificação não encontrados.")
        try:
            await membra.remove_roles(unverified_role, reason=f"Verificada por {ctx.author.name}")
            await membra.add_roles(diva_role, reason=f"Verificada por {ctx.author.name}")
            await ctx.send(f"💄 Membra {membra.mention} verificada com sucesso por {ctx.author.mention}!")
        except Exception as e:
            return await ctx.send(f"Ocorreu um erro ao alterar cargos: {e}")
        verifications_data = self._load_data(VERIFICATIONS_FILE)
        current_count = verifications_data.get(staff_id_str, 0)
        new_count = current_count + 1
        verifications_data[staff_id_str] = new_count
        self._save_data(verifications_data, VERIFICATIONS_FILE)
        log_channel = None
        if is_prep_heart_staff:
            log_channel_id = int(self.config.get('preparation_heart_log_channel_id', 0))
            log_channel = self.bot.get_channel(log_channel_id)
        elif is_main_staff:
            log_channel_id = int(self.config['staff_diaries'][staff_id_str])
            log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(title="✨ Nova Verificação Realizada!", color=0xee82ee)
            embed.add_field(name="Staff", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="Total da Staff", value=f"`{new_count}`", inline=True)
            embed.add_field(name="Membra Verificada", value=f"{membra.mention} (`{membra.id}`)", inline=False)
            embed.set_footer(text=f"ID da Staff: {staff_id_str}")
            embed.timestamp = datetime.now(timezone.utc)
            await log_channel.send(embed=embed)
        else:
            await ctx.send("Aviso: O canal de log para esta verificação não foi encontrado.")
            print(f"AVISO: Canal de log não encontrado para a staff {ctx.author.name} ({staff_id_str})")

    # Listener on_member_join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != int(self.config['dreamhouse_server_id']): return
        print(f"Nova membra detectada: {member.name}. Iniciando monitoramento.")
        unverified_users = self._load_data(UNVERIFIED_USERS_FILE)
        unverified_users[str(member.id)] = {"join_timestamp": int(datetime.now(timezone.utc).timestamp()), "reminders_sent": []}
        self._save_data(unverified_users, UNVERIFIED_USERS_FILE)

    # Tarefa check_unverified_members
    @tasks.loop(minutes=1)
    async def check_unverified_members(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(int(self.config['dreamhouse_server_id']))
        if not guild: return
        unverified_role = guild.get_role(int(self.config['unverified_role_id']))
        if not unverified_role: return
        all_unverified = self._load_data(UNVERIFIED_USERS_FILE)
        for member_id_str, data in list(all_unverified.items()):
            member = guild.get_member(int(member_id_str))
            if not member or unverified_role not in member.roles:
                del all_unverified[member_id_str]
                continue
            now = int(datetime.now(timezone.utc).timestamp())
            elapsed_seconds = now - data["join_timestamp"]
            reminders_sent = data["reminders_sent"]
            try:
                # FUNÇÃO DE EXPULSÃO DESATIVADA POIS ESTAVA DANDO PROBLEMAS 
                #if elapsed_seconds > 86400:
                #    await member.kick(reason="Não se verificou em 24 horas.")
                #    del all_unverified[member_id_str]
                #    print(f"Membro {member.name} expulso por inatividade.")
                
                # Terceiro lembrete após 15 horas (54000 segundos)
                if elapsed_seconds > 54000 and 3 not in reminders_sent:
                    await member.send("Olá! Este é nosso último lembrete. Por favor, verifique-se no servidor DreamHouse para ter acesso aos canais.")
                    all_unverified[member_id_str]["reminders_sent"].append(3)
                
                # Segundo lembrete após 3 horas (10800 segundos)
                elif elapsed_seconds > 10800 and 2 not in reminders_sent:
                    await member.send("Oie! Só passando para lembrar que sua verificação no servidor DreamHouse está pendente. Qualquer dúvida, é só chamar o suporte!")
                    all_unverified[member_id_str]["reminders_sent"].append(2)

                # Primeiro lembrete após 10 minutos (600 segundos)
                elif elapsed_seconds > 600 and 1 not in reminders_sent:
                    await member.send("Bem-vinda à DreamHouse! ✨ Vimos que você ainda não iniciou sua verificação. Clique no botão no canal #verifique-se para começar!")
                    all_unverified[member_id_str]["reminders_sent"].append(1)
            except Exception as e:
                print(f"Erro ao processar {member.name}: {e}")
        self._save_data(all_unverified, UNVERIFIED_USERS_FILE)

async def setup(bot):
    await bot.add_cog(Verificacao(bot))