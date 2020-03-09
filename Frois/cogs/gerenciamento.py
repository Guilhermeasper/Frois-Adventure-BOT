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
        personagem = self.db.procurar_player_id(ctx.author.id)
        if personagem is None:
            self.db.iniciar_personagem(ctx.author.id, ctx.author.name, "", 1, 0, 1, 16, 14)
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
        if ctx.message.content.strip() == "$novo":
            await ctx.channel.send(ctx.author.name + " use o comando seguido do nome desejado")
            await ctx.channel.send("Ex: $novo João das Neve")
        else:
            personagem_id = self.db.procurar_player_id(ctx.author.id)
            if personagem_id is None:
                await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
            elif personagem_id[2] == "":
                avatar = ctx.message.content.replace('$novo ', '')
                personagem_avatar = self.db.procurar_personagem(avatar)
                if personagem_avatar is None:
                    self.db.atualizar_avatar(ctx.author.id, avatar)
                    await ctx.channel.send(
                        ctx.author.name + ' você criou um novo personagem e o nome dele é ' + avatar)
                else:
                    await ctx.channel.send(ctx.author.name + ' já existe um personagem com o nome ' + avatar)

            else:
                await ctx.channel.send(
                    ctx.author.name + " você já criou um personagem, use o comando $renomear")

    # @commands.command(name='info', help='Mostra as informações do seu personagem.')
    # async def info(self, ctx):
    #     self.c.execute('SELECT * FROM players WHERE id=?', (ctx.author.id,))
    #     found = self.c.fetchone()
    #     if found is None:
    #         await ctx.channel.send("Você ainda não possui um personagem, use o comando $começar para criar um!")
    #     elif found[2] == "":
    #         await ctx.channel.send(
    #             "Você ainda não terminou a criação do seu personagem, use o comando $novo seguido do nome que desejar.")
    #     else:
    #         labels = ["", "Usuário: ", "Avatar: ", "Nível: ", "Exp.: ", "Localização: Seção ", "Itens: ",
    #                   "Mão esquerda: ",
    #                   "Mão direita: ", "Buff: ", "X: ", "Y: ", "Atributos: "]
    #         infos = ""
    #         for i in range(1, 13):
    #             infos += labels[i] + str(found[i]) + "\n"
    #         await ctx.channel.send("```" + infos + "```")

    @commands.command(name='renomear', help='Renomeia o seu personagem')
    async def renomear(self, ctx):
        if ctx.message.content.strip() == "$renomear":
            await ctx.channel.send(ctx.author.name + " use o comando seguido do nome desejado")
            await ctx.channel.send("Ex: $renomear João das Neve")
        else:
            personagem_id = self.db.procurar_player_id(ctx.author.id)
            if personagem_id is None:
                await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
            else:
                avatar_novo = ctx.message.content.replace("$renomear ", "")
                avatar_antigo = personagem_id[2]
                personagem_avatar = self.db.procurar_personagem(avatar_novo)
                if avatar_novo.lower() == avatar_antigo.lower():
                    await ctx.channel.send(ctx.author.name + " o nick novo é igual ao antigo")
                elif personagem_avatar is None:
                    self.db.atualizar_avatar(ctx.author.id, avatar_novo)
                    await ctx.channel.send(ctx.author.name + " o novo nome do seu personagem é " + nick_novo)
                else:
                    await ctx.channel.send(ctx.author.name + " já possui um personagem com o nick escolhido")


def setup(bot):
    db = Banco()
    bot.add_cog(Gerenciamento(bot, db))
