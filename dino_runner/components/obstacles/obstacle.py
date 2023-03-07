from pygame.sprite import Sprite
from dino_runner.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BIRD
import pygame
class Obstacle(Sprite):
    
    def __init__(self, image, type):
        self.type = type
        self.image = image[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.bird_fly = True
        if image == BIRD:
            self.bird_fly = True
        
    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            obstacles.pop()
            
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)