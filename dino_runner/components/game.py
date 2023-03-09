import random
import time
import pygame
from dino_runner.components.dino import Dino
from dino_runner.components.obstacles.obstaclemanager import ObstacleManager
from dino_runner.components import text_utils
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD, DINO_STATE


class Game:
    START = 0
    END = 0
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dino()
        self.obstacle_manager = ObstacleManager()
        self.points = 0
        self.points_history = []
        self.runing = True
        self.death_count = 0
        self.x_pos_cloud = SCREEN_WIDTH
        self.y_pos_cloud_a = 200
        self.y_pos_cloud_b = 125
        self.y_pos_cloud_c = 267
        self.power_up_manager = PowerUpManager()
        self.high_point = 0
        
    def run(self):
        # Game loop: events - update - draw
        self.START = time.time()
        self.create_component()
        self.playing = True
        self.points = 0
        self.x_pos_cloud = SCREEN_WIDTH
        self.game_speed = 20
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))    
        self.draw_background()
        self.player.draw(self.screen)
        self.score()
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
        self.screen.blit(CLOUD, (self.x_pos_cloud, self.y_pos_cloud_a))
        self.screen.blit(CLOUD, (self.x_pos_cloud + 350, self.y_pos_cloud_b))
        self.screen.blit(CLOUD, (self.x_pos_cloud + 650, self.y_pos_cloud_c))
        if self.x_pos_cloud +650 <= - CLOUD.get_width():
            self.x_pos_cloud = SCREEN_WIDTH
            self.y_pos_cloud_a = random.randint(100, 300)
            self.y_pos_cloud_b = random.randint(100, 300)
            self.y_pos_cloud_c = random.randint(100, 300)
        self.x_pos_cloud -= self.game_speed -15
        
        
    def execute(self):
        while self.runing:
            if not self.playing:
                self.show_menu()
            
    def show_menu(self):
        self.runing = True
        white_color = (255,255,255)
        self.screen.fill(white_color)
        self.print_menu_elements()
        pygame.display.update()
        self.handle_key_events_on_menu()
        
    def print_menu_elements(self):
        if self.death_count == 0:
            text, text_rect = text_utils.get_centered_message("Press any Key to start", font_size= 25)
            self.screen.blit(text, text_rect)
        else:
            if self.points > self.high_point:
                self.high_point = self.points
            text, text_rect = text_utils.get_centered_message(f" You have {self.death_count} deaths and {self.points} points on this {self.death_count}º round", font_size=20)
            self.screen.blit(text, text_rect)
            minutes = 0
            if int(self.END - self.START) > 59:
                minutes += 1
            text, text_rect = text_utils.get_centered_message(f"Time {minutes} minutes and {int((self.END - self.START)//1)} seconds", 150, 100, 16)
            self.screen.blit(text, text_rect)
        self.screen.blit(DINO_STATE[0], (80, 310))
        
        
    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runing = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()
                
    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        text, text_rect = text_utils.get_score_element("Points: ", self.points)
        self.screen.blit(text, text_rect)
        text, text_rect = text_utils.get_score_element("High Score: ",self.high_point, 880)
        self.screen.blit(text, text_rect)
        self.player.check_invincibility(self.screen)
    
    def create_component(self):
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.points)