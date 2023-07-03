from PIL import Image, ImageDraw, ImageFont

# Ouvrir l'image
image = Image.open("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/qrcode/black_qrcode_71_Test entreprise.png")

# Créer un objet ImageDraw pour dessiner sur l'image
draw = ImageDraw.Draw(image)

# Définir la police et la taille du texte
font = ImageFont.truetype("Arial.ttf", 40)

# Définir le texte à écrire
text_top = "DIAW ELEC"
text_bottom = "CONTACTEZ-NOUS !"

# Obtenir la taille du texte
text_width_top, text_height_top = draw.textsize(text_top, font=font)
text_width_bottom, text_height_bottom = draw.textsize(text_bottom, font=font)

# Calculer les coordonnées x et y pour centrer le texte en bas de l'image
x_top = (image.width - text_width_top) / 2
y_top = 0 # 20px de marge en haut

x_bottom = (image.width - text_width_bottom) / 2
y_bottom = image.height - text_height_bottom - 20 # 20px de marge en bas

# Écrire le texte sur l'image en blanc (couleur entière : 16777215)
draw.text((x_top, y_top), text_top, font=font, fill=0)
draw.text((x_bottom, y_bottom), text_bottom, font=font, fill=0)

# Enregistrer l'image modifiée
image.show()
