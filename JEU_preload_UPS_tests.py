import pygame
import random
import sys

# Initialisation
pygame.init()

# --- Configuration de base ---
LARGEUR, HAUTEUR = 1155, 768
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu de tri des camions - Lille")
font = pygame.font.SysFont("Comic Sans MS", 36)
small_font = pygame.font.SysFont("Comic Sans MS", 28)

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (220, 20, 60)
VERT = (50, 205, 50)
BLEU = (30, 144, 255)
GRIS = (200, 200, 200)

# --- Données des camions ---
from vieux_lille import vieux_lille
from lille_centre import lille_centre
from lille_moulin import lille_moulin

adresses = {
    "Vieux Lille": vieux_lille,
    "Lille Centre": lille_centre,
    "Lille Moulin": lille_moulin
}

camions = ["Vieux Lille", "Lille Centre", "Lille Moulin"]

# Zones cliquables correspondant aux camions dans l'image
camion_rects = {
    "Vieux Lille": pygame.Rect(50, 460, 330, 200),
    "Lille Centre": pygame.Rect(410, 460, 310, 200),
    "Lille Moulin": pygame.Rect(760, 460, 330, 200)
}

# Boutons
stop_button = pygame.Rect(1000, 20, 130, 50)
rejouer_button = pygame.Rect(LARGEUR // 2 - 75, 160, 150, 50)

# Charger les images de fond
fond = pygame.image.load("fond_camions.png")
fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))

fond_fin = pygame.image.load("fond_fin.png")
fond_fin = pygame.transform.scale(fond_fin, (LARGEUR, HAUTEUR))

# Préparer une liste unique de toutes les adresses avec tous les camions possibles
seen = set()
all_adresses = []
for camion in camions:
    for adresse in adresses[camion]:
        if adresse not in seen:
            seen.add(adresse)
            all_adresses.append((adresse, [camion]))
        else:
            for i in range(len(all_adresses)):
                if all_adresses[i][0] == adresse:
                    all_adresses[i][1].append(camion)
random.shuffle(all_adresses)
adresse_index = 0

def nouvelle_adresse():
    global adresse_index
    if adresse_index >= len(all_adresses):
        random.shuffle(all_adresses)
        adresse_index = 0
    adresse, camions_possibles = all_adresses[adresse_index]
    adresse_index += 1
    return camions_possibles, adresse

bons_camions, adresse_actuelle = nouvelle_adresse()
message = ""
score = 0
fautes = 0
erreurs = []
attente = False
attente_timer = 0
fin_jeu = False

# --- Boucle principale ---
scroll_offset = 0
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if fin_jeu:
                if rejouer_button.collidepoint(event.pos):
                    score = 0
                    fautes = 0
                    erreurs = []
                    message = ""
                    bon_camion, adresse_actuelle = nouvelle_adresse()
                    fin_jeu = False
                    scroll_offset = 0
                elif stop_button.collidepoint(event.pos):
                    running = False
                elif event.button == 4:
                    scroll_offset = max(0, scroll_offset - 30)
                elif event.button == 5:
                    scroll_offset = min(max(0, len(erreurs) * 30 - 400), scroll_offset + 30)
            elif not attente:
                for nom in camions:
                    if camion_rects[nom].collidepoint(event.pos):
                                            if nom in bons_camions:
                            if len(bons_camions) == 1:
                                message = "Bien joué !"
                                score += 1
                            else:
                                autres = [c for c in bons_camions if c != nom]
                                if autres:
                                    message = f"Bien joué ! ({nom}) était un des bons camions. Les autres étaient : " + ", ".join(autres)
                                else:
                                    message = f"Bien joué ! ({nom}) est un des bons camions."
                                score += 1
                        else:
                            message = "Raté ! C'était " + " ou ".join(bons_camions)
                            fautes += 1
                            erreurs.append((adresse_actuelle, " ou ".join(bons_camions), nom))
                        attente = True
                        attente_timer = 0

    screen.blit(fond_fin if fin_jeu else fond, (0, 0))

    if fin_jeu:
        fin_text = font.render("Fin du jeu", True, NOIR)
        screen.blit(fin_text, (LARGEUR // 2 - fin_text.get_width() // 2, 50))
        score_final = font.render(f"Score final: {score} | Fautes: {fautes}", True, NOIR)
        screen.blit(score_final, (LARGEUR // 2 - score_final.get_width() // 2, 100))

        pygame.draw.rect(screen, GRIS, rejouer_button, border_radius=10)
        rejouer_label = font.render("Rejouer", True, NOIR)
        screen.blit(rejouer_label, (rejouer_button.centerx - rejouer_label.get_width() // 2, rejouer_button.centery - rejouer_label.get_height() // 2))

        pygame.draw.rect(screen, GRIS, stop_button, border_radius=10)
        stop_label = font.render("Arrêter", True, NOIR)
        screen.blit(stop_label, (stop_button.centerx - stop_label.get_width() // 2, stop_button.centery - stop_label.get_height() // 2))

        if erreurs:
            err_title = font.render("Erreurs :", True, ROUGE)
            screen.blit(err_title, (50, 220))

            scroll_surface = pygame.Surface((LARGEUR - 100, 400))
            scroll_surface.fill((255, 255, 255))
            
            max_scroll = max(0, len(erreurs) * 30 - 400)
            for i, (adresse, bon, choisi) in enumerate(erreurs):
                couleur = BLEU if bon == "Vieux Lille" else ROUGE if bon == "Lille Centre" else VERT
                err_text = small_font.render(f"- {adresse} : attendu '{bon}', choisi '{choisi}'", True, couleur)
                scroll_surface.blit(err_text, (10, i * 30))

            screen.blit(scroll_surface, (50, 260), area=pygame.Rect(0, scroll_offset, LARGEUR - 100, 400))

            # gestion du scroll (molette)
# (déplacée dans la boucle principale — à ne pas dupliquer ici)

