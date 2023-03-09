import random

import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer


class PowerUpManager:
    
    def __init__(self):
        self.power_ups = []
        self.when_appers = 0
        self.points = 0
        self.options_number = list(range(1, 10))
        self.type_powerup = None
            
    def reset_power_ups(self, points):
        self.power_ups = []
        self.points = points
        #self.when_appers = random.randint(200, 300) + self.points
        self.when_appers = random.randint(200, 300)
        
    def generate_power_ups(self, points):
        #ran = random.randint(0, 1)
        ran = 1 # modi
        self.points = points
        if len(self.power_ups) == 0:
            if self.when_appers == self.points:
                print("generating powerup")
                if ran == 0:
                    self.power_ups.append(Shield())
                elif ran == 1:
                    self.power_ups.append(Hammer())
                self.type_powerup = ran
                self.when_appers = random.randint(self.when_appers + 200, 500 + self.when_appers)
        return self.power_ups
    
    def update(self, points, game_speed, player, screen):
        self.generate_power_ups(points)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rest.colliderect(power_up.rect):
                if self.type_powerup == 0:
                    player.shield = True
                elif self.type_powerup == 1:
                    player.hammer = True
                power_up.start_time = pygame.time.get_ticks()
                time_random = random.randrange(5, 8)
                player.powerup_time_up = power_up.start_time + (time_random *1000)
                player.type = power_up.type
                player.show_text = True
                self.power_ups.remove(power_up)
    
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)