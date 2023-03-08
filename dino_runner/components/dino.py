from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING
import pygame
class Dino(Sprite):
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8
    Y_DUCK = 35
    def __init__(self):
        self.image = RUNNING[0] #lista que contiene las 2 imagenes del dino
        self.dino_rest = self.image.get_rect()
        self.dino_rest.x = self.X_POS
        self.dino_rest.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        
    def update(self, user_input):
        if self.dino_run:
            self.run()
            
        elif self.dino_jump:
            self.jump()
            if user_input[pygame.K_DOWN]:
                self.dino_rest.y = self.Y_POS
                self.dino_jump = False 
                self.jump_vel = self.JUMP_VEL
                
        elif self.dino_duck:
            self.duck()
            
        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            
        elif user_input[pygame.K_DOWN] and not self.dino_duck:
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
            
        elif not self.dino_jump:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False
            
        if self.step_index >= 10:
            self.step_index = 0
    
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rest.x, self.dino_rest.y))
        
    
    def run(self):
        if self.step_index < 5:
            self.image = RUNNING[0]
        else:
            self.image = RUNNING[1]
        
        self.dino_rest.x = self.X_POS
        self.dino_rest.y = self.Y_POS
        self.step_index += 1
        self.dino_run = False
        
    def duck(self):
        
        if self.step_index < 5:
            self.image = DUCKING[0]
        else:
            self.image = DUCKING[1]
        
        self.dino_rest.y = self.Y_POS + self.Y_DUCK
        self.step_index += 1
        self.dino_duck = False
        
    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rest.y -= self.jump_vel * 4
            self.jump_vel -= 0.8 # controlamos estos valores para poder conseguir un numero negativo y asi poder cambiar de posicion
        if self.jump_vel < -self.JUMP_VEL :# si es menor al valor negativo del global
            self.dino_rest.y = self.Y_POS# se altera estado en Y
            self.dino_jump = False 
            self.jump_vel = self.JUMP_VEL # se vuelve al estado jump vel inicial