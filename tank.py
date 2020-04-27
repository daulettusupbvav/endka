#pylint: disable=no-member

import pygame
import random
from pathlib import Path
import os
import math
from pygame import mixer
from os import path

speed = 4
bulletspeed = 9

white = (255,255,255)
black = (0,0,0)
grey = (192,192,192)
red = (200,0,0)
light_red = (255,0,0)
med_red = (255, 153, 51)
green = (34,177,76)
light_green = (0,255,0)
med_green = (47, 116,127)
yellow = (200,200,0)
light_yellow = (255,255,0)

pygame.init()
screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Tanks')
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)
pygame.mixer.music.load(path.join('back.mp3'))
over = mixer.Sound("gameover.wav")
shoot = mixer.Sound("shoot.wav")
hate = mixer.Sound("hit.wav")
playsound = mixer.Sound("play.wav")
def button(text,x,y,width,height,inactive_color,active_color,action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < cur[0] < x + width and y < cur[1] < y + height:
        pygame.draw.rect(screen,active_color,(x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "play":               
                playsound.play()
                gameloop()
            if action == "controls":
                game_controls()
            if action == "quit":
                pygame.quit()
                quit()
            
    else:
        pygame.draw.rect(screen,inactive_color,(x,y,width,height))
    text_to_button(text,black,x,y,width,height)

def text_to_button(msg,color,buttonx,buttony,buttonwidth,buttonheight, size="small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+int(buttonwidth/2)),buttony+int(buttonheight/2))
    screen.blit(textSurf,textRect)

def text_objects(text,color,size="small"):
    if size == 'small':
        textSurface = smallfont.render(text, 1, color)
    if size == "medium":
        textSurface = medfont.render(text, 1, color)
    if size == "large":
        textSurface = largefont.render(text, 1, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size="small"):
    textSurf,textRect = text_objects(msg,color,size)
    textRect.center = (int(screenwidth/2),int(screenheight/2)+y_displace)
    screen.blit(textSurf, textRect)

def game_controls():
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(white)
        message_to_screen("Controls",med_green,-100,size="large")
        message_to_screen("Move Player1: Up,Down,Right and Left arrows",black,-30)
        message_to_screen("Fire: Spacebar",black,10)
        message_to_screen("Move Player2: W,S,D ana A keyboard keys",black,50)
        message_to_screen("Fire: Enter",black,90)
        message_to_screen("Pause: P",black,130)
        
        button("play",150,500,100,50,green,light_green,action="play")
        button("quit",550,500,100,50,red,light_red,action="quit")

        pygame.display.flip()
        clock.tick(15)

def game_intro():
    intro = True
    
    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro = False
        screen.fill(white)
        message_to_screen("Welcome to Tanks!",med_red,-100,size="large")
        button("play",150,370,100,50,green,light_green,action="play")
        button("controls",350,370,100,50,yellow,light_yellow,action="controls")
        button("quit",550,370,100,50,red,light_red,action="quit")
        pygame.display.flip()
        clock.tick(FPS)
   
def intersect(colbox1,colbox2):
    return(colbox2[0] <= colbox1[0]+colbox1[2] and colbox2[1] <= colbox1[1]+colbox1[3]) and (colbox2[0]+colbox2[2] >= colbox1[0] and colbox2[1]+colbox2[3] >= colbox1[1])
class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
class Bullet:
    def __init__(self, x, y, sx, sy, tank):
        self.x = x
        self.y = y
        self.radius = 9
        self.speedx = sx
        self.speedy = sy
        self.tank = tank
        self.state = False
    def draw(self):
        if self.state == False:
            pygame.draw.circle(screen, self.tank.color, (self.x, self.y), self.radius,1)
    
    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        if  0 >= self.x or self.x >= 800:
            self.state=True
        if 0 >= self.y or self.y >= 600:
            self.state=True
        self.draw()

class Tank:

    def __init__(self, x, y, speed, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.x = random.randint(200,500)
        self.y = random.randint(100,400)
        self.life = 3
        self.color = color
        self.speed = speed
        self.width = 40
        self.direction = random.randint(1, 4)
        self.bounds = (x,y,self.width,self.width) 
        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}
        self.state = True
    def draw(self):
        if self.state == True:
            center = (self.x + self.width // 2, self.y + self.width // 2)
            #pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width),10)
            pygame.draw.circle(screen, self.color, center, int(self.width/2),2)
            # pygame.draw.circle(screen, self.color, center, int(self.width // 1.1),5)

            if self.direction == Direction.RIGHT:
                pygame.draw.line(screen, self.color, center, (self.x + self.width + int(self.width/3), self.y + int(self.width / 2)), 2)
            if self.direction == Direction.LEFT:
                pygame.draw.line(screen, self.color, center, (self.x - int(self.width/3), self.y + int(self.width / 2)), 2)
            if self.direction == Direction.UP:
                pygame.draw.line(screen, self.color, center, (self.x + int(self.width/2), self.y - int(self.width / 3)), 2)
            if self.direction == Direction.DOWN:
                pygame.draw.line(screen, self.color, center, (self.x + int(self.width/2), self.y + self.width + int(self.width / 3)), 2)  
    
    def change_direction(self, direction):
        self.direction = direction
    def random_pos(self):
        self.x = random.randint(200,600)
        self.y = random.randint(200,400)
    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed

        if self.y < -40:
            self.y = 600
        if self.y > 600:
            self.y = 0
        if self.x < -40:
            self.x = 800
        if self.x > 800:
            self.x = 0
        
        self.draw()
        

def Life1(x):
    font = pygame.font.SysFont("comicsansms", 25)
    pnt = font.render("Daulet: " + str(x), True, (35,187,17))
    screen.blit(pnt, (20, 20))

def Life2(x):
    font = pygame.font.SysFont("comicsansms", 25)
    pnt = font.render("Player2: " + str(x), True, (255,170,35))
    screen.blit(pnt, (650, 20))

                
FPS = 60
clock = pygame.time.Clock()

tank1 = Tank(200, 300, 3, (35,187,17))
tank2 = Tank(500, 300, 3, (255,170,35), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
tanks=[]
tanks.append(tank1)
tanks.append(tank2)
bullets = []
def gameloop():
    tank1.state=True
    tank2.state=True
    gameExit = False
    gameOver = False
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    while not gameExit:    
        if gameOver == True:
            screen.fill(white)
            if tank1.life>0:
                tank1.speed = 0
                tank1.draw()
            elif tank2.life>0:
                tank2.speed = 0
                tank2.draw()
            if tank1.life <= 0:
                tank1.state=False
            elif tank2.life <= 0:
                tank2.state=False
            mixer.music.stop() 
            over.play()             
            message_to_screen("Game Over",red,-50,size='small')
            message_to_screen("Press C to play again",black,50) 
            message_to_screen("Press M to open the main menu",black,90)
            message_to_screen("Press Q to quit",black,130)
            pygame.display.update()
            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            tank1.life = 3
                            tank2.life = 3
                            tank1.speed = tank2.speed = 4
                            tank1.x = random.randint(50,screenwidth - 70)
                            tank1.y = random.randint(50,screenheight - 70)
                            tank2.x = random.randint(50,screenwidth - 70)
                            tank2.y = random.randint(50,screenheight - 70)
                            gameloop()
                        elif event.key == pygame.K_q:
                            gameExit = True
                            gameOver = False  
                        elif event.key == pygame.K_m: 
                            game_intro()     
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameExit = True
                if event.key in tank1.KEY.keys():
                    tank1.change_direction(tank1.KEY[event.key])
                if event.key in tank2.KEY.keys():
                    tank2.change_direction(tank2.KEY[event.key])
                if event.key == pygame.K_RETURN:
                    shoot.play()
                    if tank1.direction == Direction.LEFT:
                        bullet = Bullet(tank1.x - 20, tank1.y + 20, -bulletspeed, 0,tank1)
                    if tank1.direction == Direction.RIGHT:
                        bullet = Bullet(tank1.x + 60, tank1.y + 20, bulletspeed, 0,tank1)
                    if tank1.direction == Direction.UP:
                        bullet = Bullet(tank1.x + 21, tank1.y - 20, 0, -bulletspeed,tank1)
                    if tank1.direction == Direction.DOWN:
                        bullet = Bullet(tank1.x + 21, tank1.y + 60, 0, bulletspeed,tank1)
                    bullets.append(bullet)    
                if event.key == pygame.K_SPACE:
                    shoot.play()
                    if tank2.direction == Direction.LEFT:
                        bullet = Bullet(tank2.x - 20, tank2.y+20, -bulletspeed, 0,tank2)
                    if tank2.direction == Direction.RIGHT:
                        bullet = Bullet(tank2.x + 60, tank2.y+20, bulletspeed, 0,tank2)
                    if tank2.direction == Direction.UP:
                        bullet = Bullet(tank2.x + 21, tank2.y - 20, 0, -bulletspeed,tank2)
                    if tank2.direction == Direction.DOWN:
                        bullet = Bullet(tank2.x + 21, tank2.y + 60, 0, bulletspeed,tank2)
                    bullets.append(bullet)
        for bu in bullets:
            if bu.x < 0 or bu.x > 800 or bu.y < 0 or bu.y > 600:
                bullets.pop(0)
            if bu.x in range(tank2.x, tank2.x + 60) and bu.y in range(tank2.y, tank2.y + 60):
                if tank2.life>1:
                    hate.play()
                bullets.pop(0)
                tank2.random_pos()
                tank2.life -= 1
            if bu.x in range(tank1.x, tank1.x + 60) and bu.y in range(tank1.y, tank1.y + 60):
                if tank1.life>1:
                    hate.play()
                bullets.pop(0)
                tank1.random_pos()
                tank1.life -= 1               
        
        screen.fill((255, 255, 255))
        Life1(tank1.life)
        Life2(tank2.life)
        if tank1.life <= 0 or tank2.life <= 0:
            gameOver = True 
        for bullet in bullets:
            bullet.move()
        for tank in tanks:
            tank.draw()
        tank1.move()
        tank2.move()  
        pygame.display.flip() 
		   
    pygame.quit()
    quit()
    
game_intro()