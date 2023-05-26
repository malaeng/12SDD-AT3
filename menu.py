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
        #mouse_pos = (mouse_x + surface.get_rect().x, mouse_y + surface.get_rect().y)
        self.fill(self.colors['normal'])
        if rel_rect.collidepoint(mouse_pos):
            self.fill(self.colors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.fill(self.colors['pressed'])
                if self.one_press:
                    
                    self.on_click_function()
                    
                elif not self.already_pressed:
                    print("============")
                    print('pressed')
                    print(f'original mouse position: {pygame.mouse.get_pos()}')
                    print(f'added: {surface.get_rect().x}, {surface.get_rect().y}')
                    print(f'mouse position: {mouse_pos}')
                    print(f'button_rect from get_input: {button_rect}')
                    
                    self.on_click_function()
                    self.already_pressed = True
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
        print(self.rect)

        self.title_font = pygame.font.Font('graphics/pixeled.ttf', 50)

    def start_menu(self):
        title_surf = self.title_font.render('Game Title', False, 'black')
        title_rect = title_surf.get_rect(center = (self.get_width()/2, self.get_height()/6))
        self.blit(title_surf, title_rect)

        self.play_button = Button(300, 100, "Play", self.print)
        self.play_button_rect = self.play_button.get_rect(center = (self.get_width()/2, self.get_height()/2))

        #self.play_button_rect = self.play_button.get_rect()
        
        self.play_button.get_input(self.play_button_rect, self)
        self.play_button.draw_text()
        self.blit(self.play_button, (self.play_button_rect.x, self.play_button_rect.y))


    def print(self):
        print(f'button_rect from Menu: {self.play_button_rect}')
