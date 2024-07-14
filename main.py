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
        self.background = pygame.image.load("tiled\\png\\mountains_b.png")
        self.background = pygame.transform.scale(self.background, (largura, altura))

        self.num_nivel = 0
        # Carregar mapas
        self.tmx_maps = {
            0: load_pygame(join("tiled\\TiledLava.tmx")),
            1: load_pygame(join("tiled\\TiledForest.tmx")),
            2: load_pygame(join("tiled\\TiledSnow.tmx"))

        }
        self.current_stage = Nivel(self.tmx_maps[self.num_nivel], self.switch_stage)

        self.tempo = time.time()

    def switch_stage(self, num_nivel):
        #  print(num_nivel)
        self.current_stage = Nivel(self.tmx_maps[num_nivel], self.switch_stage)

    def run(self):
        while True:
            self.clock.tick(FPS)
            dt = time.time() - self.tempo
            self.tempo = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Executar lógica do nível
            self.surface.fill("#3a1e3d")
            self.surface.blit(self.background, (0, 0))
            self.current_stage.run(dt)

            # Atualizar a tela
            # print(f"fps: {pygame.time.Clock.get_fps(self.clock):.0f}")
            pygame.display.flip()

if __name__ == '__main__':
    jogo = Game()
    jogo.run()
