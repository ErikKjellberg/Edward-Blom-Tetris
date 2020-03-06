import pygame
import pygame.freetype
import math
import random
import time
import displaytext as d
import createimage as c

pi = math.pi
sin = math.sin
cos = math.cos
atan = math.atan

pygame.init()
width,height = 500,500
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
fps = 120
fps = 60



class Piece:
    def __init__(self,piecetype,isnext,speed):
        self.type = piecetype
        self.color = (random.randrange(100,255),random.randrange(100,255),random.randrange(100,255))
        # self.images = ["cyanblock.png","yellowblock.png","blueblock.png","orangeblock.png","greenblock.png","purpleblock.png","redblock.png"]
        # self.images = ["naan.png","naan.png","naan.png","naan.png","naan.png","naan.png","naan.png"]
        self.images = ["cyaned.png","yellowed.png","blueed.png","orangeed.png","greened.png","purpleed.png","reded.png"]
        self.image = c.create_image(self.images[self.type])
        self.angle = 0
        xy_list = [[4,0],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1]]
        self.x, self.y = xy_list[self.type][0],xy_list[self.type][1]
        self.start_x = self.x
        self.start_y = self.y
        self.is_next = isnext
        if self.is_next:
            self.x = 12
            self.y = 10
        i_piece = [[[self.x,self.y+2],[self.x+1,self.y+2],[self.x+2,self.y+2],[self.x+3,self.y+2]],\
            [[self.x+2,self.y],[self.x+2,self.y+1],[self.x+2,self.y+2],[self.x+2,self.y+3]]]
        o_piece = [[[self.x+1,self.y+1],[self.x+2,self.y+1],[self.x+1,self.y+2],[self.x+2,self.y+2]]]
        j_piece = [[[self.x,self.y+1],[self.x+1,self.y+1],[self.x+2,self.y+1],[self.x+2,self.y+2]],\
            [[self.x+1,self.y],[self.x+1,self.y+1],[self.x+1,self.y+2],[self.x,self.y+2]],\
            [[self.x,self.y],[self.x,self.y+1],[self.x+1,self.y+1],[self.x+2,self.y+1]],\
            [[self.x+1,self.y],[self.x+2,self.y],[self.x+1,self.y+1],[self.x+1,self.y+2]]]
        l_piece = [[[self.x,self.y+1],[self.x+1,self.y+1],[self.x+2,self.y+1],[self.x,self.y+2]],\
            [[self.x,self.y],[self.x+1,self.y],[self.x+1,self.y+1],[self.x+1,self.y+2]],\
            [[self.x+2,self.y],[self.x,self.y+1],[self.x+1,self.y+1],[self.x+2,self.y+1]],\
            [[self.x+1,self.y],[self.x+1,self.y+1],[self.x+1,self.y+2],[self.x+2,self.y+2]]]
        s_piece = [[[self.x+1,self.y+1],[self.x+2,self.y+1],[self.x,self.y+2],[self.x+1,self.y+2]],\
            [[self.x+1,self.y],[self.x+1,self.y+1],[self.x+2,self.y+1],[self.x+2,self.y+2]]]
        t_piece = [[[self.x,self.y+1],[self.x+1,self.y+1],[self.x+2,self.y+1],[self.x+1,self.y+2]],\
            [[self.x+1,self.y],[self.x,self.y+1],[self.x+1,self.y+1],[self.x+1,self.y+2]],\
            [[self.x+1,self.y],[self.x,self.y+1],[self.x+1,self.y+1],[self.x+2,self.y+1]],\
            [[self.x+1,self.y+2],[self.x+1,self.y+1],[self.x+2,self.y+1],[self.x+1,self.y]]]
        z_piece = [[[self.x,self.y+1],[self.x+1,self.y+1],[self.x+1,self.y+2],[self.x+2,self.y+2]],\
            [[self.x+2,self.y],[self.x+1,self.y+1],[self.x+2,self.y+1],[self.x+1,self.y+2]]]
        piece_list = [i_piece,o_piece,j_piece,l_piece,s_piece,t_piece,z_piece]
        self.rotation = 0
        self.pieces = piece_list[self.type]
        self.current_rotation = self.pieces[self.rotation]
        color_list = [(50,50,255),(255,50,50),(255,170,50),(50,255,255),(50,255,50),(255,255,50),(255,50,255)]
        self.color = color_list[self.type]
        self.normal_speed = speed
        self.speed = self.normal_speed
        self.turbo_speed = 3
        self.initial_time_to_press = 16
        self.latter_time_to_press = 6
        self.time_to_press = self.initial_time_to_press
        self.time = self.initial_time_to_press
        self.holding = False
        self.time_to_rotate = 10
        self.rotate_time = 10

    def rotate(self,direction):
        if direction == -1:
            self.rotation -= 1
        elif direction == 1:
            self.rotation += 1
        self.rotation = self.rotation % len(self.pieces)
        self.current_rotation = self.pieces[self.rotation]

    def update(self,time,board):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_LEFT]:
            if pressed[pygame.K_RIGHT]: direction = 1
            if pressed[pygame.K_LEFT]: direction = -1
            stop = False
            for i in range(len(board.block_list)):
                for j in range(len(board.block_list[i])):
                    for block in self.pieces[self.rotation]:
                        if (block[0] + 1 == i and block[1] == j and direction == 1 or \
                            block[0] - 1 == i and block[1] == j and direction == -1 ) and board.block_list[i][j] != None:
                            stop = True
                        if block[0] == board.width-1 and direction == 1 or block[0] == 0 and direction == -1:
                            stop = True
            if not stop and self.time == self.time_to_press:
                """if self.time_to_press == self.initial_time_to_press:
                    self.holding = True
                    self.time_to_press = self.latter_time_to_press"""
                self.time = 0
                self.time_to_press = self.latter_time_to_press
                for piece in self.pieces:
                    for block in piece:
                        block[0] += direction
        else:
            self.time = self.time_to_press
            self.time_to_press = self.initial_time_to_press
        if pressed[pygame.K_DOWN]:
            self.speed = self.turbo_speed
        else:
            self.speed = self.normal_speed
        if pressed[pygame.K_z] or pressed[pygame.K_UP]:
            if self.rotate_time == self.time_to_rotate:
                self.rotate(1)
                for block in self.current_rotation:
                    if block[0] < 0 or block[0] >= board.width:
                        self.rotate(-1)
                        break
                    for i in range(len(board.block_list)):
                        for j in range(len(board.block_list[i])):
                            if block[0] == i and block[1] == j and board.block_list[i][j] != None:
                                self.rotate(-1)
                                break
                self.rotate_time = 0
        if pressed[pygame.K_x]:
            if self.rotate_time == self.time_to_rotate:
                self.rotate(-1)
                for block in self.current_rotation:
                    if block[0] < 0 or block[0] >= board.width:
                        self.rotate(1)
                        break
                    for i in range(len(board.block_list)):
                        for j in range(len(board.block_list[i])):
                            if block[0] == i and block[1] == j and board.block_list[i][j] != None:
                                self.rotate(1)
                                break
                self.rotate_time = 0
        """if time%self.speed==0 and time!=0:
            for piece in self.pieces:
                for block in piece:
                    block[1] += 1"""
        if self.time < self.time_to_press:
            self.time += 1
        if self.rotate_time < 10:
            self.rotate_time += 1


