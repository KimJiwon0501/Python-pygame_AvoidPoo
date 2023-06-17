import pygame
import random
import time
from datetime import datetime

pygame.init()

size = [450, 800]
screen = pygame.display.set_mode(size)

title = "[Avoid Poo]"
pygame.display.set_caption(title)

clock = pygame.time.Clock()


bgColor = (210, 200, 140)
black = (0, 0, 0)

class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
    def put_img(self, address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
            self.sx, self.sy = self.img.get_size()
    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()
    def show(self):
        screen.blit(self.img, (self.x, self.y))

def crash(a, b):
    if (a.x-b.sx <= b.x) and (b.x <= a.x + a.sx):
        if (a.y - b.sy <= b.y) and (b.y <= a.y + a.sy):
            return True
        else:
            return False
    else:
        return False

Player = obj()
Player.put_img("img\Character_Right.png")
Player.change_size(72, 72)
Player.x = round(size[0] / 2 - Player.sx / 2)
Player.y = size[1] - Player.sy - 70
Player.move = 7

left_go = False
right_go = False

Umbrella = obj()
Umbrella.put_img("img/Umbrella_Right.png")
Umbrella.change_size(90, 48)
Umbrella.x = Player.x
Umbrella.y = Player.y
Umbrella_show = False

Ground = obj()
Ground.put_img("img\Ground.png")
Ground.x = 0
Ground.y = 730
Ground.change_size(860, 141)

BestScore = 0
Score = 0

intro_character = pygame.image.load("img\Character_Right.png").convert_alpha()
intro_poo = pygame.image.load("img\Poo.png").convert_alpha()
intro_poo = pygame.transform.scale(intro_poo, (64, 64))

title_sound = pygame.mixer.Sound("sound/title_sound.mp3")
title_sound.play(-1)

SB = 1

Title_Height = 885
#인트로
while Title_Height != 100:
    font = pygame.font.Font("font\BMDOHYEON_ttf.ttf", 60)
    text = font.render("AVOID POO", True, (random.randint(1, 250), random.randint(1, 250), random.randint(1, 250)))
    screen.blit(text, (63, Title_Height))
    pygame.display.flip()
    Title_Height -= 5
    time.sleep(0.01)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
text = font.render("AVOID POO", True, (255, 215, 0))
screen.blit(text, (63, Title_Height))

while SB == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 0
    screen.blit(intro_poo, (200, 237))
    screen.blit(intro_character, (130, 300))
    #키 눌러서 시작
    font = pygame.font.Font("font\BMDOHYEON_ttf.ttf", 20)
    text = font.render("PRESS THE SPACE BAR TO START", True, (255, 255, 255))
    screen.blit(text, (50, 600))
    font = pygame.font.Font("font\BMDOHYEON_ttf.ttf", 15)
    text = font.render("MOVE TO [ ← ]  [ → ]     USE ITEM TO [ ↑ ]", True, (255, 255, 255))
    screen.blit(text, (80, 650))
    pygame.display.flip()

title_sound.stop()

# play_sound = pygame.mixer.Sound("sound/play_sound.mp3")

Have_Umbrella = 0

while True:

    Pp_list = []
    Um_list = []

    SB = 0
    Score = 0
    Umbrella_show = False

    while SB == 0:

        # play_sound.play(-1)

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_go = True
                elif event.key == pygame.K_RIGHT:
                    right_go = True
                elif event.key == pygame.K_UP:
                    if Have_Umbrella > 0:
                        if Umbrella_show != True:
                            Have_Umbrella -= 1
                            Umbrella_show = True
                            start_time = datetime.now()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_go = False
                elif event.key == pygame.K_RIGHT:
                    right_go = False
        
        if left_go == True:
            Player.put_img("img\Character_Left.png")
            Player.change_size(72, 72)
            Player.x -= Player.move
            if Player.x <= 0:
                Player.x = 0
        elif right_go == True:
            Player.put_img("img\Character_Right.png")
            Player.change_size(72, 72)
            Player.x += Player.move
            if Player.x >= size[0] - Player.sx:
                Player.x = size[0] - Player.sx

        if Umbrella_show == True:
            Umbrella.x = Player.x - 8
            Umbrella.y = Player.y - 37


        if random.randint(1, 800) == 1:
            Fall_Umbrella = obj()
            Fall_Umbrella.put_img("img/Umbrella_Right.png")
            Fall_Umbrella.change_size(60, 32)
            Fall_Umbrella.x = random.randrange(0, size[0] - Fall_Umbrella.sx)
            Fall_Umbrella.y = 5
            Fall_Umbrella.move = 6
            Um_list.append(Fall_Umbrella)
        d_list = []
        for i in range(len(Um_list)):
            Um = Um_list[i]
            Um.y += Um.move
            if crash(Fall_Umbrella, Ground):
                d_list.append(i)
            if crash(Fall_Umbrella, Player):
                Have_Umbrella += 1
                d_list.append(i)
        for d in d_list:
            del Um_list[d]

        if random.random() > 0.98:
            Poo = obj()
            Poo.put_img("img\Poo.png")
            Poo.change_size(64, 64)
            Poo.x = random.randrange(0, size[0] - Poo.sx)
            Poo.y = 5
            Poo.move = 6
            Pp_list.append(Poo)
        d_list = []
        for i in range(len(Pp_list)):
            Pp = Pp_list[i]
            Pp.y += Pp.move
            if crash(Pp, Player):
                SB = 1
            if crash(Pp, Ground):
                d_list.append(i)
                Score += round(random.randint(1, 8) * 0.1)
            if Umbrella_show == True:
                if crash(Pp, Umbrella):
                    d_list.append(i)
                    Score += round(random.randint(1, 15) * 0.1)
        for d in d_list:
            del Pp_list[d]


        screen.fill(bgColor)
        Ground.show()
        Player.show()
        if Umbrella_show == True:
            Umbrella.show()
        for Pp in Pp_list:
            Pp.show()
        for Um in Um_list:
            Um.show()

        font = pygame.font.Font("font\BMDOHYEON_ttf.ttf", 20)
        text = font.render("Score : {0}".format(Score), True, (150, 75, 0))
        screen.blit(text, (10, 5))
        if Have_Umbrella > 0:
            text = font.render("Umbrella : {0}".format(Have_Umbrella), True, (150, 75, 0))
            screen.blit(text, (130, 5))
        if Umbrella_show == True:
            time = 5 - int((datetime.now() - start_time).total_seconds())
            if time <= 0:
                Umbrella_show = False
            text = font.render("Time :  {0}".format(time), True, (150, 75, 0))
            screen.blit(text, (300, 5))

        pygame.display.flip()
        
    #게임 오버
    # play_sound.stop()
    left_go = False
    right_go = False
    while SB == 1:
        clock.tick(60)
        if BestScore < Score:
            BestScore = Score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SB = 0
        screen.fill(black)
        font = pygame.font.Font("font\BMDOHYEON_ttf.ttf", 60)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (50, 100))
        #점수
        font = pygame.font.Font("font\BMDOHYEON_ttf.ttf", 40)
        text = font.render("Score : {0}".format(Score), True, (255, 215, 0))
        screen.blit(text, (70, 270))
        #베스트 점수
        font = pygame.font.Font("font\BMDOHYEON_ttf.ttf", 40)
        text = font.render("BestScore : {0}".format(BestScore), True, (255, 215, 0))
        screen.blit(text, (70, 220))
        #키 눌러서 재시작
        font = pygame.font.Font("font\BMDOHYEON_ttf.ttf", 15)
        text = font.render("PRESS THE SPACE BAR TO RESTART", True, (255, 255, 255))
        screen.blit(text, (70, 700))
        pygame.display.flip()