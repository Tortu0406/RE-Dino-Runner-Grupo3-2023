import time
import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
import random

class ObstacleManager:
    
    def __init__(self):
        self.obstacles = []
    def update(self, game):
        ran = random.randint(0,2)
        if len(self.obstacles) == 0:
            if ran == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif ran == 1:
                large = Cactus(LARGE_CACTUS)
                large.rect.y = large.POS_Y_LARGE
                self.obstacles.append(large)
                
            else:
                self.obstacles.append(Bird(BIRD, random.randint(220, 300)))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rest.colliderect(obstacle.rect):
                if not game.player.shield:
                    pygame.time.delay(1000)
                    game.playing = False
                    game.death_count += 1
                    game.END = time.time()
                    break
                else:
                    self.obstacles.remove(obstacle)
            
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            
    def reset_obstacles(self):
        self.obstacles = []