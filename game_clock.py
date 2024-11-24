import pygame
import time

class GameClock:
    def __init__(self, difficulty="medium"):
        # Set time limit based on difficulty
        self.time_limits = {
            "easy": 120,    # 2 minutes
            "medium": 180,  # 3 minutes
            "hard": 240     # 4 minutes
        }
        self.time_limit = self.time_limits[difficulty]
        self.start_time = time.time()
        self.font = pygame.font.Font(None, 36)
    
    def update(self):
        elapsed = time.time() - self.start_time
        remaining = self.time_limit - elapsed
        return remaining <= 0
    
    def draw(self, screen):
        elapsed = time.time() - self.start_time
        remaining = max(0, self.time_limit - elapsed)
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        text_surface = self.font.render(time_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))