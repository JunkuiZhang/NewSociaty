import pygame
from pygame.locals import *



class Animation:

    def __init__(self, resolution, dimension, world, entities):
        self.__resolution = resolution
        self.__dimension = dimension
        self.__world = world
        self.__entities = entities

    @property
    def resolution(self):
        return self.__resolution

    @resolution.setter
    def resolution(self, num):
        self.__resolution = num

    @property
    def dimension(self):
        return self.__dimension

    @dimension.setter
    def dimension(self, num):
        self.__dimension = num

    @property
    def world(self):
        return self.__world

    @property
    def entities(self):
        return self.__entities

    def playing(self):
        pass