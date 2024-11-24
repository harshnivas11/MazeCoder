import pygame
import random
import time
from queue import Queue

class Maze:
    def __init__(self, width, height, cell_size):
        self.width = width // cell_size
        self.height = height // cell_size
        self.cell_size = cell_size
        self.maze = self.generate_maze()
        self.player_pos = [1, 1]
        self.end_pos = [self.width - 2, self.height - 2]
        self.path_color = (50, 50, 50)
        self.wall_color = (0, 0, 0)
        self.end_color = (0, 200, 0)
        self.player_color = (255, 69, 0)
        self.last_move_time = time.time()
        self.move_delay = 0.15
        self.shortest_path = self.find_shortest_path()
        self.question_points = self.generate_question_points()
    
    def generate_maze(self):
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        def carve_path(x, y):
            maze[y][x] = 0
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 < new_x < self.width-1 and 0 < new_y < self.height-1 
                    and maze[new_y][new_x] == 1):
                    maze[y + dy//2][x + dx//2] = 0
                    carve_path(new_x, new_y)
        
        carve_path(1, 1)
        maze[1][1] = 0
        maze[self.height-2][self.width-2] = 2
        
        return maze
    
    def find_shortest_path(self):
        def bfs(start, end):
            queue = Queue()
            queue.put(start)
            visited = {start: None}
            
            while not queue.empty():
                current = queue.get()
                if current == tuple(end):
                    path = []
                    while current:
                        path.append(current)
                        current = visited[current]
                    return path[::-1]
                
                x, y = current
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    next_x, next_y = x + dx, y + dy
                    next_pos = (next_x, next_y)
                    if (0 <= next_x < self.width and 0 <= next_y < self.height and
                        self.maze[next_y][next_x] != 1 and next_pos not in visited):
                        visited[next_pos] = current
                        queue.put(next_pos)
            return []
        
        return bfs((1, 1), (self.width - 2, self.height - 2))
    
    def generate_question_points(self):
        points = set()
        path = self.shortest_path[1:-1]  # Exclude start and end points
        
        if len(path) >= 25:  # Ensure path is long enough for all questions
            # Calculate step sizes for each difficulty
            easy_step = len(path) // 10  # 10 questions
            medium_step = len(path) // 8  # 8 questions
            hard_step = len(path) // 7    # 7 questions
            
            # Add points for easy questions (first third of path)
            easy_section = path[:len(path)//3]
            for i in range(10):
                if i * easy_step < len(easy_section):
                    points.add(easy_section[i * easy_step])
            
            # Add points for medium questions (middle third of path)
            medium_section = path[len(path)//3:2*len(path)//3]
            for i in range(8):
                if i * medium_step < len(medium_section):
                    points.add(medium_section[i * medium_step])
            
            # Add points for hard questions (final third of path)
            hard_section = path[2*len(path)//3:]
            for i in range(7):
                if i * hard_step < len(hard_section):
                    points.add(hard_section[i * hard_step])
        
        return points
    
    def is_question_point(self, pos):
        return tuple(pos) in self.question_points
    
    def move_player(self, dx, dy):
        current_time = time.time()
        if current_time - self.last_move_time < self.move_delay:
            return False
        
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if (0 <= new_x < self.width and 0 <= new_y < self.height and 
            self.maze[new_y][new_x] != 1):
            self.player_pos = [new_x, new_y]
            self.last_move_time = current_time
            return True
        return False
    
    def is_at_end(self):
        return self.player_pos == [self.width - 2, self.height - 2]
    
    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                rect = (x * self.cell_size, y * self.cell_size, 
                       self.cell_size, self.cell_size)
                if self.maze[y][x] == 1:
                    pygame.draw.rect(screen, self.wall_color, rect)
                elif self.maze[y][x] == 2:
                    pygame.draw.rect(screen, self.end_color, rect)
                else:
                    pygame.draw.rect(screen, self.path_color, rect)
        
        # Draw player
        player_x = self.player_pos[0] * self.cell_size + self.cell_size // 2
        player_y = self.player_pos[1] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(screen, self.player_color, (player_x, player_y), 
                         self.cell_size // 3)