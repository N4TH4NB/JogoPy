from config import *
from timer import Timer
import pygame


class Jogador(pygame.sprite.Sprite):
    def __init__(self, image, pos, groups, collision_sprites, semi_collision_sprites, right_key, left_key, down_key,
                 jump_key):
        super().__init__(groups)
        self.original_image = image
        self.image = image
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(0, 0)
        self.old_rect = self.hitbox_rect.copy()
        self.direction = vector()
        self.speed = 150
        self.gravity = 20
        self.jump = False
        self.climb = False
        self.jump_height = -4.5
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_ground = {"chao": False, "left": False, "right": False}
        self.plataforma = None
        self.timers = {
            "wall jump": Timer(15),
            "wall climb": Timer(100),
            "plataforma fall": Timer(250)
        }
        self.right_key = right_key
        self.left_key = left_key
        self.down_key = down_key
        self.jump_key = jump_key

    def input(self):
        keys = pygame.key.get_pressed()
        key = pygame.key.get_just_pressed()
        input_vector = vector(0, 0)
        if not self.timers["wall jump"].active:
            if keys[self.right_key]:
                input_vector.x += 1
                self.image = self.original_image
            if keys[self.left_key]:
                input_vector.x -= 1
                self.image = pygame.transform.flip(self.original_image, True, False)
            if keys[self.down_key]:
                self.timers["plataforma fall"].activate()
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if key[self.jump_key]:
            self.jump = True
        if keys[self.jump_key]:
            self.climb = True

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")

        if not self.on_ground["chao"] and (self.on_ground["left"] or self.on_ground["right"]) and not self.timers[
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
        self.hitbox_rect.x = 100
        self.hitbox_rect.y = 50

    def plataform_move(self, dt):
        if self.plataforma:
            self.hitbox_rect.topleft += self.plataforma.direcao * self.plataforma.Vel * dt

    def check_contact(self):
        chao_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        left_rect = pygame.Rect((self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4)),
                                (1, self.hitbox_rect.width / 2))
        right_rect = pygame.Rect((self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4)),
                                 (1, self.hitbox_rect.width / 2))
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
