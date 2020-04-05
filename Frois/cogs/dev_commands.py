from discord.ext import commands
from game.game import Game
from database.banco import Banco

mapa = Game()

class Desenvolvedor(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command(name='hard_reset', help='Exclui todas as informações do jogo')
    async def hard_reset(self, ctx):
        player_id = str(ctx.author.id)
        if player_id == "214257187592077313" or player_id == "305838877866721280":
            senha = ctx.message.content.replace("$hard_reset ", "")
            if senha == "17051996":
                self.db.hard_reset()
                await ctx.message.delete()
                await ctx.channel.send("```Todas as informações do jogo foram apagadas```")
            elif senha == "":
                await ctx.channel.send("```Esse comando irá apagar todas as informações do jogo\n"
                                       "Cuidado ao utilizar o mesmo"
                                       "Utilize $hard_reset senha```")
            else:
                await ctx.channel.send("```Senha incorreta```")
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='zerar', help='Retorna o personagem ao ponto inicial do jogo')
    async def reset(self, ctx):
        player_id = str(ctx.author.id)
        if player_id == "214257187592077313" or player_id == "305838877866721280":
            avatar = ctx.message.content.replace("$zerar ", "")
            personagem = self.db.procurar_personagem(avatar)
            if personagem is None:
                await ctx.channel.send("Não existe nenhum personagem com o nick informado")
            else:
                self.db.atualizar_posicao(player_id, 3, 3, "section_1_room")
                await ctx.channel.send(personagem[2] + " voltou para o ponto inicial do mapa.")
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='limpar', help='Limpa o inventário do personagem')
    async def limpar(self, ctx):
        player_id = str(ctx.author.id)
        if player_id == "214257187592077313" or player_id == "305838877866721280":
            avatar = ctx.message.content.replace("$limpar ", "")
            personagem = self.db.procurar_personagem(avatar)
            if personagem is None:
                await ctx.channel.send("Não existe nenhum personagem com o avatar informado")
            else:
                self.db.limpar_itens(player_id)
                await ctx.channel.send("O inventário de " + personagem[2] + " foi esvaziada.")
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='mapa', help='Mostra o mapa do personagem')
    async def map(self, ctx):
        player_id = str(ctx.author.id)
        if player_id == "214257187592077313" or player_id == "305838877866721280":
            avatar = ctx.message.content.replace("$mapa ", "")
            section = self.db.get_section_by_avatar(avatar)[0]
            location = self.db.get_location_by_avatar(avatar)
            matriz = mapa.get_section(section)
            mapaprint = ""
            if avatar is None:
                await ctx.channel.send("O personagem informado ainda não foi criado")
            else:
                for i in range(len(matriz)):
                    for j in range(len(matriz[i])):
                        if (i, j) == location:
                            mapaprint += "7 "
                        else:
                            mapaprint += str(matriz[i][j]) + " "
                    mapaprint += "\n"
                await ctx.channel.send("```" + mapaprint + "```", delete_after=20)
        else:
            await ctx.channel.send("```Junte-se ao time de desenvolvimento para desbloquear esse comando```")

    @commands.command(name='remover', help='Remove todas as informações do personagem')
    async def remover(self, ctx):
        player_id = str(ctx.author.id)
        if player_id == "214257187592077313" or player_id == "305838877866721280":
            avatar = ctx.message.content.replace("$remover ", "")
            personagem = self.db.procurar_personagem(avatar)
            if personagem is None:
                await ctx.channel.send("O personagem informado ainda não foi criado")
            else:
                self.db.remover_personagem(avatar)
                await ctx.channel.send("O personagem " + personagem[2] + " foi removido do jogo")

    @commands.command(name='test', help='Comando para ser implementado com funções aleatórias para fins de desenvolvimento.')
    async def test(self, ctx):
        player_id = str(ctx.author.id)
        if True:
            avatar = ctx.message.content.replace("$test ", "")
            await ctx.author.send("Oi "+ctx.author.name)


def setup(bot):
    banco = Banco()
    bot.add_cog(Desenvolvedor(bot, banco))
