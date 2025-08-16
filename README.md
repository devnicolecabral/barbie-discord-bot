# 💖 Bot Barbie
O Barbie Bot foi desenvolvido em Python com a biblioteca **discord.py** para ser a principal ferramenta de automação e gerenciamento do servidor **DreamHouse** — um espaço seguro e acolhedor para mulheres. Ele trabalha em conjunto com outros bots (como o Ken) para criar uma experiência de verificação fluida, segura e engajante para as novas membras, além de fornecer ferramentas poderosas para a equipe de Staff.

O projeto foi construído com uma arquitetura de Cogs, separando cada funcionalidade em módulos para facilitar a manutenção e a adição de novos recursos no futuro.

Trabalhando junto com o Ken, a nossa querida Barbie é responsável por:
- Automação de Boas-Vindas: Monitora a entrada de novas membras e inicia um processo de acompanhamento para garantir que elas se verifiquem.
-  Lembretes Automáticos por DM: Envia mensagens diretas e personalizadas em intervalos de tempo (10 min, 3h e 15h) para membras que ainda não iniciaram sua verificação.
-  Gerenciamento de Inatividade: Remove automaticamente do servidor as membras que não se verificam dentro de 24 horas, mantendo a comunidade limpa e segura.
- Comando de Verificação (!verificar): Permite que a Staff finalize o processo de verificação com um simples comando, que automaticamente ajusta os cargos da membra.
-  Logs Detalhados e Personalizados: Cada verificação realizada é registrada em um canal de "diário" privado para a staff que a realizou, contendo informações detalhadas e a contagem total de verificações.
- Ranking da Staff (!rankingverificacoes): Um comando exclusivo para o servidor da equipe que exibe um ranking de quem mais realizou verificações, promovendo o engajamento.
- Fechamento Automático de Tickets: Mantém o servidor organizado fechando automaticamente os tickets de verificação ou suporte que estão inativos há mais de 48 horas

## 💻 Tecnologias

- Python 3.10+
- [discord.py](https://discordpy.readthedocs.io/) - Principal biblioteca para interação com a API do Discord.
- [python-dotenv](https://pypi.org/project/python-dotenv.) - Para gerenciamento de variáveis de ambiente e segurança do token.
- [json5](https://pypi.org/project/json5) - Para a leitura de arquivos de configuração com suporte a comentários.

## 🗂️ Estrutura
barbie-bot/ <br>
├── .venv/<br>
├── cogs/<br>
│   ├── verificacao.py       # Lógica de verificação e monitoramento<br>
│   ├── ranking.py           # Comando de ranking<br>
│   └── tickets.py           # Lógica de fechamento de tickets<br>
├── data/<br>
│   ├── verifications.json   # "Banco de dados" das contagens<br>
│   └── unverified_users.json# "Banco de dados" das membras não verificadas<br>
│
├── .env                     # Arquivo com o token do bot (secreto)<br>
├── config.jsonc             # Configurações gerais (IDs, prefixo, etc.)<br>
├── main.py                  # Ponto de entrada do bot<br>
└── requirements.txt         # Lista de dependências Python<br>
<br>
Organizado com base em boas práticas, o projeto conta com módulos separados para comandos, eventos, utilitários e agendamento.

## 🤖 Referência de Comandos
| Comando                 | Descrição                                         | Exemplo de Uso                      | Local de Uso          |
| ----------------------- | ------------------------------------------------- | ----------------------------------- | --------------------- |
| `!verificar`            | Finaliza a verificação e atualiza os cargos.      | `!verificar @usuaria`               | Servidor **DreamHouse** |
| `!rankingverificacoes`  | Exibe o ranking de verificações da equipe.        | `!rankingverificacoes`              | Servidor **Staff DRH** |


## 💖 Feito com propósito

Este bot foi criado de mulheres e para mulheres, para tornar a experiência de entrada no servidor mais acolhedora, controlada e eficiente, com toda a elegância de uma verdadeira **Barbie**.
