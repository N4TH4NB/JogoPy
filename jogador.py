from config import *
from timer import Timer
from os.path import join


class Jogador(pygame.sprite.Sprite):
    def __init__(self, image, pos, groups, collision_sprites, semi_collision_sprites, right_key, left_key, down_key,
                 jump_key, outro_jogador=None):
        super().__init__(groups)
        self.image = image #image
        # self.image = pygame.Surface((8, 8))  #16,16
        #  self.image.fill("pink")
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(0, 0)
        self.old_rect = self.hitbox_rect.copy()
        self.direction = vector()
        self.speed = 150
        self.gravity = 20
        self.doublejump_check = False
        self.doublejump = 1
        self.jump = False
        self.climb = False
        # self.on_ground = False
        self.void = False
        self.jump_height = -4.5  # -15
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_ground = {"chao": False, "left": False, "right": False, "obstaculos": False}
        self.plataforma = None
        print(self.collision_sprites)
        self.timers = {"wall jump": Timer(15), "wall climb": Timer(100), "plataforma fall": Timer(250)}
        self.right_key = right_key
        self.left_key = left_key
        self.down_key = down_key
        self.jump_key = jump_key
        self.outro_jogador = outro_jogador

    def input(self):
        keys = pygame.key.get_pressed()
        key = pygame.key.get_just_pressed()
        input_vector = vector(0, 0)
        if not self.timers["wall jump"].active:
            # Direita
            if keys[self.right_key]:
                input_vector.x += 1
            # Esquerda
            if keys[self.left_key]:
                input_vector.x -= 1
            if keys[self.down_key]:
                self.timers["plataforma fall"].activate()

            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        # Pular
        if key[self.jump_key]:
            self.jump = True

        # Escalar
        if keys[self.jump_key]:
            self.climb = True

            #  self.direction.y = -5
        #  print("cima")

    def move(self, dt):  # data time
        #   self.rect.topleft += self.direction * self.speed * dt
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")

        if not self.on_ground["chao"] and any((self.on_ground["left"], self.on_ground["right"])) and not self.timers[
            "wall climb"].active:
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
                self.doublejump += 3

                self.direction.y = self.jump_height
                self.hitbox_rect.bottom -= 1
                self.timers["wall climb"].activate()

            elif any((self.on_ground["right"], self.on_ground["left"])) and not self.timers["wall climb"].active:
                self.doublejump += 3
                self.timers["wall jump"].activate()
                self.direction.y = self.jump_height
                self.direction.x = 1 if self.on_ground["left"] else -1

            # self.direction.x = 1 if self.on_ground["left"] or self.on_ground["right"] else -1

            #    self.doublejump = 17

        self.jump = False
        self.collision("vertical")
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center
        # print(self.direction.y)

    def die(self):
        if self.hitbox_rect.x > 1000 or self.hitbox_rect.y > 1000 or self.hitbox_rect.x < -5:
            self.respawn()
            self.outro_jogador.respawn()

    def respawn(self):
        self.hitbox_rect.x = 100  # 445
        self.hitbox_rect.y = 50

    def pressed_botao(self):
        if self.pressed_botao():
            pass

    def plataform_move(self, dt):
        if self.plataforma:
            if self.plataforma.Vel == 35:
                if self.plataforma.direcao == [0, 1]:
                    pass
                # self.hitbox_rect.topleft += self.plataforma.direcao * self.plataforma.Vel * dt
                else:
                    self.hitbox_rect.topleft += self.plataforma.direcao * self.plataforma.Vel * dt

                # print(self.plataforma.direcao)
            else:

                self.hitbox_rect.topleft += self.plataforma.direcao * self.plataforma.Vel * dt

    def check_contact(self):
        chao_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))  # w,h
        left_rect = pygame.Rect((self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4)),
                                (1, self.hitbox_rect.width / 2))
        right_rect = pygame.Rect((self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4)),
                                 (1, self.hitbox_rect.width / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rect = [sprite.rect for sprite in self.semi_collision_sprites]

        self.on_ground["chao"] = True if chao_rect.collidelist(collide_rects) >= 0 or chao_rect.collidelist(
            semi_collide_rect) >= 0 and self.direction.y >= 0 else False
        self.on_ground["left"] = True if left_rect.collidelist(collide_rects) >= 0 else False
        self.on_ground["right"] = True if right_rect.collidelist(collide_rects) >= 0 else False

        self.plataforma = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, "moving")]:
            if sprite.rect.colliderect(chao_rect):
                self.plataforma = sprite
        self.pressed_botao = None
        for sprite in [sprite for sprite in sprites if hasattr(sprite, "pressed_botao")]:
            if sprite.rect.colliderect(chao_rect):
                self.pressed_botao = sprite

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == "horizontal":
                    if self.hitbox_rect.left <= sprite.rect.right and int(
                            self.old_rect.left) >= sprite.old_rect.right:  # 1. conferir se o lado esquerdo do player ta colidindo com o lado direito de algum objeto; 2. Confere a última posição do player
                        self.hitbox_rect.left = sprite.rect.right
                    if self.hitbox_rect.right >= sprite.rect.left and int(
                            self.old_rect.right) <= sprite.old_rect.left:  # conferir se o lado direito do player ta colidindo com o lado esquerdo de algum objeto
                        self.hitbox_rect.right = sprite.rect.left
                else:  # if axis == "vertical":
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= sprite.old_rect.bottom:
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, "moving"):
                            self.hitbox_rect.top += 6
                        #  pass
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0
                # else:

                #   pass

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
        self.die()
    #   print(self.timers["wall climb"].active)

    #   print(self.doublejump)
