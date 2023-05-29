import pygame

class Button(pygame.Surface):
    def __init__(self, width: int, height: int, button_text: str):
        super().__init__((width, height))

        # Flags
        self.already_pressed = False
        self.already_hovered = False

        # Border
        self.border_surf = pygame.Surface((width+6, height+6))
        self.border_surf.fill('black')

        # Colours
        self.colours = {
            'normal': '#f2d3ab',
            'hover': '#c69fa5',
            'pressed': '#8b6d9c'
        }

        # Text
        self.font = pygame.font.Font('graphics/PressStart2P.ttf', 16)
        self.text_surf = self.font.render(button_text, True, (20, 20, 20))
        self.text_rect = self.text_surf.get_rect(center = (self.get_width()/2, self.get_height()/2))

        # Audio
        self.click_down_SFX = pygame.mixer.Sound("audio/click_002.ogg")
        self.click_up_SFX = pygame.mixer.Sound("audio/click_003.ogg")

        self.hover_SFX = pygame.mixer.Sound('audio/glass_006.ogg')
        self.hover_SFX.set_volume(0.1)

    def get_input(self, button_rect, surface, mouse_state):
        mouse_pos = pygame.mouse.get_pos()
        # The button's x and y coordinates are relative to the parent surface. 
        # However, the mouse_pos is not, so the x and y values of the parent surface are added to ensure it lines up correctly with the mouse_pos
        # Note that this currently only works if the button only has one parent surface. 
        # If the button was drawn on a surface on another surface, it would not work correctly
        real_rect = pygame.Rect((button_rect.x + surface.rect.x, button_rect.y + surface.rect.y), (button_rect.width, button_rect.height))

        self.fill(self.colours['normal'])

        # If statements check if the button is being hovered over, pressed, and released.
        # Flags ensure some actions only occur once (e.g. playing sound)
        if real_rect.collidepoint(mouse_pos): # If the mouse is over the button
            self.fill(self.colours['hover'])
            if not self.already_hovered: pygame.mixer.Sound.play(self.hover_SFX)
            self.already_hovered = True

            if mouse_state == 'PRESSED': # If the button has been pressed
                if not self.already_pressed: pygame.mixer.Sound.play(self.click_down_SFX)
                self.fill(self.colours['pressed'])
                self.already_pressed = True
            
            if mouse_state == 'RELEASED' and self.already_pressed: # If the button has been released
                pygame.mixer.Sound.play(self.click_up_SFX)
                self.already_pressed = False
                return True
        else:
            self.already_hovered = False
            
    
    def draw_text(self):
        self.blit(self.text_surf, self.text_rect)

class Menu(pygame.Surface): # Menu inherits from pygame.Surface
    def __init__(self, size: tuple, parent_surface_dimensions: tuple, colour: str, alpha: int, title: str, buttons: list):
        super().__init__(size)
        # Color
        self.fill(colour)
        self.set_alpha(alpha)

        # Dimensions
        self.rect = self.get_rect(center = (parent_surface_dimensions[0]/2, parent_surface_dimensions[1]/2))
        self.width = self.get_width()
        self.height = self.get_height()

        # Title
        self.title_font = pygame.font.Font('graphics/PressStart2P.ttf', 50)
        self.title = title

        # Buttons
        self.button_titles = buttons
        self.buttons = [Button(300, 100, self.button_titles[i]) for i in range(len(self.button_titles))]

    def process(self, mouse_state):
        # Title
        title_surf = self.title_font.render(self.title, False, 'black')
        title_rect = title_surf.get_rect(center = (self.width/2, self.height/5))
        self.blit(title_surf, title_rect)     

        
        for button in self.buttons:
            index = self.buttons.index(button)
            button_rect = button.get_rect(center = (self.width/2, ((index+2) * self.height) / (len(self.buttons)+2)))
            button_border_rect = button.border_surf.get_rect(center = (self.width/2, ((index+2) * self.height) / (len(self.buttons)+2)))

            # Returns the index of the button if it has been pressed and released
            if button.get_input(button_rect, self, mouse_state): return index

            # Draw buttons
            button.draw_text()
            self.blit(button.border_surf, button_border_rect)
            self.blit(button, button_rect)


