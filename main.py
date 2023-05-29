# https://lospec.com/palette-list/oil-6
# https://www.dafont.com/press-start-2p.font
# https://www.kenney.nl/assets/sci-fi-sounds 
# https://www.kenney.nl/assets/interface-sounds


import pygame, sys, random
 
from player import Player
from menu import Menu
from enemy import Asteroid


class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((screen_width / 2, screen_height - screen_height/ 8), screen_width)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Enemies
        self.enemies = pygame.sprite.Group()
        self.time_spawned = 0
        self.spawn_cooldown = 1000

        # Menus
        self.main_menu = Menu(
            size = (screen_width, screen_height),
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 255, 
            title = "Game Title",
            buttons = ["Play", "Options", "Quit"]
            )        
        
        self.pause_menu = Menu(
            size = (8*screen_width/9, 8*screen_height/9),
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 200, 
            title = "Game Paused",
            buttons = ["Continue", "Options", "Quit to Menu"]
            )

        # Fonts
        self.font = pygame.font.Font('graphics/pixeled.ttf', 20)

        # Flags
        self.game_running = False
        self.game_paused = True
        self.mouse_state = 'PASSIVE'

    def main_menu_run(self):
        screen.blit(self.main_menu, self.main_menu.rect)
        button_pressed = self.main_menu.process(self.mouse_state)
        #if self.mouse_state == 'PRESSED':
        if button_pressed == 0: # Run
            self.game_running = True
            self.game_paused = False
            self.run()
        elif button_pressed == 1: #Options
            print("options")
        elif button_pressed == 2: #Quit
            self.quit_game()

    def pause_menu_run(self):
        screen.blit(self.pause_menu, self.pause_menu.rect)
        button_pressed = self.pause_menu.process(self.mouse_state)
        if button_pressed == 0: # Continue
            self.game_paused = False
            self.run()
        elif button_pressed == 1: #Options
            print("options")
        elif button_pressed == 2: #Quit 
            self.game_running = False
            pygame.time.wait(100)
            self.main_menu_run()

    def enemy_handler(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_spawned >= self.spawn_cooldown:
            self.spawn_enemy()
        self.enemies.update()

    def spawn_enemy(self):
        self.time_spawned = pygame.time.get_ticks()
        spawn_x = random.randint(0, screen_width)
        self.enemies.add(Asteroid((spawn_x, -20)))


    def quit_game(self):
        pygame.quit()
        quit()

    def run(self):
        if self.game_running == False:
            self.main_menu_run()
        elif self.game_paused == True:
            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.pause_menu_run()
        else:
            self.player.sprite.lasers.draw(screen)
            
            self.player.update()
            self.player.draw(screen)
            self.enemy_handler()
            self.enemies.draw(screen)
           
if __name__ == '__main__':
    pygame.init()
    screen_width = 960
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space game [to be renamed]")
    clock = pygame.time.Clock()
    game = Game()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.mouse_state = 'PRESSED'
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    game.mouse_state = 'RELEASED'


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.game_paused = True

                            
        
        screen.fill("#272744")
        game.run()
        pygame.display.flip()
        clock.tick(60)

''' 
black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)
 
block_color = (53,115,255)
 
car_width = 73
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
 
carImg = pygame.image.load('racecar2.png')
gameIcon = pygame.image.load('carIcon.png')

pygame.display.set_icon(gameIcon)

pause = False
#crash = True
 
def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))
 
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
 
def car(x,y):
    gameDisplay.blit(carImg,(x,y))
 
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
    
        def quitgame(self):
        pygame.quit()
        quit()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, 'black')
        return textSurface, textSurface.get_rect()




 
def crash():

    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        

        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15) 

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
    

def paused():

    pygame.mixer.music.pause()

    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)   


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)
        
        
    
    

    
def game_loop():
    global pause

    pygame.mixer.music.load('jazz.wav')
    pygame.mixer.music.play(-1)

    x = (display_width * 0.45)
    y = (display_height * 0.8)
 
    x_change = 0
 
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
 
    thingCount = 1
 
    dodged = 0
 
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                    
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
 
        x += x_change
        gameDisplay.fill(white)
 
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
 
 
        
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)
 
        if x > display_width - car_width or x < 0:
            crash()
 
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)
 
        if y < thing_starty+thing_height:
            #print('y crossover')
 
            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                #print('x crossover')
                crash()
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()
'''