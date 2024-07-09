from os.path import join
from sys import exit

import pygame
import time
from pytmx.util_pygame import load_pygame

from config import *
from nivel import Nivel


class Game:
    def __init__(self):
        pygame.init()

        # Criação da janela de jogo
        self.surface = pygame.display.set_mode((largura, altura), pygame.SCALED | pygame.HIDDEN)

        janela = pygame.Window.from_display_module()
        janela.size = (largura_janela, altura_janela)
        janela.position = pygame.WINDOWPOS_CENTERED
        janela.show()

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
            self.current_stage.run(dt)

            # Atualizar a tela
            print(f"fps: {pygame.time.Clock.get_fps(self.clock):.0f}")
            pygame.display.update()


if __name__ == '__main__':
    jogo = Game()
    jogo.run()
