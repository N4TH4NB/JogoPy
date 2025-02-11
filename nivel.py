import pygame.sprite
from config import *  # Importa todas as configurações do arquivo config
from sprites import Sprite, PlataformaMovel, Dano  # Importa as classes Sprite, PlataformaMovel e Dano
from jogador import Jogador  # Importa a classe Jogador
from groups import AllSprites  # Importa o grupo AllSprites
from os.path import join  # Importa a função join para manipulação de caminhos de arquivos


class Nivel:
    def __init__(self, tmx_map, switch_stage):
        # Inicializa os atributos da classe
        self.level_finish_rect = None
        self.num_niveis = None
        self.jogador2 = None
        self.jogador = None
        self.switch_stage = switch_stage
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.dano_sprites = pygame.sprite.Group()
        self.setup(tmx_map)  # Configura o nível com base no mapa tmx

    def setup(self, tmx_map):
        # Cria os diferentes elementos do nível
        self.criar_objetos_estaticos(tmx_map)
        self.criar_sprites_dano(tmx_map)
        self.criar_plataforma(tmx_map)
        self.criar_sprites_camadas(tmx_map, "Chao", self.collision_sprites)
        self.criar_sprites_camadas(tmx_map, "Decoracao")
        self.criar_jogadores(tmx_map)

    def criar_sprites_camadas(self, tmx_map, layer_name, *groups):
        # Cria sprites baseados nas camadas do mapa tmx
        for x, y, surf in tmx_map.get_layer_by_name(layer_name).tiles():
            Sprite((x * tamanho_bloco, y * tamanho_bloco), surf, (self.all_sprites, *groups))

    def criar_jogadores(self, tmx_map):
        # Cria os jogadores com base na camada "Jogador" do mapa tmx
        camada_jogador = tmx_map.get_layer_by_name("Jogador")
        for obj in camada_jogador:
            if obj.name == "jogador1":
                self.jogador = self.criar_jogador(obj, obj.properties["Image"], pygame.K_d, pygame.K_a, pygame.K_s,
                                                  pygame.K_w)
            elif obj.name == "jogador2":
                self.jogador2 = self.criar_jogador(obj, obj.properties["Image"], pygame.K_RIGHT, pygame.K_LEFT,
                                                   pygame.K_DOWN, pygame.K_UP)

    def criar_jogador(self, obj, image_path, right_key, left_key, down_key, up_key):
        # Cria um objeto jogador
        return Jogador(
            pygame.image.load(join(image_path)), (obj.x, obj.y),
            (self.all_sprites,), self.collision_sprites, self.semi_collision_sprites,
            right_key, left_key, down_key, up_key
        )

    def criar_objetos_estaticos(self, tmx_map):
        # Cria objetos estáticos com base na camada "ObjEstatico" do mapa tmx
        for obj in tmx_map.get_layer_by_name("ObjEstatico"):
            if obj.name == "bandeira":
                self.num_niveis = obj.properties["nivel"]
                image = obj.properties["Image"]
                image = pygame.image.load(join(image))
                self.level_finish_rect = Sprite((obj.x, obj.y), image, self.all_sprites)

    def criar_sprites_dano(self, tmx_map):
        # Cria sprites de dano com base na camada "Dano" do mapa tmx
        for obj in tmx_map.get_layer_by_name("Dano"):
            image = obj.properties["Image"]
            image = pygame.image.load(join(image))
            if image:
                if obj.name in ["danoreset", "danocontinuo"]:
                    direcao_movi = obj.properties["direcao"]
                    vel = 30
                    pos_inicial, pos_final = self.get_posicao_dano(obj, direcao_movi)
                    Dano((self.all_sprites, self.dano_sprites), pos_inicial, pos_final, direcao_movi, vel,
                                    image, obj.name)
                elif obj.name == "danoparado":
                    Sprite((obj.x, obj.y), image, (self.all_sprites, self.dano_sprites))

    def get_posicao_dano(self, obj, direcao_movi):
        # Calcula a posição inicial e final do dano com base na direção de movimento
        pos_inicial = (obj.x, obj.y)
        if direcao_movi == "y":
            pos_final = (obj.x, obj.y + 100)
        elif direcao_movi == "-y":
            pos_final = (obj.x, obj.y - 100)
        else:
            pos_final = (obj.x + 50, obj.y)
        return pos_inicial, pos_final

    def criar_plataforma(self, tmx_map):
        # Cria plataformas móveis com base na camada "Plataformas" do mapa tmx
        for obj in tmx_map.get_layer_by_name("Plataformas"):
            direcao_movi, pos_inicial, pos_final = self.get_posicao_plataforma(obj)
            vel = obj.properties["Vel"]
            image = obj.properties["Image"]
            image = pygame.image.load(join(image))
            PlataformaMovel((self.all_sprites, self.semi_collision_sprites), pos_inicial, pos_final, direcao_movi, vel,
                            image)

    def get_posicao_plataforma(self, obj):
        # Calcula a posição inicial e final da plataforma com base em suas dimensões
        if obj.width > obj.height:  # horizontal
            direcao_movi = "x"
            pos_inicial = (obj.x, obj.y + obj.height / 2)
            pos_final = (obj.x + obj.width, obj.y + obj.height / 2)
        else:  # vertical
            direcao_movi = "y"
            pos_inicial = (obj.x + obj.width / 2, obj.y)
            pos_final = (obj.x + obj.width / 2, obj.y + obj.height)
        return direcao_movi, pos_inicial, pos_final

    def map_change(self, num_nivel):
        # Muda o mapa se os jogadores atingirem a área de finalização do nível
        if self.jogador.hitbox_rect.colliderect(self.level_finish_rect) and self.jogador2.hitbox_rect.colliderect(
                self.level_finish_rect):
            self.switch_stage(num_nivel)

    def morrer(self):
        # Verifica se os jogadores colidiram com um sprite de dano ou caíram da tela, e os respawna se necessário
        for sprite in self.dano_sprites:
            colisao_dano = sprite.rect.colliderect(
                self.jogador2.hitbox_rect.inflate(-5, -5)) or sprite.rect.colliderect(
                self.jogador.hitbox_rect.inflate(-5, -5))
            if colisao_dano or self.jogador.hitbox_rect.y > 700 or self.jogador2.hitbox_rect.y > 700:
                self.jogador2.respawn()
                self.jogador.respawn()

    def run(self, dt):
        # Atualiza e desenha todos os sprites, verifica mudança de mapa e verifica se os jogadores morreram
        self.all_sprites.update(dt)
        x = (self.jogador.hitbox_rect.x + self.jogador2.hitbox_rect.x) / 2
        y = (self.jogador.hitbox_rect.y + self.jogador2.hitbox_rect.y) / 2
        center = [x, y]
        self.all_sprites.draw(center)
        self.map_change(self.num_niveis)
        self.morrer()
