# https://lospec.com/palette-list/oil-6
# https://www.dafont.com/press-start-2p.font
# https://www.kenney.nl/assets/sci-fi-sounds 
# https://www.kenney.nl/assets/interface-sounds


import pygame, sys, random
 
from player import Player
from ui import UI
from menu import Menu, Button
from level import Level
from star import Star



class Game:
    def __init__(self):

        # Flags
        self.game_running = False
        self.game_paused = False
        self.mouse_state = 'PASSIVE'
        self.game_end = False

        # Audio
        self.music_on = True
        self.SFX_on = True

        pygame.mixer.music.load('audio/TremLoadingloopl.wav')
        pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=100)


        # Player
        player_sprite = Player((screen_width / 2, screen_height - screen_height/ 6), screen_width)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # UI
        self.ui = UI((screen_width, screen_height/8))
        self.ui_rect = self.ui.get_rect(midtop = (screen_width/2, 7*screen_height/8))

        # Fonts
        self.font = pygame.font.Font('graphics/pixeled.ttf', 20)


        # Stars
        self.stars = pygame.sprite.Group()
        self.num_stars = 40

        # Create all stars at random locations on the screen. 
        for i in range(self.num_stars):
            rand_x = random.randint(0, screen_width)
            rand_y = random.randint(0, screen_height)
            self.stars.add(Star((rand_x, rand_y), screen_height, screen_width))

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
                text = "Without the cover of the asteroids, you encounter more enemy ships trying to take you down. Any retaliation is dangerous, as it puts your vessel in the path of enemy fire, but may be worth it.",
                asteroids = 5,
                fighters = 15,
                scouts = 5,
                sciences = 2,
                difficulty = 1
            ),
            Level( # Level 3
                screen_size = (screen_width, screen_height),
                title = "Level 3",
                text = "You are in the final stretch now. The enemy is sending larger quantites of more advanced ships, so be prepared...",
                asteroids = 0,
                fighters = 5,
                scouts = 10,
                sciences = 10,
                difficulty = 1
            )
        ]

        # Set starting level to level 1
        self.level = self.levels[0]

        
        # Menus
        self.main_menu = Menu(
            size = (screen_width, screen_height),
            title_size = 50,
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 255, 
            title = "Celestial Smuggler",
            text = [],
            buttons = [Button(300, 75, "Play"), 
                       Button(300, 75, "Options/Help"),
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
                       Button(300, 100, "Options/Help"),
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
            text = [("You Lose", 20)],
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

        self.greetings = f"Hi {name},"
        self.options_menu = Menu(
            size = (screen_width, screen_height),
            title_size=50,
            parent_surface_dimensions = (screen_width, screen_height),
            colour = '#fbf5ef', 
            alpha = 255,
            title = "Options",
            text = [("How to Play", 20),
                    (self.greetings, 12),
                    ("Use left and right arrow keys to move, and spacebar to shoot", 12),
                    ("Press 'Esc' or 'p' key to pause at any time.", 12),
                    ("Settings", 20)],
            buttons = [Button(300, 50, "Music On", "Music Off"),
                       Button(300, 50, "SFX On", "SFX Off"),
                       Button(300, 50, "Back")],
            stack = True
        )

        # Set current menu to main menu
        self.current_menu_function = self.main_menu_run

    # Menu Functions

    # If I had more time I would update the menu class to be able to respond to button input internally/independantly.
    # This would mean there wouldn't be so many similar functions like below, but would have to be quite complex to be able to handle so many varied procedures.

    # All menu functions blit and update the menu, and respond to any button input. 
    # the menu update function returns an integer value of the index of the button that is pressed, which is used to respond to this input. 

    def main_menu_run(self):
        screen.blit(self.main_menu, self.main_menu.rect)
        button_pressed = self.main_menu.update(self.mouse_state, self.SFX_on)

        if button_pressed == 0: # Run
            self.game_running = True
            self.game_paused = False
            self.change_music('GAME')
            self.current_menu_function = self.pause_menu_run
        elif button_pressed == 1: #Options
            self.current_menu_function = self.options_menu_run
        elif button_pressed == 2: # Level Select
            self.current_menu_function = self.level_select_menu_run
        elif button_pressed == 3: #Quit
            self.quit_game()

    def level_select_menu_run(self):
        screen.blit(self.level_select_menu, self.level_select_menu.rect)
        button_pressed = self.level_select_menu.update(self.mouse_state, self.SFX_on)

        # Runs the level of the index of the button pressed.
        if button_pressed != None:
            if button_pressed in [i for i in range(len(self.levels))]: # Levels
                self.game_running = True
                self.game_paused = False
                self.level = self.levels[button_pressed]
                self.current_menu_function = self.pause_menu_run
            else: # Return to menu
                self.current_menu_function = self.main_menu_run

    def pause_menu_run(self):
        self.game_paused = True
        screen.blit(self.pause_menu, self.pause_menu.rect)
        button_pressed = self.pause_menu.update(self.mouse_state, self.SFX_on)

        if button_pressed == 0: # Continue
            self.game_paused = False
        elif button_pressed == 1: #O ptions
            self.current_menu_function = self.options_menu_run
        elif button_pressed == 2: # Return to menu
            self.game_paused = False
            self.game_running = False
            self.change_music('MENU')
            self.current_menu_function = self.main_menu_run

    def options_menu_run(self):
        screen.blit(self.options_menu, self.options_menu.rect)
        button_pressed = self.options_menu.update(self.mouse_state, self.SFX_on)

        if button_pressed == 0: # Toggle music
            if self.music_on: 
                pygame.mixer.music.set_volume(0)
                self.music_on = False
            else: 
                pygame.mixer.music.set_volume(1)
                self.music_on = True
        elif button_pressed == 1: # Toggle SFX
            if self.SFX_on:
                self.SFX_on = False
                self.player.sprite.laser_SFX.set_volume(0)
            else:
                self.SFX_on = True
                self.player.sprite.laser_SFX.set_volume(0.3)
        elif button_pressed == 2: # Return
            if self.game_paused:
                self.current_menu_function = self.pause_menu_run
            else:
                self.game_running = False
                self.current_menu_function = self.main_menu_run

    def game_over_menu_run(self):
        screen.blit(self.game_over_menu, self.game_over_menu.rect)
        button_pressed = self.game_over_menu.update(self.mouse_state, self.SFX_on)

        if button_pressed == 0: # Return to menu
            self.game_running = False
            self.game_end = True
            self.current_menu_function = self.main_menu_run

    def upgrade_menu_run(self): # Unused due to time constraints
        screen.blit(self.upgrade_menu, self.upgrade_menu.rect)
        button_pressed = self.upgrade_menu.update(self.mouse_state, self.SFX_on)

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
        button_pressed = self.level.intro_menu.update(self.mouse_state, self.SFX_on)

        if button_pressed == 0: # Start
            self.game_paused = False
            self.level.intro_done = True
            self.change_music('GAME')
            self.run()

    def collision_manager(self):
        # Because all collision objects are sprites, pygame's 'spritecollide' can be used.
        # This method is more readable than the tutorial, which compares x and y coordinates of both objects
        # It also can better handle multiple objects

        # Player lasers colliding with Enemy
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:

                # Kill laser and reduce enemy health by player damage
                enemies_hit = pygame.sprite.spritecollide(laser, self.level.current_enemies, False)
                if enemies_hit:
                    for enemy in enemies_hit:
                        enemy.take_damage(self.player.sprite.damage, self.SFX_on)
                    laser.kill()

        # Enemy lasers colliding with player
        if self.level.enemy_lasers:
            for laser in self.level.enemy_lasers:

                # Kill laser and reduce player health by 50
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.player.sprite.health -= 50


        # Player colliding with enemy
        if self.level.current_enemies:
            for enemy in self.level.current_enemies:

                # Kill enemy and reduce player health by 150
                if pygame.sprite.spritecollide(enemy, self.player, False):
                    enemy.kill()
                    self.player.sprite.health -= 150

        # Check if player health is below zero
        if self.player.sprite.health <= 0:
            # Game Over
            self.game_running = False
            self.current_menu_function = self.game_over_menu_run
                    

    def level_manager(self):
        self.level.update(self.SFX_on)

        # Level cleared
        if len(self.level.all_enemies) == 0 and len(self.level.current_enemies) == 0:

            # integer value of current level
            current_level = self.levels.index(self.level)

            # End of game
            if current_level+1 == len(self.levels):
                self.game_running = False
                self.game_over_menu.text_elements = [("You Win!", 20), ("You have successfully delivered the secret plans", 15), ("to the rebel outpost. The revolution lives on!", 15)]
                self.current_menu_function = self.game_over_menu_run

            # Next Level
            else:
                self.level = self.levels[current_level+1]
                self.player.sprite.health = self.player.sprite.max_health
            

    def quit_game(self):
        pygame.quit()
        quit()

    def change_music(self, track):
        # Stop and unload current music
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        # Change track to menu track
        if track == 'MENU':
            pygame.mixer.music.load('audio/TremLoadingloopl.wav')
            pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=100)

        # Change track to game track
        elif track == 'GAME':
            pygame.mixer.music.load('audio/Lunar Harvest v1_0.wav')
            pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=3000)

    def run(self):
        if self.game_running == False: # Menus (pregame)
            # Run menu function
            self.current_menu_function()


        elif self.game_paused == True: # Menus (midgame)
            # Draw background
            self.player.draw(screen)
            self.stars.draw(screen)
            self.level.current_enemies.draw(screen)

            # Run menu function
            self.current_menu_function()


        elif not self.level.intro_done: # Level intro
            # Run level intro
            self.level_menu_run()


        else: # Game Running
            # Game Managers
            self.collision_manager()
            self.level_manager()

            # stars
            self.stars.update()
            self.stars.draw(screen)


            # Player
            self.player.sprite.lasers.draw(screen)

            self.player.update()
            self.player.draw(screen)

           # Enemies
            self.level.current_enemies.draw(screen)
            self.level.enemy_lasers.draw(screen)

            # UI
            self.ui.update()
            self.ui.player_healthbar.update(self.player.sprite.health/self.player.sprite.max_health)
            self.ui.level_progress.update(1-len(self.level.all_enemies)/self.level.total_num_enemies)
            screen.blit(self.ui, self.ui_rect)
            
           


if __name__ == '__main__':
    # Name
    print("===============================================\n")
    name = input("Please enter your name: ")
    print("\n===============================================")

    # Initiate pygame
    pygame.init()

    # Display
    screen_width = 960
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Celestial Smuggler")

    # other variables
    clock = pygame.time.Clock()
    game = Game()


    while True:
        for event in pygame.event.get():
            # Pressing X in top-right corner of pygame window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mousebutton state of left-click (right click is not used in this game)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.mouse_state = 'PRESSED'
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    game.mouse_state = 'RELEASED'

            # Pause game if 'escape' or 'p' key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    game.game_paused = True


        screen.fill("#272744")

        # Run game loop.
        # If game ends, create a new game (resets any progress)
        game.run()
        if game.game_end: game = Game()

        # Update screen
        pygame.display.update()

        clock.tick(60)
