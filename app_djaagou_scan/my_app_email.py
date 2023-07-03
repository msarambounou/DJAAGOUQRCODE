from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

def my_email_new_user(link_html, receiver_address, random_code):
    html = "<!DOCTYPE html>" \
           "<html>" \
           "<head>" \
           "<title>Example</title>" \
           "</head>" \
           "<body>" \
           "<p>Veuillez trouvez votre code de confirmation :</p>" \
           "<h2>CODE :"+random_code+"</h2>" \
           "</body>" \
           "</html>"

    # The mail addresses and password
    sender_address = settings.EMAIL_HOST_USER
    sender_pass = settings.EMAIL_HOST_PASSWORD
    receiver_address = receiver_address

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "DJAAGOU : Confirmer l'inscription"

    # The body and the attachments for the mail
    message.attach(MIMEText(html, 'html'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()

    session.starttls()  # enable security
    session.ehlo()
    session.login(sender_address, sender_pass)
    text = message.as_string()

    return session.sendmail(sender_address, receiver_address, text)


def email_qr_code(receiver_address, qr_code_path):
    html = "<!DOCTYPE html>" \
           "<html>" \
           "<head>" \
           "<title>Example</title>" \
           "</head>" \
           "<body>" \
           "<p>Veuillez trouvez votre QR-CODE :</p>" \
           "</body>" \
           "</html>"

    # The mail addresses and password
    sender_address = settings.EMAIL_HOST_USER
    sender_pass = settings.EMAIL_HOST_PASSWORD
    receiver_address = receiver_address

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "DJAAGOU : Votre QR-CODE"

    # The body and the attachments for the mail
    message.attach(MIMEText(html, 'html'))

    #image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    #message.attach(image)
    #message.attach(qr_code_path)

    fp = open("/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/media/Users_QRCODE/"+qr_code_path+".png", 'rb')  # Read image
    msgImage = MIMEImage(fp.read())
    fp.close()
    # Define the image's ID as referenced above
    #msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()

    session.starttls()  # enable security
    session.ehlo()
    session.login(sender_address, sender_pass)
    text = message.as_string()

    return session.sendmail(sender_address, receiver_address, text)