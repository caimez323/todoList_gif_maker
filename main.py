import os
from PIL import Image, ImageDraw, ImageFont

FICHIER_TACHES = "todolist.txt"
IMAGE_TACHES = "todolist.png"


def nettoyer_ecran():
  os.system('cls' if os.name == 'nt' else 'clear')


def afficher_menu():
  print("Gestionnaire de To-Do List")
  print("1. Afficher les tâches")
  print("2. Ajouter une tâche")
  print("3. Supprimer une tâche")
  print("4. Exporter la liste en image")
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


def exporter_en_image(taches):
  nettoyer_ecran()
  if not taches:
    print("Aucune tâche à exporter.")
    return

  largeur_image = 3840  # 4K largeur
  hauteur_image = 2160  # 4K hauteur
  couleur_fond = (255, 255, 255)  # Blanc
  couleur_texte = (0, 0, 0)  # Noir

  # Crée une nouvelle image avec une résolution de 4K
  image = Image.new('RGB', (largeur_image, hauteur_image), couleur_fond)
  draw = ImageDraw.Draw(image)

  # Utiliser une autre police intégrée ou disponible pour tester
  try:
    font = ImageFont.truetype(os.path.join("polices", "Reey-Regular.otf"), 220)
  except IOError:
    font = ImageFont.load_default()

  # Ajoute les tâches, en commençant à 250 pixels de hauteur
  y_offset = 100
  for i, tache in enumerate(taches, start=1):
    tache_texte = f"• {tache}"
    largeur_texte, hauteur_texte = draw.textbbox((0, 0),
                                                 tache_texte,
                                                 font=font)[2:]
    draw.text((100, y_offset), tache_texte, font=font, fill=couleur_texte)
    y_offset += hauteur_texte + 60  # Espacement entre les lignes avec une plus grande police

  # Redimensionner l'image finale en 1920x1080
  image = image.resize((1920, 1080), Image.LANCZOS)
  image.save(IMAGE_TACHES)
  print(f"Liste des tâches exportée en tant qu'image : {IMAGE_TACHES}")


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
      exporter_en_image(taches)
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
