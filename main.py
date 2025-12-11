from PPlay.window import Window
from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
import time
import os

#LEMBRAR DE COMENTAR TUDO P NAO DAR RUIM SE FOR MEXER EM ALGO
class Sokoban:
    def __init__(self, window_size=504):
        self.window_size = window_size
        self.image_size = window_size // 9
        self.level = 1
        self.show_level = True
        self.running = True
        self.game_started = False
        self.in_menu = True  #controlar se estamos no menu
        
        #controle de entrada
        self.last_key_state = {
            "UP": False,
            "LEFT": False,
            "DOWN": False,
            "RIGHT": False,
            "r": False,
            "ESC": False,
            "SPACE": False
        }
        
        #controle de tempo para evitar teclas repetidas muito rápido
        self.last_move_time = 0
        self.move_delay = 0.15
        
        #criar janela
        self.window = Window(window_size, window_size)
        self.window.set_title("Sokoban")
        self.keyboard = Keyboard()
        self.mouse = Mouse()  # Adicionado para controlar o mouse
        
        #definir botões do menu
        self.button_width = 200
        self.button_height = 60
        self.button_y_start = 200
        self.button_spacing = 80
        
        #carregar sprites dos botões
        self.load_button_sprites()
        
        #carregar imagens do jogo
        self.load_game_images()

        #definir todos os níveis do jogo
        self.setup_levels()
        self.main_level = [['' for _ in range(9)] for _ in range(9)]
        self.select_level()

    def load_button_sprites(self):
        """Carrega sprites para os botões do menu"""
        try:
            #carregar sprite do retângulo
            if os.path.exists('./retangulo.png'):
                self.button_sprite = Sprite('./retangulo.png')
                #configurar dimensões
                self.button_sprite.width = self.button_width
                self.button_sprite.height = self.button_height
            else:
                print("Aviso: retangulo.png não encontrado.")
                #criar sprite vazio como fallback
                self.button_sprite = Sprite()
                self.button_sprite.width = self.button_width
                self.button_sprite.height = self.button_height
        except Exception as e:
            print(f"Erro ao carregar sprite do botão: {e}")
            #criar sprite vazio como fallback
            self.button_sprite = Sprite()
            self.button_sprite.width = self.button_width
            self.button_sprite.height = self.button_height

    def load_game_images(self):
        """Carrega todas as imagens do jogo"""
        image_files = [
            './agent.png',
            './agent on target.png',
            './box on target.png',
            './box.png',
            './floor.png',
            './target.png',
            './tree.png',
            './wall.png'
        ]
        
        missing_images = []
        for img_file in image_files:
            if not os.path.exists(img_file):
                missing_images.append(img_file)
        
        if missing_images:
            print("Aviso: Algumas imagens não foram encontradas:")
            for img in missing_images:
                print(f"  - {img}")
            print("O jogo pode não funcionar corretamente.")
            time.sleep(1)

        try:
            self.agent = Sprite('./agent.png')
            self.agent_on_target = Sprite('./agent on target.png')
            self.box_on_target = Sprite('./box on target.png')
            self.box = Sprite('./box.png')
            self.floor = Sprite('./floor.png')
            self.target = Sprite('./target.png')
            self.tree = Sprite('./tree.png')
            self.wall = Sprite('./wall.png')

            #redimensionar sprites
            sprites = [self.agent, self.agent_on_target, self.box_on_target, 
                       self.box, self.floor, self.target, self.tree, self.wall]
            
            for sprite in sprites:
                sprite.set_position(0, 0)
                sprite.width = self.image_size
                sprite.height = self.image_size
                
        except Exception as e:
            print(f"Erro ao carregar imagens: {e}")
            #criar sprites vazios para evitar erros
            self.agent = Sprite()
            self.agent_on_target = Sprite()
            self.box_on_target = Sprite()
            self.box = Sprite()
            self.floor = Sprite()
            self.target = Sprite()
            self.tree = Sprite()
            self.wall = Sprite()

    def setup_levels(self):
        """Define todos os níveis do jogo"""
        self.level_1 = [['t', 't', 'w', 'w', 'w', 't', 't', 't', 't'],
                        ['t', 't', 'w', 'o', 'w', 't', 't', 't', 't'],
                        ['t', 't', 'w', 'f', 'w', 'w', 'w', 'w', 't'],
                        ['w', 'w', 'w', 'b', 'f', 'b', 'o', 'w', 't'],
                        ['w', 'o', 'f', 'b', 'a', 'w', 'w', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'b', 'w', 't', 't', 't'],
                        ['t', 't', 't', 'w', 'o', 'w', 't', 't', 't'],
                        ['t', 't', 't', 'w', 'w', 'w', 't', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_2 = [['w', 'w', 'w', 'w', 'w', 't', 't', 't', 't'],
                        ['w', 'f', 'f', 'f', 'w', 't', 't', 't', 't'],
                        ['w', 'f', 'b', 'a', 'w', 't', 'w', 'w', 'w'],
                        ['w', 'f', 'b', 'b', 'w', 't', 'w', 'o', 'w'],
                        ['w', 'w', 'w', 'f', 'w', 'w', 'w', 'o', 'w'],
                        ['t', 'w', 'w', 'f', 'f', 'f', 'f', 'o', 'w'],
                        ['t', 'w', 'f', 'f', 'f', 'w', 'f', 'f', 'w'],
                        ['t', 'w', 'f', 'f', 'f', 'w', 'w', 'w', 'w'],
                        ['t', 'w', 'w', 'w', 'w', 'w', 't', 't', 't']]

        self.level_3 = [['t', 'w', 'w', 'w', 'w', 't', 't', 't', 't'],
                        ['w', 'w', 'f', 'f', 'w', 't', 't', 't', 't'],
                        ['w', 'f', 'a', 'b', 'w', 't', 't', 't', 't'],
                        ['w', 'w', 'b', 'f', 'w', 'w', 't', 't', 't'],
                        ['w', 'w', 'f', 'b', 'f', 'w', 't', 't', 't'],
                        ['w', 'o', 'b', 'f', 'f', 'w', 't', 't', 't'],
                        ['w', 'o', 'o', 'bot', 'o', 'w', 't', 't', 't'],
                        ['w', 'w', 'w', 'w', 'w', 'w', 't', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_4 = [['t', 'w', 'w', 'w', 'w', 't', 't', 't', 't'],
                        ['t', 'w', 'a', 'f', 'w', 'w', 'w', 't', 't'],
                        ['t', 'w', 'f', 'b', 'f', 'f', 'w', 't', 't'],
                        ['w', 'w', 'w', 'f', 'w', 'f', 'w', 'w', 't'],
                        ['w', 'o', 'w', 'f', 'w', 'f', 'f', 'w', 't'],
                        ['w', 'o', 'b', 'f', 'f', 'w', 'f', 'w', 't'],
                        ['w', 'o', 'f', 'f', 'f', 'b', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_5 = [['t', 't', 'w', 'w', 'w', 'w', 'w', 'w', 't'],
                        ['t', 't', 'w', 'f', 'f', 'f', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'b', 'b', 'b', 'f', 'w', 't'],
                        ['w', 'a', 'f', 'b', 'o', 'o', 'f', 'w', 't'],
                        ['w', 'f', 'b', 'o', 'o', 'o', 'w', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'f', 'f', 'w', 't', 't'],
                        ['t', 't', 't', 'w', 'w', 'w', 'w', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_6 = [['t', 't', 'w', 'w', 'w', 'w', 'w', 't', 't'],
                        ['w', 'w', 'w', 'f', 'f', 'a', 'w', 't', 't'],
                        ['w', 'f', 'f', 'b', 'o', 'f', 'w', 'w', 't'],
                        ['w', 'f', 'f', 'o', 'b', 'o', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'f', 'bot', 'b', 'f', 'w', 't'],
                        ['t', 't', 'w', 'f', 'f', 'f', 'w', 'w', 't'],
                        ['t', 't', 'w', 'w', 'w', 'w', 'w', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_7 = [['t', 't', 'w', 'w', 'w', 'w', 't', 't', 't'],
                        ['t', 't', 'w', 'o', 'o', 'w', 't', 't', 't'],
                        ['t', 'w', 'w', 'f', 'o', 'w', 'w', 't', 't'],
                        ['t', 'w', 'f', 'f', 'b', 'o', 'w', 't', 't'],
                        ['w', 'w', 'f', 'b', 'f', 'f', 'w', 'w', 't'],
                        ['w', 'f', 'f', 'w', 'b', 'b', 'f', 'w', 't'],
                        ['w', 'f', 'f', 'a', 'f', 'f', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_8 = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 't'],
                        ['w', 'f', 'f', 'w', 'f', 'f', 'f', 'w', 't'],
                        ['w', 'a', 'b', 'o', 'o', 'b', 'f', 'w', 't'],
                        ['w', 'f', 'b', 'o', 'bot', 'f', 'w', 'w', 't'],
                        ['w', 'f', 'b', 'o', 'o', 'b', 'f', 'w', 't'],
                        ['w', 'f', 'f', 'w', 'f', 'f', 'f', 'w', 't'],
                        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_9 = [['w', 'w', 'w', 'w', 'w', 'w', 't', 't', 't'],
                        ['w', 'f', 'f', 'f', 'f', 'w', 't', 't', 't'],
                        ['w', 'f', 'b', 'b', 'b', 'w', 'w', 't', 't'],
                        ['w', 'f', 'f', 'w', 'o', 'o', 'w', 'w', 'w'],
                        ['w', 'w', 'f', 'f', 'o', 'o', 'b', 'f', 'w'],
                        ['t', 'w', 'f', 'a', 'f', 'f', 'f', 'f', 'w'],
                        ['t', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't'],
                        ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_10 = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 't', 't'],
                         ['w', 'o', 'o', 'b', 'o', 'o', 'w', 't', 't'],
                         ['w', 'o', 'o', 'w', 'o', 'o', 'w', 't', 't'],
                         ['w', 'f', 'b', 'b', 'b', 'f', 'w', 't', 't'],
                         ['w', 'f', 'f', 'b', 'f', 'f', 'w', 't', 't'],
                         ['w', 'f', 'b', 'b', 'b', 'f', 'w', 't', 't'],
                         ['w', 'f', 'f', 'w', 'a', 'f', 'w', 't', 't'],
                         ['w', 'w', 'w', 'w', 'w', 'w', 'w', 't', 't'],
                         ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_11 = [['t', 'w', 'w', 'w', 'w', 'w', 't', 't', 't'],
                         ['t', 'w', 'f', 'a', 'f', 'w', 'w', 'w', 't'],
                         ['w', 'w', 'f', 'w', 'b', 'f', 'f', 'w', 't'],
                         ['w', 'f', 'bot', 'o', 'f', 'o', 'f', 'w', 't'],
                         ['w', 'f', 'f', 'b', 'b', 'f', 'w', 'w', 't'],
                         ['w', 'w', 'w', 'f', 'w', 'o', 'w', 't', 't'],
                         ['t', 't', 'w', 'f', 'f', 'f', 'w', 't', 't'],
                         ['t', 't', 'w', 'w', 'w', 'w', 'w', 't', 't'],
                         ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_12 = [['w', 'w', 'w', 'w', 'w', 'w', 't', 't', 't'],
                         ['w', 'f', 'f', 'f', 'f', 'w', 't', 't', 't'],
                         ['w', 'f', 'b', 'f', 'a', 'w', 't', 't', 't'],
                         ['w', 'w', 'bot', 'f', 'f', 'w', 't', 't', 't'],
                         ['w', 'f', 'bot', 'f', 'w', 'w', 't', 't', 't'],
                         ['w', 'f', 'bot', 'f', 'w', 't', 't', 't', 't'],
                         ['w', 'f', 'bot', 'f', 'w', 't', 't', 't', 't'],
                         ['w', 'f', 'o', 'f', 'w', 't', 't', 't', 't'],
                         ['w', 'w', 'w', 'w', 'w', 't', 't', 't', 't']]

        self.level_13 = [['t', 't', 'w', 'w', 'w', 'w', 't', 't', 't'],
                         ['t', 't', 'w', 'f', 'f', 'w', 't', 't', 't'],
                         ['w', 'w', 'w', 'b', 'f', 'w', 'w', 't', 't'],
                         ['w', 'f', 'f', 'bot', 'f', 'a', 'w', 't', 't'],
                         ['w', 'f', 'f', 'bot', 'f', 'f', 'w', 't', 't'],
                         ['w', 'f', 'f', 'bot', 'f', 'w', 'w', 't', 't'],
                         ['w', 'w', 'w', 'bot', 'f', 'w', 't', 't', 't'],
                         ['t', 't', 'w', 'o', 'w', 'w', 't', 't', 't'],
                         ['t', 't', 'w', 'w', 'w', 't', 't', 't', 't']]

        self.level_14 = [['w', 'w', 'w', 'w', 'w', 't', 't', 't', 't'],
                         ['w', 'f', 'f', 'f', 'w', 'w', 'w', 'w', 'w'],
                         ['w', 'f', 'w', 'f', 'w', 'f', 'f', 'f', 'w'],
                         ['w', 'f', 'b', 'f', 'f', 'f', 'b', 'f', 'w'],
                         ['w', 'o', 'o', 'w', 'b', 'w', 'b', 'w', 'w'],
                         ['w', 'o', 'a', 'b', 'f', 'f', 'f', 'w', 't'],
                         ['w', 'o', 'o', 'f', 'f', 'w', 'w', 'w', 't'],
                         ['w', 'w', 'w', 'w', 'w', 'w', 't', 't', 't'],
                         ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_15 = [['t', 'w', 'w', 'w', 'w', 'w', 'w', 't', 't'],
                         ['t', 'w', 'f', 'f', 'f', 'f', 'w', 'w', 't'],
                         ['w', 'w', 'o', 'w', 'w', 'b', 'f', 'w', 't'],
                         ['w', 'f', 'o', 'o', 'b', 'f', 'f', 'w', 't'],
                         ['w', 'f', 'f', 'w', 'b', 'f', 'f', 'w', 't'],
                         ['w', 'f', 'f', 'a', 'f', 'w', 'w', 'w', 't'],
                         ['w', 'w', 'w', 'w', 'w', 'w', 't', 't', 't'],
                         ['t', 't', 't', 't', 't', 't', 't', 't', 't'],
                         ['t', 't', 't', 't', 't', 't', 't', 't', 't']]

        self.level_16 = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                         ['w', 'o', 'f', 'f', 'o', 'f', 'f', 'o', 'w'],
                         ['w', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'w'],
                         ['w', 'f', 'f', 'b', 'b', 'b', 'f', 'f', 'w'],
                         ['w', 'o', 'f', 'b', 'a', 'b', 'f', 'o', 'w'],
                         ['w', 'f', 'f', 'b', 'b', 'b', 'f', 'f', 'w'],
                         ['w', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'w'],
                         ['w', 'o', 'f', 'f', 'o', 'f', 'f', 'o', 'w'],
                         ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']]

    def copy_level(self, level):
        """Copia um nível para o main_level"""
        for y in range(9):
            for x in range(9):
                self.main_level[y][x] = level[y][x]

    def select_level(self):
        """Seleciona o nível atual"""
        level_mapping = {
            1: self.level_1, 2: self.level_2, 3: self.level_3, 4: self.level_4,
            5: self.level_5, 6: self.level_6, 7: self.level_7, 8: self.level_8,
            9: self.level_9, 10: self.level_10, 11: self.level_11, 12: self.level_12,
            13: self.level_13, 14: self.level_14, 15: self.level_15, 16: self.level_16
        }
        
        if self.level in level_mapping:
            self.copy_level(level_mapping[self.level])

    def draw_map(self):
        """Desenha o mapa na tela"""
        self.window.set_background_color((200, 200, 200))
        
        for y in range(9):
            for x in range(9):
                cell = self.main_level[y][x]
                pos_x = x * self.image_size
                pos_y = y * self.image_size
                
                #desenhar chão primeiro (exceto onde há árvore)
                if cell != 't':
                    self.floor.set_position(pos_x, pos_y)
                    self.floor.draw()
                
                #desenhar elementos específicos
                if cell == 'a':
                    self.agent.set_position(pos_x, pos_y)
                    self.agent.draw()
                elif cell == 'aot':
                    self.target.set_position(pos_x, pos_y)
                    self.target.draw()
                    self.agent_on_target.set_position(pos_x, pos_y)
                    self.agent_on_target.draw()
                elif cell == 't':
                    self.tree.set_position(pos_x, pos_y)
                    self.tree.draw()
                elif cell == 'w':
                    self.wall.set_position(pos_x, pos_y)
                    self.wall.draw()
                elif cell == 'o':
                    self.target.set_position(pos_x, pos_y)
                    self.target.draw()
                elif cell == 'b':
                    self.box.set_position(pos_x, pos_y)
                    self.box.draw()
                elif cell == 'bot':
                    self.target.set_position(pos_x, pos_y)
                    self.target.draw()
                    self.box_on_target.set_position(pos_x, pos_y)
                    self.box_on_target.draw()
        
        #desenhar informações na tela
        self.window.draw_text(f"Nível: {self.level}", 10, 10, 20, (0, 0, 0))
        self.window.draw_text("Setas: Mover  R: Reiniciar  ESC: Sair", 10, 470, 16, (100, 100, 100))

    def get_agent_position(self):
        """Encontra a posição do agente no mapa"""
        for y in range(9):
            for x in range(9):
                if self.main_level[y][x] in ['a', 'aot']:
                    return [x, y]
        return [0, 0]

    def handle_input(self):
        """Processa a entrada do usuário com controle para evitar múltiplos movimentos"""
        current_time = time.time()
        
        #verificar se passou tempo suficiente desde o último movimento
        can_move = (current_time - self.last_move_time) >= self.move_delay
        
        #verificar tecla ESPAÇO para iniciar/mudar estado
        if self.keyboard.key_pressed("SPACE"):
            if not self.last_key_state["SPACE"] and self.show_level:
                self.show_level = False
            self.last_key_state["SPACE"] = True
        else:
            self.last_key_state["SPACE"] = False
            
        #se estamos no menu, não processa teclas de jogo
        if self.in_menu:
            return
            
        #se o jogo não começou, não processa outras teclas
        if not self.game_started:
            return
            
        #verificar teclas de movimento
        if self.keyboard.key_pressed("UP"):
            if not self.last_key_state["UP"] and can_move:
                self.move_agent('w')
                self.last_move_time = current_time
            self.last_key_state["UP"] = True
        else:
            self.last_key_state["UP"] = False
            
        if self.keyboard.key_pressed("LEFT"):
            if not self.last_key_state["LEFT"] and can_move:
                self.move_agent('a')
                self.last_move_time = current_time
            self.last_key_state["LEFT"] = True
        else:
            self.last_key_state["LEFT"] = False
            
        if self.keyboard.key_pressed("DOWN"):
            if not self.last_key_state["DOWN"] and can_move:
                self.move_agent('s')
                self.last_move_time = current_time
            self.last_key_state["DOWN"] = True
        else:
            self.last_key_state["DOWN"] = False
            
        if self.keyboard.key_pressed("RIGHT"):
            if not self.last_key_state["RIGHT"] and can_move:
                self.move_agent('d')
                self.last_move_time = current_time
            self.last_key_state["RIGHT"] = True
        else:
            self.last_key_state["RIGHT"] = False
        
        #as outras teclas
        if self.keyboard.key_pressed("r"):
            if not self.last_key_state["r"]:
                self.select_level()
            self.last_key_state["r"] = True
        else:
            self.last_key_state["r"] = False
            
        if self.keyboard.key_pressed("ESC"):
            if not self.last_key_state["ESC"]:
                self.running = False
            self.last_key_state["ESC"] = True
        else:
            self.last_key_state["ESC"] = False

    def move_agent(self, direction):
        """Move o agente na direção especificada"""
        agent_pos = self.get_agent_position()
        new_x, new_y = agent_pos
        ahead_x, ahead_y = agent_pos
        
        #calcular novas posições
        if direction == 'w':  #cima
            new_y -= 1
            ahead_y -= 2
        elif direction == 'a':  #esquerda
            new_x -= 1
            ahead_x -= 2
        elif direction == 's':  #baixo
            new_y += 1
            ahead_y += 2
        elif direction == 'd':  #direita
            new_x += 1
            ahead_x += 2

        #verificar limites do tabuleiro
        if not (0 <= new_x < 9 and 0 <= new_y < 9):
            return
            
        current_cell = self.main_level[new_y][new_x]
        
        #se for parede ou árvore, não pode mover
        if current_cell in ['w', 't']:
            return
            
        #se for caixa, verificar se pode empurrar
        if current_cell in ['b', 'bot']:
            if not (0 <= ahead_x < 9 and 0 <= ahead_y < 9):
                return
                
            ahead_cell = self.main_level[ahead_y][ahead_x]
            if ahead_cell in ['w', 't', 'b', 'bot']:
                return  #não pode 
            
            #empurrar a caixa
            if ahead_cell == 'f':
                self.main_level[ahead_y][ahead_x] = 'b'
            elif ahead_cell == 'o':
                self.main_level[ahead_y][ahead_x] = 'bot'
                
            #atualizar célula da caixa
            if current_cell == 'b':
                self.main_level[new_y][new_x] = 'a'
            else:  #'bot'
                self.main_level[new_y][new_x] = 'aot'
                
        else:
            #mover para célula vazia
            if current_cell == 'f':
                self.main_level[new_y][new_x] = 'a'
            elif current_cell == 'o':
                self.main_level[new_y][new_x] = 'aot'
        
        #atualizar posição anterior do agente
        if self.main_level[agent_pos[1]][agent_pos[0]] == 'a':
            self.main_level[agent_pos[1]][agent_pos[0]] = 'f'
        elif self.main_level[agent_pos[1]][agent_pos[0]] == 'aot':
            self.main_level[agent_pos[1]][agent_pos[0]] = 'o'

    def show_level_screen(self):
        """Mostra a tela de nível até o jogador pressionar ESPAÇO"""
        if self.show_level:
            #mostrar tela até pressionar ESPAÇO
            waiting_for_space = True
            
            while waiting_for_space and self.running:
                #verificar tecla ESC (para poder sair na tela de nível também)
                if self.keyboard.key_pressed("ESC"):
                    self.running = False
                    break
                
                #verificar tecla ESPAÇO
                if self.keyboard.key_pressed("SPACE"):
                    waiting_for_space = False
                
                #desenhar tela do nível
                self.window.set_background_color((240, 240, 240))
                text = f'Nível {self.level}'
                
                #calcular posição centralizada
                x = self.window.width // 2 - 80
                y = self.window.height // 2 - 60
                
                #desenhar título
                self.window.draw_text(text, x, y, 48, (0, 0, 0), "Arial", bold=True)
                
                #instruções
                instr_x = x - 40
                instr_y = y + 70
                self.window.draw_text("CONTROLES:", instr_x, instr_y, 24, (100, 100, 100), "Exo")
                self.window.draw_text("Setas: Mover", instr_x, instr_y + 30, 20, (80, 80, 80), "Arial")
                self.window.draw_text("R: Reiniciar nível", instr_x, instr_y + 55, 20, (80, 80, 80), "Arial")
                self.window.draw_text("ESC: Sair", instr_x, instr_y + 80, 20, (80, 80, 80), "Arial")
                
                #instrução para começar
                start_x = self.window.width // 2 - 140
                start_y = y + 250
                self.window.draw_text("Pressione ESPAÇO para jogar", start_x, start_y, 20, (50, 150, 50), "Arial", bold=True)
                
                #atualizar janela
                self.window.update()
                
                #pequena pausa
                time.sleep(0.016)
            
            self.show_level = False

    def check_level_complete(self):
        """Verifica se o nível foi completado"""
        #contar caixas que não estão nos alvos
        for y in range(9):
            for x in range(9):
                if self.main_level[y][x] == 'b':
                    return False
        
        #nível completo - preparar para mostrar tela de próximo nível
        self.show_level = True
        self.level += 1
        if self.level > 16:  #volta ao primeiro nível após completar todos
            self.level = 1
            #mostrar mensagem de vitória
            self.window.set_background_color((240, 240, 240))
            self.window.draw_text("Parabéns!", 150, 200, 48, (0, 100, 0), "Arial", bold=True)
            self.window.draw_text("Você completou todos os níveis!", 80, 260, 24, (0, 100, 0), "Arial")
            self.window.draw_text("Pressione ESPAÇO para continuar", 100, 300, 24, (50, 150, 50), "Arial")
            self.window.update()
            
            #esperar ESPAÇO para continuar
            waiting = True
            while waiting and self.running:
                #verificar tecla ESC (para poder sair)
                if self.keyboard.key_pressed("ESC"):
                    self.running = False
                    break
                    
                if self.keyboard.key_pressed("SPACE"):
                    waiting = False
                time.sleep(0.016)
        
        #carregar o próximo nível
        self.select_level()
        return True

    def draw_menu(self):
        """Desenha o menu principal com botões usando sprites"""
        #configurar cor de fundo do menu
        self.window.set_background_color((230, 240, 250))
        
        #título do jogo
        title_x = self.window.width // 2 - 120
        self.window.draw_text("SOKOBAN", title_x, 100, 48, (30, 60, 120), "Arial", bold=True)
        
        #subtítulo
        subtitle_x = self.window.width // 2 - 180
        self.window.draw_text("Empurre as caixas para os alvos", subtitle_x + 40, 160, 20, (80, 100, 150), "Arial")
        
        #posição do botão Jogar
        button_x = (self.window.width - self.button_width) // 2
        play_button_y = self.button_y_start
        
        #desenhar botão Jogar
        self.button_sprite.set_position(button_x, play_button_y)
        self.button_sprite.draw()
        
        #texto do botão Jogar
        play_text_x = button_x + (self.button_width - 70) // 2
        play_text_y = play_button_y + (self.button_height - 30) // 2
        self.window.draw_text("JOGAR", play_text_x - 10, play_text_y, 28, (255, 255, 255), "Arial", bold=True)
        
        #posição do botão Sair
        quit_button_y = self.button_y_start + self.button_spacing
        
        #desenhar botão Sair
        self.button_sprite.set_position(button_x, quit_button_y)
        self.button_sprite.draw()
        
        #texto do botão Sair
        quit_text_x = button_x + (self.button_width - 60) // 2
        quit_text_y = quit_button_y + (self.button_height - 30) // 2
        self.window.draw_text("SAIR", quit_text_x - 3, quit_text_y, 28, (255, 255, 255), "Arial", bold=True)
        
        #instruções
        instr_x = self.window.width // 2 - 150
        self.window.draw_text("Clique nos botões para navegar", instr_x + 40, 450, 16, (100, 100, 150), "Arial")
        
        #verificar clique do mouse nos botões
        mouse_x, mouse_y = self.mouse.get_position()
        
        #verificar se o mouse está sobre o botão Jogar
        play_hover = (button_x <= mouse_x <= button_x + self.button_width and 
                     play_button_y <= mouse_y <= play_button_y + self.button_height)
        
        #verificar se o mouse está sobre o botão Sair
        quit_hover = (button_x <= mouse_x <= button_x + self.button_width and 
                     quit_button_y <= mouse_y <= quit_button_y + self.button_height)
        
        #verificar clique nos botões
        if self.mouse.is_button_pressed(1):  # Botão esquerdo do mouse
            if play_hover:
                #iniciar o jogo
                self.in_menu = False
                self.game_started = True
                self.show_level = True
            elif quit_hover:
                #sair do jogo
                self.running = False

    def run(self):
        """Loop principal do jogo"""
        print("=" * 50)
        print("SOKOBAN")
        print("=" * 50)
        print("Controles:")
        print("  ESPAÇO: Começar/Continuar")
        print("  Setas: Mover")
        print("  R: Reiniciar nível atual")
        print("  ESC: Sair do jogo")
        print("=" * 50)
        print("Objetivo: Empurre todas as caixas para os alvos")
        print("=" * 50)
        
        #loop principal do jogo
        while self.running:
            #menu principal
            if self.in_menu:
                self.draw_menu()
            
            #jogo
            elif self.game_started:
                #mostrar tela de nível se necessário
                if self.show_level:
                    self.show_level_screen()
                    continue
                
                #processar entrada do usuário
                self.handle_input()
                
                #desenhar o jogo
                self.draw_map()
                
                #verificar se o nível foi completado
                if self.check_level_complete():
                    #mostrar tela do próximo nível
                    self.show_level_screen()
            
            #atualizar janela
            self.window.update()
            
            #controlar a taxa de atualização
            time.sleep(0.016)

        print("Jogo finalizado!")
        print("Obrigado por jogar!")

#executar o jogo
if __name__ == "__main__":
    try:
        game = Sokoban(504)
        game.run()
    except KeyboardInterrupt:
        print("\nJogo interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")