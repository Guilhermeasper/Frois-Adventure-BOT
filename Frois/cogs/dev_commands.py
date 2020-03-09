import sqlite3

from discord.ext import commands
from Frois.game import game

mapa = game.Game()


class Desenvolvedor(commands.Cog):
    def __init__(self, bot, conn, c):
        self.bot = bot
        self.c = c
        self.conn = conn

    @commands.command(name='zerar', help='Retorna o personagem ao ponto inicial do jogo')
    async def reset(self, ctx):
        if ctx.author.id == 214257187592077313 or ctx.author.id == 305838877866721280:
            self.c.execute('SELECT nick from players WHERE nick=?', (ctx.message.content.strip("$zerar "),))
            found = self.c.fetchone()
            if found is None:
                await ctx.channel.send("Não existe nenhum personagem com o nick informado")
            else:
                self.c.execute('UPDATE players SET pos_x=?, pos_y=? WHERE id=?', (16, 14, ctx.author.id))
                self.conn.commit()
                await ctx.channel.send(found[0] + " voltou para o ponto inicial do mapa.")
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='limpar', help='Limpa o inventário do personagem')
    async def limpar(self, ctx):
        if ctx.author.id == 214257187592077313 or ctx.author.id == 305838877866721280:
            self.c.execute('SELECT nick from players WHERE nick=?', (ctx.message.content.strip("$limpar "),))
            found = self.c.fetchone()
            if found is None:
                await ctx.channel.send("Não existe nenhum personagem com o nick informado")
            else:
                self.c.execute('UPDATE players SET bag=? WHERE id=?', ("", ctx.message.content.strip("$limpar ")))
                self.conn.commit()
                await ctx.channel.send("A bolsa de " + found[0] + " foi esvaziada.")
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='mapa', help='Mostra o mapa do personagem')
    async def map(self, ctx):
        if ctx.author.id == 214257187592077313 or ctx.author.id == 305838877866721280 or ctx.author.id == 164786521180733440:
            self.c.execute('SELECT pos_x, pos_y, sec FROM players WHERE nick=?', (ctx.message.content.strip("$mapa "),))
            found = self.c.fetchone()
            mapaprint = ""
            if found is None:
                await ctx.channel.send("O personagem informado ainda não foi criado")
            else:
                for i in range(30):
                    for j in range(30):
                        if i == found[0] and j == found[1]:
                            mapaprint += "7 "
                        else:
                            mapaprint += str(mapa.get_section(found[2])[i][j]) + " "
                    mapaprint += "\n"
                await ctx.channel.send("```" + mapaprint + "```", delete_after=50)
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='remover', help='Remove todas as informações do personagem')
    async def remover(self, ctx):
        if ctx.author.id == 214257187592077313 or ctx.author.id == 305838877866721280:
            self.c.execute('SELECT nick FROM players WHERE nick=?', (ctx.message.content.strip("$remover "),))
            nick = self.c.fetchone()[0]
            if nick is None:
                await ctx.channel.send("O personagem informado ainda não foi criado")
            else:
                self.c.execute('DELETE FROM players WHERE nick=?', (nick,))
                self.conn.commit()
                await ctx.channel.send("O personagem " + nick + " foi removido do jogo")


def setup(bot):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    bot.add_cog(Desenvolvedor(bot, conn, c))
