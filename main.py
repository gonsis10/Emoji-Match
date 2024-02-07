import pygame
import os
import random
from items import Item
pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("match")
clock = pygame.time.Clock()
current_item = None

"""Sorting"""
RULES = {frozenset(["stopwatch", "bomb"]): "collision",
         frozenset(['collision', 'pile-of-poo']): "radioactive",
         frozenset(['radioactive', 'electric-plug']): "cityscape-at-dusk"
         }

directory = "images"
IMAGES = {}

for file_name in os.listdir(directory):
    file = os.path.join(directory, file_name)
    file_short = file_name.split("_")[0]
    if os.path.isfile(file):
        IMAGES[file_short] = file

""""""""""""

""""Random Generator"""
items_group = pygame.sprite.LayeredUpdates()


def make_item(amount):
    global items_group
    item_x = random.sample(range(50, WIDTH - 50), amount)
    item_y = random.sample(range(50, HEIGHT - 50), amount)
    for i, item_name in enumerate(random.sample(list(IMAGES.keys()), amount)):
        items_group.add(Item((item_x[i], item_y[i]), item_name, IMAGES[item_name]))


make_item(random.randint(4, 6))
""""""""""""

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in items_group:
                if item.rect.collidepoint(event.pos):
                    items_group.move_to_front(item)
                    current_item = item
                    item.moving = True
                    print(f"{item.name}: true")
                    break
            print("down")
        if event.type == pygame.MOUSEBUTTONUP:
            if current_item:
                current_item.moving = False
                for item in items_group:
                    if item == current_item:
                        continue
                    else:
                        if current_item.rect.colliderect(item.rect):
                            x = (current_item.rect.centerx + item.rect.centerx)/2
                            y = (current_item.rect.centery + item.rect.centery)/2
                            combination = frozenset([current_item.name, item.name])
                            if combination in RULES:
                                name = RULES[combination]
                                items_group.add(Item((x, y), name, IMAGES[name]))
                            else:
                                make_item(3)
                            current_item.kill()
                            item.kill()
                            break
                current_item = None

            print("up")

    # for item in items_group:
    #     if item == current_item:
    #         continue
    #     elif current_item:
    #         if current_item.rect.colliderect(item.rect):
    #             item.selected = True
    #             # print("collided")
    #         else:
    #             item.selected = False
    #     else:
    #         item.selected = False

    screen.fill("white")
    items_group.draw(screen)
    items_group.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
