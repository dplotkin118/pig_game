import pygame, sys, random, time

from pygame.locals import *

clock = pygame.time.Clock()
BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PALE_GREEN = (117,217,143)
WINDOW_SIZE = (400,400)

class Player():
    def __init__(self, player_location, player_y_momentum, player_image):
        self.player_location = player_location
        self.player_y_momentum = player_y_momentum
        #self.player_image = player_image
        self.can_teleport = False
        self.player_image = pygame.transform.scale(player_image, (player_image.get_width() * 3, player_image.get_height() * 3))
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1], self.player_image.get_width(), self.player_image.get_height())
    
class Mushroom():
    def __init__(self):
        self.mush_rect = pygame.Rect(random.randrange(24, WINDOW_SIZE[0] - 24), random.randrange(
            int(WINDOW_SIZE[1] / 4) - 24, int(WINDOW_SIZE[1] * 3/4) - 24), 24, 24)
        
        
class Red_Mushroom(Mushroom):
    def __init__(self):
        super().__init__()
        self.mush_image = pygame.image.load("red_mushroom.png").convert_alpha()
        self.mush_image = pygame.transform.scale(
            self.mush_image, (self.mush_image.get_width() * 3, self.mush_image.get_height() * 3))
        self.mush_type = "red"
        self.mush_value = 3

class Brown_Mushroom(Mushroom):
    def __init__(self):
        super().__init__()
        self.mush_image = pygame.image.load("mushroom.png").convert_alpha()
        self.mush_image = pygame.transform.scale(
            self.mush_image, (self.mush_image.get_width() * 3, self.mush_image.get_height() * 3))
        self.mush_type = "brown"
        self.mush_value = 1

class Portal():
    def __init__(self, portal_location):
        self.portal_image = pygame.image.load("portal.png").convert_alpha()
        self.portal_image = pygame.transform.scale(
            self.portal_image, (self.portal_image.get_width() * 1.5, self.portal_image.get_height() * 1.5))
        self.portal_location = portal_location
        self.is_active = False
        self.portal_rect = pygame.Rect(0,0,0,0)
    
    def spawn_portal(self, screen):
        self.portal_rect = pygame.Rect(self.portal_location[0], self.portal_location[1], self.portal_image.get_width()
            / 2, self.portal_image.get_height() / 2)
        screen.blit(self.portal_image, (self.portal_rect[0], self.portal_rect[1]))

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
    portal_timer = 0
    

    prev_time = time.time()
    
    is_dead = False #death

    p_moving = False #move the platforms

    
    platform_rect = pygame.Rect(50, 350, 300, 10) #platforms
    
    mushrooms = []
    red_count = 0

    portals = [Portal([0,0]), Portal([0,0])]

    while True:
        clock.tick(60)
        now = time.time()
        dt = now - prev_time
        prev_time = now
        #death code
        if is_dead == True:
            game_over(screen)
        #initial things to do
        screen.fill(PALE_GREEN)
        timer -= dt
        score_display = score_font.render("Score: " + str(score), 1, WHITE)
        fps_display = score_font.render(str(clock.get_fps()), 1, WHITE)
        screen.blit(fps_display, (WINDOW_SIZE[0] - 50, 0))

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
            if red_count < 3:
                mushrooms.append(Brown_Mushroom())
                red_count += 1
            else:
                mushrooms.append(Red_Mushroom())
                red_count = 0
            timer = 3
        for mushroom in mushrooms:
            if(pig.player_rect.colliderect(mushroom.mush_rect)):
                mushrooms.remove(mushroom)
                score += mushroom.mush_value
                yum_timer = .5
                yum_location = (random.randrange(0, WINDOW_SIZE[0]), random.randrange(0, WINDOW_SIZE[1]))
            screen.blit(mushroom.mush_image, (mushroom.mush_rect[0], mushroom.mush_rect[1]))

        #draw platforms on collision
        #for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform_rect)
        if pig.player_rect.colliderect(platform_rect) and pig.player_y_momentum > 0:
            pig.player_y_momentum = -425
            
        if p_moving == True:
            if pig.player_y_momentum > 0:
                p_moving = False
    
        #portals
        if portal_timer > 0:
            pig.can_teleport = False
        else:
            pig.can_teleport = True
        portal_timer -= dt

        for count, portal in enumerate(portals):
            if portal.is_active:
                portal.spawn_portal(screen)
            if pig.player_rect.colliderect(portal.portal_rect) and pig.can_teleport:
                if count == 0:
                    if portals[count + 1].is_active:
                        pig.player_location[0] = portals[count + 1].portal_location[0]
                        pig.player_location[1] = portals[count +
                                                         1].portal_location[1]
                elif count == 1:
                    if portals[count - 1].is_active:
                        pig.player_location[0] = portals[count -
                                                         1].portal_location[0]
                        pig.player_location[1] = portals[count -
                                                         1].portal_location[1]
                pig.can_teleport = False
                portal_timer = 1


        
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
                if event.key == K_SPACE:
                    for portal in portals:
                        if portal.is_active == False:
                            portal.portal_location[0] = pig.player_location[0]
                            portal.portal_location[1] = pig.player_location[1]
                            portal.is_active = True
                            pig.can_teleport = False
                            portal_timer = 1
                            break
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
    
