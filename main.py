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

font_game_over = pygame.font.SysFont("consolas", 60)

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

    lives = 5

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        game_over_text = font_game_over.render(f"Game Over!", True, (255, 255, 255), (0, 0, 0))

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                if player.shield_active:
                    player.shield_active = False
                    asteroid.kill()  # ou split()
                else:
                    if lives > 1:
                        lives -= 1
                        asteroid.kill()
                    else:
                        log_event("player_hit")
                        print("Game over!")
                        sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    scoring += asteroid.split()
                    shot.kill()

        if scoring // 100 > player.last_shield_score:
            player.shield_active = True
            player.last_shield_score = scoring // 100

        screen.blit(BG,(0,0))

        score_text = font.render(f"Score: {scoring}", True, (255, 255, 255), (0, 0, 0))

        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255), (0, 0, 0))
        
        text_rect = score_text.get_rect()
        text_rect.topright = (screen.get_width() - 10, 10)

        screen.blit(score_text, text_rect)

        screen.blit(lives_text, (10, 10))
        
        for draw in drawable:
            draw.draw(screen)

        pygame.display.flip()

        dt = CLOCK.tick(60)/1000
        

if __name__ == "__main__":
    main()
