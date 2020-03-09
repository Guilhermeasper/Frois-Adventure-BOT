import sqlite3
from discord.ext import commands
from game.game import Game

mapa = Game()


class Gerenciamento(commands.Cog):
    def __init__(self, bot, conn, c):
        self.bot = bot
        self.c = c
        self.conn = conn

    @commands.command(name='começar', help='Inicia o jogo para o seu perfil')
    async def comecar(self, ctx):
        self.c.execute('SELECT nick FROM players WHERE id=?', (ctx.author.id,))
        found = self.c.fetchone()
        if found is None:
            await ctx.channel.send(
                'Oi ' + ctx.author.name + ' seu perfil foi adicionado, agora use o comando $novo para criar o nome do seu personagem!')
            self.c.execute("INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (ctx.author.id, ctx.author.name, "", 1, 0, 1, "", "", "", "", 16, 14, ""))
            self.conn.commit()
        elif found is not None:
            await ctx.channel.send("Use o comando $novo para criar o nome do seu personagem")
        else:
            await ctx.channel.send("Você já possui um personagem " + ctx.author.name)
            await ctx.channel.send("Seu Personagem atual se chama " + found[0])
            print(found)

    @commands.command(name='novo', help='Cria o nome do seu personagem')
    async def novo(self, ctx):
        if ctx.message.content.strip() == "$novo":
            await ctx.channel.send(ctx.author.name + " use o comando seguido do nome desejado")
            await ctx.channel.send("Ex: $novo João das Neve")
        else:
            self.c.execute('SELECT * FROM players WHERE id=?', (ctx.author.id,))
            found = self.c.fetchone()
            if found is None:
                await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
            elif found[2] == "":
                nick = ctx.message.content.replace('$novo ', '').capitalize()
                self.c.execute('SELECT * FROM players WHERE nick=?', (nick,))
                found2 = self.c.fetchone()
                if found2 is None:
                    if nick != "":
                        self.c.execute('UPDATE players SET nick=? WHERE id=?', (nick, ctx.author.id))
                        self.conn.commit()
                        await ctx.channel.send(
                            ctx.author.name + ' você criou um novo personagem e o nome dele é ' + nick)
                else:
                    await ctx.channel.send(ctx.author.name + ' já existe um personagem com o nome ' + nick)

            else:
                await ctx.channel.send(
                    ctx.author.name + " você já criou um personagem, use o comando $renomear")

    @commands.command(name='info', help='Mostra as informações do seu personagem.')
    async def info(self, ctx):
        self.c.execute('SELECT * FROM players WHERE id=?', (ctx.author.id,))
        found = self.c.fetchone()
        if found is None:
            await ctx.channel.send("Você ainda não possui um personagem, use o comando $começar para criar um!")
        elif found[2] == "":
            await ctx.channel.send(
                "Você ainda não terminou a criação do seu personagem, use o comando $novo seguido do nome que desejar.")
        else:
            labels = ["", "Usuário: ", "Avatar: ", "Nível: ", "Exp.: ", "Localização: Seção ", "Itens: ",
                      "Mão esquerda: ",
                      "Mão direita: ", "Buff: ", "X: ", "Y: ", "Atributos: "]
            infos = ""
            for i in range(1, 13):
                infos += labels[i] + str(found[i]) + "\n"
            await ctx.channel.send("```" + infos + "```")

    @commands.command(name='renomear', help='Renomeia o seu personagem')
    async def renomear(self, ctx):
        if ctx.message.content.strip() == "$renomear":
            await ctx.channel.send(ctx.author.name + " use o comando seguido do nome desejado")
            await ctx.channel.send("Ex: $renomear João das Neve")
        else:
            self.c.execute('SELECT nick FROM players WHERE id=?', (ctx.author.id,))
            nick_atual = self.c.fetchone()[0].capitalize()
            if nick_atual is None:
                await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
            else:
                nick_novo = ctx.message.content.replace("$renomear ", "").capitalize()
                print(nick_novo)
                print(nick_atual)
                self.c.execute('SELECT nick FROM players WHERE nick=?', (nick_novo,))
                found = self.c.fetchone()
                print(found)
                if nick_atual.lower() == nick_novo.lower():
                    await ctx.channel.send(ctx.author.name + " o nick novo é igual ao antigo")
                elif found is None:
                    self.c.execute('UPDATE players SET nick=? WHERE id=?', (nick_novo, ctx.author.id))
                    self.conn.commit()
                    await ctx.channel.send(ctx.author.name + " o novo nome do seu personagem é " + nick_novo)
                else:
                    await ctx.channel.send(ctx.author.name + " já possui um personagem com o nick escolhido")


def setup(bot):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    bot.add_cog(Gerenciamento(bot, conn, c))
