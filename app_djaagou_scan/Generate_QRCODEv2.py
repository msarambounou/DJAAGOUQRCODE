from PIL import Image
import segno

flyer = Image.open(r"/Users/mamadousarambounou/Desktop/Unknown.jpeg")
qrcode = segno.make("https://www.instagram.com/itsmams.sb/").save("monqrcode.png")




# Récupération des dimensions actuelles
width, height = flyer.size

# Calcul des nouvelles dimensions
new_width = width / 2
new_height = height / 3

# Redimensionnement de l'image
qrcode2 = Image.open(r"monqrcode.png").resize((int(new_width), int(new_height)))

# Calculate the position to paste the overlay image
base_width, base_height = flyer.size
overlay_width, overlay_height = qrcode2.size
position = ((base_width - overlay_width) // 2, (base_height - overlay_height) // 2)




flyer.paste(qrcode2, position)

flyer.show()