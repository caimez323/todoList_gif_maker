import os
from PIL import Image, ImageDraw, ImageFont

FICHIER_TACHES = "todolist.txt"
GIF_TACHES = "todolist.gif"

def nettoyer_ecran():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_menu():
    print("Gestionnaire de To-Do List")
    print("1. Afficher les tâches")
    print("2. Ajouter une tâche")
    print("3. Supprimer une tâche")
    print("4. Exporter la liste en GIF avec défilement fluide")
    print("5. Paramètres")
    print("6. Quitter")

def afficher_taches(taches):
    nettoyer_ecran()
    if not taches:
        print("Aucune tâche dans la liste.")
    else:
        print("Liste des tâches :")
        for i, tache in enumerate(taches, 1):
            print(f"{i}. {tache}")

def ajouter_tache(taches):
    nettoyer_ecran()
    tache = input("Entrez la nouvelle tâche : ")
    taches.append(tache)
    print(f"Tâche '{tache}' ajoutée.")

def supprimer_tache(taches):
    nettoyer_ecran()
    afficher_taches(taches)
    if not taches:
        return
    try:
        choix = int(input("Entrez le numéro de la tâche à supprimer : "))
        nettoyer_ecran()
        if 1 <= choix <= len(taches):
            tache_supprimee = taches.pop(choix - 1)
            print(f"Tâche '{tache_supprimee}' supprimée.")
        else:
            print("Numéro de tâche invalide.")
    except ValueError:
        print("Veuillez entrer un numéro valide.")

def sauvegarder_taches(taches):
    with open(FICHIER_TACHES, "w") as fichier:
        for tache in taches:
            fichier.write(f"{tache}\n")

def charger_taches():
    if os.path.exists(FICHIER_TACHES):
        with open(FICHIER_TACHES, "r") as fichier:
            return [ligne.strip() for ligne in fichier.readlines()]
    return []

def exporter_en_gif_defilement(taches, largeur_image, hauteur_image, vitesse_defilement, taille_police, couleur_fond, couleur_texte):
    nettoyer_ecran()
    if not taches:
        print("Aucune tâche à exporter.")
        return

    try:
        font = ImageFont.truetype(os.path.join("polices", "Reey-Regular.otf"), taille_police)
    except IOError:
        font = ImageFont.load_default()

    # Calculer la hauteur nécessaire pour contenir toutes les tâches
    hauteur_texte = font.getbbox("Test")[3]
    espacement = 60
    hauteur_total = len(taches) * (hauteur_texte + espacement) + 200

    image_complete = Image.new('RGB', (largeur_image, hauteur_total), couleur_fond)
    draw = ImageDraw.Draw(image_complete)

    y_offset = 100
    for tache in taches:
        tache_texte = f"• {tache}"
        draw.text((100, y_offset), tache_texte, font=font, fill=couleur_texte)
        y_offset += hauteur_texte + espacement

    images = []

    if hauteur_total <= hauteur_image:
        images.append(image_complete.crop((0, 0, largeur_image, hauteur_image)))
    else:
        for i in range(0, hauteur_total - hauteur_image + vitesse_defilement, vitesse_defilement):
            image = image_complete.crop((0, i, largeur_image, i + hauteur_image))
            images.append(image)

    if images:
        images[0].save(GIF_TACHES, save_all=True, append_images=images[1:], loop=0, duration=30)
        print(f"Liste des tâches exportée en tant que GIF avec défilement fluide : {GIF_TACHES}")
    else:
        print("Aucune image n'a été générée pour le GIF.")

def modifier_parametres():
    print("\nModification des paramètres:")
    largeur_image = int(input("Largeur de l'image (par défaut 1920) : ") or 1920)
    hauteur_image = int(input("Hauteur de l'image (par défaut 1080) : ") or 1080)
    vitesse_defilement = int(input("Vitesse de défilement (en pixels, par défaut 5) : ") or 5)
    taille_police = int(input("Taille de la police (par défaut 100) : ") or 100)
    couleur_fond = tuple(map(int, input("Couleur de fond (R G B, par défaut 255 255 255) : ").split() or (255, 255, 255)))
    couleur_texte = tuple(map(int, input("Couleur du texte (R G B, par défaut 0 0 0) : ").split() or (0, 0, 0)))
    
    return largeur_image, hauteur_image, vitesse_defilement, taille_police, couleur_fond, couleur_texte

def main():
    taches = charger_taches()
    
    largeur_image = 1920
    hauteur_image = 1080
    vitesse_defilement = 5
    taille_police = 100
    couleur_fond = (255, 255, 255)
    couleur_texte = (0, 0, 0)

    while True:
        nettoyer_ecran()
        afficher_menu()
        choix = input("Choisissez une option : ")

        if choix == "1":
            afficher_taches(taches)
            input("\nAppuyez sur Entrée pour revenir au menu.")
        elif choix == "2":
            ajouter_tache(taches)
            sauvegarder_taches(taches)
            input("\nAppuyez sur Entrée pour revenir au menu.")
        elif choix == "3":
            supprimer_tache(taches)
            sauvegarder_taches(taches)
            input("\nAppuyez sur Entrée pour revenir au menu.")
        elif choix == "4":
            exporter_en_gif_defilement(taches, largeur_image, hauteur_image, vitesse_defilement, taille_police, couleur_fond, couleur_texte)
            input("\nAppuyez sur Entrée pour revenir au menu.")
        elif choix == "5":
            largeur_image, hauteur_image, vitesse_defilement, taille_police, couleur_fond, couleur_texte = modifier_parametres()
            input("\nParamètres modifiés. Appuyez sur Entrée pour revenir au menu.")
        elif choix == "6":
            sauvegarder_taches(taches)
            print("Au revoir!")
            break
        else:
            print("Option invalide, veuillez réessayer.")
            input("\nAppuyez sur Entrée pour revenir au menu.")

if __name__ == "__main__":
    main()
