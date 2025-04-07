import pygame
import random
import sys
from vieux_lille import vieux_lille
from lille_centre import lille_centre
from lille_moulin import lille_moulin


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

# Choisir une adresse au hasard
def nouvelle_adresse():
    camion = random.choice(camions)
    adresse = random.choice(adresses[camion])
    return camion, adresse

bon_camion, adresse_actuelle = nouvelle_adresse()
message = ""
score = 0
fautes = 0
erreurs = []
attente = False
attente_timer = 0
fin_jeu = False

# --- Boucle principale ---
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60)
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
            for i, (adresse, bon, choisi) in enumerate(erreurs):
                couleur = BLEU if bon == "Vieux Lille" else ROUGE if bon == "Lille Centre" else VERT
                err_text = small_font.render(f"- {adresse} : attendu '{bon}', choisi '{choisi}'", True, couleur)
                screen.blit(err_text, (60, 260 + i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rejouer_button.collidepoint(event.pos):
                    score = 0
                    fautes = 0
                    erreurs = []
                    message = ""
                    bon_camion, adresse_actuelle = nouvelle_adresse()
                    fin_jeu = False
                elif stop_button.collidepoint(event.pos):
                    running = False

        pygame.display.flip()
        continue

    # Afficher la consigne sans surbrillance
    consigne_text = font.render("Dans quel camion va un colis à l'adresse :", True, NOIR)
    screen.blit(consigne_text, (LARGEUR // 2 - consigne_text.get_width() // 2, HAUTEUR // 4 - 70))

    couleur_adresse = BLEU if bon_camion == "Vieux Lille" else ROUGE if bon_camion == "Lille Centre" else VERT
    adresse_text = font.render(f"{adresse_actuelle}", True, couleur_adresse if attente else NOIR)
    screen.blit(adresse_text, (LARGEUR // 2 - adresse_text.get_width() // 2, HAUTEUR // 4 - 20))

    # Afficher le message de résultat juste en dessous de l'adresse
    if message:
        couleur_message = couleur_adresse
        msg_surface = font.render(message, True, couleur_message)
        screen.blit(msg_surface, (LARGEUR // 2 - msg_surface.get_width() // 2, HAUTEUR // 4 + 30))

    # Afficher le score et fautes
    score_text = font.render(f"Score: {score}", True, VERT)
    screen.blit(score_text, (10, 10))
    fautes_text = font.render(f"Fautes: {fautes}", True, ROUGE)
    screen.blit(fautes_text, (10, 50))

    # Afficher le bouton d'arrêt
    pygame.draw.rect(screen, GRIS, stop_button, border_radius=10)
    stop_label = font.render("Arrêter", True, NOIR)
    screen.blit(stop_label, (stop_button.centerx - stop_label.get_width() // 2, stop_button.centery - stop_label.get_height() // 2))

    # Attente après réponse
    if attente:
        attente_timer += dt
        if attente_timer > 2000:
            bon_camion, adresse_actuelle = nouvelle_adresse()
            message = ""
            attente = False
            attente_timer = 0

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if stop_button.collidepoint(pos):
                fin_jeu = True
            elif not attente:
                for nom in camions:
                    if camion_rects[nom].collidepoint(pos):
                        if nom == bon_camion:
                            message = "Bien joué !"
                            score += 1
                        else:
                            message = f"Raté ! C'était {bon_camion}"
                            fautes += 1
                            erreurs.append((adresse_actuelle, bon_camion, nom))
                        attente = True
                        attente_timer = 0

    pygame.display.flip()

pygame.quit()
sys.exit()

