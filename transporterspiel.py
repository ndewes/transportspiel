import pygame
import sys
import os
from math import sin, radians, degrees, copysign

class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getPosition(self):
        return self.x, self.y

class Quelle(pygame.sprite.Sprite):

    def __init__(self, kapazitaet, volumen):
        self.kapazitaet = kapazitaet
        self.volumen = volumen

    def setKapazitaet(self, kapazitaet):
        self.kapazitaet = kapazitaet

    def getKapazitaet(self):
        return self.kapazitaet

    def setVolumen(self, volumen):
        self.volumen = volumen

    def getVolumen(self):
        return self.volumen

class Richtwerte(pygame.sprite.Sprite):

    def __init__(self, geschwindigkeit, r_x, r_y):
        self.geschwindigkeit = geschwindigkeit
        self.r_x = r_x
        self.r_y = r_y

    def setGeschwindigkeit(self, geschwindigkeit):
        self.geschwindigkeit = geschwindigkeit

    def getGeschwindigkeit(self):
        return self.geschwindigkeit
    
    def setRichtung(self, r_x, r_y):
        self.r_x = r_x
        self.r_y = r_y

    def getRichtung(self):
        return self.richtg, self.r_x, self.r_y


class LKW(pygame.sprite.Sprite):

    def __init__(self, tank):
        self.tank = tank

    def setTank(self, tank):
        self.tank = tank

    def getTank(self):
        return self.tank

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Transportspiel")
        breite = 1280
        hoehe = 720
        self.screen = pygame.display.set_mode((breite, hoehe))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "grafik/lkw.png")
        lkw_image = pygame.image.load(image_path)
        lkw = LKW(5)
        ppu = 32

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_d]:
                lkw -= 30 * dt
            elif pressed[pygame.K_a]:
                lkw += 30 * dt

            # Logic
            lkw.update(dt)

            # Drawing
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(lkw_image, lkw.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, lkw.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


def main():
    
    heli = pygame.image.load("grafik/heli.png").convert
    hintergrund = pygame.image.load("grafik/hintergrund.png").convert
    
    game = Game()
    game.run()


if __name__ == '__main__':
    main()