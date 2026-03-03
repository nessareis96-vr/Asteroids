import pygame
import sys
pygame.font.init()
from constants import *
from logger import log_state
from logger import log_event
from player import *
from asteroid import *
from asteroidfield import *
from circleshape import *
from shot import *

font = pygame.font.SysFont("consolas", 28)

def main():
    
    pygame.init()

    VERSION = pygame.version.ver 
    
    print(f"Starting Asteroids with pygame version: {VERSION}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    CLOCK = pygame.time.Clock()

    dt=0

    updatable = pygame.sprite.Group()

    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)   

    asteroids = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable,)

    asteroid_field = AsteroidField()

    shots = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)

    scoring = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    scoring += asteroid.split()
                    shot.kill()

        screen.blit(BG,(0,0))

        score_text = font.render(f"Score: {scoring}", True, (255, 255, 255), (0, 0, 0))
        
        text_rect = score_text.get_rect()
        text_rect.topright = (screen.get_width() - 10, 10)

        screen.blit(score_text, text_rect)

        for draw in drawable:
            draw.draw(screen)

        pygame.display.flip()

        dt = CLOCK.tick(60)/1000
        

if __name__ == "__main__":
    main()
