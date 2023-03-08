import time
import pygame
from dino_runner.components.dino import Dino
from dino_runner.components.obstacles.obstaclemanager import ObstacleManager
from dino_runner.components import text_utils
from dino_runner.utils.constants import BG, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, CLOUD


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
        self.runing = True
        self.death_count = 0
        self.x_pos_cloud = 0
        self.y_pos_cloud = 200
    def run(self):
        # Game loop: events - update - draw
        self.START = time.time()
        self.playing = True
        self.points = 0
        self.game_speed = 20
        self.obstacle_manager.reset_obstacles()
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

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))    
        self.draw_background()
        self.player.draw(self.screen)
        self.score()
        self.obstacle_manager.draw(self.screen)
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
            text, text_rect = text_utils.get_centered_message("Press any Key to start")
            self.screen.blit(text, text_rect)
        else:
            text, text_rect = text_utils.get_centered_message(f" You have {self.death_count} deaths and {self.points} points on this {self.death_count}º round")
            self.screen.blit(text, text_rect)
            minutes = 0
            if int(self.END - self.START) > 59:
                minutes += 1
            text, text_rect = text_utils.get_centered_message(f"Time {minutes} minutes and {int((self.END - self.START)//1)} seconds", 150, 100, 16)
            self.screen.blit(text, text_rect)
        self.screen.blit(RUNNING[0], ((SCREEN_WIDTH // 2) - 50 , 370))
        
        
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
        text, text_rect = text_utils.get_score_element(self.points)
        self.screen.blit(text, text_rect)