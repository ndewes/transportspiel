import random
from math import radians, sqrt
from turtle import pos

import pygame
from pygame.locals import *

#Standard für RGB und weitere
GRUEN = (0, 255, 0)
ROT   = (255, 0, 0)
BLAU  = (0, 0, 255)
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)

#Fenster Angaben
BREITE = 1600
HOEHE = 900
FPS = 60

#Transporter Richtungen
G_TRANSPORTER = 4
G_TRANSPORTER_MINUS = -4

#Geschwindigkeit Heli
G_HELI = 4.5

#Verktorrechnung für den Helikopter
class PVec:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  # Addition Subtraktion
  def __add__(self, other): 
    return PVec( self.x + other.x, self.y + other.y )  

  def __sub__(self, other): 
    return PVec( self.x - other.x, self.y - other.y )  
  
  # Skalarmultiplikation
  def __mul__(self, other): 
    if type(other) in [int, float]:
      return PVec( self.x * other, self.y * other )
    else:
      raise NotImplementedError('Other multiplication than scalar not implemented')

  def __truediv__(self, other):
    if type(other) in [int, float]:
      return PVec( self.x / other, self.y / other )
    else:
      raise NotImplementedError('Other multiplication than scalar not implemented')

  # Betrag
  def __abs__(self): 
    return sqrt( self.x*self.x + self.y*self.y )

  def normalized(self): 
    return self / abs(self)

  # Aufrunden, Abrunden, Kaufm. Runden
  def __ceil__(self):
    return PVec( self.x.__ceil__(), self.y.__ceil__() )

  def __floor__(self):
    return PVec( self.x.__floor__(), self.y.__floor__() )

  def __round__(self):
    return PVec( self.x.__round__(), self.y.__round__() )

  # Darstellung im interaktiven Python
  def __repr__(self):
    return f"({self.x} {self.y})"


#Gebäudeparameter für Tankstelle, Lager und der Mine
class Gebaeude(pygame.sprite.Sprite):

    def __init__(self, ladestand, kapazitaet, posX, posY, bildPfad):
        super().__init__()
        self.ladestand_ = ladestand
        self.kapazitaet_ = kapazitaet
        self.posX = posX
        self.posY = posY
        self.image = pygame.image.load(bildPfad)
        self.scalled = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center=(self.posX, self.posY)

    def draw(self, flaeche):
        flaeche.blit(self.scalled, self.rect)

    def setLadestand(self, neuLadestand):
        self.ladestand_ = neuLadestand

    def getLadeStand(self):
        return self.ladestand_

    def setKapazität(self, Kapazitaet):
        self.kapazitaet_ = Kapazitaet

    def getKapazitaet(self):
        return self.kapazitaet_

#Transporterparameter
class Transporter(pygame.sprite.Sprite):

    def __init__(self, ladung, tank):
        super().__init__()
        self.transporter = pygame.image.load('grafik/transporter.png')
        self.image = pygame.transform.scale(self.transporter, (125,100))
        self.rect = self.image.get_rect()
        self.rect.center=(1000, 600)
        self.ladung_ = ladung
        self.tank_ = tank

    def draw(self, flaeche):
        flaeche.blit(self.image, self.rect)

    def setTank(self, tank):
        self.tank_ = tank

    def getTank(self):
        return self.tank_

    def setLadung(self, ladung):
        self.ladung_ = ladung

    def getLadung(self):
        return self.ladung_

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.top > 0:
            if pressed_keys[K_w]:
                self.rect.move_ip(0, G_TRANSPORTER_MINUS)
        if self.rect.bottom < HOEHE:
            if pressed_keys[K_s]:
                self.rect.move_ip(0, G_TRANSPORTER)
        if self.rect.left > 0:
            if pressed_keys[K_a]:
                self.rect.move_ip(G_TRANSPORTER_MINUS, 0)
        if self.rect.left < BREITE-self.rect.width:
            if pressed_keys[K_d]:
                self.rect.move_ip(G_TRANSPORTER, 0)
                

