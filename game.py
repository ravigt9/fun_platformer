import eel
import random
import time

# Initialize eel with web files directory
eel.init('web')

class Game:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.width = 800
        self.height = 400
        self.ground_y = 300
        
        # Player properties
        self.player = {
            'x': 50,
            'y': self.ground_y,
            'width': 40,
            'height': 40,
            'velocity_y': 0,
            'jump_power': -15,
            'gravity': 0.8,
            'is_jumping': False
        }
        
        # Game properties
        self.obstacles = []
        self.base_obstacle_speed = 5
        self.obstacle_speed = self.base_obstacle_speed
        self.spawn_timer = 0
        self.base_min_spawn_interval = 45
        self.base_max_spawn_interval = 90
        self.min_spawn_interval = self.base_min_spawn_interval
        self.max_spawn_interval = self.base_max_spawn_interval
        self.spawn_interval = random.randint(self.min_spawn_interval, self.max_spawn_interval)
        self.score = 0
        self.game_over = False
        self.level = 0
        self.multi_obstacle_chance = 0  # Chance to spawn multiple obstacles at once

    def generate_obstacle(self):
        # Different types of obstacles
        obstacle_types = [
            # Standard block
            lambda: {
                'x': self.width,
                'y': self.ground_y - random.randint(20, 40),
                'width': random.randint(30, 50),
                'height': random.randint(30, 50),
                'type': 'rectangle'
            },
            # Tall thin obstacle
            lambda: {
                'x': self.width,
                'y': self.ground_y - random.randint(60, 80),
                'width': random.randint(20, 30),
                'height': random.randint(60, 80),
                'type': 'rectangle'
            },
            # Wide low obstacle
            lambda: {
                'x': self.width,
                'y': self.ground_y - random.randint(20, 30),
                'width': random.randint(60, 80),
                'height': random.randint(20, 30),
                'type': 'rectangle'
            },
            # Triangle
            lambda: {
                'x': self.width,
                'y': self.ground_y,
                'width': random.randint(40, 60),
                'height': random.randint(40, 60),
                'type': 'triangle'
            }
        ]
        
        obstacles_to_generate = []
        
        # Randomly select an obstacle type
        main_obstacle = random.choice(obstacle_types)()
        obstacles_to_generate.append(main_obstacle)
        
        # Chance to add additional obstacles based on multi_obstacle_chance
        if random.random() < self.multi_obstacle_chance:
            # Calculate minimum gap based on player size (125% of player width)
            min_obstacle_gap = self.player['width'] * 1.25
            
            # Add a second obstacle with proper spacing
            second_obstacle = random.choice(obstacle_types)()
            # Ensure the gap is at least min_obstacle_gap plus the width of the first obstacle
            gap = max(min_obstacle_gap, random.randint(100, 150))
            second_obstacle['x'] = self.width + gap + main_obstacle['width']
            obstacles_to_generate.append(second_obstacle)
        
        # Ensure minimum gap from previous obstacles
        min_gap = max(120, self.player['width'] * 1.25)  # Use larger of default or player-based gap
        if self.obstacles:
            last_obstacle = self.obstacles[-1]
            if self.width - last_obstacle['x'] < min_gap:
                return None
                
        return obstacles_to_generate
        
    def jump(self):
        if not self.player['is_jumping']:
            self.player['velocity_y'] = self.player['jump_power']
            self.player['is_jumping'] = True
    
    def update(self):
        if self.game_over:
            return

        # Update player
        self.player['y'] += self.player['velocity_y']
        self.player['velocity_y'] += self.player['gravity']
        
        # Ground collision
        if self.player['y'] >= self.ground_y:
            self.player['y'] = self.ground_y
            self.player['velocity_y'] = 0
            self.player['is_jumping'] = False
        
        # Update obstacles
        for obstacle in self.obstacles:
            obstacle['x'] -= self.obstacle_speed
        
        # Remove off-screen obstacles
        self.obstacles = [obs for obs in self.obstacles if obs['x'] > -obs['width']]
        
        # Spawn new obstacles
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            new_obstacles = self.generate_obstacle()
            if new_obstacles:
                self.obstacles.extend(new_obstacles)
            # Randomize next spawn interval
            self.spawn_interval = random.randint(self.min_spawn_interval, self.max_spawn_interval)
        
        # Check collisions
        player_rect = (self.player['x'], self.player['y'], 
                      self.player['width'], self.player['height'])
        
        for obstacle in self.obstacles:
            if obstacle['type'] == 'rectangle':
                obstacle_rect = (obstacle['x'], obstacle['y'],
                               obstacle['width'], obstacle['height'])
                if self.check_collision(player_rect, obstacle_rect):
                    self.game_over = True
                    return
            elif obstacle['type'] == 'triangle':
                if self.check_triangle_collision(player_rect, obstacle):
                    self.game_over = True
                    return
        
        # Increase difficulty every 1000 points
        new_level = self.score // 500
        if new_level > self.level:
            self.level = new_level
            # Increase speed (max 15)
            self.obstacle_speed = min(15, self.base_obstacle_speed + (self.level * 0.8))
            
            # Decrease spawn intervals (min 20)
            self.min_spawn_interval = max(20, self.base_min_spawn_interval - (self.level * 3))
            self.max_spawn_interval = max(40, self.base_max_spawn_interval - (self.level * 5))
            
            # Increase chance of multiple obstacles (max 0.4 or 40% chance)
            self.multi_obstacle_chance = min(0.4, self.level * 0.08)
        
        # Update score
        self.score += 1
    
    def check_collision(self, rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def check_triangle_collision(self, player_rect, triangle):
        # Simplified triangle collision - treat it as a rectangle for now
        # but only use the top half of the height for better gameplay
        triangle_rect = (triangle['x'], 
                        triangle['y'] - triangle['height'],
                        triangle['width'],
                        triangle['height'] // 2)
        return self.check_collision(player_rect, triangle_rect)
    
    def get_state(self):
        return {
            'player': self.player,
            'obstacles': self.obstacles,
            'score': self.score,
            'game_over': self.game_over
        }

# Create game instance
game = Game()

@eel.expose
def jump():
    game.jump()

@eel.expose
def restart_game():
    game.reset_game()

def game_loop():
    while True:
        game.update()
        eel.updateGame(game.get_state())()
        time.sleep(1/60)  # 60 FPS

# Start the game loop in a separate thread
eel.spawn(game_loop)

# Start the application
eel.start('index.html', size=(800, 400))