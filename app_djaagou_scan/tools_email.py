from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

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

#----------------------------------------------- NEW USER -----------------------------------------------

def my_email_new_user(link_html, receiver_address, random_code):
    html = """<html>
    <body>
        <div>
             <img style="display: block; margin-right: auto; margin-left: auto" width="170px;" src="https://media.licdn.com/dms/image/C4D03AQGmq9uxPGMQ9A/profile-displayphoto-shrink_400_400/0/1626703178998?e=1678924800&v=beta&t=V6XBgHxeXZwsYWROHk3gydsV92RUhebS0aJozh_S1Y0">
        </div>

        <div style="box-shadow: rgba(6, 24, 44, 0.4) 0px 0px 0px 2px, rgba(6, 24, 44, 0.65) 0px 4px 6px -1px, rgba(255, 255, 255, 0.08) 0px 1px 0px inset;;
         width: 100%; display: block; margin-left: auto; margin-right: auto";>
            <div style="margin-left: 5%; margin-right: 5%; margin-top:5% ;padding-bottom: 5%; padding-top: 5%">
                <p>Bienvenu !</p>
            </br>
            <p>
                Pour bénéficier de toutes les fonctionnalités de <b>MY QR-CODE SOLUTIONS</b>,
                veuillez saisir le code ci-dessous dans le champs prévus de la page de validation de
                votre email :
            </p>
            <div style="box-shadow: rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px;
                  ; display: block; margin-right: auto; margin-left: auto; background-color: #45b8d3" >
                <h1 style="text-align: center">"""+random_code+"""</h1>
            </div>
            <p>
                Ce code est valable 10 minutes. Au-delà, vous pouvez demander le renvoi
                d'un code par email directement depuis la page vous demandant de saisir le code ou depuis
                la rubrique Mon Compte de l'application.</p>

            <br/>

            <p>L'équipe MY QR-CODE SOLUTIONS</p>

            </div>


        </div>
    </body>
</html>"""

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

#------------------------------------------ PASSWORD ---------------------------------------------

def forget_password(request):
    users = list(User.objects.values_list("username", flat=True))

    if request.method == "POST":
        email_request = request.POST["email"]

        if email_request in users:

            html = open('/Users/mamadousarambounou/Desktop/projet/DJAAGOU_SCAN/app_djaagou_scan/templates/02_Email/email_forget_password.html', 'r')
            html = html.read()

            # The mail addresses and password
            sender_address = settings.EMAIL_HOST_USER
            sender_pass = settings.EMAIL_HOST_PASSWORD
            receiver_address = "msarambounou11@gmail.com"

            # Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'DJAAGOU : Mot de passe oublié'

            # The body and the attachments for the mail
            message.attach(MIMEText(html, 'html'))

            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.ehlo()

            session.starttls()  # enable security
            session.ehlo()
            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            messages.success(request, "Vous allez recevoir un email")
            return redirect("/mot_de_passe_oublie/")

        else:
            messages.error(request, "Cet email n'existe de pas")
            return redirect("/mot_de_passe_oublie/")

    return render(request, '01_Authentification/forget_password.html')