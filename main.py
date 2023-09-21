import pygame
import pygame_menu
import os
from game import Game
from trainer import run_neat, run_with_best_genome

pygame.init()

screenWidth = 600
screenHeight = 600

draw_net = False

save_model_name = 'train_model.pkl'

screen = pygame.display.set_mode((screenWidth, screenHeight))


def play_game():
    game = Game(screen=screen, screenWidth=screenWidth, screenHeight=screenHeight)
    game.loop()
    

def train_model():
    run_neat(save_model_name=save_model_name, generations=10, screen=screen, screenWidth=screenWidth, screenHeight=screenHeight, draw_net=draw_net)
    

def load_model():
    if os.path.exists(os.path.join(os.getcwd(), save_model_name)):
        run_with_best_genome(screen=screen, screenWidth=screenWidth, screenHeight=screenHeight, file_name=save_model_name)


def set_draw(value, difficulty):
    global draw_net
    if value[1] == 1:
        draw_net = True
    else:
        draw_net = False
    

def create_menu():
    menu = pygame_menu.Menu('Flappy AI', screenWidth, screenHeight, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', play_game)
    menu.add.selector('Draw net: ', [('False', False), ('True', True)], onchange=set_draw)
    menu.add.button('Train model', train_model)
    menu.add.button('Load trained model', load_model)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    
    menu.mainloop(screen)
    
    

if __name__ == "__main__":
    
    create_menu()
    
    






