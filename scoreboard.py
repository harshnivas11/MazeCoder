import pygame
import json
import os

class Scoreboard:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.high_scores = self.load_high_scores()
        self.player_count = self.get_next_player_number()
    
    def get_next_player_number(self):
        return len(self.high_scores) + 1
    
    def load_high_scores(self):
        if os.path.exists('high_scores.json'):
            try:
                with open('high_scores.json', 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_high_scores(self):
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f)
    
    def add_score(self, correct):
        if correct:
            self.score += 5
        else:
            self.score = max(0, self.score - 2)
    
    def add_to_high_scores(self):
        player_score = {
            'player': f'Player {self.player_count}',
            'score': self.score
        }
        self.high_scores.append(player_score)
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep top 5 scores
        self.save_high_scores()
    
    def get_high_scores(self):
        return self.high_scores
    
    def draw(self, screen):
        score_text = f"Score: {self.score}"
        text_surface = self.font.render(score_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 50))
    
    def show_final_score(self, screen):
        s = pygame.Surface((800, 600))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))
        
        pygame.draw.rect(screen, (255, 255, 255), (200, 150, 400, 300))
        
        font = pygame.font.Font(None, 48)
        title_text = "Game Over!"
        title_surface = font.render(title_text, True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(400, 200))
        screen.blit(title_surface, title_rect)
        
        score_text = f"Player {self.player_count}"
        score_surface = font.render(score_text, True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(400, 250))
        screen.blit(score_surface, score_rect)
        
        final_score = f"Final Score: {self.score}"
        final_surface = font.render(final_score, True, (0, 0, 0))
        final_rect = final_surface.get_rect(center=(400, 300))
        screen.blit(final_surface, final_rect)
        
        continue_text = "Press SPACE to continue"
        continue_surface = font.render(continue_text, True, (0, 0, 0))
        continue_rect = continue_surface.get_rect(center=(400, 400))
        screen.blit(continue_surface, continue_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
        return "continue"