import pygame
import os
import random
from bird import Bird
from pipe import Pipe


class Game:
    
    def __init__(self, screen, screenWidth, screenHeight, genome=None, config=None):
        self.screen = screen
        self.width = screenWidth
        self.height = screenHeight
        self.config = config
        
        self.genome = genome
        
        self.colors = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'white': (255, 255, 255),
            'purple': (128, 0, 128)
        }
        
        bg_path = os.path.join(os.getcwd(), 'images', 'bg.jpg')
        background = pygame.image.load(bg_path)
        
        self.background_image = pygame.transform.scale(background, (self.width, self.height))
    
    
    def update(self):
        pygame.display.flip()
        
    
    def draw_score(self, score):
        font = pygame.font.Font(None, 36)
        score_surface = font.render(f"Score: {score}", True, self.colors['white'])
        score_rect = score_surface.get_rect(topleft=(10, 10))
        self.screen.blit(score_surface, score_rect)
        
    
    def get_game_state(self, bird, bottom_pipe, top_pipe, spawn_interval):
        bird_velocity = bird.velocity
        bird_y = bird.y
        distance_to_bottom_pipe_x = bottom_pipe.x - bird.x
        distance_to_bottom_pipe_y = bird.y - bottom_pipe.y
        
        distance_to_top_pipe_y = top_pipe.y + top_pipe.height - bird.y
        
        return [bird_velocity, bird_y, distance_to_bottom_pipe_x, distance_to_bottom_pipe_y, distance_to_top_pipe_y]
    
    
    def determine_jump(self, action_outputs):
        max_value_index = action_outputs.index(max(action_outputs))
        
        if max_value_index == 0:
            return True
        
        else:
            return False
        
    
    def extract_neurons(self, genome):
        return list(genome.nodes.values())
            
    
    def extract_connections(self, genome):
        return list(genome.connections.values())
    
    
    def draw_net_with_pygame(self, node_names=None, show_disabled=True, node_colors=None):
        node_radius = 20
        margin = 30
        vertical_gap = 40
        line_width = 2

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        num_inputs = len(self.config.genome_config.input_keys)
        num_outputs = len(self.config.genome_config.output_keys)

        node_positions = {}

        start_y_input = (screen_height - (num_inputs * (node_radius * 2 + vertical_gap))) // 2
        for i, key in enumerate(self.config.genome_config.input_keys):
            x = margin
            y = start_y_input + i * (node_radius * 2 + vertical_gap) + node_radius
            node_positions[key] = (x, y)

        start_y_output = (screen_height - (num_outputs * (node_radius * 2 + vertical_gap))) // 2
        for i, key in enumerate(self.config.genome_config.output_keys):
            x = screen_width - margin
            y = start_y_output + i * (node_radius * 2 + vertical_gap) + node_radius
            node_positions[key] = (x, y)

        hidden_nodes = [k for k in self.genome.nodes.keys() if k not in self.config.genome_config.input_keys and k not in self.config.genome_config.output_keys]
        start_y_hidden = (screen_height - (len(hidden_nodes) * (node_radius * 2 + vertical_gap))) // 2
        middle_x = screen_width // 2
        for i, key in enumerate(hidden_nodes):
            y = start_y_hidden + i * (node_radius * 2 + vertical_gap) + node_radius
            node_positions[key] = (middle_x, y)

        for key, (x, y) in node_positions.items():
            pygame.draw.circle(self.screen, self.colors['white'], (x, y), node_radius)

        for cg in self.genome.connections.values():
            if cg.enabled or show_disabled:
                input, output = cg.key
                start_pos = node_positions[input]
                end_pos = node_positions[output]
                normalized_weight = abs(cg.weight) / 1.0  
                width = int(1 + normalized_weight * 2)

                color = self.colors['green'] if cg.weight > 0 else self.colors['red']  # green for positive, red for negative
                
                pygame.draw.line(self.screen, color, start_pos, end_pos, width)

        pygame.display.update()

    
    def loop(self, player='human', net=None, showcase=False, draw_net=False):
        
        clock = pygame.time.Clock()
        
        state = True
        
        clock_speed = 60
        
        
        #bird settings
        bird_starting_cords = (self.width // 2, self.height // 2)
        bird_size = 10
        gravity = 0.5
        jump_power = 10
        
        bird = Bird(screen=self.screen, color=self.colors['yellow'], center=bird_starting_cords, radius=bird_size)
        
        
        #pipe settings
        pipe_width = 60
        pipe_height = 320
        pipe_speed = 5
        first_pipe_x = self.width // 2 + 280
        first_pipe_y = self.height - pipe_height
        first_pipe_cords = (first_pipe_x, first_pipe_y)
        gap_between_pipes = 150
        top_pipe_height = self.height - pipe_height - gap_between_pipes
        top_pipe_cords = (first_pipe_x, 0)

        top_pipe = Pipe(screen=self.screen, cords=top_pipe_cords, color=self.colors['blue'], width=pipe_width, height=top_pipe_height, speed=pipe_speed, is_top=True)
        bot_pipe = Pipe(screen=self.screen, cords=first_pipe_cords, color=self.colors['blue'], width=pipe_width, height=pipe_height, speed=pipe_speed)
        
        pipes = [bot_pipe, top_pipe]
        
        margin = bird_size * 2
        
        
        pipe_spawn_interval = 2000
        elapsed_since_last_pipe = 0
        
        pipe_min_height = max(50, bird_size * 2)
        pipe_max_height = self.height / 2 - gap_between_pipes / 2 + 30
        
        #score and rewards
        score = 0
        reward = 0

        while state:
            
            dt = clock.tick(clock_speed)
            elapsed_since_last_pipe += dt
            pipe_max_height = self.height - margin * 2
            max_bottom_pipe_height = 450
            bottom_pipe_height = random.randint(pipe_min_height, min(pipe_max_height, max_bottom_pipe_height))
            top_pipe_y = self.height - bottom_pipe_height - gap_between_pipes

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = False
                    
                if player == 'human':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            bird.jump(jump_power)
            
            
            if player == 'ai':
                if len(pipes) >= 2:
                    inputs = self.get_game_state(bird=bird, bottom_pipe=pipes[0], top_pipe=pipes[1], spawn_interval=pipe_spawn_interval)
                    action_outputs = net.activate(inputs)
                    determine_jump = self.determine_jump(action_outputs)

                    if determine_jump:
                        bird.jump(jump_power)

            
            bird_current_x, bird_current_y = bird.get_current_position()
            
            if bird_current_y >= self.height or bird_current_y <= 0:
                reward -= 1
                state = False
            
            if elapsed_since_last_pipe >= pipe_spawn_interval:
                elapsed_since_last_pipe = 0
                first_pipe_x = self.width
                bottom_pipe = Pipe(screen=self.screen, cords=(first_pipe_x, self.height - bottom_pipe_height), color=self.colors['blue'], width=pipe_width, height=bottom_pipe_height, speed=pipe_speed)
                top_pipe = Pipe(screen=self.screen, cords=(first_pipe_x, 0), color=self.colors['blue'], width=pipe_width, height=self.height - bottom_pipe_height - gap_between_pipes, speed=pipe_speed, is_top=True)

                pipes.append(bottom_pipe) 
                pipes.append(top_pipe)

            
            self.screen.blit(self.background_image, (0, 0))
            
            #bird methods
            bird.apply_gravity(gravity=gravity)
            bird.draw()
            
            
            #pipe methods
            for pipe in pipes:
                pipe.move()
                pipe.draw()
                
                #collision
                if bird.rect.colliderect(pipe.rect):
                    reward -= 1
                    state = False
                    
               
                if bird_current_x > pipe.x + pipe_width and not pipe.passed:
                    pipe.passed = True
                    score += 0.5
                    reward += 0.5
                    
            self.draw_score(score=int(score))
                
            #clearing the list of pipes
            pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]
            
            if self.genome and player == 'ai' and not showcase and draw_net:
                self.draw_net_with_pygame()
            
            
            self.update()
            
        return reward
            
            