class Board:
    def __init__(self):
        self.width = 10
        self.height = 22
        self.invisible_rows = 2
        self.cell_width = 20
        self.cell_height = 20
        self.board_width = self.width*self.cell_width
        self.board_height = self.height*self.cell_height
        self.x = width/2-self.width*self.cell_width/2
        self.y = height/2-(self.height-self.invisible_rows)*self.cell_height/2
        self.block_list = []
        for i in range(self.width):
            self.block_list.append([])
            for j in range(self.height):
                self.block_list[i].append(None)
        self.bg_color = (25,25,25)
        # self.bg_image = c.create_image("edward_bg.png",self.board_width,self.board_height)
        self.bg_image = c.create_image("edward_bg.png", width, height)
        self.next_text = d.create_text("courier",20,"NEXT",color=(255,255,255))

    def to_real_coord(self,coord):
        return [self.x+coord[0]*self.cell_width,self.y+coord[1]*self.cell_height]

    def clear_line(self,n):
        for i in range(len(self.block_list)):
            self.block_list[i][n] = None
            for j in range(n-1,0,-1):
                self.block_list[i][j+1] = self.block_list[i][j]
                self.block_list[i][j] = None

    def draw(self,game_manager):
        # screen.blit(self.bg_image,(self.x,self.y))
        screen.blit(self.bg_image, (0, 0))
        surface = pygame.Surface((self.board_width,self.board_height-self.cell_height))
        surface.set_alpha(200)
        surface.fill(self.bg_color)
        screen.blit(surface,(self.x,self.y+self.cell_height))
        # pygame.draw.rect(screen,self.bg_color,(self.x,self.y+self.cell_height*2,self.board_width,self.board_height-self.cell_height*2))
        pygame.draw.rect(screen,self.bg_color,(self.to_real_coord([11,9])[0],self.to_real_coord([11,9])[1],5*self.cell_width,5*self.cell_height))
        screen.blit(self.next_text,(self.to_real_coord([11,9])[0]+5/2*self.cell_width-self.next_text.get_width()/2,self.to_real_coord([11,9])[1]+2))
        lines_text = d.create_text("courier",20,("LINES: "+str(game_manager.lines)),color=(255,255,255))
        screen.blit(lines_text,(self.x+self.board_width/2-lines_text.get_width()/2,self.y-2-lines_text.get_height()))
        screen.blit(lines_text,(self.x+self.board_width+self.cell_width,self.y+self.cell_height*2))
        level_text = d.create_text("courier",20,("LEVEL: "+str(game_manager.level)),color=(255,255,255))
        screen.blit(level_text,(self.x+self.board_width+self.cell_width,self.y+self.cell_height*4))
        score_text = d.create_text("courier",20,("SCORE: "+str(game_manager.score)),color=(255,255,255))
        screen.blit(score_text,(self.x+self.board_width+self.cell_width,self.y+self.cell_height*3))
        """for i in range(0,self.width+1):
            pygame.draw.line(screen,(150,150,150),(self.x+self.cell_width*i,self.y),(self.x+self.cell_width*i,self.y+self.board_height),1)
        for i in range(0,self.height+1):
            pygame.draw.line(screen,(150,150,150),(self.x,self.y+self.cell_height*i),(self.x+self.board_width,self.y+self.cell_height*i),1)"""

    def draw_blocks(self,game_manager):
        for block in game_manager.current_piece.current_rotation:
            #pygame.draw.rect(screen,game_manager.current_piece.color,(self.to_real_coord(block)[0],self.to_real_coord(block)[1],self.cell_width,self.cell_height))
            screen.blit(game_manager.current_piece.image,(self.to_real_coord(block)[0],self.to_real_coord(block)[1]))
        for block in game_manager.next_piece.current_rotation:
            #pygame.draw.rect(screen,game_manager.next_piece.color,(self.to_real_coord(block)[0],self.to_real_coord(block)[1],self.cell_width,self.cell_height))
            screen.blit(game_manager.next_piece.image,(self.to_real_coord(block)[0],self.to_real_coord(block)[1]))
        for i in range(len(self.block_list)):
            for j in range(len(self.block_list[i])):
                if self.block_list[i][j] != None:
                    #pygame.draw.rect(screen,self.block_list[i][j],(self.to_real_coord([i,j])[0],self.to_real_coord([i,j])[1],self.cell_width,self.cell_height))
                    screen.blit(self.block_list[i][j],(self.to_real_coord([i,j])[0],self.to_real_coord([i,j])[1]))
        # pygame.draw.rect(screen,(0,0,0),(self.x,self.y,self.board_width,self.cell_height*self.invisible_rows))


