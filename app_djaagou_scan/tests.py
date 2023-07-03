from PIL import Image

# Ouvrir l'image à coller
image_to_paste = Image.open("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/qrcode/black_qrcode_71_Test entreprise.png")

# Taille de l'image à coller
image_width, image_height = image_to_paste.size

# Taille de l'image A4
a4_width, a4_height = 2480, 3508 # en pixels

# Calculer la taille d'une image collée
paste_width = int((a4_width / 3)) # 10px de marge
paste_height = int((a4_height / 5)) # 10px de marge

# Créer une nouvelle image A4
a4_image = Image.new('RGB', (a4_width, a4_height), (255, 255, 255))

# Coller l'image 15 fois sur la nouvelle image
for i in range(20):
    x = (i % 3) * (paste_width) # 10px de marge
    y = int(i / 3) * (paste_height) # 10px de marge
    a4_image.paste(image_to_paste, (x, y))

# Enregistrer l'image A4
a4_image.show()
