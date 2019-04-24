import pygame
import time
import random
import math
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    """
    Player 1's paddle.
    attributes: rect, surf, direction
    returns: player 1 object
    functions: update
    """
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((5, 37))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.y = 160
        self.rect.x = 40

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 640:
            self.rect.right = 640
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 480:
            self.rect.bottom = 480

class Player2(pygame.sprite.Sprite):
    """
    Player 2's paddle.
    attributes: rect, surf, computer
    returns: player 2 object
    functions: update
    """
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((5, 37))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.x = 595
        self.rect.y = 160
        self.computer = False

    def update(self, pressed_keys):
        if self.computer:
            if abs(self.rect.centerx - ball.rect.centerx) < 50:
                rand = random.choice([-15, 15])
                if self.rect.centery < ball.rect.centery + rand:
                    self.rect.move_ip(0, 2.5)
                if self.rect.centery > ball.rect.centery + rand:
                    self.rect.move_ip(0, -2.5)
            else:
                if self.rect.centery < ball.rect.centery:
                    self.rect.move_ip(0, 2.5)
                if self.rect.centery > ball.rect.centery:
                    self.rect.move_ip(0, -2.5)
        else:

            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 640:
            self.rect.right = 640
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 480:
            self.rect.bottom = 480

class Ball(pygame.sprite.Sprite):
    """
    Pong ball + score.
    returns: ball object
    attributes: rect, vector, area, surf, score1, score2, stuck
    functions: update, mov, scored
    """
    def __init__(self, vector):
        super().__init__()
        self.surf = pygame.Surface((7, 7))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.x = 316.5
        self.rect.y = random.randint(10, 470)
        self.area = scale.get_rect()
        self.vector = vector
        self.score1 = 0
        self.score2 = 0
        self.stuck = False

    def update(self):
        pos = self.mov(self.rect, self.vector)
        self.rect = pos
        (angle, z) = self.vector

        if not self.area.contains(pos):
            tleft = not self.area.collidepoint(pos.topleft)
            tright = not self.area.collidepoint(pos.topright)
            bleft = not self.area.collidepoint(pos.bottomleft)
            bright = not self.area.collidepoint(pos.bottomright)
            if tright and tleft or (bright and bleft):
                angle = -angle
                pygame.mixer.Sound.play(hit)
            if tleft and bleft:
                pygame.mixer.Sound.play(score)
                self.rect.x = 316.5
                self.rect.y = random.randint(10, 470)
                self.score2 += 1
                angle = random.choice(directions)
                z = 3
            if tright and bright:
                pygame.mixer.Sound.play(score)
                self.rect.x = 316.5
                self.rect.y = random.randint(10, 470)
                self.score1 += 1
                angle = random.choice(directions)
                z = 3
        else:
            if self.rect.colliderect(player.rect) and not self.stuck:
                if self.rect.centery > player.rect.centery + 13:
                    angle = math.pi / 3
                elif self.rect.centery > player.rect.centery + 8.5:
                    angle = math.pi / 4
                elif self.rect.centery > player.rect.centery + 3:
                    angle = math.pi / 6
                elif self.rect.centery < player.rect.centery - 3:
                    angle = -math.pi / 6
                elif self.rect.centery < player.rect.centery - 8.5:
                    angle = -math.pi / 4
                elif self.rect.centery < player.rect.centery - 13:
                    angle = -math.pi / 3
                else:
                    angle = 0
                pygame.mixer.Sound.play(hit)
                self.stuck = not self.stuck
            elif self.rect.colliderect(player2.rect) and not self.stuck:
                if self.rect.centery > player2.rect.centery + 13:
                    angle = math.pi / 3
                elif self.rect.centery > player2.rect.centery + 8.5:
                    angle = math.pi / 4
                elif self.rect.centery > player2.rect.centery + 3:
                    angle = math.pi / 6
                elif self.rect.centery < player2.rect.centery - 3:
                    angle = -math.pi / 6
                elif self.rect.centery < player2.rect.centery - 8.5:
                    angle = -math.pi / 4
                elif self.rect.centery < player2.rect.centery - 13:
                    angle = -math.pi / 3
                else:
                    angle = 0
                pygame.mixer.Sound.play(hit)
                angle = math.pi - angle
                self.stuck = not self.stuck
            elif self.stuck:
                self.stuck = not self.stuck
        if z < 11:
            z += 0.001
        self.vector = (angle, z)

    def mov(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z*math.cos(angle), z*math.sin(angle))
        return rect.move(dx, dy)

