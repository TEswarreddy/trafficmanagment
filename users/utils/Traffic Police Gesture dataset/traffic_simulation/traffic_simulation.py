import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
ROAD_WIDTH = 80
LANE_WIDTH = ROAD_WIDTH // 2
VEHICLE_WIDTH = 40
VEHICLE_HEIGHT = 60
SPAWN_RATE = 0.05  # Probability of spawning a vehicle each frame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

class TrafficLight:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 'horizontal' or 'vertical'
        self.state = 'RED'  # RED, YELLOW, GREEN, LEFT_GREEN, RIGHT_GREEN
        self.timer = 0
        self.cycle_time = 300  # frames
        
    def update(self, gesture_signal=None):
        if gesture_signal and gesture_signal != "UNKNOWN":
            self.state = gesture_signal
            self.timer = 0
        else:
            self.timer += 1
            if self.timer >= self.cycle_time:
                self.timer = 0
                # Cycle through states
                if self.state == 'GREEN':
                    self.state = 'YELLOW'
                elif self.state == 'YELLOW':
                    self.state = 'RED'
                elif self.state == 'RED':
                    self.state = 'GREEN'
        
    def draw(self, screen):
        # Draw traffic light base
        if self.direction == 'horizontal':
            pygame.draw.rect(screen, BLACK, (self.x - 15, self.y - 45, 30, 90))
        else:
            pygame.draw.rect(screen, BLACK, (self.x - 45, self.y - 15, 90, 30))
        
        # Draw lights
        states = ['RED', 'YELLOW', 'GREEN']
        colors = [RED, YELLOW, GREEN]
        
        for i, (state, color) in enumerate(zip(states, colors)):
            if self.direction == 'horizontal':
                light_x = self.x - 10
                light_y = self.y - 35 + i * 30
            else:
                light_x = self.x - 35 + i * 30
                light_y = self.y - 10
            
            # Draw light background
            pygame.draw.circle(screen, GRAY, (light_x, light_y), 8)
            
            # Draw active light
            if (state == 'RED' and self.state in ['RED', 'YELLOW']) or \
               (state == 'YELLOW' and self.state == 'YELLOW') or \
               (state == 'GREEN' and self.state in ['GREEN', 'LEFT_GREEN', 'RIGHT_GREEN']):
                pygame.draw.circle(screen, color, (light_x, light_y), 6)
        
        # Draw arrow indicators for turn signals
        if self.state in ['LEFT_GREEN', 'RIGHT_GREEN']:
            arrow_color = GREEN
            if self.direction == 'horizontal':
                if self.state == 'LEFT_GREEN':
                    points = [(self.x - 20, self.y), (self.x, self.y - 10), (self.x, self.y + 10)]
                else:
                    points = [(self.x + 20, self.y), (self.x, self.y - 10), (self.x, self.y + 10)]
            else:
                if self.state == 'LEFT_GREEN':
                    points = [(self.x, self.y - 20), (self.x - 10, self.y), (self.x + 10, self.y)]
                else:
                    points = [(self.x, self.y + 20), (self.x - 10, self.y), (self.x + 10, self.y)]
            
            pygame.draw.polygon(screen, arrow_color, points)

