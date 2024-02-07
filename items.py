import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, pos, name, file = None):
        super(Item, self).__init__()
        if file:
            self.image = pygame.transform.scale(pygame.image.load(file).convert_alpha(), (50, 50))
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill(name)
        self.rect = self.image.get_rect(center = pos)

        self.selected = False
        self.moving = False
        self.name = name
        self.start = False
        self.diffx = 0
        self.diffy = 0

    def is_following(self):
        x, y = pygame.mouse.get_pos()
        if self.moving and not self.start:
            self.start = True
            self.diffx = x - self.rect.centerx
            self.diffy = y - self.rect.centery

        if self.moving:
            self.rect.center = (x - self.diffx, y - self.diffy)
        else:
            self.start = False

    def is_selected(self):
        # if self.selected:
        #     self.image.fill("grey")
        # else:
        #     self.image.fill(self.name)
        pass

    def update(self):
        self.is_following()
        self.is_selected()
