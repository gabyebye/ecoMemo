import pygame
import random
import time

class EcoMemory():
    def __init__(self):

        pygame.init()
        # Configuration de la fenêtre
        self.screen_width = 800
        self.screen_height = 600
 
        # Configuration des positions des cartes
        self.rows = 4
        self.cols = 5
        self.card_width = self.screen_width // self.cols
        self.card_height = self.screen_height // self.rows
 
        # Chargement des images des cartes
        self.card_images = []
 
        # Variables de jeu
        self.cards = []
        self.flipped_cards = []
        self.matched_cards = []
        self.show_popup = False
        self.popup_image = None
        self.popup_rect = None
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.lorem_ipsum_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
 
        # Ecran du jeu
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Memory Game')
 
    def init_images(self):
        for i in range(1, 11):
            image = pygame.image.load(f'cards/card_{i}.png')  # Assurez-vous d'avoir 10 images nommées card_1.png, card_2.png, etc.
            image = pygame.transform.smoothscale(image, (self.card_width, self.card_height))  # Ajustement de la taille des cartes
            self.card_images.append(image)
            self.card_images.append(image)  # Ajout d'une copie pour créer les paires
 
        # Mélange des cartes
        random.shuffle(self.card_images)
 
    def reveal_cards(self):
        for i in range(self.rows):
            for j in range(self.cols):
                rect = pygame.Rect(j * self.card_width, i * self.card_height, self.card_width, self.card_height)
                self.cards.append((self.card_images.pop(), rect))
 
    def draw_cards(self):
        for image, rect in self.cards:
            if rect in self.matched_cards or rect in self.flipped_cards:
                self.screen.blit(image, rect.topleft)
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
 
    def draw_popup(self, image):
        popup_width, popup_height = 400, 300
        popup_x = (self.screen_width - popup_width) // 2
        popup_y = (self.screen_height - popup_height) // 2
        self.popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
 
        # Fond de la popup
        pygame.draw.rect(self.screen, (200, 200, 200), self.popup_rect)
 
        # Centre l'image
        image_width, image_height = image.get_size()
        image_x = popup_x + (popup_width - image_width) // 2
        image_y = popup_y + 20
        self.screen.blit(image, (image_x, image_y))
 
        # Texte centré
        text_y = image_y + image_height + 20
        lines = [self.lorem_ipsum_text[i:i + 50] for i in range(0, len(self.lorem_ipsum_text), 50)]
        for idx, line in enumerate(lines):
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(popup_x + popup_width // 2, text_y + idx * 20))
            self.screen.blit(text_surface, text_rect.topleft)
 
        # Bouton de fermeture
        self.close_button_rect = pygame.Rect(popup_x + popup_width - 30, popup_y, 30, 30)
        pygame.draw.rect(self.screen, (255, 0, 0), self.close_button_rect)
        pygame.draw.line(self.screen, (255, 255, 255), (self.close_button_rect.left + 5, self.close_button_rect.top + 5), (self.close_button_rect.right - 5, self.close_button_rect.bottom - 5), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (self.close_button_rect.left + 5, self.close_button_rect.bottom - 5), (self.close_button_rect.right - 5, self.close_button_rect.top + 5), 2)
 
    def run_game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_popup:
                        if not self.popup_rect.collidepoint(event.pos) or self.close_button_rect.collidepoint(event.pos):
                            self.show_popup = False
                    else:
                        if len(self.flipped_cards) < 2:
                            for image, rect in self.cards:
                                if rect.collidepoint(event.pos) and rect not in self.matched_cards and rect not in self.flipped_cards:
                                    self.flipped_cards.append(rect)
                                    break
 
            if not self.show_popup and len(self.flipped_cards) == 2:
                time.sleep(0.5)
                first_rect = self.flipped_cards[0]
                second_rect = self.flipped_cards[1]
                first_image = None
                second_image = None
                for image, rect in self.cards:
                    if rect == first_rect:
                        first_image = image
                    elif rect == second_rect:
                        second_image = image
                if first_image == second_image:
                    self.matched_cards.append(first_rect)
                    self.matched_cards.append(second_rect)
                    self.popup_image = first_image
                    self.show_popup = True
                self.flipped_cards = []
 
            self.screen.fill((0, 0, 0))
            self.draw_cards()
            if self.show_popup:
                self.draw_popup(self.popup_image)
            pygame.display.flip()
            self.clock.tick(30)

        
        pygame.quit()