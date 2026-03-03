import random
import math
from constants import *
from circleshape import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

        self.radius = radius
        self.points = []
        self.generate_shape()

    def generate_shape(self):
        num_points = random.randint(8, 14)
        angle_step = 360 / num_points

        self.points = []

        for i in range(num_points):
            angle = math.radians(i * angle_step)

            # variação orgânica
            offset = random.uniform(0.7, 1.3)

            x = math.cos(angle) * self.radius * offset
            y = math.sin(angle) * self.radius * offset

            self.points.append(pygame.Vector2(x, y))
        
    def draw (self, screen):
        # pygame.draw.circle(screen, self.color, self.position, self.radius)
        world_points = [ (int(self.position.x + point.x), int(self.position.y + point.y)) for point in self.points]

        pygame.draw.polygon(screen, self.color, world_points)

    def update (self, dt):

        self.position += self.velocity*dt

        if self.position.x - self.radius <= 0 and self.velocity.x < 0:
            self.velocity.x *= -1

        if self.position.x + self.radius >= SCREEN_WIDTH and self.velocity.x > 0:
            self.velocity.x *= -1

        if self.position.y - self.radius <= 0 and self.velocity.y < 0:
            self.velocity.y *= -1

        if self.position.y + self.radius >= SCREEN_HEIGHT and self.velocity.y > 0:
            self.velocity.y *= -1


    def split (self):
        self.kill()
        
        scoring = 0

        if self.radius != 0:
            scoring = 120/self.radius
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            return scoring 
        
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

        return scoring
