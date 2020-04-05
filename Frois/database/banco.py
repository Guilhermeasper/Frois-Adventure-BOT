import sqlite3

class Banco():
    def __init__(self):
        self.conn = sqlite3.connect('game.db')
        self.c = self.conn.cursor()

    def iniciar(self):
        print("Tabela de jogadores:", end=" ")
        try:
            self.c.execute(
                '''CREATE TABLE IF NOT EXISTS players ( id TEXT PRIMARY KEY,
                                                        nome TEXT,
                                                        avatar TEXT,
                                                        avatar_level INTEGER,
                                                        exp INTEGER,
                                                        sec TEXT,
                                                        pos_x INTEGER,
                                                        pos_y INTEGER,
                                                        classe TEXT,
                                                        inteligencia INTEGER,
                                                        forca INTEGER,
                                                        destreza INTEGER,
                                                        ouro INTEGER,
                                                        batalhando INTEGER,  
                                                        sangrando INTEGER,
                                                        envenenado INTEGER,
                                                        cansado INTEGER,
                                                        vida INTEGER,
                                                        mana INTEGER
                                                        );''')
            print("Sucesso")
        except:
            print("Falha")

        print("Tabela de itens:", end=" ")
        try:
            self.c.execute(
                '''CREATE TABLE IF NOT EXISTS itens ( id TEXT PRIMARY KEY,
                                                        item TEXT,
                                                        quantidade INTEGER,
                                                        valor_unit INTEGER,
                                                        player_id TEXT,
                                                        FOREIGN KEY (player_id) REFERENCES players(id)
                                                        );''')
            print("Sucesso")
        except:
            print("Falha")

        print("Tabela de conquistas:", end=" ")
        try:
            self.c.execute(
                '''CREATE TABLE IF NOT EXISTS conquistas ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        nome TEXT,
                                                        valor INTEGER,
                                                        recompensa INTEGER,
                                                        player_id TEXT,
                                                        FOREIGN KEY (player_id) REFERENCES players(id)
                                                        );''')
            print("Sucesso")
        except:
            print("Falha")

    def salvar(self):
        self.conn.commit()

    def fechar(self):
        self.conn.close()

    def iniciar_personagem(self, data):
        self.c.execute('INSERT INTO players VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (data['id'],
                        data['name'],
                        data['avatar'],
                        data['avatar_level'],
                        data['exp'],
                        data['sec'],
                        data['pos_x'],
                        data['pos_y'],
                        data['classe'],
                        data['inteligencia'],
                        data['forca'],
                        data['destreza'],
                        data['ouro'],
                        data['batalhando'],
                        data['sangrando'],
                        data['envenenado'],
                        data['cansado'],
                        data['vida'],
                        data['mana']))
        self.c.execute('INSERT INTO conquistas VALUES (?, ?, ?, ?, ?)',
                       (None,
                        "Caçador de Tesouros",
                        0,
                        50,
                        data['id']))
        self.c.execute('INSERT INTO conquistas VALUES (?, ?, ?, ?, ?)',
                       (None,
                        "Chaveiro",
                        0,
                        50,
                        data['id']))
        self.c.execute('INSERT INTO conquistas VALUES (?, ?, ?, ?, ?)',
                       (None,
                        "Porteiro",
                        0,
                        50,
                        data['id']))
        self.salvar()

    def atualizar_avatar(self, player_id, avatar):
        self.c.execute('UPDATE players SET avatar=? WHERE id=?', (avatar, player_id,))
        self.salvar()

    def atualizar_classe(self, player_id, classe):
        self.c.execute('UPDATE players SET classe=? WHERE id=?', (classe, player_id,))
        self.salvar()

    def atualizar_posicao(self, player_id, pos_x, pos_y, sec):
        self.c.execute('UPDATE players SET pos_x=?, pos_y=?, sec=? WHERE id=?', (pos_x, pos_y, sec, player_id,))
        self.salvar()

    def atualizar_secao(self, player_id, sec):
        self.c.execute('UPDATE players SET sec=? WHERE id=?', (sec, player_id,))
        self.salvar()

    def procurar_personagem(self, avatar):
        self.c.execute('SELECT * FROM players WHERE avatar=?', (avatar,))
        return self.c.fetchone()

    def procurar_player_id(self, player_id):
        self.c.execute('SELECT * FROM players WHERE id=?',(player_id,))
        return self.c.fetchone()

    def posicao_player_id(self, player_id):
        self.c.execute('SELECT sec, pos_x, pos_y FROM players WHERE id=?', (player_id,))
        return self.c.fetchone()

    def info_personagem(self, avatar):
        self.c.execute('SELECT * FROM players INNER JOIN atributos a on players.id = a.player_id AND players.avatar = ?', (avatar,))
        return self.c.fetchone()

    def get_section_by_avatar(self, avatar):
        self.c.execute('SELECT sec FROM players WHERE avatar=?', (avatar,))
        return self.c.fetchone()

    def get_location_by_avatar(self, avatar):
        self.c.execute('SELECT pos_x, pos_y FROM players WHERE avatar=?', (avatar,))
        return self.c.fetchone()

    def get_personagem_by_id(self, player_id):
        self.c.execute('SELECT avatar FROM players WHERE id=?', (player_id,))
        return self.c.fetchone()

    def get_classe_by_id(self, player_id):
        self.c.execute('SELECT classe FROM players WHERE id=?', (player_id,))
        return self.c.fetchone()

    def remover_personagem(self, avatar):
        self.c.execute('DELETE FROM players WHERE avatar=?', (avatar,))
        self.salvar()

    def procurar_itens(self, player_id):
        self.c.execute('SELECT * FROM itens WHERE player_id=?', (player_id,))
        return self.c.fetchall()

    def procurar_item_nome(self, nome, player_id):
        self.c.execute('SELECT * FROM itens WHERE item=? AND player_id=?', (nome, player_id,))
        return self.c.fetchone()

    def procurar_item_id(self, item_id, player_id):
        self.c.execute('SELECT * FROM itens WHERE id=? AND player_id=?', (item_id, player_id,))
        return self.c.fetchone()

    def inserir_item(self, item_id, nome, quantidade, valor, player_id):
        self.c.execute('INSERT INTO itens VALUES(?,?,?,?,?)', (item_id, nome, quantidade, valor, player_id,))
        self.salvar()

    def atualizar_item(self, item_id, quantidade, player_id):
        self.c.execute('UPDATE itens SET quantidade=? WHERE item_id=? AND player_id=?', (quantidade, item_id, player_id,))
        self.salvar()

    def remover_item(self, item_id, player_id):
        self.c.execute('DELETE FROM itens WHERE id=? AND player_id=?', (item_id, player_id,))
        self.salvar()

    def limpar_itens(self, player_id):
        self.c.execute('DELETE FROM itens WHERE player_id=?', (player_id,))
        self.salvar()

    def atualizar_atributo_max(self, atributo_id, player_id, valor):
        self.c.execute('UPDATE atributos SET valor_max=? WHERE id=? AND player_id=?', (valor, atributo_id, player_id,))
        self.salvar()

    def atualizar_atributo_atual(self, atributo_id, player_id, valor):
        self.c.execute('UPDATE atributos SET valor_atual=? WHERE id=? AND player_id=?', (valor, atributo_id, player_id,))
        self.salvar()

    def set_battle_mode(self, mode, player_id):
        self.c.execute('UPDATE players SET batalhando=? WHERE id=?', (mode, player_id,))
        self.salvar()

    def get_battle_mode(self, player_id):
        self.c.execute('SELECT batalhando FROM players WHERE id=?', (player_id,))
        return self.c.fetchone()

    def get_conquistas(self, player_id):
        self.c.execute('SELECT * FROM conquistas WHERE player_id=?', (player_id,))
        return self.c.fetchall()

    def atualizar_conquista(self, nome, player_id):
        self.c.execute('UPDATE conquistas SET valor=? WHERE nome=? AND player_id=?', (1, nome, player_id,))
        self.salvar()

    def hard_reset(self):
        self.c.execute("DROP TABLE players")
        self.c.execute("DROP TABLE itens")
        self.c.execute("DROP TABLE conquistas")
        self.salvar()
        self.iniciar()
