#ui.py

import pygame

def draw_score(screen, score, font, position):
    # Render the score as text
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
    screen.blit(score_text, position) # Draw the score text on the screen

def draw_lives(screen, lives, font, position):
    lives_text = font.render(f"Lives: {lives}", True, "white")
    screen.blit(lives_text, position)

def draw_game_over(screen, font, position):
    game_over_text = font.render("GAME OVER", True, "red")
    screen.blit(game_over_text, position)

def draw_restart_prompt(screen, font, position):
    restart_text = font.render("Press R to restart", True, "white")
    screen.blit(restart_text, position)