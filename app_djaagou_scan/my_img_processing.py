from PIL import Image
import segno


def design_qrcode(initial, new):

    background1 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/background/backgroud1.jpg")
    background2 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/background/background2.JPG")
    background3 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/background/background3.JPG")

    qrcode_white = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/qrcode_initial/white"+initial+".png")
    qrcode_white = qrcode_white.resize((1000,1150))

    qrcode_black = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/qrcode_initial/black" + initial + ".png")
    qrcode_black = qrcode_black.resize((1000, 1150))

    background1.paste(qrcode_white, (320,1120), mask=qrcode_white)
    background1.save("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/qrcode_design/modele1_"+new+".png")
    path1 = "/media/Users_QRCODE/qrcode_design/modele1_"+new+".png"

    background2.paste(qrcode_black, (320, 1120))
    background2.save("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/qrcode_design/modele2_"+new+".png")
    path2 = "/media/Users_QRCODE/qrcode_design/modele2_"+new+".png"

    background3.paste(qrcode_white, (320, 1120), mask=qrcode_white)
    background3.save("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/qrcode_design/modele3_"+new+".png")
    path3 = "/media/Users_QRCODE/qrcode_design/modele3_"+new+".png"

    return path1, path2, path3

def concat_qrcode():
    img = Image.open("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/qrcode_initail_6_McDonald's.png")
    #img1 = Image.open("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/qrcode_initail_6_McDonald's.png")
    img.size
    #img1.size
    img_size = img.resize((250, 90))
    #img1_size = img1.resize((250, 90))

        # creating a new image and pasting
        # the images
    img2 = Image.new("RGB", (500, 500), "white")

        # pasting the first image (image_name,
        # (position))
    img2.paste(img_size, (0, 0))
    img2.paste(img_size, (0, 250))
    #img2.paste(img_size, (250, 0))

        # pasting the second image (image_name,
        # (position))
    #img2.paste(img1_size, (250, 0))

    #plt.imshow(img2)
    img2.show()


qrcode = segno.make("https://www.instagram.com/itsmams.sb/")

background1 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/background/backgroud1.jpg")
background2 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/background/background2.JPG")
background3 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/background/background3.JPG")

qrcode.save("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/test_QRCODE/qrcode1.png",dark='white', light='black', scale=20)
qrcode.save("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/test_QRCODE/qrcode2.png",dark='black', light='white', scale=20)

qrcode1 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/test_QRCODE/qrcode1.png")
#qrcode2 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/test_QRCODE/bg1_qrcode2.png")

qrcode1 = qrcode1.resize((1000, 1150))
#qrcode2 = qrcode2.resize((1000, 1150))

#background1 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/background/background1.jpg")
#background2 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/background/background2.JPG")

background1.paste(qrcode1, (320,1120), mask=qrcode1)
background1.save("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/app_djaagou_scan/static/modele_design/bg1_qrcode1.png")

#background2.paste(qrcode1, (320, 1120))
#background2.save("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/app_djaagou_scan/static/modele_design/bg2_qrcode1.png")

#background2.paste(qrcode2, (320, 1120))
background2.save("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/test_QRCODE/bg2_qrcode2.png")

qrcode_white = Image.open(
    r"/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/test_QRCODE/qrcode1.png")
qrcode_white = qrcode_white.resize((1000, 1150))
background3.paste(qrcode_white, (320, 1120), mask=qrcode_white)
background3.save("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/app_djaagou_scan/static/modele_design/modele3.png")