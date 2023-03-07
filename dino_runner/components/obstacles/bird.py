import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD


class Bird(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)
        self.rect.y = 265
        self.step_index = 0
        
    def update(self, game_speed, obstacles):
        self.fly()
        if self.step_index >= 10:
            self.step_index = 0
        return super().update(game_speed, obstacles)
    
    def fly(self):
        if self.step_index < 5:
            self.image = BIRD[0]
        else:
            self.image = BIRD[1]
        
        self.step_index += 1