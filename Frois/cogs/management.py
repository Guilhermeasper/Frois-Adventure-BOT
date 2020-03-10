import sqlite3
from discord.ext import commands
from game.game import Game
from database.banco import Banco

mapa = Game()


class Gerenciamento(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command(name='começar', help='Inicia o jogo para o seu perfil')
    async def comecar(self, ctx):
        player_id = str(ctx.author.id)
        personagem = self.db.procurar_player_id(player_id)
        if personagem is None:
            self.db.iniciar_personagem(player_id, ctx.author.name, "", 1, 0, 1, 16, 14)
            await ctx.channel.send(
                'Oi ' + ctx.author.name + ' seu perfil foi adicionado, agora use o comando $novo para criar o nome do seu personagem!')
        elif personagem is not None and personagem[2] == "":
            await ctx.channel.send("Use o comando $novo para criar o nome do seu personagem.")
        else:
            await ctx.channel.send("Você já possui um personagem " + ctx.author.name)
            await ctx.channel.send("Seu Personagem atual se chama " + personagem[2])
            await ctx.channel.send("Use o comando $renomear caso deseje alterar o nome do seu personagem.")

    @commands.command(name='novo', help='Cria o nome do seu personagem')
    async def novo(self, ctx):
        player_id = str(ctx.author.id)
        if ctx.message.content.strip() == "$novo":
            await ctx.channel.send(ctx.author.name + " use o comando seguido do nome desejado")
            await ctx.channel.send("Ex: $novo João das Neve")
        else:
            personagem_id = self.db.procurar_player_id(player_id)
            if personagem_id is None:
                await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
            elif personagem_id[2] == "":
                avatar = ctx.message.content.replace('$novo ', '')
                personagem_avatar = self.db.procurar_personagem(avatar)
                if personagem_avatar is None:
                    self.db.atualizar_avatar(player_id, avatar)
                    await ctx.channel.send(
                        ctx.author.name + ' você criou um novo personagem e o nome dele é ' + avatar)
                else:
                    await ctx.channel.send(ctx.author.name + ' já existe um personagem com o nome ' + avatar)

            else:
                await ctx.channel.send(
                    ctx.author.name + " você já criou um personagem, use o comando $renomear")

    @commands.command(name='info', help='Mostra as informações do seu personagem.')
    async def info(self, ctx):
        player_id = str(ctx.author.id)
        personagem_id = self.db.procurar_player_id(player_id)
        if personagem_id is None:
            await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
        elif personagem_id[2] == "":
            await ctx.channel.send(
                "Você ainda não terminou a criação do seu personagem, use o comando $novo seguido do nome que desejar.")
        else:
            infos = ""
            for item in personagem_id:
                infos += str(item) + "\n"
            await ctx.channel.send("```" + infos + "```")

    @commands.command(name='renomear', help='Renomeia o seu personagem')
    async def renomear(self, ctx):
        player_id = str(ctx.author.id)
        if ctx.message.content.strip() == "$renomear":
            await ctx.channel.send(ctx.author.name + " use o comando seguido do nome desejado")
            await ctx.channel.send("Ex: $renomear João das Neve")
        else:
            personagem_id = self.db.procurar_player_id(player_id)
            if personagem_id is None:
                await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
            else:
                avatar_novo = ctx.message.content.replace("$renomear ", "")
                avatar_antigo = personagem_id[2]
                personagem_avatar = self.db.procurar_personagem(avatar_novo)
                if avatar_novo.lower() == avatar_antigo.lower():
                    await ctx.channel.send(ctx.author.name + " o nick novo é igual ao antigo")
                elif personagem_avatar is None:
                    self.db.atualizar_avatar(player_id, avatar_novo)
                    await ctx.channel.send(ctx.author.name + " o novo nome do seu personagem é " + avatar_novo)
                else:
                    await ctx.channel.send(ctx.author.name + " já possui um personagem com o nick escolhido")

    @commands.command(name='itens', help='Mostra os itens do seu personagem.')
    async def itens(self, ctx):
        player_id = str(ctx.author.id)
        personagem_id = self.db.procurar_player_id(player_id)
        if personagem_id is None:
            await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
        else:
            itens = self.db.procurar_itens(player_id)
            itens_string = ""
            for item in itens:
                itens_string += item[1] + "\n"
            await ctx.channel.send("```" + itens_string + "```")

    @commands.command(name='conquistas', help='Mostra os itens do seu personagem.')
    async def conquistas(self, ctx):
        player_id = str(ctx.author.id)
        personagem_id = self.db.procurar_player_id(player_id)
        if personagem_id is None:
            await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
        else:
            conquistas = self.db.get_conquistas(player_id)
            conquistas_string = ""
            for conquista in conquistas:
                print(conquista)
                if conquista[2] == 0:
                    conquistas_string += conquista[1] + ": Bloqueada\n"
                else:
                    conquistas_string += conquista[1] + ": Desbloqueada\n"
            await ctx.channel.send("```" + conquistas_string + "```")

def setup(bot):
    db = Banco()
    bot.add_cog(Gerenciamento(bot, db))