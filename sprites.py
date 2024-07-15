from config import *  # Importa todas as configurações do arquivo config


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image=pygame.Surface((tamanho_bloco, tamanho_bloco)), groups=None):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()


class PlataformaMovel(Sprite):
    def __init__(self, groups, pos_inicial, pos_final, direcao_movi, vel, image):
        super().__init__(pos_inicial, image, groups)
        self.rect.center = pos_inicial
        self.pos_inicial = pos_inicial
        self.pos_final = pos_final
        self.vel = vel

        # Define a direção do movimento com base na direção fornecida
        self.moving = True
        self.direcao = vector(1, 0) if direcao_movi == "x" else vector(0, 1)
        self.direcao_movi = direcao_movi

    def check_borda(self):
        # Verifica se a plataforma móvel atingiu as bordas e inverte a direção se necessário
        if self.direcao_movi == "x":
            if self.rect.right >= self.pos_final[0] and self.direcao.x == 1:
                self.direcao.x = -1
                self.rect.right = self.pos_final[0]
            if self.rect.right <= self.pos_inicial[0] and self.direcao.x == -1:
                self.direcao.x = 1
                self.rect.right = self.pos_inicial[0]

        if self.direcao_movi == "y":
            if self.rect.top >= self.pos_final[1] and self.direcao.y == 1:
                self.direcao.y = -1
                self.rect.top = self.pos_final[1]
            if self.rect.top <= self.pos_inicial[1] and self.direcao.y == -1:
                self.direcao.y = 1
                self.rect.top = self.pos_inicial[1]

    def update(self, dt):
        self.old_rect = self.rect.copy()
        # Atualiza a posição da plataforma móvel com base na direção e velocidade
        self.rect.topleft += self.direcao * self.vel * dt
        self.check_borda()


class Dano(Sprite):
    def __init__(self, groups, pos_inicial, pos_final, direcao_movi, vel, image, tipo_dano):
        super().__init__(pos_inicial, image, groups)
        self.rect.center = pos_inicial
        self.pos_inicial = pos_inicial
        self.pos_final = pos_final
        self.vel = vel
        self.tipo_dano = tipo_dano

        # Define a direção do movimento com base na direção fornecida
        self.direcao = vector(1, 0) if direcao_movi == "x" else vector(0, 1)
        self.direcao_movi = direcao_movi

    def check_borda(self):
        if self.direcao_movi == "x":
            if self.tipo_dano == "danoreset":
                if self.rect.right >= self.pos_final[0] and self.direcao.x == 1:
                    self.rect.right = self.pos_inicial[0]
                elif self.rect.right <= self.pos_inicial[0] and self.direcao.x == -1:
                    self.rect.right = self.pos_inicial[0]

            elif self.tipo_dano == "danocontinuo":
                if self.rect.right >= self.pos_final[0] and self.direcao.x == 1:
                    self.direcao.x = -1
                    self.rect.right = self.pos_final[0]
                    self.image = pygame.transform.flip(self.image, True, False)
                elif self.rect.right <= self.pos_inicial[0] and self.direcao.x == -1:
                    self.direcao.x = 1
                    self.rect.right = self.pos_inicial[0]
                    self.image = pygame.transform.flip(self.image, True, False)

        elif self.direcao_movi == "y" or "-y":
            if self.tipo_dano == "danocontinuo":
                if self.rect.top >= self.pos_final[1] and self.direcao.y == 1:
                    self.direcao.y = -1
                    self.rect.top = self.pos_final[1]
                elif self.rect.top <= self.pos_inicial[1] and self.direcao.y == -1:
                    self.direcao.y = 1
                    self.rect.top = self.pos_inicial[1]

            if not self.direcao_movi == "y":
                self.direcao.y = -1

            if self.tipo_dano == "danoreset":
                if self.rect.top >= self.pos_final[1] and self.direcao.y == 1:
                    self.rect.top = self.pos_inicial[1]
                elif self.rect.top <= self.pos_final[1] and self.direcao.y == -1:
                    self.rect.top = self.pos_inicial[1]

    def update(self, dt):
        self.old_rect = self.rect.copy()
        # Atualiza a posição do dano móvel com base na direção e velocidade
        self.rect.topleft += self.direcao * self.vel * dt
        self.check_borda()
