from config import *
from nivel import Nivel
import pygame
from sys import exit
from os.path import join
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        pygame.init()

        self.largura_upscale = largura * escala
        self.altura_upscale = altura * escala

        # Criação da janela de jogo
        self.surface = pygame.display.set_mode((largura, altura))
        #self.surface = pygame.transform.scale_by(pygame.display.set_mode((largura, altura)),10)
        #self.surface = pygame.transform.scale_by(self.surface, 10)
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

            # Ampliar a superfície do jogo
            scaled_surface = pygame.transform.scale(self.surface, (self.largura_upscale, self.altura_upscale))
            #scaled_surface = pygame.transform.scale2x(self.surface)

            # Desenhar a superfície ampliada na tela
            self.surface.blit(scaled_surface, (-largura, -altura))
            # escala 2: (-(largura/2), -(altura/2))
            # escala 3: (-largura, -altura)
            # escala 4: (-largura*1.5, -altura*1.5)

            # Atualizar a tela
            print(f"fps: {pygame.time.Clock.get_fps(self.clock):.0f}")
            pygame.display.update()


if __name__ == '__main__':
    jogo = Game()
    jogo.run()
