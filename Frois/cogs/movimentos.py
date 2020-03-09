import sqlite3
from discord.ext import commands
from game.game import Game

mapa = Game()


class Movimentos(commands.Cog):
    def __init__(self, bot, conn, c):
        self.bot = bot
        self.c = c
        self.conn = conn

    @commands.command(name='frente', aliases=['ahead', 'cima'],
                      help='Move seu personagem para frente, caso não o caminho não esteja bloqueado.')
    async def frente(self, ctx):
        self.c.execute('SELECT pos_x, pos_y, sec FROM players WHERE id=?', (ctx.author.id,))
        found = self.c.fetchone()
        if mapa.get_section(found[2])[found[0] - 1][found[1]] == 0:
            self.c.execute('UPDATE players SET pos_x=? WHERE id=?', (found[0] - 1, ctx.author.id))
            self.conn.commit()
            await ctx.channel.send('Você se movimentou para frente e não tem nada aqui')
        elif mapa.get_section(found[2])[found[0] - 1][found[1]] == 2:
            await ctx.channel.send('Você encontrou uma porta, está trancada, use o comando abrir caso tenha uma chave')
        elif mapa.get_section(found[2])[found[0] - 1][found[1]] == 3:
            self.c.execute('UPDATE players SET pos_x=? WHERE id=?', (found[0] - 1, ctx.author.id))
            self.conn.commit()
            await ctx.channel.send('Você se movimentou e encontrou um baú')
            await ctx.channel.send('Utilize o comando $abrir sempre que encontrar um baú')
        else:
            await ctx.channel.send('O caminho está bloqueado')

    @commands.command(name='tras', aliases=['behind', 'baixo'],
                      help='Move seu personagem para trás, caso não o caminho não esteja bloqueado.')
    async def tras(self, ctx):
        self.c.execute('SELECT pos_x, pos_y, sec FROM players WHERE id=?', (ctx.author.id,))
        found = self.c.fetchone()
        if found is None:
            await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
        else:
            if mapa.get_section(found[2])[found[0] + 1][found[1]] == 0:
                self.c.execute('UPDATE players SET pos_x=? WHERE id=?', (found[0] + 1, ctx.author.id))
                self.conn.commit()
                await ctx.channel.send('Você se movimentou para trás e não tem nada aqui')
            elif mapa.get_section(found[2])[found[0] + 1][found[1]] == 3:
                self.c.execute('UPDATE players SET pos_x=? WHERE id=?', (found[0] + 1, ctx.author.id))
                self.conn.commit()
                await ctx.channel.send('Você se movimentou para trás e encontrou um baú')
            else:
                await ctx.channel.send('O caminho está bloqueado')

    @commands.command(name='esquerda', aliases=['left', 'pt'],
                      help='Move seu personagem para esquerda, caso não o caminho não esteja bloqueado.')
    async def esquerda(self, ctx):
        self.c.execute('SELECT pos_x, pos_y, sec FROM players WHERE id=?', (ctx.author.id,))
        found = self.c.fetchone()
        if found is None:
            await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
        else:
            if mapa.get_section(found[2])[found[0]][found[1] - 1] == 0:
                self.c.execute('UPDATE players SET pos_y=? WHERE id=?', (found[1] - 1, ctx.author.id))
                self.conn.commit()
                await ctx.channel.send('Você se movimentou para esquerda e não tem nada aqui')
            elif mapa.get_section(found[2])[found[0]][found[1] - 1] == 3:
                self.c.execute('UPDATE players SET pos_y=? WHERE id=?', (found[1] - 1, ctx.author.id))
                self.conn.commit()
                await ctx.channel.send('Você se movimentou para esquerda e encontrou um baú')
            else:
                await ctx.channel.send('O caminho está bloqueado')

    @commands.command(name='direita', aliases=['right'],
                      help='Move seu personagem para direita, caso não o caminho não esteja bloqueado.')
    async def direita(self, ctx):
        self.c.execute('SELECT pos_x, pos_y, sec FROM players WHERE id=?', (ctx.author.id,))
        found = self.c.fetchone()
        if found is None:
            await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
        else:
            if mapa.get_section(found[2])[found[0]][found[1] + 1] == 0:
                self.c.execute('UPDATE players SET pos_y=? WHERE id=?', (found[1] + 1, ctx.author.id))
                self.conn.commit()
                await ctx.channel.send('Você se movimentou para direita e não tem nada aqui')
            elif mapa.get_section(found[2])[found[0]][found[1] + 1] == 3:
                self.c.execute('UPDATE players SET pos_y=? WHERE id=?', (found[1] + 1, ctx.author.id))
                self.conn.commit()
                await ctx.channel.send('Você se movimentou para direita e encontrou um baú')
            else:
                await ctx.channel.send('O caminho está bloqueado')

    @commands.command(name='abrir', help='Abre baús, portas e tudo mais que possa ser aberto')
    async def abrir(self, ctx):
        self.c.execute('SELECT pos_x, pos_y, bag FROM players WHERE id=?', (ctx.author.id,))
        found = self.c.fetchone()
        if mapa.get_section(1)[found[0]][found[1]] == 3:
            self.c.execute('UPDATE players SET bag=? WHERE id=?', (found[2] + "Chave,", ctx.author.id))
            self.conn.commit()
            await ctx.channel.send("Você encontrou uma chave no baú, ela foi adicionada ao seu inventário")
        elif mapa.get_section(1)[found[0] - 1][found[1]] == 2:
            self.c.execute('SELECT bag FROM players WHERE id=?', (ctx.author.id,))
            bag = self.c.fetchone()
            print(bag)
            if bag[0].split(",")[0] == "Chave":
                self.c.execute('UPDATE players SET pos_x=? WHERE id=?', (found[0] - 2, ctx.author.id))
                self.conn.commit()
                await ctx.channel.send('Você abriu a porta e não parece ter nada aqui')
            else:
                await ctx.channel.send('Você precisa de uma chave pra abrir a porta, procure o baú')


def setup(bot):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    bot.add_cog(Movimentos(bot, conn, c))
