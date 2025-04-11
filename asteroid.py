from circleshape import *
from constants import *
import random
import pygame


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        # Kill itself
        self.kill()
        # Check if radius is too small to split further
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        # Generate random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)
        # Create two new velocit vectors by rotating current velocity
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)
        # Make the new asteroids move faster by scaling velocity
        new_velocity1 *= 1.2
        new_velocity2 *= 1.2
        # Calculate new radius for smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # Create two new asteroids
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = new_velocity1
    
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = new_velocity2