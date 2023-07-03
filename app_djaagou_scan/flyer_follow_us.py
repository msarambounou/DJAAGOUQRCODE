from PIL import Image

flyer = Image.open(r"/Users/mamadousarambounou/Downloads/Sans titre-6/3.png")
flyer2 = Image.open(r"/Users/mamadousarambounou/Downloads/Sans titre-6/2.png")
flyer3 = Image.open(r"/Users/mamadousarambounou/Downloads/Sans titre-6/1.png")

# Récupération des dimensions actuelles
width, height = flyer.size

# Calcul des nouvelles dimensions
new_width = width / 1.5
new_height = height / 2.1

qrcode_modele = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/qrcode/modele.png").resize((int(new_width), int(new_height)))
qrcode = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/qrcode/black_qrcode_71_Test entreprise.png").resize((int(new_width), int(new_height)))

flyer_width, flyer_height = flyer.size
qrcode_width, qrcode_height = qrcode.size
position = ((flyer_width - qrcode_width) // 2, (flyer_height - qrcode_height) // 2)

flyer.paste(qrcode, position)
flyer2.paste(qrcode, position)
flyer3.paste(qrcode, position)

flyer.show()
flyer2.show()
flyer3.show()
