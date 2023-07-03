import qrcode
import segno
from PIL import Image
from .models import user_qrcode


def new_qrcode(id_user, url_redirection, id_entreprise, nom_entreprise):
    qrcode = segno.make(url_redirection)
    path_qrcode_folder = "/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/qrcode/"

    white_qrcode_name = "white_qrcode_" + id_entreprise + "_" + nom_entreprise
    black_qrcode_name = "black_qrcode_" + id_entreprise + "_" + nom_entreprise

    qrcode.save(path_qrcode_folder + white_qrcode_name + ".png", dark='white', light='black', scale=20)
    qrcode.save(path_qrcode_folder + black_qrcode_name + ".png", dark='black', light='white', scale=20)

    user_qrcode.objects.create(id_user=id_user,
                               path_black_qrcode=black_qrcode_name + white_qrcode_name + ".png",
                               path_white_qrcode=path_qrcode_folder + white_qrcode_name + ".png",
                               id_entreprise=id_entreprise
                               )




