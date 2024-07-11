import pygame
class MemoryGameEngine:
    def __init__(self, draw_function, input_handler, settings):
        pygame.init()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.draw_function = draw_function
        self.settings = settings
        self.setup_display()
        self.cards = pygame.sprite.Group()
        self.input_handler = input_handler
        pygame.display.set_caption('Memory Game')

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _update_screen(self):
        self.draw_function()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            else:
                self.input_handler(event)

    def setup_display(self):
        if self.settings.should_full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_width()
            self.settings.screen_height = self.screen.get_height()
        else:
            self.settings.screen_width = 800
            self.settings.screen_height = 900
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))