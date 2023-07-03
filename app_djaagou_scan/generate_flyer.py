from PIL import Image
import segno
from .models import user_flyer
import string
import random

def new_flyer(id_user, id_entreprise, nom_entreprise):
    path_background = "/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/flyer/background/"
    path_qrcode_folder = "/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/qrcode/"
    path_flyer_folder = "/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/flyer/"

    background_1 = Image.open(r"" + path_background + "background1.jpg")
    background_2 = Image.open(r"" + path_background + "background2.JPG")
    background_3 = Image.open(r"" + path_background + "background3.JPG")
    test_cutom = Image.open(r"/Users/mamadousarambounou/Desktop/test_cutom_flyer.png")

    white_qrcode_path = "white_qrcode_" + id_entreprise + "_" + nom_entreprise + ".png"
    black_qrcode_path = "black_qrcode_" + id_entreprise + "_" + nom_entreprise + ".png"

    white_qrcode = Image.open(r"" + path_qrcode_folder + white_qrcode_path).resize((1000, 1150))
    black_qrcode = Image.open(r"" + path_qrcode_folder + black_qrcode_path).resize((1000, 1150))

    background_1.paste(white_qrcode, (320, 1120), mask=white_qrcode)
    background_2.paste(black_qrcode, (320, 1120))
    background_3.paste(white_qrcode, (320, 1120), mask=white_qrcode)

# SAVE LES 3 MODELE
    path_modele1 = path_flyer_folder + id_entreprise + "_" + nom_entreprise + "modele1" + ".png"
    path_modele2 = path_flyer_folder + id_entreprise + "_" + nom_entreprise + "modele2" + ".png"
    path_modele3 = path_flyer_folder + id_entreprise + "_" + nom_entreprise + "modele3" + ".png"

    background_1.save(path_modele1)
    background_2.save(path_modele2)
    background_3.save(path_modele3)

# AJOUTER A LA BASE DE DONNEES
    user_flyer.objects.create(id_user=id_user, id_entreprise=id_entreprise, name_modele= "1",
                              path_modele=path_modele1)
    user_flyer.objects.create(id_user=id_user, id_entreprise=id_entreprise, name_modele="2",
                              path_modele=path_modele2)
    user_flyer.objects.create(id_user=id_user, id_entreprise=id_entreprise, name_modele="3",
                              path_modele=path_modele3)

def custom_flyer(path_flyer, id_user, id_entreprise, nom_entreprise):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(8))

    path_flyer_prefixe = "/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN"
    path_qrcode_prefixe = "/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/qrcode/"
    path_flyer_final_prefixe = "/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/flyer/cutom/"
    path_user_qrcode = "black_qrcode_" + id_entreprise + "_" + nom_entreprise + ".png"

    name_flyer_final = random_string + "custom_flyer_" + id_entreprise + nom_entreprise + ".png"

    path_custom_flyer_bdd = "/media/flyer/cutom/" + name_flyer_final


    flyer = Image.open(r"" + path_flyer_prefixe + path_flyer)
    flyer2 = Image.open(r"" + path_flyer_prefixe + path_flyer)


    # Récupération des dimensions actuelles
    width, height = flyer.size

    # Calcul des nouvelles dimensions
    new_width = width / 2
    new_height = height / 3

    qrcode_modele = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/qrcode/modele.png").resize((int(new_width), int(new_height)))
    qrcode = Image.open(r"" + path_qrcode_prefixe + path_user_qrcode).resize((int(new_width), int(new_height)))

    flyer_width, flyer_height = flyer.size
    qrcode_width, qrcode_height = qrcode.size
    position = ((flyer_width - qrcode_width) // 2, (flyer_height - qrcode_height) // 2)

    flyer.paste(qrcode, position)
    flyer2.paste(qrcode_modele, position)

    flyer.save(path_flyer_final_prefixe + name_flyer_final)
    flyer.save(path_flyer_final_prefixe + "modele_" +name_flyer_final)

    user_flyer.objects.create(id_user=id_user, id_entreprise=id_entreprise, name_modele="perso",
                              path_modele=path_custom_flyer_bdd)