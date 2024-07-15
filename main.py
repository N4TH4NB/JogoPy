import time
from os.path import join
from sys import exit
from pytmx.util_pygame import load_pygame
from config import *  # Importa todas as configurações do arquivo config
from nivel import Nivel  # Importa a classe Nivel

class Game:
    def __init__(self):
        pygame.init()  # Inicializa todos os módulos do Pygame

        # Criação da janela de jogo
        self.surface = pygame.display.set_mode((largura, altura), pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption(titulo)  # Define o título da janela do jogo
        self.clock = pygame.time.Clock()  # Cria um relógio para controlar a taxa de quadros

        self.num_nivel = 0  # Inicializa o nível atual

        # Carregar mapas
        self.tmx_maps = {
            0: load_pygame(join("tiled/Fase1.tmx")),
            1: load_pygame(join("tiled/Fase2.tmx")),
            2: load_pygame(join("tiled/Fase3.tmx"))
        }

        # Carregar imagens de fundo
        self.background_images = {
            0: pygame.image.load("tiled/png/trees.png"),
            1: pygame.image.load("tiled/png/mountains_a.png"),
            2: pygame.image.load("tiled/png/mountains_b.png")
        }

        # Escalonar as imagens de fundo para o tamanho da janela
        self.background_images = {i: pygame.transform.scale(j, (largura, altura)) for i, j in self.background_images.items()}

        # Definir cores de fundo para cada nível
        self.background_color = {
            0: "#76CED9",
            1: "#CAE4E7",
            2: "#3A1E3D"
        }

        # Configurar o primeiro estágio e o fundo
        self.current_stage = Nivel(self.tmx_maps[self.num_nivel], self.switch_stage)
        self.background = self.background_images[self.num_nivel]

        self.tempo = time.time()  # Inicializa o tempo

    def switch_stage(self, num_nivel):
        # Troca para o próximo estágio ou sai do jogo se o nível for 3
        if num_nivel == 3:
            exit()
        else:
            self.current_stage = Nivel(self.tmx_maps[num_nivel], self.switch_stage)
            self.background = self.background_images[num_nivel]

    def run(self):
        while True:
            # Limita os quadros por segundo (FPS)
            self.clock.tick(FPS)
            # Calcula o tempo delta (dt)
            dt = time.time() - self.tempo
            self.tempo = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Finaliza o Pygame
                    exit()  # Sai do programa

            # Desenhar o fundo apropriado
            self.surface.fill(self.background_color[self.num_nivel])  # Preenche a superfície com a cor de fundo
            self.surface.blit(self.background, (0, 0))  # Desenha a imagem de fundo
            self.current_stage.run(dt)  # Atualiza o estágio atual
            pygame.display.flip()  # Atualiza a tela

if __name__ == '__main__':
    jogo = Game()  # Cria uma instância do jogo
    jogo.run()  # Executa o método run do jogo
