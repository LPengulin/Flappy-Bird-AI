import neat
import pickle
import os
from game import Game
from functools import partial

config_path = 'config-feedforward.txt'
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)


def eval_genomes(genomes, config, screen, screenWidth, screenHeight, draw_net):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game(screen=screen, screenWidth=screenWidth, screenHeight=screenHeight, genome=genome, config=config)
        fitness = game.loop(player='ai', net=net, draw_net=draw_net)
        genome.fitness = fitness


def run_neat(save_model_name, generations, screen, screenWidth, screenHeight, config=config, draw_net=False):
 

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    
    eval_function_with_screen = partial(eval_genomes, screen=screen, screenWidth=screenWidth, screenHeight=screenHeight, draw_net=draw_net)
    
    winner = p.run(eval_function_with_screen, generations)
    
    with open(save_model_name, 'wb') as output:
        pickle.dump(winner, output, 1)
        
    return winner



def run_with_best_genome(screen, screenWidth, screenHeight, config=config, file_name='best_genome.pkl'):
    with open(file_name, 'rb') as input_file:
        best_genome = pickle.load(input_file)
        
    net = neat.nn.FeedForwardNetwork.create(best_genome, config=config)
    game = Game(screen=screen, screenWidth=screenWidth, screenHeight=screenHeight, genome=best_genome)
    game.loop(player='ai', net=net, showcase=True)