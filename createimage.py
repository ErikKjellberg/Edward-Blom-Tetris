import pygame

def create_image(image, x=0, y=0):
    if x>0 and y>0:
        finished_image = pygame.transform.scale(pygame.image.load("C:\\Users\\erikkg\\Documents\\Dokument\\Python\\Tetris\\"+image).convert_alpha(),(x,y))
    else:
        finished_image = pygame.image.load("C:\\Users\\erikkg\\Documents\\Dokument\\Python\\Tetris\\"+image).convert_alpha()
    return finished_image