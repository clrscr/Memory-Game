import pygame
from pathlib import Path

p = Path(__file__).resolve().with_name("card.jpg")
card_image = pygame.image.load(p)


class MGCard(pygame.sprite.Sprite):
    def __init__(self, screen, card_value, x, y):
        super().__init__()
        self.screen = screen
        self.image = card_image

        self.rect = self.image.get_rect()
        self.og_x = x
        self.og_y = y

        self.card_value = card_value
        self.is_flipped = False
        self.font = pygame.font.SysFont(None, 48)

        self._prep_card()

    def clicked(self, current_flipped):
        new_flipped_count = current_flipped
        if self.is_flipped:
            new_flipped_count -= 1
        else:
            new_flipped_count += 1

        if new_flipped_count > 2:
            print("More than 2 cards flipped")
            return 2

        self.is_flipped = not self.is_flipped

        if self.is_flipped:
            self.image = self.text_surface
            self.show_card()
        else:
            self.image = card_image
            self.rect.x = self.og_x
            self.rect.y = self.og_y
        return new_flipped_count

    def _prep_card(self):
        self.text_surface = self.font.render(str(self.card_value),
                                             True,
                                             pygame.Color('red'), pygame.Color(0, 0, 0))

    def show_card(self):
        self.rect.x = self.rect.centerx
        self.rect.y = self.rect.centery
        self.screen.fill(pygame.Color('black'), card_image.get_rect())
        self.screen.blit(self.text_surface, self.rect)

    def reset(self):
        self.is_flipped = False
        self.image = card_image
        self.rect.x = self.og_x
        self.rect.y = self.og_y
