# https://lospec.com/palette-list/oil-6
# https://www.dafont.com/press-start-2p.font
# https://www.kenney.nl/assets/sci-fi-sounds 
# https://www.kenney.nl/assets/interface-sounds


import pygame, sys, random
 
from player import Player
from ui import UI
from menu import Menu, Button
from enemy import Enemy
from level import Level

class Star(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, screen_height: int):
        super().__init__()
        self.screen_height = screen_height
        self.image = pygame.image.load('graphics/star.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.image.set_alpha(random.randint(150, 200))
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.screen_height:
            rand_x = random.randint(0, screen_width)
            self.rect = self.image.get_rect(center = (rand_x, 0))

class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((screen_width / 2, screen_height - screen_height/ 6), screen_width)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # UI
        self.ui = UI((screen_width, screen_height/8))
        self.ui_rect = self.ui.get_rect(midtop = (screen_width/2, 7*screen_height/8))

        # Enemies
        self.enemies = pygame.sprite.Group()
        self.time_spawned = 0
        self.spawn_cooldown = 2000

        self.enemy_lasers = pygame.sprite.Group()

        # Stars
        self.stars = pygame.sprite.Group()
        for i in range(30):
            rand_x = random.randint(0, screen_width)
            rand_y = random.randint(0, screen_height)
            self.stars.add(Star((rand_x, rand_y), screen_height))

        # Levels
        self.levels = [
            Level( # Level 1
                screen_size = (screen_width, screen_height),
                title = "Level 1",
                text = "You comandeer a small rebel vessel tasked with delivering secret plans to the rebel base located on the other side of the sector. This asteroid field may allow you to stay undetected, but watch out for rebel scouts",
                asteroids = 25,
                fighters = 0,
                scouts = 5,
                sciences = 0,
                difficulty = 1
            ),
            Level( # Level 2
                screen_size = (screen_width, screen_height),
                title = "Level 2",
                text = "Leaving and asteroid field, ... etc.",
                asteroids = 5,
                fighters = 15,
                scouts = 5,
                sciences = 2,
                difficulty = 1
            ),
            Level( # Level 3
                screen_size = (screen_width, screen_height),
                title = "Level 3",
                text = "Leaving and asteroid field, ... etc.",
                asteroids = 0,
                fighters = 5,
                scouts = 10,
                sciences = 10,
                difficulty = 3
            )
        ]
        self.level = self.levels[0]

        
        # Menus
        self.main_menu = Menu(
            size = (screen_width, screen_height),
            title_size = 50,
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 255, 
            title = "Game Title",
            text = [],
            buttons = [Button(300, 75, "Play"), 
                       Button(300, 75, "Options"),
                       Button(300, 75, "Level Select"),
                       Button(300, 75, "Quit")],
            stack = True
            )

        self.level_select_menu = Menu(
            size = (screen_width, screen_height),
            title_size = 50,
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 255, 
            title = "Level Select",
            text = [],
            buttons = [Button(300, 75, "Level 1"), 
                       Button(300, 75, "Level 2"),
                       Button(300, 75, "Level 3"),
                       Button(300, 75, "Back to Menu")],
            stack = True
            )     
        
        self.pause_menu = Menu(
            size = (8*screen_width/9, 8*screen_height/9),
            title_size = 50,
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 200, 
            title = "Game Paused",
            text = [],
            buttons = [Button(300, 100, "Continue"),
                       Button(300, 100, "Options"),
                       Button(300, 100, "Quit to Menu")],
            stack = True
            )
        
        self.game_over_menu = Menu(
            size = (8*screen_width/9, 8*screen_height/9),
            title_size = 50,
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 200, 
            title = "Game Over",
            text = [("You win!", 20) if self.player.sprite.health <= 0 else ("You Lose", 20)],
            buttons = [Button(300, 100, "Return to Menu")],
            stack = True
            )
        
        self.upgrade_menu = Menu(
            size = (2*screen_width/3, 2*screen_height/3),
            title_size = 50,
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 200, 
            title = "Choose Upgrade",
            text = [],
            buttons = ["Upgrade 1", "Upgrade 2"],
            stack = False
        )

        self.options_menu = Menu(
            size = (screen_width, screen_height),
            title_size=50,
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 255,
            title = "Options",
            text = [("How to Play", 20),
                    ("Use left and right arrow keys to move.", 12),
                    ("Press spacebar to shoot.", 12),
                    ("Settings", 20)],
            buttons = [Button(300, 50, "Music On", "Music Off"),
                       Button(300, 50, "SFX On", "SFX Off"),
                       Button(300, 75, "Return to Menu")],
            stack = True
        )
        self.current_menu_function = self.main_menu_run

        # Fonts
        self.font = pygame.font.Font('graphics/pixeled.ttf', 20)

        # Flags
        self.game_running = False
        self.game_paused = True
        self.mouse_state = 'PASSIVE'
        self.game_end = False

    def main_menu_run(self):
        screen.blit(self.main_menu, self.main_menu.rect)
        button_pressed = self.main_menu.process(self.mouse_state)
        if button_pressed == 0: # Run
            self.game_running = True
            self.game_paused = False
            self.current_menu_function = self.pause_menu_run
            #self.run()
        elif button_pressed == 1: #Options
            print("options")
            self.current_menu_function = self.options_menu_run
        elif button_pressed == 2: # Level Select
            print("level select")
            self.current_menu_function = self.level_select_menu_run
        elif button_pressed == 3: #Quit
            self.quit_game()

    def level_select_menu_run(self):
        screen.blit(self.level_select_menu, self.level_select_menu.rect)
        button_pressed = self.level_select_menu.process(self.mouse_state)
        if button_pressed != None:
            if button_pressed in [i for i in range(len(self.levels))]: # Levels
                self.game_running = True
                self.game_paused = False
                self.level = self.levels[button_pressed]
                self.run()
            else: # Return to menu
                self.current_menu_function = self.main_menu_run

    def pause_menu_run(self):
        screen.blit(self.pause_menu, self.pause_menu.rect)
        button_pressed = self.pause_menu.process(self.mouse_state)
        if button_pressed == 0: # Continue
            self.game_paused = False
            self.run()
        elif button_pressed == 1: #Options
            self.current_menu_function = self.options_menu_run
        elif button_pressed == 2: #Quit 
            self.game_running = False
            self.current_menu_function = self.main_menu_run

    def options_menu_run(self):
        screen.blit(self.options_menu, self.options_menu.rect)
        button_pressed = self.options_menu.process(self.mouse_state)
        if button_pressed == 0: # 
            self.game_paused = False
            self.run()
        elif button_pressed == 1: #Options
            print("options_optionsmenu")
        elif button_pressed == 2: #Quit 
            self.game_running = False
            self.current_menu_function = self.main_menu_run

    def game_over_menu_run(self):
        screen.blit(self.game_over_menu, self.game_over_menu.rect)
        button_pressed = self.game_over_menu.process(self.mouse_state)
        if button_pressed == 0: # Return to menu
            self.game_running = False
            self.game_end = True
            self.current_menu_function = self.main_menu_run

    def upgrade_menu_run(self):
        screen.blit(self.upgrade_menu, self.upgrade_menu.rect)
        button_pressed = self.upgrade_menu.process(self.mouse_state)
        if button_pressed == 0:
            # apply upgrade
            self.game_paused = False
            self.run()
        elif button_pressed == 1:
            # apply upgrade
            self.game_paused = False
            self.run()

    def level_menu_run(self):
        screen.blit(self.level.intro_menu, self.level.intro_menu.rect)
        button_pressed = self.level.intro_menu.process(self.mouse_state)
        if button_pressed == 0: # Start
            self.game_paused = False
            self.level.intro_done = True
            self.run()

    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Enemy collisions
                enemies_hit = pygame.sprite.spritecollide(laser, self.level.current_enemies, False)
                if enemies_hit:
                    for enemy in enemies_hit:
                        enemy.take_damage(self.player.sprite.damage)
                    laser.kill()

        if self.level.enemy_lasers:
            for laser in self.level.enemy_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    print('player hit')
                    self.player.sprite.health -= 50

        
        if self.level.current_enemies:
            for enemy in self.level.current_enemies:
                if pygame.sprite.spritecollide(enemy, self.player, False):
                    enemy.kill()
                    self.player.sprite.health -= 150

        if self.player.sprite.health <= 0:
            print('game over')
            self.game_running = False
            self.current_menu_function = self.game_over_menu_run
                    

    def level_manager(self):
        self.level.update()
        if len(self.level.all_enemies) == 0 and len(self.level.current_enemies) == 0:
            current_level = self.levels.index(self.level)
            if current_level == len(self.levels):
                print('game over')
                self.game_running = False
                self.current_menu_function = self.game_over_menu_run
            else:
                self.level = self.levels[current_level+1]
            

    def quit_game(self):
        pygame.quit()
        quit()

    def run(self):
        if self.game_running == False:
            self.current_menu_function()
        elif self.game_paused == True:
            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.current_menu_function()
        elif not self.level.intro_done:
            self.level_menu_run()
        else:
            # stars

            self.stars.draw(screen)
            self.stars.update()
            self.player.sprite.lasers.draw(screen)

            self.player.update()
            self.player.draw(screen)
            
            
            self.collision_checks()

            self.level_manager()

            #self.level.enemy_lasers.update()
            self.level.current_enemies.draw(screen)
            self.level.enemy_lasers.draw(screen)

            # UI
            screen.blit(self.ui, self.ui_rect)
            self.ui.update()
            self.ui.player_healthbar.update(self.player.sprite.health/self.player.sprite.max_health)
            self.ui.level_progress.update(1-len(self.level.all_enemies)/self.level.total_num_enemies)
            
           
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

            # Mousebutton state of left-click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.mouse_state = 'PRESSED'
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    game.mouse_state = 'RELEASED'

            # Pause game
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    game.game_paused = True


        screen.fill("#272744")
        game.run()
        if game.game_end: game = Game()
        pygame.display.flip()
        clock.tick(60)
