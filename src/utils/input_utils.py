################################# responsible for checking user input and reading files #################################

import pygame
import tkinter as tk
from tkinter import Tk

pygame.init()

# Initialiser pygame.scrap de manière sécurisée
try:
    import pygame.scrap
    pygame.scrap.init()
    SCRAP_AVAILABLE = True
except Exception:
    SCRAP_AVAILABLE = False

# Fonctions pour gérer le presse-papiers
def set_clipboard_text(text):
    """Copie du texte dans le presse-papiers"""
    if SCRAP_AVAILABLE:
        try:
            pygame.scrap.put(pygame.SCRAP_TEXT, text.encode("utf-8"))
            return
        except Exception:
            pass
    
    # Fallback avec tkinter
    try:
        root = Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.destroy()
    except Exception:
        pass

def get_clipboard_text():
    """Récupère le texte du presse-papiers"""
    if SCRAP_AVAILABLE:
        try:
            raw = pygame.scrap.get(pygame.SCRAP_TEXT)
            if raw:
                return raw.decode("utf-8")
        except Exception:
            pass
    
    # Fallback avec tkinter
    try:
        root = Tk()
        root.withdraw()
        text = root.clipboard_get()
        root.destroy()
        return text
    except Exception:
        return ""


class InputField:
    def __init__(self, x, y, w, h, placeholder="Entrez votre pseudo...",
                 font_path=None, font_size=32):

        self.rect = pygame.Rect(x, y, w, h)

        # Couleurs
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color_active = pygame.Color("dodgerblue2")
        self.color_placeholder = pygame.Color("gray70")
        self.color = self.color_inactive

        # Police personnalisée ou défaut
        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)

        # Texte
        self.text = ""
        self.placeholder = placeholder
        self.active = False

        # Curseur
        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_counter = 0

    # -----------------------------------------------------------
    # GESTION DES ÉVÈNEMENTS
    # -----------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Active / désactive le champ
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:

            # ---------- Copié / Collé ----------
            ctrl = pygame.key.get_mods() & pygame.KMOD_CTRL

            if ctrl and event.key == pygame.K_c:
                set_clipboard_text(self.text)
                return

            if ctrl and event.key == pygame.K_v:
                paste_text = get_clipboard_text()
                if paste_text:
                    self.text = (
                        self.text[:self.cursor_pos] + paste_text + self.text[self.cursor_pos:]
                    )
                    self.cursor_pos += len(paste_text)
                return

            # ---------- Déplacements du curseur ----------
            if event.key == pygame.K_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
                return

            if event.key == pygame.K_RIGHT:
                if self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
                return

            if event.key == pygame.K_HOME:
                self.cursor_pos = 0
                return

            if event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
                return

            # ---------- Suppression ----------
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                return

            if event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                return

            # ---------- Entrée ----------
            if event.key == pygame.K_RETURN:
                print("Texte entré :", self.text)
                return

            # ---------- Ajout texte (UTF-8 OK) ----------
            self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
            self.cursor_pos += len(event.unicode)

    # -----------------------------------------------------------
    # MISE À JOUR DU CURSEUR
    # -----------------------------------------------------------
    def update(self):
        self.cursor_counter += 1
        if self.cursor_counter >= 60:
            self.cursor_counter = 0
        self.cursor_visible = self.cursor_counter < 30

    # -----------------------------------------------------------
    # AFFICHAGE
    # -----------------------------------------------------------
    def draw(self, screen):
        # Texte principal
        if self.text != "":
            txt_surface = self.font.render(self.text, True, pygame.Color("white"))
        else:
            # Placeholder quand le champ est vide
            txt_surface = self.font.render(self.placeholder, True, self.color_placeholder)

        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Curseur (seulement si actif + pas placeholder)
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + self.font.size(self.text[:self.cursor_pos])[0]
            cursor_y = self.rect.y + 5
            cursor_h = self.font.get_height()

            pygame.draw.line(screen, pygame.Color("white"),
                             (cursor_x, cursor_y),
                             (cursor_x, cursor_y + cursor_h), 2)


# -----------------------------------------------------------
# EXEMPLE D’UTILISATION
# -----------------------------------------------------------
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# Exemple avec une police personnalisée
# Mets ton fichier .ttf si tu veux
input_field = InputField(150, 150, 300, 40,
                         placeholder="Entrez votre pseudo...",
                         font_path=None,
                         font_size=32)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_field.handle_event(event)

    input_field.update()

    screen.fill((30, 30, 30))
    input_field.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
