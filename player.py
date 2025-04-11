from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.lives = 3 # Add lives attribute
        self.is_respawning = False
        self.respawn_timer = 0
        self.initial_position = pygame.Vector2(x, y) # Store initial position for respawning
        self.is_flashing = False
        self.flash_timer = 0
        self.flash_duration = 1000  # milliseconds
        self.flash_interval = 100   # milliseconds
        self.last_flash_toggle = 0
        self.visible_when_flashing = True  # Track visibility state

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Calculate visibility based on both effects
        should_draw = True
    
        if self.is_respawning:
            should_draw = (self.respawn_timer % 20 < 10)
        
        if self.is_flashing:
            should_draw = self.visible_when_flashing
    
        # Draw only if visible
        if should_draw:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        # Update respawn timer if respawning
        if self.is_respawning:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.is_respawning = False
                self.respawn_timer = 0
        
        # Key controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        # Handle flashing if active
        if self.is_flashing:
            self.flash_timer -= dt * 1000
        
            # Toggle visibility
            self.last_flash_toggle += dt * 1000
            if self.last_flash_toggle >= self.flash_interval:
                self.last_flash_toggle = 0
                self.visible_when_flashing = not self.visible_when_flashing
            
            # End flashing when timer expires
            if self.flash_timer <= 0:
                self.is_flashing = False
                self.visible_when_flashing = True
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
            
    def shoot(self):
        if self.shoot_timer <= 0:
            new_shot = Shot(self.position.x, self.position.y)
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            new_shot.velocity = forward * PLAYER_SHOOT_SPEED
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN

    # Method for life management    
    def lose_life(self):
        self.lives -= 1

        # Start flashing
        self.is_flashing = True
        self.flash_timer = self.flash_duration
        self.last_flash_toggle = 0

        if self.lives <= 0:
            self.lives = 0
            return True # Game over
        else:
            self.respawn()
            return False # Not game over yet
        
    def respawn(self):
        # Reset position to starting location
        self.position = self.initial_position.copy()
        self.velocity = pygame.Vector2(0, 0)
        # Add invulnerability period
        self.is_respawning = True
        self.respawn_timer = 2.0  # 2 seconds of invulnerability
        