class GameManager:
    def __init__(self,level):
        self.time = 0
        self.score = 0
        self.lines = 0
        self.level = level
        # self.speed_list = [48,43,38,33,28,23,18,13,8,6,5,5,5,4,4,4,3,3,3,2,2,2,2,2,2,2,2,2,2,1]
        self.speed_list = [48,43,38,33,28,23,18,13,8,6,5,5,5,4,4,4,3,3,3,2,2,2,2,2,2,2,2,2,2,1]
        self.points_list = [0,40,100,300,1200]
        self.current_piece = Piece(random.randrange(0,7),False,self.speed_list[self.level])
        self.next_piece = Piece(random.randrange(0,7),True,self.speed_list[self.level])

    def check_line_clear(self,board,y_min,y_max):
        temp = self.lines
        for k in range(y_min,y_max+1):
            clear = True
            for l in range(0,board.width):
                if board.block_list[l][k] == None:
                    clear = False
            if clear:
                board.clear_line(k)
                self.lines += 1
                if self.lines % 10 == 0:
                    self.level += 1
        self.score += self.points_list[self.lines-temp]*(self.level+1)

    def update(self,board):
        self.current_piece.update(self.time,board)
        if self.time%self.current_piece.speed==0 and self.time!=0:
            stop = False
            for block in self.current_piece.current_rotation:
                if block[1]==board.height-1:
                    stop = True
                elif board.block_list[block[0]][block[1]+1] != None:
                    stop = True
            if not stop:
                for piece in self.current_piece.pieces:
                    for block in piece:
                        block[1] += 1
        for block in self.current_piece.current_rotation:
            for i in range(len(board.block_list)):
                for j in range(len(board.block_list[i])):
                    if board.block_list[i][j] != None and block[0]==i and block[1]==j-1 and (self.time%self.current_piece.speed>=20 or self.time%self.current_piece.speed >= self.current_piece.speed/2):
                        y_min = 21
                        y_max = 0
                        for block in self.current_piece.current_rotation:
                            board.block_list[block[0]][block[1]] = self.current_piece.image
                            if block[1] < y_min:
                                y_min = block[1]
                            if block[1] > y_max:
                                y_max = block[1]
                        self.check_line_clear(board,y_min,y_max)
                        self.current_piece = Piece(self.next_piece.type,False,self.speed_list[self.level])
                        self.next_piece = Piece(random.randrange(0,7),True,self.speed_list[self.level])
                        self.time = 0
            if block[1] == board.height-1 and (self.time%self.current_piece.speed>=20 or self.time%self.current_piece.speed >= self.current_piece.speed/2):
                for block in self.current_piece.current_rotation:
                    board.block_list[block[0]][block[1]] = self.current_piece.image
                self.check_line_clear(board,board.height-4,board.height-1)
                self.current_piece = Piece(self.next_piece.type,False,self.speed_list[self.level])
                self.next_piece = Piece(random.randrange(0,7),True,self.speed_list[self.level])
                self.time = 0
        board.draw(self)
        board.draw_blocks(self)
        self.time += 1

def title_screen():
    while True:
        screen.fill((0,0,0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

def game():
    board = Board()
    game_manager = GameManager(0)
    while True:
        screen.fill((0,0,0))
        game_manager.update(board)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()
        clock.tick(fps)

game()
