from config import *  # Importa todas as configurações do arquivo config
from timer import Timer  # Importa a classe Timer
import pygame

class Jogador(pygame.sprite.Sprite):
    def __init__(self, image, pos, groups, collision_sprites, semi_collision_sprites, right_key, left_key, down_key, jump_key):
        super().__init__(groups)  # Inicializa a classe base pygame.sprite.Sprite
        self.original_image = image  # Guarda a imagem original do jogador
        self.image = image  # Define a imagem atual do jogador
        self.spawn_pos = pos  # Guarda a posição inicial de spawn do jogador
        self.rect = self.image.get_frect(topleft=pos)  # Cria um retângulo de colisão para o jogador
        self.hitbox_rect = self.rect.inflate(0, 0)  # Cria um retângulo de hitbox para o jogador
        self.old_rect = self.hitbox_rect.copy()  # Guarda a antiga posição da hitbox do jogador
        self.direction = vector()  # Vetor de direção do jogador
        self.speed = 150  # Velocidade de movimento do jogador
        self.gravity = 20  # Força da gravidade que afeta o jogador
        self.jump = False  # Indicador de pulo
        self.climb = False  # Indicador de escalada
        self.jump_height = -5  # Altura do pulo
        self.collision_sprites = collision_sprites  # Grupo de sprites de colisão
        self.semi_collision_sprites = semi_collision_sprites  # Grupo de sprites de semi-colisão
        self.on_ground = {"chao": False, "left": False, "right": False}  # Indicadores de contato com o chão e paredes
        self.plataforma = None  # Plataforma atual em que o jogador está
        self.timers = {
            "wall jump": Timer(15),  # Timer para pulo na parede
            "wall climb": Timer(100),  # Timer para escalada na parede
            "plataforma fall": Timer(250)  # Timer para queda da plataforma
        }
        self.right_key = right_key  # Tecla para mover para a direita
        self.left_key = left_key  # Tecla para mover para a esquerda
        self.down_key = down_key  # Tecla para descer
        self.jump_key = jump_key  # Tecla para pular

    def input(self):
        keys = pygame.key.get_pressed()  # Obtém o estado de todas as teclas pressionadas
        input_vector = vector(0, 0)  # Vetor de entrada para movimento
        if not self.timers["wall jump"].active:  # Se o timer de pulo na parede não está ativo
            if keys[self.right_key]:  # Se a tecla para mover para a direita está pressionada
                input_vector.x += 1
                self.image = self.original_image
            if keys[self.left_key]:  # Se a tecla para mover para a esquerda está pressionada
                input_vector.x -= 1
                self.image = pygame.transform.flip(self.original_image, True, False)
            if keys[self.down_key]:  # Se a tecla para descer está pressionada
                self.timers["plataforma fall"].activate()
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[self.jump_key]:  # Se a tecla para pular está pressionada continuamente
            self.jump = True
            self.climb = True

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt  # Move o jogador horizontalmente
        self.collision("horizontal")  # Checa colisão horizontal

        if not self.on_ground["chao"] and (self.on_ground["left"] or self.on_ground["right"]) and not self.timers["wall climb"].active:
            if self.climb:
                self.hitbox_rect.y -= 30 * dt
                self.climb = False
            else:
                self.direction.y = 0
                self.hitbox_rect.y += self.gravity / 10 * dt * FPS_Fisica
        else:
            self.direction.y += self.gravity / 2 * dt
            self.hitbox_rect.y += self.direction.y * dt * FPS_Fisica
            self.direction.y += self.gravity / 2 * dt

        if self.jump:
            if self.on_ground["chao"]:
                self.direction.y = self.jump_height
                self.hitbox_rect.bottom -= 1
                self.timers["wall climb"].activate()
            elif (self.on_ground["right"] or self.on_ground["left"]) and not self.timers["wall climb"].active:
                self.timers["wall jump"].activate()
                self.direction.y = self.jump_height

        self.jump = False
        self.collision("vertical")
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center

    def respawn(self):
        x, y = self.spawn_pos
        self.hitbox_rect.x = x
        self.hitbox_rect.y = y

    def plataform_move(self, dt):
        if self.plataforma:
            self.hitbox_rect.topleft += self.plataforma.direcao * self.plataforma.vel * dt

    def check_contact(self):
        chao_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        left_rect = pygame.Rect((self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4)), (1, self.hitbox_rect.width / 2))
        right_rect = pygame.Rect((self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4)), (1, self.hitbox_rect.width / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rect = [sprite.rect for sprite in self.semi_collision_sprites]

        self.on_ground["chao"] = chao_rect.collidelist(collide_rects) >= 0 or (
                chao_rect.collidelist(semi_collide_rect) >= 0 and self.direction.y >= 0)
        self.on_ground["left"] = left_rect.collidelist(collide_rects) >= 0
        self.on_ground["right"] = right_rect.collidelist(collide_rects) >= 0

        self.plataforma = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, "moving")]:
            if sprite.rect.colliderect(chao_rect):
                self.plataforma = sprite

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == "horizontal":
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= sprite.old_rect.right:
                        self.hitbox_rect.left = sprite.rect.right
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= sprite.old_rect.left:
                        self.hitbox_rect.right = sprite.rect.left
                else:
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= sprite.old_rect.bottom:
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, "moving"):
                            self.hitbox_rect.top += 6
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def semi_collision(self):
        if not self.timers["plataforma fall"].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.plataform_move(dt)
        self.check_contact()
