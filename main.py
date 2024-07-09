from config import *
from nivel import Nivel
import pygame
from sys import exit
from os.path import join
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        pygame.init()

        # Criação da janela de jogo
        self.surface = pygame.display.set_mode((largura, altura), pygame.DOUBLEBUF | pygame.SCALED)

        pygame.display.set_caption(titulo)  # Título do jogo
        self.clock = pygame.time.Clock()

        self.num_nivel = 0
        # Carregar mapas
        self.tmx_maps = {
            0: load_pygame(join("tiled\\TiledLava.tmx")),
            1: load_pygame(join("tiled\\TiledForest.tmx")),
            2: load_pygame(join("tiled\\TiledSnow.tmx"))

        }
        self.current_stage = Nivel(self.tmx_maps[self.num_nivel], self.switch_stage)

    def switch_stage(self, num_nivel):
        #  print(num_nivel)
        self.current_stage = Nivel(self.tmx_maps[num_nivel], self.switch_stage)

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Executar lógica do nível
            self.current_stage.run(dt)

            # Atualizar a tela
            print(f"fps: {pygame.time.Clock.get_fps(self.clock):.0f}")
            pygame.display.update()


if __name__ == '__main__':
    jogo = Game()
    jogo.run()
