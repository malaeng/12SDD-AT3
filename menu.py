import pygame

class Button(pygame.Surface):
    def __init__(self, width: int, height: int, button_text: str, on_click_function=None):
        super().__init__((width, height))
        self.on_click_function = on_click_function
        self.already_pressed = False

        self.font = pygame.font.Font('graphics/pixeled.ttf', 10)

        self.colours = {
            'normal': 'white',
            'hover': 'red',
            'pressed': 'green'
        }

        self.text_surf = self.font.render(button_text, True, (20, 20, 20))
        self.text_rect = self.text_surf.get_rect(center = (self.get_width()/2, self.get_height()/2))

    def get_input(self, button_rect, surface):
        
        mouse_pos = pygame.mouse.get_pos()
        rel_rect = pygame.Rect((button_rect.x + surface.rect.x, button_rect.y + surface.rect.y), (button_rect.width, button_rect.height))

        self.fill(self.colours['normal'])
        if rel_rect.collidepoint(mouse_pos):
            self.fill(self.colours['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.already_pressed = True
                return True
            #else:
                self.already_pressed = False
    
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
        self.title_font = pygame.font.Font('graphics/pixeled.ttf', 50)
        self.title = title

        # Buttons
        self.button_titles = buttons
        self.buttons = [Button(300, 100, self.button_titles[i]) for i in range(len(self.button_titles))]

    def process(self):
        # Title
        title_surf = self.title_font.render(self.title, False, 'black')
        title_rect = title_surf.get_rect(center = (self.width/2, self.height/5))
        self.blit(title_surf, title_rect)     

        
        for button in self.buttons:
            index = self.buttons.index(button)
            button_rect = button.get_rect(center = (self.width/2, ((index+2) * self.height) / (len(self.buttons)+2)))
            pygame.event.clear()
            if button.get_input(button_rect, self): 
                return index
            button.draw_text()
            self.blit(button, button_rect)


    def print(self):
        print("Button Press")

