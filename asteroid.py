import random
from constants import *
from circleshape import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
    
    def draw (self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
    
    def update (self, dt):
        self.position += self.velocity*dt

    def split (self):
        self.kill()
        
        if self.radius < ASTEROID_MIN_RADIUS:
            return
        
        else:
            log_event("asteroid_split")

            angle = random.uniform (20,50)

            velocity_01 = self.velocity.rotate(angle)
            velocity_02 = self.velocity.rotate(-angle)

            new_radius = self.radius - ASTEROID_MIN_RADIUS

            asteroid_01 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid_02 = Asteroid(self.position.x, self.position.y, new_radius)

            asteroid_01.velocity = velocity_01 * 1.2
            asteroid_02.velocity = velocity_02 * 1.2
