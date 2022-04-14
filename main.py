import pygame
import sys
 
pygame.init()
hintergrund = pygame.image.load("hintergrund.png")
screen = pygame.display.set_mode([1228, 717])
clock = pygame.time.Clock()
pygame.display.set_caption("Transporterspiel")
 
stehen = pygame.image.load("lkw.png")
 
class spieler:
    def __init__(self,x,y,geschw,breite,hoehe,richtg,schritteRechts,schritteLinks):
        self.x = x
        self.y = y
        self.geschw = geschw
        self.breite = breite
        self.hoehe = hoehe
        self.richtg = richtg
        self.schritteRechts = schritteRechts
        self.schritteLinks = schritteLinks
        self.sprung = False
    def laufen(self,liste):
        if liste[0]:
            self.x -= self.geschw
            self.richtg = [1,0,0,0]
            self.schritteLinks += 1
        if liste[1]:
            self.x += self.geschw
            self.richtg = [0,1,0,0]
            self.schritteRechts += 1
    def resetSchritte(self):
        self.schritteLinks = 0
        self.schritteRechts = 0
    def stehen(self):
        self.richtg = [0,0,1,0]
        self.resetSchritte()
 
linkeWand = pygame.draw.rect(screen, (0,0,0), (-2,0,2,600), 0)
rechteWand = pygame.draw.rect(screen, (0,0,0), (1229,0,2,718), 0)
spieler1 = spieler(300,393,5,96,128,[0,0,1,0],0,0)
go = True
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
 
    spielerRechteck = pygame.Rect(spieler1.x,spieler1.y,96,128)
    gedrueckt = pygame.key.get_pressed()
 
    if gedrueckt[pygame.K_RIGHT] and not spielerRechteck.colliderect(rechteWand):
        spieler1.laufen([0,1])
    elif gedrueckt[pygame.K_LEFT] and not spielerRechteck.colliderect(linkeWand):
        spieler1.laufen([1,0])
    else:
        spieler1.stehen()
 
    clock.tick(60)