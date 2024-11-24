import pygame
import sys
from menu import Menu
from game_clock import GameClock
from question_handler import QuestionHandler
from maze import Maze
from scoreboard import Scoreboard
from init_db import init_database

class Game:
    def __init__(self):
        pygame.init()
        self.is_fullscreen = False
        self.base_width = 800
        self.base_height = 600
        self.screen = pygame.display.set_mode((self.base_width, self.base_height))
        pygame.display.set_caption("Maze DSA Game")
        
        # Create fullscreen toggle button
        self.fullscreen_btn = pygame.Rect(self.base_width - 40, 10, 30, 30)
        
        self.menu = Menu(self.screen, self.base_width, self.base_height)
        self.clock = None
        self.question_handler = None
        self.current_question = None
        self.show_feedback = False
        self.feedback_time = 0
        self.feedback_message = ""
        self.feedback_color = (0, 0, 0)
        self.maze = None
        self.scoreboard = Scoreboard()
        self.question_active = False
        self.running = True
    
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            display_info = pygame.display.Info()
            self.screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.base_width, self.base_height))
        # Update menu with new screen dimensions
        current_w, current_h = self.screen.get_size()
        self.menu = Menu(self.screen, current_w, current_h)
    
    def draw_fullscreen_button(self):
        pygame.draw.rect(self.screen, (100, 100, 100), self.fullscreen_btn)
        pygame.draw.rect(self.screen, (200, 200, 200), self.fullscreen_btn, 2)
        inner_rect = pygame.Rect(self.fullscreen_btn.x + 5, self.fullscreen_btn.y + 5, 20, 20)
        pygame.draw.rect(self.screen, (200, 200, 200), inner_rect, 1)
    
    def show_feedback_message(self, message, color):
        self.show_feedback = True
        self.feedback_message = message
        self.feedback_color = color
        self.feedback_time = pygame.time.get_ticks()
    
    def draw_feedback(self):
        if self.show_feedback:
            font = pygame.font.Font(None, 36)
            text = font.render(self.feedback_message, True, self.feedback_color)
            screen_width, screen_height = self.screen.get_size()
            text_rect = text.get_rect(center=(screen_width // 2, screen_height - 100))
            self.screen.blit(text, text_rect)
            
            if pygame.time.get_ticks() - self.feedback_time > 2000:
                self.show_feedback = False
    
    def handle_movement(self):
        if not self.question_active:
            moved = False
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                moved = self.maze.move_player(-1, 0)
            elif keys[pygame.K_RIGHT]:
                moved = self.maze.move_player(1, 0)
            elif keys[pygame.K_UP]:
                moved = self.maze.move_player(0, -1)
            elif keys[pygame.K_DOWN]:
                moved = self.maze.move_player(0, 1)
            
            if moved and self.maze.is_question_point(self.maze.player_pos):
                self.current_question = self.question_handler.get_random_question()
                if self.current_question:
                    self.question_active = True
    
    def run_game(self):
        self.maze = Maze(800, 600, 40)
        self.clock = GameClock(self.menu.selected_difficulty)
        self.question_handler = QuestionHandler(self.menu.selected_difficulty)
        self.scoreboard.score = 0
        
        game_running = True
        while game_running and self.running:
            self.screen.fill((26, 26, 26))
            
            if self.clock.update():
                result = self.scoreboard.show_final_score(self.screen)
                if result == "exit":
                    return "exit"
                self.scoreboard.add_to_high_scores()
                return "time_up"
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "exit"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.fullscreen_btn.collidepoint(event.pos):
                        self.toggle_fullscreen()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.is_fullscreen:
                            self.toggle_fullscreen()
                        else:
                            game_running = False
                            return "exit"
                    elif self.question_active and event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d]:
                        answer = chr(event.key - pygame.K_a + ord('A'))
                        if self.question_handler.check_answer(self.current_question, answer):
                            self.show_feedback_message("Correct!", (0, 255, 0))
                            self.scoreboard.add_score(True)
                            self.question_handler.mark_question_used()
                            self.question_active = False
                        else:
                            self.show_feedback_message("Incorrect! Try again.", (255, 0, 0))
                            self.scoreboard.add_score(False)
            
            self.handle_movement()
            self.maze.draw(self.screen)
            self.clock.draw(self.screen)
            self.scoreboard.draw(self.screen)
            self.draw_fullscreen_button()
            
            if self.question_active and self.current_question:
                self.question_handler.draw_question(self.screen, self.current_question)
            
            if self.maze.is_at_end():
                result = self.scoreboard.show_final_score(self.screen)
                if result == "exit":
                    return "exit"
                self.scoreboard.add_to_high_scores()
                return "completed"
            
            self.draw_feedback()
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def run(self):
        init_database()
        
        while self.running:
            action = self.menu.handle_menu(self.scoreboard)
            
            if action == "exit":
                self.running = False
            elif action == "play":
                result = self.run_game()
                if result == "exit":
                    self.running = False
                elif result == "time_up":
                    self.show_feedback_message("Time's up!", (255, 0, 0))
                elif result == "completed":
                    self.show_feedback_message("Maze Completed!", (0, 255, 0))
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()