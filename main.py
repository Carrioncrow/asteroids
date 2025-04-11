# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from ui import *
from constants import *
from player import *
from shot import *
from asteroid import *
from asteroidfield import AsteroidField

def restart_game():
    global player, asteroid_field, updatable, drawable, asteroids, shots, score, survival_score, game_over
    
    # Clear all sprite groups
    updatable.empty()
    drawable.empty()
    asteroids.empty()
    shots.empty()
    
    # Re-set the containers
    AsteroidField.containers = updatable
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    # Create new objects
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    # Reset game state
    score = 0
    survival_score = 0
    game_over = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # Create sprite groups
    global updatable, drawable, asteroids, shots, player, asteroid_field, score, survival_score, game_over
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set up containers
    AsteroidField.containers = updatable
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    #Instantiate objects
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # Initialize scores and lives-related variables
    score = 0
    survival_score = 0
    game_over = False

    # Font for dawing UI
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()

        screen.fill("black")
        dt = clock.tick(60) / 1000

        # Only update game if not game over
        if not game_over:
            updatable.update(dt)
            survival_score += dt * 10

            for asteroid in asteroids:
                for shot in shots:  # Create a copy of the shots group to iterate safely
                    if asteroid.collision(shot):
                        asteroid.split()
                        shot.kill()
                        score += POINTS_PER_ASTEROID
                        break
                    if player.collision(asteroid) and not player.is_respawning:
                        # Instead of exiting, call lose_life
                        game_over = player.lose_life()

        # Draw all sprites            
        for entity in drawable:
            entity.draw(screen)

        # Calculate total score
        total_score = score + int(survival_score)

        # Render UI elements
        draw_score(screen, total_score, font,(10, 10))

        # Also draw the lives counter if you have that UI function
        if not game_over:
            draw_lives(screen, player.lives, font, (10, 50))
        else:
            draw_game_over(screen, font, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            draw_restart_prompt(screen, font, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 40))

        pygame.display.flip()
        

if __name__ == "__main__":
    main()