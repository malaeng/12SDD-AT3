import pygame

class Button(pygame.Surface):
    def __init__(self, width: int, height: int, button_text: str, on_click_function=None, one_press=False):
        super().__init__((width, height))
        self.on_click_function = on_click_function
        self.one_press = one_press
        self.already_pressed = False

        self.font = pygame.font.Font('graphics/pixeled.ttf', 10)

        self.colors = {
            'normal': 'white',
            'hover': 'red',
            'pressed': 'blue',
        }

        self.text_surf = self.font.render(button_text, True, (20, 20, 20))
        self.text_rect = self.text_surf.get_rect(center = (self.get_width()/2, self.get_height()/2))

    def get_input(self, button_rect, surface):
        
        mouse_pos = pygame.mouse.get_pos()
        rel_rect = pygame.Rect((button_rect.x + surface.rect.x, button_rect.y + surface.rect.y), (button_rect.width, button_rect.height))

        self.fill(self.colors['normal'])
        if rel_rect.collidepoint(mouse_pos):
            self.fill(self.colors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.fill(self.colors['pressed'])
                if self.one_press:
                    # self.on_click_function()
                    return True
                    
                elif not self.already_pressed:
                    # self.on_click_function()
                    self.already_pressed = True
                    return True
            else:
                self.already_pressed = False
    
    def draw_text(self):
        self.blit(self.text_surf, self.text_rect)

class Menu(pygame.Surface): # Menu inherits from pygame.Surface
    def __init__(self, size, colour, alpha, parent_surface_dimensions):
        super().__init__(size)
        self.fill(colour)
        self.set_alpha(alpha)

        self.rect = self.get_rect(center = (parent_surface_dimensions[0]/2, parent_surface_dimensions[1]/2))
        self.width = self.get_width()
        self.height = self.get_height()

        self.title_font = pygame.font.Font('graphics/pixeled.ttf', 50)



    def start_menu(self):
        # Title
        title_surf = self.title_font.render('Game Title', False, 'black')
        title_rect = title_surf.get_rect(center = (self.width/2, self.height/5))
        self.blit(title_surf, title_rect)

        button_pressed = False        

        # Play Button
        self.play_button = Button(300, 100, "Play")
        self.play_button_rect = self.play_button.get_rect(center = (self.width/2, 2*self.height/5))
        
        if self.play_button.get_input(self.play_button_rect, self): return "PLAY"
        self.play_button.draw_text()
        self.blit(self.play_button, self.play_button_rect)

        # Options Button
        self.options_button = Button(300, 100, "Options")
        self.options_button_rect = self.options_button.get_rect(center = (self.width/2, 3*self.height/5))

        if self.options_button.get_input(self.options_button_rect, self): return "OPTIONS"
        self.options_button.draw_text()
        self.blit(self.options_button, self.options_button_rect)

        # Quit Button
        self.quit_button = Button(300, 100, "Quit")
        self.quit_button_rect = self.quit_button.get_rect(center = (self.width/2, 4*self.height/5))

        if self.quit_button.get_input(self.quit_button_rect, self): return "QUIT"
        self.quit_button.draw_text()
        self.blit(self.quit_button, self.quit_button_rect)

    def print(self):
        print("Button Press")

