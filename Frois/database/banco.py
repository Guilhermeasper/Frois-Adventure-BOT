import sqlite3

class Banco():
    def __init__(self):
        self.conn = sqlite3.connect('players.db')
        self.c = self.conn.cursor()

    def iniciar(self):
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS players ( id INTEGER PRIMARY KEY,
                                                    nome TEXT,
                                                    avatar TEXT,
                                                    avatar_level INTEGER,
                                                    exp INTEGER,
                                                    sec INTEGER,
                                                    pos_x INTEGER,
                                                    pos_y INTEGER
                                                    );''')

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS itens ( id INTEGER PRIMARY KEY,
                                                    item TEXT,
                                                    quantidade INTEGER,
                                                    valor_unit INTEGER,
                                                    player_id INTEGER,
                                                    FOREIGN KEY (player_id) REFERENCES players(id)
                                                    );''')

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS atributos ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    nome TEXT,
                                                    valor_atual INTEGER,
                                                    valor_max INTEGER,
                                                    player_id INTEGER,
                                                    FOREIGN KEY (player_id) REFERENCES players(id)
                                                    );''')

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS status ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    nome TEXT,
                                                    valor INTEGER,
                                                    player_id INTEGER,
                                                    FOREIGN KEY (player_id) REFERENCES players(id)
                                                    );''')

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS conquistas ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    nome TEXT,
                                                    valor INTEGER,
                                                    recompensa INTEGER,
                                                    player_id INTEGER,
                                                    FOREIGN KEY (player_id) REFERENCES players(id)
                                                    );''')

    def salvar(self):
        self.conn.commit()

    def fechar(self):
        self.conn.close()

    def iniciar_personagem(self, id, nome, avatar, avatar_level, exp, sec, pos_x, pos_y):
        self.c.execute('INSERT INTO players VALUES(?,?,?,?,?,?,?,?)', (id, nome, avatar, avatar_level, exp, sec, pos_x, pos_y))

    def atualizar_avatar(self, id, avatar):
        self.c.execute('UPDATE players SET avatar=? WHERE id=?', (avatar, id))

    def atualizar_posicao(self, id, pos_x, pos_y):
        self.c.execute('UPDATE players SET pos_x=?, pos_y=? WHERE id=?', (pos_y, pos_y, id))

    def atualizar_secao(self, id, sec):
        self.c.execute('UPDATE players SET sec=? WHERE id=?', (sec, id))

    def procurar_personagem(self, avatar):
        self.c.execute('SELECT * FROM players WHERE avatar=?', avatar)
        return self.c.fetchone()

    def procurar_player_id(self, id):
        self.c.execute('SELECT * FROM players WHERE id=?', id)
        return self.c.fetchone()

    def info_personagem(self, avatar):
        self.c.execute('SELECT * FROM players INNER JOIN atributos a on players.id = a.player_id AND players.avatar = ?', avatar)
        return self.c.fetchone()

    def remover_personagem(self, avatar):
        self.c.execute('DELETE FROM players WHERE avatar=?', avatar)

    def inserir_item(self, id, nome, quantidade, valor, player_id):
        self.c.execute('INSERT INTO itens VALUES(?,?,?,?,?)', (id, nome, quantidade, valor, player_id))