class Vehicle:
    def __init__(self, x, y, direction, speed, color=None):
        self.x = x
        self.y = y
        self.direction = direction  # 'up', 'down', 'left', 'right'
        self.speed = speed
        self.color = color or random.choice(COLORS)
        self.stopped = False
        self.turning = None  # 'left', 'right', or None
        self.turn_progress = 0
        
    def update(self, traffic_lights):
        if self.stopped:
            return
            
        # Check if vehicle should stop at traffic light
        for light in traffic_lights:
            if self.should_stop_at_light(light):
                self.stopped = True
                return
        
        self.stopped = False
        
        # Move vehicle
        if self.turning:
            self.execute_turn()
        else:
            # Decide if vehicle should turn (random chance)
            if random.random() < 0.005:  # 0.5% chance per frame to start turning
                self.turning = random.choice(['left', 'right'])
                self.turn_progress = 0
            
            # Normal movement
            if self.direction == 'up':
                self.y -= self.speed
            elif self.direction == 'down':
                self.y += self.speed
            elif self.direction == 'left':
                self.x -= self.speed
            elif self.direction == 'right':
                self.x += self.speed
        
        # Remove vehicles that go off screen
        return (0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT)
    
    def should_stop_at_light(self, light):
        distance_threshold = 50
        
        if light.direction == 'horizontal' and self.direction in ['up', 'down']:
            if abs(self.x - light.x) < distance_threshold and abs(self.y - light.y) < distance_threshold:
                if light.state == 'RED':
                    return True
                elif light.state == 'YELLOW' and abs(self.y - light.y) < 100:
                    return True
                elif light.state in ['LEFT_GREEN', 'RIGHT_GREEN']:
                    if self.turning:
                        if (self.turning == 'left' and light.state != 'LEFT_GREEN') or \
                           (self.turning == 'right' and light.state != 'RIGHT_GREEN'):
                            return True
                    else:
                        return True
        
        elif light.direction == 'vertical' and self.direction in ['left', 'right']:
            if abs(self.x - light.x) < distance_threshold and abs(self.y - light.y) < distance_threshold:
                if light.state == 'RED':
                    return True
                elif light.state == 'YELLOW' and abs(self.x - light.x) < 100:
                    return True
                elif light.state in ['LEFT_GREEN', 'RIGHT_GREEN']:
                    if self.turning:
                        if (self.turning == 'left' and light.state != 'LEFT_GREEN') or \
                           (self.turning == 'right' and light.state != 'RIGHT_GREEN'):
                            return True
                    else:
                        return True
        
        return False
    
    def execute_turn(self):
        turn_radius = 30
        self.turn_progress += self.speed
        
        if self.turning == 'left':
            if self.direction == 'up':
                angle = math.radians(self.turn_progress)
                self.x -= turn_radius * (1 - math.cos(angle))
                self.y -= turn_radius * math.sin(angle)
                if self.turn_progress >= 90:
                    self.direction = 'left'
                    self.turning = None
            elif self.direction == 'right':
                angle = math.radians(self.turn_progress)
                self.x += turn_radius * math.sin(angle)
                self.y += turn_radius * (1 - math.cos(angle))
                if self.turn_progress >= 90:
                    self.direction = 'up'
                    self.turning = None
            # Add other turn cases as needed
        elif self.turning == 'right':
            if self.direction == 'up':
                angle = math.radians(self.turn_progress)
                self.x += turn_radius * (1 - math.cos(angle))
                self.y -= turn_radius * math.sin(angle)
                if self.turn_progress >= 90:
                    self.direction = 'right'
                    self.turning = None
            # Add other turn cases as needed
    
    def draw(self, screen):
        # Draw vehicle body
        if self.direction in ['up', 'down']:
            rect = pygame.Rect(self.x - VEHICLE_WIDTH//2, self.y - VEHICLE_HEIGHT//2, 
                             VEHICLE_WIDTH, VEHICLE_HEIGHT)
        else:
            rect = pygame.Rect(self.x - VEHICLE_HEIGHT//2, self.y - VEHICLE_WIDTH//2, 
                             VEHICLE_HEIGHT, VEHICLE_WIDTH)
        
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        
        # Draw direction indicator if turning
        if self.turning:
            indicator_color = YELLOW
            if self.turning == 'left':
                points = [(self.x - 10, self.y), (self.x, self.y - 5), (self.x, self.y + 5)]
            else:
                points = [(self.x + 10, self.y), (self.x, self.y - 5), (self.x, self.y + 5)]
            pygame.draw.polygon(screen, indicator_color, points)

class TrafficSimulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Traffic Signal Simulation with Hand Gesture Control")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create traffic lights at intersection
        self.traffic_lights = [
            TrafficLight(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100, 'horizontal'),  # Top
            TrafficLight(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100, 'horizontal'),  # Bottom
            TrafficLight(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 'vertical'),    # Left
            TrafficLight(SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2, 'vertical')     # Right
        ]
        
        self.vehicles = []
        self.spawn_points = self.create_spawn_points()
        
    def create_spawn_points(self):
        return [
            # Top spawn points (going down)
            {'x': SCREEN_WIDTH//2 - LANE_WIDTH, 'y': -50, 'direction': 'down', 'speed': 3},
            {'x': SCREEN_WIDTH//2 + LANE_WIDTH, 'y': -50, 'direction': 'down', 'speed': 2},
            # Bottom spawn points (going up)
            {'x': SCREEN_WIDTH//2 - LANE_WIDTH, 'y': SCREEN_HEIGHT + 50, 'direction': 'up', 'speed': 3},
            {'x': SCREEN_WIDTH//2 + LANE_WIDTH, 'y': SCREEN_HEIGHT + 50, 'direction': 'up', 'speed': 2},
            # Left spawn points (going right)
            {'x': -50, 'y': SCREEN_HEIGHT//2 - LANE_WIDTH, 'direction': 'right', 'speed': 3},
            {'x': -50, 'y': SCREEN_HEIGHT//2 + LANE_WIDTH, 'direction': 'right', 'speed': 2},
            # Right spawn points (going left)
            {'x': SCREEN_WIDTH + 50, 'y': SCREEN_HEIGHT//2 - LANE_WIDTH, 'direction': 'left', 'speed': 3},
            {'x': SCREEN_WIDTH + 50, 'y': SCREEN_HEIGHT//2 + LANE_WIDTH, 'direction': 'left', 'speed': 2}
        ]
    
    def spawn_vehicle(self):
        if random.random() < SPAWN_RATE and len(self.vehicles) < 50:
            spawn_point = random.choice(self.spawn_points)
            self.vehicles.append(Vehicle(
                spawn_point['x'],
                spawn_point['y'],
                spawn_point['direction'],
                spawn_point['speed']
            ))
    
    def draw_roads(self):
        # Draw background
        self.screen.fill(WHITE)
        
        # Draw roads
        # Horizontal road
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_HEIGHT//2 - ROAD_WIDTH//2, 
                                           SCREEN_WIDTH, ROAD_WIDTH))
        # Vertical road
        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH//2 - ROAD_WIDTH//2, 0,
                                           ROAD_WIDTH, SCREEN_HEIGHT))
        
        # Draw lane markings
        lane_mark_length = 20
        lane_mark_gap = 10
        
        # Horizontal lane markings
        for x in range(0, SCREEN_WIDTH, lane_mark_length + lane_mark_gap):
            pygame.draw.rect(self.screen, WHITE, (x, SCREEN_HEIGHT//2 - 2, lane_mark_length, 4))
        
        # Vertical lane markings
        for y in range(0, SCREEN_HEIGHT, lane_mark_length + lane_mark_gap):
            pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH//2 - 2, y, 4, lane_mark_length))
    
    def update(self, gesture_signal=None):
        # Spawn new vehicles
        self.spawn_vehicle()
        
        # Update traffic lights
        for light in self.traffic_lights:
            light.update(gesture_signal)
        
        # Update vehicles
        self.vehicles = [v for v in self.vehicles if v.update(self.traffic_lights)]
    
    def draw(self):
        self.draw_roads()
        
        # Draw vehicles
        for vehicle in self.vehicles:
            vehicle.draw(self.screen)
        
        # Draw traffic lights
        for light in self.traffic_lights:
            light.draw(self.screen)
        
        # Draw intersection center
        pygame.draw.circle(self.screen, YELLOW, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 10)
        
        pygame.display.flip()
    
    def run(self, gesture_callback=None):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    # Manual control for testing
                    elif event.key == pygame.K_r:
                        for light in self.traffic_lights:
                            light.state = 'RED'
                    elif event.key == pygame.K_g:
                        for light in self.traffic_lights:
                            light.state = 'GREEN'
                    elif event.key == pygame.K_y:
                        for light in self.traffic_lights:
                            light.state = 'YELLOW'
                    elif event.key == pygame.K_l:
                        for light in self.traffic_lights:
                            light.state = 'LEFT_GREEN'
                    elif event.key == pygame.K_t:  # 't' for right turn
                        for light in self.traffic_lights:
                            light.state = 'RIGHT_GREEN'
            
            # Get gesture signal if callback provided
            gesture_signal = gesture_callback() if gesture_callback else None
            
            self.update(gesture_signal)
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()