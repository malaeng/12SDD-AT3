# Created by Malachi English, 12/6/2023
# Contains the level and button classes

import pygame

# The Button function from the original tutorial was functional, but I rewrote it for a few reasons:
# - It does not have separate actions for pressing and releasing the button
# - The collisions did not use pygame's 'collidepoint' function, and so were less readablel
# - The exact size and location had to be defined on creation, instead of being separated in surfaces and rects which are easier to manipulate
# - It was not a separate Class, so not as object-orientated, and so doens't integrate as well with the rest of my code.
class Button(pygame.Surface):
    def __init__(self, width: int, height: int, button_text: str, toggle_text=None):
        super().__init__((width, height))

        # Flags
        self.already_pressed = False
        self.already_hovered = False
        self.toggled = False
        if toggle_text: 
            self.is_toggle = True
        else:
            self.is_toggle = False

        # Border
        self.border_surf = pygame.Surface((width+6, height+6))
        self.border_surf.fill('black')

        # Colours
        self.colours = {
            'normal': '#f2d3ab',
            'hover': '#c69fa5',
            'pressed': '#8b6d9c',
            'toggled': '#8b6d9c'
        }

        # Text
        self.font = pygame.font.Font('graphics/PressStart2P.ttf', 16)
        self.text_surf = self.font.render(button_text, True, (20, 20, 20))
        self.text_rect = self.text_surf.get_rect(center = (self.get_width()/2, self.get_height()/2))
        self.button_text = button_text
        self.toggle_text = toggle_text

        # Audio
        self.click_down_SFX = pygame.mixer.Sound("audio/click_002.ogg")
        self.click_up_SFX = pygame.mixer.Sound("audio/click_003.ogg")

        self.hover_SFX = pygame.mixer.Sound('audio/glass_006.ogg')
        self.hover_SFX.set_volume(0.1)

    def get_input(self, button_rect: pygame.rect, surface: pygame.surface, mouse_state: str, SFX_on: bool) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        # The button's x and y coordinates are relative to the parent surface. 
        # However, the mouse_pos is not, so the x and y values of the parent surface are added to ensure it lines up correctly with the mouse_pos
        # Note that this currently only works if the button only has one parent surface. 
        # If the button was drawn on a surface on another surface, it would not work correctly
        real_rect = pygame.Rect((button_rect.x + surface.rect.x, button_rect.y + surface.rect.y), (button_rect.width, button_rect.height))

        if self.toggled: self.fill(self.colours['toggled'])
        else: self.fill(self.colours['normal'])

        # If statements check if the button is being hovered over, pressed, and released.
        # Flags ensure some actions only occur once (e.g. playing sound)
        if real_rect.collidepoint(mouse_pos): # If the mouse is over the button
            self.fill(self.colours['hover'])
            if not self.already_hovered: 
                if SFX_on: pygame.mixer.Sound.play(self.hover_SFX)
            self.already_hovered = True

            if mouse_state == 'PRESSED': # If the button has been pressed
                if not self.already_pressed: 
                    if SFX_on: pygame.mixer.Sound.play(self.click_down_SFX)
                self.fill(self.colours['pressed'])
                self.already_pressed = True
            
            if mouse_state == 'RELEASED' and self.already_pressed: # If the button has been released
                if SFX_on: pygame.mixer.Sound.play(self.click_up_SFX)
                self.already_pressed = False
                if self.is_toggle: 
                    if self.toggled: 
                        self.toggled = False
                        self.text_surf = self.font.render(self.button_text, True, (20, 20, 20))
                        self.text_rect = self.text_surf.get_rect(center = (self.get_width()/2, self.get_height()/2))
                    else: 
                        self.toggled = True
                        self.text_surf = self.font.render(self.toggle_text, True, (20, 20, 20))
                        self.text_rect = self.text_surf.get_rect(center = (self.get_width()/2, self.get_height()/2))
                return True
        else:
            self.already_hovered = False
            
    
    def draw_text(self):
        self.blit(self.text_surf, self.text_rect)

class Menu(pygame.Surface): # Menu inherits from pygame.Surface
    def __init__(self, size: tuple, title_size: int, parent_surface_dimensions: tuple, colour: str, alpha: int, title: str, text: list, buttons: list, stack: bool):
        super().__init__(size)

        # Layout
        self.stack = stack

        # Color
        self.fill(colour)
        self.set_alpha(alpha)

        # Dimensions
        self.rect = self.get_rect(center = (parent_surface_dimensions[0]/2, parent_surface_dimensions[1]/2))
        self.width = self.get_width()
        self.height = self.get_height()

        self.total_elements = (len(text) + len(buttons) + 2)*2
        self.element_centers = [(i * (self.height/self.total_elements)) for i in range(self.total_elements)]
        self.current_center = 1

        # Title
        self.title_font = pygame.font.Font('graphics/PressStart2P.ttf', title_size)
        self.title = title

        # Text
        self.text_elements = text
        
        self.text_surfs = []
        for i in self.text_elements:
            self.text_font = pygame.font.Font('graphics/PressStart2P.ttf', i[1])
            self.text_surfs.append(self.text_font.render(i[0], False, 'black'))
            
        # Buttons
        self.buttons = buttons

        

    def update(self, mouse_state: str, SFX_on: bool, ) -> int:

        # Tracker for element placing
        self.current_center = 2


        # Title
        title_surf = self.title_font.render(self.title, False, 'black')
        title_rect = title_surf.get_rect(center = (self.width/2, self.element_centers[self.current_center]))
        self.current_center += 2
        self.blit(title_surf, title_rect)

        # Text
        if self.text_surfs:
            for text_surf in self.text_surfs:
                index = self.text_surfs.index(text_surf)

                text_rect = text_surf.get_rect(center = (self.width/2, self.element_centers[self.current_center]))

                # If text element is a title located before buttons, add more space underneath it
                if self.text_elements[index][1] >= 16 and index+1 == len(self.text_surfs): self.current_center += 3
                else: self.current_center += 1
                
                self.blit(text_surf, text_rect)
        
        # Buttons
        for button in self.buttons:
            index = self.buttons.index(button)

            # Stack all buttons on top of each other
            if self.stack:
                button_rect = button.get_rect(center = (self.width/2, self.element_centers[self.current_center]))
                button_border_rect = button.border_surf.get_rect(center = (self.width/2, self.element_centers[self.current_center]))
                self.current_center += 2

            # Put all buttons next to each other (disfunctional and not used, due to time constraints)
            elif not self.stack:
                button_rect = button.get_rect(center = (self.width/2, self.element_centers[self.current_center]))
                button_border_rect = button.border_surf.get_rect(center = (self.width/2, self.element_centers[self.current_center]))
                self.current_center += 2

            # Returns the index of the button if it has been pressed and released
            if button.get_input(button_rect, self, mouse_state, SFX_on): return index

            # Draw buttons
            button.draw_text()
            self.blit(button.border_surf, button_border_rect)
            self.blit(button, button_rect)
        


