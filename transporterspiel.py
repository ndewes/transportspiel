from re import X
import pygame

class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setPosition(self):
        pass

    def getPosition(self):
        pass

class Quelle:

    def __init__(self, kapazitaet, volumen):
        self.kapazitaet = kapazitaet
        self.volumen = volumen

    def setKapazitaet(self):
        pass

    def getKapazitaet(self):
        pass

    def setVolumen(self):
        pass

    def getVolumen(self):
        pass

class Richtwerte:

    def __init__(self, geschwindigkeit, r_x, r_y):
        self.geschwindigkeit = geschwindigkeit
        self.r_x = r_x
        self.r_y = r_y

    def setGeschwindigkeit(self):
        pass

    def getGeschwindigkeit(self):
        pass
    
    def setRichtung(self):
        pass

    def getRichtung(self):
        pass

class LKW:

    def __init__(self, tank):
        self.tank = tank

    def setTank(self):
        pass

    def getTank(self):
        pass

def main():
    pass


if __name__ == '__main__':
    main()