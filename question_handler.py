import pygame
import sqlite3

class QuestionHandler:
    def __init__(self, difficulty="medium"):
        self.font = pygame.font.Font(None, 32)
        self.conn = sqlite3.connect('questions.db')
        self.cursor = self.conn.cursor()
        self.difficulty = difficulty
        self.current_question = None
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
    
    def get_random_question(self):
        self.cursor.execute('''
        SELECT * FROM questions 
        WHERE difficulty = ? AND used = 0 
        ORDER BY RANDOM() LIMIT 1
        ''', (self.difficulty,))
        
        row = self.cursor.fetchone()
        if row:
            self.current_question = {
                'id': row[0],
                'question': row[1],
                'options': {
                    'A': row[2],
                    'B': row[3],
                    'C': row[4],
                    'D': row[5]
                },
                'correct': row[6]
            }
            return self.current_question
        return None
    
    def mark_question_used(self):
        if self.current_question:
            self.cursor.execute('''
            UPDATE questions SET used = 1 
            WHERE id = ?
            ''', (self.current_question['id'],))
            self.conn.commit()
    
    def reset_used_questions(self):
        self.cursor.execute('UPDATE questions SET used = 0')
        self.conn.commit()
    
    def draw_question(self, screen, question):
        if not question:
            return
            
        s = pygame.Surface((800, 600))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))
        
        pygame.draw.rect(screen, (255, 255, 255), (100, 100, 600, 400))
        
        diff_text = self.font.render(f"Difficulty: {self.difficulty.title()}", True, (0, 0, 0))
        screen.blit(diff_text, (120, 120))
        
        lines = self.wrap_text(question['question'], 550)
        y = 160
        for line in lines:
            question_text = self.font.render(line, True, (0, 0, 0))
            screen.blit(question_text, (120, y))
            y += 40
        
        y = max(y + 20, 280)
        for option, text in question['options'].items():
            option_text = self.font.render(f"{option}: {text}", True, (0, 0, 0))
            screen.blit(option_text, (120, y))
            y += 50
    
    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.font.render(test_line, True, (0, 0, 0))
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        lines.append(' '.join(current_line))
        return lines
    
    def check_answer(self, question, answer):
        return question['correct'] == answer
    
    def __del__(self):
        self.conn.close()