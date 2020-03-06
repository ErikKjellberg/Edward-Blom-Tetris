import pygame
import pygame.freetype

def create_text(font_type, font_size, text_string, color=(0,0,0)):
    if "." in font_type:
        font = pygame.freetype.Font("C:\\Users\\erikkg\\Documents\\Dokument\\Python\\Frograce\\"+font_type,font_size)
        text = font.render(text_string,fgcolor=color)[0]
    else:
        font = pygame.font.SysFont(font_type,font_size)
        text = font.render(text_string,True,color)
    return text

def display_text(text,screen,width,height,x=0,y=0):
    if x == 0:
        x = width/2-text.get_width()/2
    elif x == -1:
        x = width-text.get_width()-20
    if y == 0:
        y = height/2-text.get_width()/2
    elif y == -1:
        y = height-text.get_height()-20
    screen.blit(text,(x,y))