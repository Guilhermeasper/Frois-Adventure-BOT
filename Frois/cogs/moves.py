import sqlite3
from discord.ext import commands
from game.game import Game
from database.banco import Banco

mapa = Game()


class Movimentos(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command(name='frente', aliases=['ahead', 'cima'],
                      help='Move seu personagem para frente, caso não o caminho não esteja bloqueado.')
    async def frente(self, ctx):
        player_id = str(ctx.author.id)
        move_type = "frente"
        pos_personagem = self.db.posicao_player_id(player_id)
        if pos_personagem is None:
            await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
        else:
            personagem = self.db.get_personagem_by_id(player_id)[0]
            sec = pos_personagem[0]
            pos_x = pos_personagem[1]
            pos_y = pos_personagem[2]
            prox_posicao = mapa.get_section(sec)[pos_x - 1][pos_y]
            battle_mode = self.db.get_battle_mode(player_id)[0]
            await self.mover(ctx, battle_mode, move_type, prox_posicao, pos_x - 1, pos_y, sec, player_id, personagem)

    @commands.command(name='tras', aliases=['behind', 'baixo', 'trás'],
                      help='Move seu personagem para trás, caso não o caminho não esteja bloqueado.')
    async def tras(self, ctx):
        player_id = str(ctx.author.id)
        move_type = "trás"
        pos_personagem = self.db.posicao_player_id(player_id)
        if pos_personagem is None:
            await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
        else:
            personagem = self.db.get_personagem_by_id(player_id)[0]
            sec = pos_personagem[0]
            pos_x = pos_personagem[1]
            pos_y = pos_personagem[2]
            prox_posicao = mapa.get_section(sec)[pos_x + 1][pos_y]
            battle_mode = self.db.get_battle_mode(player_id)[0]
            await self.mover(ctx, battle_mode, move_type, prox_posicao, pos_x + 1, pos_y, sec, player_id, personagem)

    @commands.command(name='esquerda', aliases=['left', 'pt'],
                      help='Move seu personagem para esquerda, caso não o caminho não esteja bloqueado.')
    async def esquerda(self, ctx):
        player_id = str(ctx.author.id)
        move_type = "esquerda"
        pos_personagem = self.db.posicao_player_id(player_id)
        if pos_personagem is None:
            await ctx.channel.send("Você ainda não possui um personagem")
            await ctx.channel.send(ctx.author.name + " use o comando $começar primeiro")
        else:
            personagem = self.db.get_personagem_by_id(player_id)[0]
            sec = pos_personagem[0]
            pos_x = pos_personagem[1]
            pos_y = pos_personagem[2]
            prox_posicao = mapa.get_section(sec)[pos_x][pos_y - 1]
            battle_mode = self.db.get_battle_mode(player_id)[0]
            await self.mover(ctx, battle_mode, move_type, prox_posicao, pos_x, pos_y - 1, sec, player_id, personagem)

    @commands.command(name='direita', aliases=['right'],
                      help='Move seu personagem para direita, caso não o caminho não esteja bloqueado.')
    async def direita(self, ctx):
        player_id = str(ctx.author.id)
        move_type = "direita"
        pos_personagem = self.db.posicao_player_id(player_id)
        if pos_personagem is None:
            await ctx.channel.send(ctx.author.name + " você ainda não possui um personagem.")
            await ctx.channel.send("Use o comando $começar primeiro!")
        else:
            personagem = self.db.get_personagem_by_id(player_id)[0]
            sec = pos_personagem[0]
            pos_x = pos_personagem[1]
            pos_y = pos_personagem[2]
            prox_posicao = mapa.get_section(sec)[pos_x][pos_y + 1]
            battle_mode = self.db.get_battle_mode(player_id)[0]
            await self.mover(ctx, battle_mode, move_type, prox_posicao, pos_x, pos_y + 1, sec, player_id, personagem)

    @commands.command(name='abrir', help='Abre baús, portas e tudo mais que possa ser aberto')
    async def abrir(self, ctx):
        player_name = ctx.author.name
        player_id = str(ctx.author.id)
        pos_personagem = self.db.posicao_player_id(player_id)
        if pos_personagem is None:
            await ctx.channel.send(player_name + " você ainda não possui um personagem.")
            await ctx.channel.send("Use o comando $começar primeiro")
        else:
            sec = pos_personagem[0]
            pos_x = pos_personagem[1]
            pos_y = pos_personagem[2]
            posicao = mapa.get_section(sec)[pos_x][pos_y]
            north = mapa.get_section(sec)[pos_x - 1][pos_y]
            south = mapa.get_section(sec)[pos_x + 1][pos_y]
            east = mapa.get_section(sec)[pos_x][pos_y - 1]
            west = mapa.get_section(sec)[pos_x][pos_y + 1]
            item = self.db.procurar_item_nome("Chave", player_id)
            if posicao == 3:
                if item is None:
                    item_id = str(str(sec) + str(pos_x) + str(pos_y))
                    self.db.inserir_item(item_id, "Chave", 1, 0, player_id)
                    await ctx.channel.send(
                        player_name + " você encontrou uma chave no baú, ela foi adicionada ao seu inventário")
                    await ctx.channel.send(
                        player_name + " você desbloqueou a conquista: Caçador de tesouros")
                    self.db.atualizar_conquista("Caçador de Tesouros", player_id)
                    await ctx.channel.send(
                        player_name + " você desbloqueou a conquista: Chaveiro")
                    self.db.atualizar_conquista("Chaveiro", player_id)
                else:
                    await ctx.channel.send(player_name + " o baú está vazio.")
            elif north == 2 or south == 2 or east == 2 or west == 2:
                if item is None:
                    await ctx.channel.send(player_name + ' você precisa de uma chave pra abrir a porta, procure o baú.')
                elif item[1] == "Chave":
                    string_pos = sec + "_" + str(pos_x) + "_" + str(pos_y)
                    arr_pos = mapa.get_map()[string_pos].split("_")
                    new_pos_x = arr_pos[len(arr_pos) - 2]
                    new_pos_y = arr_pos[len(arr_pos) - 1]
                    new_sec = ""
                    for index in range(len(arr_pos)-2):
                        new_sec += arr_pos[index] + "_"
                    new_sec = new_sec[:-1]
                    await ctx.channel.send("Novo x: " + new_pos_x + "\nNovo y: " + new_pos_y + "\nNovo setor: " + new_sec)

                    self.db.atualizar_posicao(player_id, new_pos_x, new_pos_y, new_sec)
                    # self.db.set_battle_mode(1, player_id)
                    # self.db.remover_item(item[0], player_id)
                    # await ctx.channel.send(player_name + ' você abriu a porta e havia um monstro a sua espera.')
                    # await ctx.channel.send('Você iniciou uma batalha com o monstro, você pode $lutar ou $fugir.')

    @commands.command(name='lutar', help='Luta com monstros')
    async def lutar(self, ctx):
        player_name = ctx.author.name
        player_id = str(ctx.author.id)
        pos_personagem = self.db.posicao_player_id(player_id)
        if pos_personagem is None:
            await ctx.channel.send(player_name + " você ainda não possui um personagem.")
            await ctx.channel.send("Use o comando $começar primeiro")
        else:
            await ctx.channel.send(player_name + " você não possui nenhuma arma.")
            await ctx.channel.send("Você tentou lutar com as próprias mãos e o monstro te matou")
            self.db.atualizar_posicao(player_id, 3, 3, 1)
            self.db.set_battle_mode(0, player_id)

    @commands.command(name='fugir', help='Foge de monstros')
    async def fugir(self, ctx):
        player_name = ctx.author.name
        player_id = str(ctx.author.id)
        pos_personagem = self.db.posicao_player_id(player_id)
        if pos_personagem is None:
            await ctx.channel.send(player_name + " você ainda não possui um personagem.")
            await ctx.channel.send("Use o comando $começar primeiro.")
        else:
            await ctx.channel.send("Você tentou fugir e o monstro te matou.")
            self.db.atualizar_posicao(player_id, 3, 3, 1)
            self.db.set_battle_mode(0, player_id)

    async def mover(self, ctx, combate, direcao, prox_posicao, pos_x, pos_y, sec, player_id, avatar):
        if combate == 1:
            await ctx.channel.send(avatar + ' você está em combate, você só pode $lutar ou $fugir.')
        else:
            if prox_posicao == 0:
                self.db.atualizar_posicao(player_id, pos_x, pos_y, sec)
                await ctx.channel.send(avatar + ' você se movimentou para ' + direcao + ' e não tem nada aqui.')
            elif prox_posicao == 2:
                self.db.atualizar_posicao(player_id, pos_x, pos_y, sec)
                await ctx.channel.send(
                    avatar + ' você encontrou uma porta, está trancada, use o comando abrir caso tenha uma chave.')
            elif prox_posicao == 3:
                self.db.atualizar_posicao(player_id, pos_x, pos_y, sec)
                await ctx.channel.send(avatar + ' você se movimentou para ' + direcao + ' e encontrou um baú.')
                await ctx.channel.send('Utilize o comando $abrir sempre que encontrar um baú.')
            else:
                await ctx.channel.send(avatar + ' o caminho está bloqueado.')


def setup(bot):
    banco = Banco()
    bot.add_cog(Movimentos(bot, banco))
