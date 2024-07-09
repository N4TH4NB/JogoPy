from config import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - largura / 2)
        self.offset.y = -(target_pos[1] - altura / 2)
        for sprite in self:
            offset_pos = sprite.rect.topleft + self.offset

            #self.display_surface.blit(pygame.transform.scale_by(sprite.image, 3), offset_pos)
            self.display_surface.blit(sprite.image, offset_pos)
