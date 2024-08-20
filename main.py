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
    print("5. Quitter")


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


def exporter_en_gif_defilement(taches):
    nettoyer_ecran()
    if not taches:
        print("Aucune tâche à exporter.")
        return

    largeur_image = 1920
    hauteur_image = 1080
    couleur_fond = (255, 255, 255)  # Blanc
    couleur_texte = (0, 0, 0)  # Noir

    # Créer une grande image contenant toutes les tâches
    try:
        font = ImageFont.truetype(os.path.join("polices", "Reey-Regular.otf"), 100)
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

    # Maintenant, générer les images pour le GIF avec un défilement fluide
    images = []
    vitesse_defilement = 5  # Nombre de pixels à déplacer entre chaque image

    for i in range(0, hauteur_total - hauteur_image, vitesse_defilement):
        # Capturer une fenêtre de la grande image
        image = image_complete.crop((0, i, largeur_image, i + hauteur_image))
        images.append(image)

    # Sauvegarder les images en tant que GIF avec défilement fluide
    images[0].save(GIF_TACHES, save_all=True, append_images=images[1:], loop=0, duration=30)
    print(f"Liste des tâches exportée en tant que GIF avec défilement fluide : {GIF_TACHES}")


def main():
    taches = charger_taches()
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
            exporter_en_gif_defilement(taches)
            input("\nAppuyez sur Entrée pour revenir au menu.")
        elif choix == "5":
            sauvegarder_taches(taches)
            print("Au revoir!")
            break
        else:
            print("Option invalide, veuillez réessayer.")
            input("\nAppuyez sur Entrée pour revenir au menu.")


if __name__ == "__main__":
    main()