pygame.init()

pygame.display.set_caption("Pong")
icon = pygame.Surface((1,1))
icon.fill((0,0,0))
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)

scale = pygame.Surface((640, 480))

clear = pygame.Surface((640, 480))
clear.fill((0,0,0))

player = Player()
player2 = Player2()

directions = [math.pi / 4, 0, (5 * math.pi) / 4, (3 * math.pi) / 4, (7 * math.pi) / 4, math.pi]
vector = (random.choice(directions), 3)
ball = Ball(vector)

running = True

font = pygame.font.Font(None, 100)
ptitle = pygame.font.Font(None, 200)
pmodes = pygame.font.Font(None, 30)
pwin = pygame.font.Font(None, 120)
pwin2 = pygame.font.Font(None, 40)

hit = pygame.mixer.Sound("hit.ogg")
score = pygame.mixer.Sound('score.ogg')
over = pygame.mixer.Sound('over.ogg')

pre = time.time() * 1000.0

def title_screen():
    """
    Allows player to choose single or two player mode.
    """
    title = True
    pre = time.time() * 1000.0
    while title:

        cur = time.time() * 1000.0
        dt = cur - pre
        pre = cur
        delay = 1000.0/60.0 - dt
        delay = max(int(delay), 0)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == K_1:
                    player2.computer = True
                    title = False
                elif event.key == K_2:
                    player2.computer = False
                    title = False
            elif event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE)
        w, h = pygame.display.get_surface().get_size()

        scale.blit(clear, (0,0))
        scale.blit(ptitle.render("Pong", True, pygame.Color('white')), (140, 20))
        scale.blit(pmodes.render('Press 1 for single player mode - W/S to move', True, pygame.Color('white')), (100, 270))
        scale.blit(pmodes.render('Press 2 for two player mode - W/S and Up/Down to move', True, pygame.Color('white')), (50, 320))

        pygame.transform.scale(scale, (w, h), screen)
        pygame.display.flip()
        pygame.time.wait(delay)

def win_screen(winner, screen):
    """
    Displays the winner of the match.
    Additionally, allows another game to be initialized.
    """
    win = True
    pre = time.time() * 1000.0
    while win:

        cur = time.time() * 1000.0
        dt = cur - pre
        pre = cur
        delay = 1000.0/60.0 - dt
        delay = max(int(delay), 0)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == K_1:
                    player2.computer = True
                    win = False
                elif event.key == K_2:
                    player2.computer = False
                    win = False
            elif event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE)

        w, h = pygame.display.get_surface().get_size()

        scale.blit(clear, (0,0))
        if winner == 1:
            scale.blit(pwin.render("Player 1 wins!", True, pygame.Color('white')), (30, 20))
        if winner == 2:
            scale.blit(pwin.render("Player 2 wins!", True, pygame.Color('white')), (30, 20))

        scale.blit(pwin2.render('Press 1 or 2 to play again with 1/2 players', True, pygame.Color('white')), (40, 270))

        pygame.transform.scale(scale, (w, h), screen)
        pygame.display.flip()
        pygame.time.wait(delay)

title_screen()

while running:
    if ball.score1 == 11:
        pygame.mixer.Sound.play(over)
        player = Player()
        player2 = Player2()
        ball = Ball(vector)
        win_screen(1, screen)
    if ball.score2 == 11:
        pygame.mixer.Sound.play(over)
        player = Player()
        player2 = Player2()
        ball = Ball(vector)
        win_screen(2, screen)
    cur = time.time() * 1000.0
    dt = cur - pre
    pre = cur
    delay = 1000.0/60.0 - dt
    delay = max(int(delay), 0)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)

    w, h = pygame.display.get_surface().get_size()
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    player2.update(pressed_keys)
    ball.update()

    scale.blit(clear, (0,0))
    scale.blit(player.surf, player.rect)
    scale.blit(player2.surf, player2.rect)
    scale.blit(ball.surf, ball.rect)

    dash = 35
    while dash <= 640:
        pygame.draw.line(scale, (255, 255, 255), (319, dash - 30), (319, dash))
        dash += 40
    scale.blit(font.render(str(ball.score1), True, pygame.Color('white')), (140, 10))
    scale.blit(font.render(str(ball.score2), True, pygame.Color('white')), (460, 10))

    pygame.transform.scale(scale, (w, h), screen)
    pygame.display.flip()
    pygame.time.wait(delay)
