import pygame

from dino_runner.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

FONT_STYLE = "freesansbold.ttf"
colors = [
    (0, 0, 0),
    (255, 255, 255)
]
def get_score_element(message, points, width = 1000, height = 50, color = 1):
    font = pygame.font.Font(FONT_STYLE, 16)
    text = font.render(message + str(points), True, colors[color])
    text_rect = text.get_rect()
    text_rect.center = (width, height)
    return text, text_rect

def get_centered_message(message, width = SCREEN_WIDTH//2, height = SCREEN_HEIGHT//2, font_size = 32):
    font = pygame.font.Font(FONT_STYLE, font_size)
    text = font.render(message, True, colors[0])
    text_rect = text.get_rect()
    text_rect.center = (width, height)
    return text, text_rect

def get_power_up_message(color, time_to_show):
    font = pygame.font.Font(FONT_STYLE, 16)
    text = font.render(f"Power Up enabled for {time_to_show}", True, colors[color])
    textReact = text.get_rect()
    textReact.center = (500, 40)
    return text, textReact