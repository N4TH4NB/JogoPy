import time
from os.path import join
from sys import exit

from pytmx.util_pygame import load_pygame

from config import *
from nivel import Nivel


class Game:
    def __init__(self):
        pygame.init()

        # Criação da janela de jogo
        self.surface = pygame.display.set_mode((largura, altura), pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption(titulo)  # Título do jogo
        self.clock = pygame.time.Clock()

        self.num_nivel = 0
        # Carregar mapas
        self.tmx_maps = {
            1: load_pygame(join("tiled/Fase1.tmx")),
            0: load_pygame(join("tiled/Fase2.tmx")),
            2: load_pygame(join("tiled/Fase3.tmx"))
        }
        # Carregar imagens de fundo
        self.background_images = {
            1: pygame.image.load("tiled/png/trees.png"),
            0: pygame.image.load("tiled/png/mountains_a.png"),
            2: pygame.image.load("tiled/png/mountains_b.png")
        }
        # Escalar as imagens de fundo para o tamanho da janela
        self.background_images = {i: pygame.transform.scale(j, (largura, altura)) for i, j in
                                  self.background_images.items()}

        self.background_color = {
            0: "#76CED9",
            1: "#CAE4E7",
            2: "#3A1E3D"
        }

        # Configurar o primeiro estágio e o fundo
        self.current_stage = Nivel(self.tmx_maps[self.num_nivel], self.switch_stage)
        self.background = self.background_images[self.num_nivel]

        self.tempo = time.time()

    def switch_stage(self, num_nivel):
        self.current_stage = Nivel(self.tmx_maps[num_nivel], self.switch_stage)
        self.background = self.background_images[num_nivel]

    def run(self):
        while True:
            #self.clock.tick(FPS)
            dt = time.time() - self.tempo
            self.tempo = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Desenhar o fundo apropriado
            self.surface.fill(self.background_color[self.num_nivel])
            self.surface.blit(self.background, (0, 0))
            self.current_stage.run(dt)
            pygame.display.flip()


if __name__ == '__main__':
    jogo = Game()
    jogo.run()
