import pygame, sys, random, time

from pygame.locals import *

clock = pygame.time.Clock()
BLACK = (0,0,0)
WHITE = (255, 255, 255)
WINDOW_SIZE = (400,400)

class Player():
    def __init__(self, player_location, player_y_momentum, player_image):
        self.player_location = player_location
        self.player_y_momentum = player_y_momentum
        self.player_image = player_image
        self.player_image = player_image = pygame.transform.scale(self.player_image, (self.player_image.get_width() * 5, self.player_image.get_height() * 5))
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1], self.player_image.get_width(), self.player_image.get_height())
    

def game_over(screen):
    while True:
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        main()
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        font = pygame.font.SysFont("monospace", 80)
        gameover = font.render("you died", 1, (0, 0, 0))
        screen.blit(gameover, (0, 200))
        pygame.display.update()


def spawn_platform(platform, screen, color):
    pygame.draw.rect(screen, color, platform)

def new_platform(player, platforms):
    #lower_bound = int(WINDOW_SIZE[1] - player.player_location[1])
    
    upper_bound = WINDOW_SIZE[1]
    x_value = random.randrange(50, WINDOW_SIZE[0] - 50)
    y_value = (platforms[-1][1]) - 50
    platform = pygame.Rect(x_value, y_value, 50, 10)
    platforms.append(platform)



def main():
    pygame.display.set_caption("game")
    

    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

    pig = Player([200, 200], 0, pygame.image.load('pig.png').convert_alpha()) #player

    score = 0 #score
    score_font = pygame.font.SysFont("monospace", 16)

    yum_font = pygame.font.SysFont("monospace", 10) #dialogue
    yum_words = ["yum", "tasty", "another pls", "delicious", "incredible"]
    yum_location = (0,0)
    

    moving_right = False #movement
    moving_left = False
    facing_left = True

    timer = 3 #time
    dt = 0
    yum_timer = 0
    

    prev_time = time.time()
    
    is_dead = False #death

    p_moving = False #move the platforms

    
    platform_rect = pygame.Rect(200, 300, 50, 10) #platforms
    platform2_rect = pygame.Rect(80, 200, 50, 10)
    platforms = [platform_rect, platform2_rect]

    mushroom_image = pygame.image.load('mushroom.png').convert_alpha() #mushrooms
    mushroom_image = pygame.transform.scale(mushroom_image, (mushroom_image.get_width() * 3, mushroom_image.get_height() * 3))
    mushrooms = []
    for i in range(3):
        mush_rect = pygame.Rect(random.randrange(mushroom_image.get_width(), WINDOW_SIZE[0] - mushroom_image.get_width()), random.randrange(mushroom_image.get_height(), WINDOW_SIZE[1] - mushroom_image.get_height()), mushroom_image.get_width(), mushroom_image.get_height())
        mushrooms.append(mush_rect)

    while True:
        clock.tick(60)
        now = time.time()
        dt = now - prev_time
        prev_time = now
        #death code
        if is_dead == True:
            game_over(screen)
        #initial things to do
        screen.fill(WHITE)
        timer -= dt
        score_display = score_font.render("Score: " + str(score), 1, (0, 0, 0))

        #movement code
        if moving_left == True:
            if facing_left == False:
                pig.player_image = pygame.transform.flip(pig.player_image, True, False)
            pig.player_location[0] -=  300 * dt
            facing_left = True
        if moving_right == True:
            if facing_left == True:
                pig.player_image = pygame.transform.flip(pig.player_image, True, False) 
            pig.player_location[0] += 300 * dt
            facing_left = False
        
        
        #display images
        screen.blit(pig.player_image, pig.player_location) 
        screen.blit(score_display, (5,0))
        
        #dialogue spawn
        if yum_timer <= 0: 
            yum_display = yum_font.render(random.choice(yum_words), 1, (0,0,0))    
        elif yum_timer > 0:
            screen.blit(yum_display, yum_location)
            yum_timer -= dt

        #mushroom spawn and collisions
        if timer <= 0:
            mush_rect = pygame.Rect(random.randrange(mushroom_image.get_width(), WINDOW_SIZE[0] - mushroom_image.get_width()), random.randrange(int(WINDOW_SIZE[1] / 4) - mushroom_image.get_height(), int(WINDOW_SIZE[1] * 3/4) - mushroom_image.get_height()), mushroom_image.get_width(), mushroom_image.get_height())
            mushrooms.append(mush_rect)
            timer = 3
        for location in mushrooms:
            if(pig.player_rect.colliderect(location)):
                mushrooms.remove(location)
                score += 1
                yum_timer = .5
                yum_location = (random.randrange(0, WINDOW_SIZE[0]), random.randrange(0, WINDOW_SIZE[1]))
            screen.blit(mushroom_image, (location[0], location[1]))

        #draw platforms on collision
        for platform in platforms:
            if pig.player_rect.colliderect(platform) and pig.player_y_momentum > 0:
                spawn_platform(platform, screen, (0, 255, 0))
                pig.player_y_momentum = -300
                p_moving = True
            else:
                spawn_platform(platform, screen, (0, 0, 0))
            
        if p_moving == True:
            if pig.player_y_momentum > 0:
                p_moving = False
            for platform in platforms:
                    pygame.Rect.move_ip(platform, 0, 1 * abs(pig.player_y_momentum * dt))

        for platform in platforms:
            if platform.bottom > WINDOW_SIZE[1]:
                platforms.remove(platform)

        while len(platforms) < 3:
            new_platform(pig, platforms)


        #if pig.player_location[1] < (WINDOW_SIZE[1] / 2):
                    
            #pig.player_y_momentum = 0

        
        #gravity/vertical momentum and death from falling off the bottom
        if pig.player_location[1] >= WINDOW_SIZE[1] - pig.player_image.get_height():
            pig.player_y_momentum = 0
            is_dead = True
        else:
            pig.player_y_momentum += 6
            pig.player_location[1] += pig.player_y_momentum * dt

        pig.player_rect[0] = pig.player_location[0] #update player location
        pig.player_rect[1] = pig.player_location[1]
        
        pressed = pygame.key.get_pressed() #movement

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                    moving_left = False
                if event.key == K_LEFT:
                    moving_left = True
                    moving_right = False
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                    if pressed[K_LEFT]:
                        moving_left = True
                if event.key == K_LEFT:
                    moving_left = False
                    if pressed[K_RIGHT]:
                        moving_right = True
                

        pygame.display.update()
        


if __name__ == "__main__":
    pygame.init()
    main()
    
