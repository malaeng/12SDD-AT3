import pygame

class UI(pygame.Surface):
    def __init__(self, size: tuple):
        super().__init__(size)
        self.font = pygame.font.Font('graphics/PressStart2P.ttf', 14)
        
        # Player Health

        self.health_label_surf = self.font.render("Player Health", True, '#272744')
        self.health_label_rect = self.health_label_surf.get_rect(midleft = (20, self.get_height()/2))

        self.player_healthbar = InfoSlider((240, 30), 1, True)
        self.player_healthbar_rect = self.player_healthbar.get_rect(midleft = (220, self.get_height()/2))

        # Level Progress

        self.progress_label_surf = self.font.render("Level Progress", True, '#272744')
        self.progress_label_rect = self.health_label_surf.get_rect(midleft = (self.get_width()/2, self.get_height()/2))

        self.level_progress = InfoSlider((240, 30), 0, False)
        self.level_progress_rect = self.player_healthbar.get_rect(midleft = (self.get_width()/2 + 220, self.get_height()/2))
    
    def update(self):
        self.fill('#f2d3ab')

        self.blit(self.health_label_surf, self.health_label_rect)
        self.blit(self.player_healthbar, self.player_healthbar_rect)

        self.blit(self.progress_label_surf, self.progress_label_rect)
        self.blit(self.level_progress, self.level_progress_rect)


class InfoSlider(pygame.Surface):
    def __init__(self, size: tuple, percent: float, change_colour: bool):
        super().__init__(size)
        self.width = size[0]
        self.height = size[1]
        self.health_percent = percent
        self.colours = {
            'border': '#fbf5ef',
            'hi_health': '#8b6d9c',
            'lo_health': '#c69fa5',
            'no_change_colour': '#494d7e'
        }
        self.change_colour = change_colour

        self.fill(self.colours['border'])
        #self.update(self.health_percent)
        #self.percent_image = pygame.Surface((self.width*percent-8, self.height-8))
        #self.percent_image.fill((random.choice(('red', 'blue'))))
        

    def update(self, percent: float):
        if self.change_colour:
            if percent > 0.3: self.current_colour = 'hi_health'
            else: self.current_colour = 'lo_health'
        else:
            self.current_colour = 'no_change_colour'
        if percent >= 0 :
            self.percent_image = pygame.Surface((self.width-8, self.height-8))
            self.percent_image = pygame.transform.scale_by(self.percent_image, (percent, 1))
            self.percent_image.fill(self.colours[self.current_colour])
            self.percent_image_rect = self.percent_image.get_rect(topleft = (4, 4))

            self.fill(self.colours['border'])
            self.blit(self.percent_image, self.percent_image_rect)