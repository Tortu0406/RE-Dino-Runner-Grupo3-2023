from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD, RUNNING_SHIELD, JUMPING_SHIELD, COLORS, HAMMER_TYPE,DUCKING_HAMMER, JUMPING_HAMMER, RUNNING_HAMMER, HAMMER_WEAPON, HAMMER
import pygame
from dino_runner.components import text_utils
class Dino(Sprite):
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8
    Y_DUCK = 35
    LIVES = 3
    def __init__(self):
        self.run_img = {
            DEFAULT_TYPE: RUNNING, 
            SHIELD_TYPE: RUNNING_SHIELD,
            HAMMER_TYPE: RUNNING_HAMMER
            }
        self.duck_img = {
            DEFAULT_TYPE: DUCKING, 
            SHIELD_TYPE: DUCKING_SHIELD,
            HAMMER_TYPE: DUCKING_HAMMER
            }
        self.jump_img = {
            DEFAULT_TYPE: JUMPING, 
            SHIELD_TYPE: JUMPING_SHIELD,
            HAMMER_TYPE: JUMPING_HAMMER
            }
        self.type = DEFAULT_TYPE
        self.step_index = 0
        self.image = self.run_img[self.type][0]
        self.dino_rest = self.image.get_rect()
        self.image_hammer = HAMMER
        self.rect_hammer = self.image_hammer.get_rect()
        self.rect_hammer.x = 100
        self.rect_hammer.y = 310
        self.dino_rest.x = self.X_POS
        self.dino_rest.y = self.Y_POS
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.lives = self.LIVES
        self.setup_state_booleans()
        
        
    def setup_state_booleans(self):
        self.has_powerup = False
        self.shield = False
        self.show_text = False
        self.powerup_time_up = 0
        self.hammer = False
        self.hammer_time_up = 0
    
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
        if self.hammer:
            screen.blit(self.image_hammer, (self.rect_hammer.x, self.rect_hammer.y))
            self.rect_hammer.x += 10
        else:
            self.rect_hammer.x = 0
        screen.blit(self.image, (self.dino_rest.x, self.dino_rest.y))
        
    
    def run(self):
        if self.step_index < 5:
            self.image = self.run_img[self.type][0]
        else:
            self.image = self.run_img[self.type][1]
        
        self.dino_rest.x = self.X_POS
        self.dino_rest.y = self.Y_POS
        self.step_index += 1
        self.dino_run = False
        
    def duck(self):
        
        if self.step_index < 5:
            self.image = self.duck_img[self.type][0]
        else:
            self.image = self.duck_img[self.type][1]
        
        self.dino_rest.y = self.Y_POS + self.Y_DUCK
        self.step_index += 1
        self.dino_duck = False
        
    def jump(self):
        self.image = self.jump_img[self.type]
        if self.dino_jump:
            self.dino_rest.y -= self.jump_vel * 4
            self.jump_vel -= 0.8 # controlamos estos valores para poder conseguir un numero negativo y asi poder cambiar de posicion
        if self.jump_vel < -self.JUMP_VEL :# si es menor al valor negativo del global
            self.dino_rest.y = self.Y_POS# se altera estado en Y
            self.dino_jump = False 
            self.jump_vel = self.JUMP_VEL # se vuelve al estado jump vel inicial
            
    def check_invincibility(self, screen, color):
        time_to_show = round((self.powerup_time_up - pygame.time.get_ticks())/ 1000, 2)
        if self.shield:
            if time_to_show >= 0:
                if self.show_text:
                    text, text_rect = text_utils.get_power_up_message(color, time_to_show)
                    screen.blit(text, text_rect)
            else:
                self.shield = False
                self.update_to_default(SHIELD_TYPE)
        if self.hammer:
            if time_to_show >= 0:
                if self.show_text:
                    text, text_rect = text_utils.get_power_up_message(color, time_to_show)
                    screen.blit(text, text_rect)
            else:
                self.hammer = False
                self.update_to_default(HAMMER_TYPE)
        
    def update_to_default(self, current_type):
        if self.type == current_type:
            self.type = DEFAULT_TYPE