#Heliparameter
class Helikopter(pygame.sprite.Sprite):

    def __init__(self): 
        super().__init__()
        self.heli = pygame.image.load('grafik/heli.png')
        self.image = pygame.transform.scale(self.heli, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.center=(100, 700)
        self.ladestand = 0

    def draw(self, flaeche):
        flaeche.blit(self.image, self.rect)

    def setLadestand(self, ladestand):
        self.ladestand = ladestand

    def getLadestand(self):
        return self.ladestand

    def tVerfolgung(self, x, y):
        posTransporter = PVec( x, y )
        posHeli = PVec( self.rect.x, self.rect.y )

        richtung = round(( posTransporter - posHeli).normalized() * G_HELI)

        self.rect.move_ip(richtung.x, richtung.y)

    def getHome(self):
        be = 5
        posHome = PVec(900, 1400)
        posHeli = PVec( self.rect.x, self.rect.y )

        richtung = round(( posHome - posHeli).normalized() * be)

        self.rect.move_ip(richtung.x, richtung.y)

class Game:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.breite, self.hoehe = BREITE, HOEHE
        self.gameOver = False
 
    def initial(self):
        pygame.init()
        pygame.display.set_caption('Transporterspiel von Niklas Dewes')
        pygame.font.init()
        pygame.mixer.init()

        self.FramePerSec = pygame.time.Clock()
        self._running = True

        self.map_ = pygame.image.load('grafik/map.png')
        self.map = pygame.transform.scale(self.map_, (1600, 900))
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.blit(self.map, (0, 0))

        self.win = pygame.image.load('grafik/win.png')
        self.winScreen = pygame.transform.scale(self.win, (1600, 900))
        self.win_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.win_surf.blit(self.winScreen, (0, 0))

        self.lose = pygame.image.load('grafik/gameover.png')
        self.loseScreen = pygame.transform.scale(self.lose, (1600, 900))
        self.lose_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.lose_surf.blit(self.loseScreen, (0, 0))

        self.font = pygame.font.Font(None, 20)
        self.helikopter = Helikopter()
        self.transporter = Transporter(0, 100)

        self.lager = Gebaeude(0, 100, 1500, 900, 'grafik/lager.png')
        self.garage = Gebaeude(0, 0, 900, 1400, 'grafik/garage.png')
        self.mine = Gebaeude(100, 100, 410, 150, 'grafik/mine.png')
        self.tankstelle = Gebaeude(100, 100, 1600, 300, 'grafik/tankstelle.png')

    def start(self):
        if self.initial() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.event(event)
            self.game_loop()
            self.render()
        self.quit()

    def textAnzeige(self):
        self.erzcounter = self.font.render('Transporter: Erz: ' + str(self.transporter.getLadung()) + ' Erz: ' + str(round(self.transporter.getTank())), False, (255, 255, 255))
        self._display_surf.blit(self.erzcounter, (10, 10))
        self.lagercounter = self.font.render('Lager: Erz: ' + str(self.lager.getLadeStand()), False, (255, 255, 255))
        self._display_surf.blit(self.lagercounter, (10, 30))
        self.helicounter = self.font.render('Helikopter: Erz: ' + str(self.helikopter.getLadestand()), False, (255, 255, 255))
        self._display_surf.blit(self.helicounter, (10, 50))
 
    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def game_loop(self):
        self._display_surf.blit(self.map, (0, 0))
        if self.helikopter.rect.colliderect(self.transporter.rect):
            self.heli_collision()
        if self.transporter.rect.colliderect(self.tankstelle.rect):
            self.tanken()
        if self.transporter.rect.colliderect(self.mine.rect):
            self.aufladen()
        if self.transporter.rect.colliderect(self.lager.rect):
            self.abladen()
        if  self.helikopter.rect.colliderect(self.garage.rect):
            self.helikopter.tVerfolgung(self.transporter.rect.x, self.transporter.rect.y)
        if self.transporter.rect.colliderect(self.mine.rect):
            self.helikopter.getHome()
        

        if self.gameOver:
            self.lose_screen()
            return

        self.transporter.update()
        self.helikopter.draw(self._display_surf)
        self.transporter.draw(self._display_surf)
        self.helikopter.tVerfolgung(self.transporter.rect.x, self.transporter.rect.y)
        self.lager.draw(self._display_surf)
        self.garage.draw(self._display_surf)
        self.mine.draw(self._display_surf)
        self.tankstelle.draw(self._display_surf)

        self.burn_petrol()
        self.textAnzeige()
        
        pygame.display.update()
        pass

    def render(self):
        self.FramePerSec.tick(FPS)
        pygame.display.update()
        pass

    def quit(self):
        pygame.quit()
 
    def heli_collision(self):
        if self.transporter.getLadung() > 0:
            self.transporter.setLadung(self.transporter.getLadung() - 5)
            self.helikopter.setLadestand(self.helikopter.getLadestand() + 5)
            self.helikopter.getHome()
        if self.helikopter.getLadestand() >= 20:
            self.lose_screen()

    def tanken(self):
        self.tankstelle.setLadestand(self.tankstelle.ladestand_-100)
        self.transporter.setTank(100)
        return

    def aufladen(self):
        #print("LKW an Mine")
        self.mine.setLadestand(self.mine.ladestand_-5)
        self.transporter.setLadung(5)
        return

    def abladen(self):
        self.lager.setLadestand(self.lager.getLadeStand() + self.transporter.getLadung())
        self.transporter.setLadung(self.transporter.getLadung() - self.transporter.getLadung())
        if self.lager.getLadeStand() >= 80:
            self.win_screen()
        return

    def lose_screen(self):
        if not self.gameOver:
            self.lose_surf.blit(self.loseScreen, (0, 0))
            self.gameOver = True
            self.gameOverScreenShown = False
        return

    def win_screen(self):
        self.win_surf.blit(self.winScreen, (0, 0))
        return


    def burn_petrol(self):
        neue_tankfüllung = self.transporter.getTank() - 0.05
        if(neue_tankfüllung < 0):
            self.lose_screen("TANK LEER!")
        else:
            self.transporter.setTank(neue_tankfüllung)
        return

def main():
    game = Game()
    game.start()

if __name__ == "__main__" :
    main()
