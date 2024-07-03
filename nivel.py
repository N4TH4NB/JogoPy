import pygame.sprite

from config import *
from sprites import Sprite, Plataforma_Movel, Botao
from jogador import Jogador
from groups import AllSprites
#from Inimigo import Enemy


class Nivel:
    def __init__(self, tmx_map):
        # Remover self.display_surface, já que vamos usar a game_surface da classe Game
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        # self.enemy_collision_sprites = pygame.sprite.Group()
        self.setup(tmx_map)

    def setup(self, tmx_map):
        #chao
        for x, y, surf in tmx_map.get_layer_by_name("Chao").tiles():
            Sprite((x * tamanho_bloco, y * tamanho_bloco), surf, (self.all_sprites, self.collision_sprites))
        #objetos
        for obj in tmx_map.get_layer_by_name("Player"):
            if obj.name == "Passaro":
                self.player = Jogador((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.semi_collision_sprites, pygame.K_d, pygame.K_a, pygame.K_s, pygame.K_w)
        for obj in tmx_map.get_layer_by_name("Player"):
            if obj.name == "Player2":
                self.player2 = Jogador((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.semi_collision_sprites, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP)
        for obj in tmx_map.get_layer_by_name("Obstaculo"):
            if obj.name == "Botao":
                self.botao = Botao((obj.x, obj.y), self.all_sprites, self.collision_sprites)
        #Plataformas
        for obj in tmx_map.get_layer_by_name("Plataformas"):
            if obj.name == "Local":
                # horizontal
                if obj.width > obj.height:
                    direcao_movi = "x"
                    pos_inicial = (obj.x,obj.y + obj.height/2)
                    pos_final = (obj.x + obj.width, obj.y + obj.height/2)

                # vertical
                else:

                    direcao_movi = "y"
                    pos_inicial = (obj.x + obj.width / 2, obj.y)
                    pos_final = (obj.x + obj.width / 2, obj.y + obj.height)
                Vel = obj.properties["Vel"]
                Plataforma_Movel((self.all_sprites, self.semi_collision_sprites), pos_inicial, pos_final, direcao_movi, Vel)

        #for obj in tmx_map.get_layer_by_name("Inimigos"):
        #    if obj.name == "Enemy":
        #        player((obj.x, obj.y), self.all_sprites, self.enemy_collision_sprites)



    def run(self, dt):
        self.display_surface.fill("#72647d")

        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)
