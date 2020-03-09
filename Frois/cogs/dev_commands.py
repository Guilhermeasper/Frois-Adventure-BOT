from discord.ext import commands
from game.game import Game
from database.banco import Banco


mapa = Game()


class Desenvolvedor(commands.Cog):
    def __init__(self, bot, banco):
        self.bot = bot
        self.banco = banco

    @commands.command(name='zerar', help='Retorna o personagem ao ponto inicial do jogo')
    async def reset(self, ctx):
        if ctx.author.id == 214257187592077313 or ctx.author.id == 305838877866721280:
            avatar = ctx.message.content.replace("$zerar ", "")
            personagem = self.banco.procurar_personagem(avatar)
            if personagem is None:
                await ctx.channel.send("Não existe nenhum personagem com o nick informado")
            else:
                await ctx.channel.send(personagem[2] + " voltou para o ponto inicial do mapa.")
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='limpar', help='Limpa o inventário do personagem')
    async def limpar(self, ctx):
        if ctx.author.id == 214257187592077313 or ctx.author.id == 305838877866721280:
            avatar = ctx.message.content.replace("$limpar ", "")
            personagem = self.banco.procurar_personagem(avatar)
            if personagem is None:
                await ctx.channel.send("Não existe nenhum personagem com o avatar informado")
            else:
                await ctx.channel.send("O inventário de " + personagem[2] + " foi esvaziada.")
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='mapa', help='Mostra o mapa do personagem')
    async def map(self, ctx):
        if ctx.author.id == 214257187592077313 or ctx.author.id == 305838877866721280 or \
                ctx.author.id == 164786521180733440:
            avatar = ctx.message.content.replace("$mapa ", "")
            personagem = self.banco.procurar_personagem(avatar)
            mapaprint = ""
            if personagem is None:
                await ctx.channel.send("O personagem informado ainda não foi criado")
            else:
                for i in range(30):
                    for j in range(30):
                        if i == personagem[6] and j == personagem[7]:
                            mapaprint += "7 "
                        else:
                            mapaprint += str(mapa.get_section(personagem[5])[i][j]) + " "
                    mapaprint += "\n"
                await ctx.channel.send("```" + mapaprint + "```", delete_after=50)
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='remover', help='Remove todas as informações do personagem')
    async def remover(self, ctx):
        if ctx.author.id == 214257187592077313 or ctx.author.id == 305838877866721280:
            avatar = ctx.message.content.replace("$remover ", "")
            personagem = self.banco.procurar_personagem(avatar)
            if personagem is None:
                await ctx.channel.send("O personagem informado ainda não foi criado")
            else:
                self.banco.remover_personagem(avatar)
                await ctx.channel.send("O personagem " + personagem[2] + " foi removido do jogo")


def setup(bot):
    banco = Banco()
    bot.add_cog(Desenvolvedor(bot, banco))
