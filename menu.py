import pygame

class Menu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, int(screen_height * 0.08))
        
        button_width = int(screen_width * 0.25)
        button_height = int(screen_height * 0.08)
        button_x = (screen_width - button_width) // 2
        
        self.main_buttons = {
            "play": pygame.Rect(button_x, screen_height * 0.3, button_width, button_height),
            "scoreboard": pygame.Rect(button_x, screen_height * 0.45, button_width, button_height),
            "exit": pygame.Rect(button_x, screen_height * 0.6, button_width, button_height)
        }
        
        self.difficulty_buttons = {
            "easy": pygame.Rect(button_x, screen_height * 0.3, button_width, button_height),
            "medium": pygame.Rect(button_x, screen_height * 0.45, button_width, button_height),
            "hard": pygame.Rect(button_x, screen_height * 0.6, button_width, button_height)
        }
        
        self.selected_difficulty = None
        self.show_difficulty = False
        self.show_scoreboard = False
    
    def draw_main_menu(self):
        self.screen.fill((26, 26, 26))
        
        title = self.font.render("MazeCoder", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height * 0.15))
        self.screen.blit(title, title_rect)
        
        for text, rect in self.main_buttons.items():
            color = (76, 175, 80) if text == "play" else (220, 53, 69)
            if text == "scoreboard":
                color = (70, 130, 180)
            pygame.draw.rect(self.screen, color, rect)
            button_text = self.font.render(text.title(), True, (255, 255, 255))
            text_rect = button_text.get_rect(center=rect.center)
            self.screen.blit(button_text, text_rect)
    
    def draw_difficulty_menu(self):
        self.screen.fill((26, 26, 26))
        
        title = self.font.render("Select Difficulty", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height * 0.15))
        self.screen.blit(title, title_rect)
        
        for text, rect in self.difficulty_buttons.items():
            color = (76, 175, 80)
            pygame.draw.rect(self.screen, color, rect)
            button_text = self.font.render(text.title(), True, (255, 255, 255))
            text_rect = button_text.get_rect(center=rect.center)
            self.screen.blit(button_text, text_rect)
    
    def draw_scoreboard(self, scoreboard):
        self.screen.fill((26, 26, 26))
        
        title = self.font.render("High Scores", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height * 0.15))
        self.screen.blit(title, title_rect)
        
        scores = scoreboard.get_high_scores()
        y = self.screen_height * 0.3
        for score in scores:
            score_text = self.font.render(f"{score['player']}: {score['score']}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.screen_width // 2, y))
            self.screen.blit(score_text, score_rect)
            y += self.screen_height * 0.08
        
        back_rect = pygame.Rect((self.screen_width - 200) // 2, self.screen_height * 0.8, 200, 50)
        pygame.draw.rect(self.screen, (220, 53, 69), back_rect)
        back_text = self.font.render("Back", True, (255, 255, 255))
        back_rect_text = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_rect_text)
        
        return back_rect
    
    def handle_menu(self, scoreboard):
        clock = pygame.time.Clock()
        
        while True:
            if self.show_scoreboard:
                back_rect = self.draw_scoreboard(scoreboard)
            elif not self.show_difficulty:
                self.draw_main_menu()
            else:
                self.draw_difficulty_menu()
            
            pygame.display.flip()
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.show_scoreboard or self.show_difficulty:
                        self.show_scoreboard = False
                        self.show_difficulty = False
                    else:
                        return "exit"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    if self.show_scoreboard:
                        if back_rect.collidepoint(mouse_pos):
                            self.show_scoreboard = False
                    elif not self.show_difficulty:
                        for action, rect in self.main_buttons.items():
                            if rect.collidepoint(mouse_pos):
                                if action == "play":
                                    self.show_difficulty = True
                                    break
                                elif action == "scoreboard":
                                    self.show_scoreboard = True
                                    break
                                else:
                                    return action
                    else:
                        for difficulty, rect in self.difficulty_buttons.items():
                            if rect.collidepoint(mouse_pos):
                                self.selected_difficulty = difficulty
                                self.show_difficulty = False
                                return "play"