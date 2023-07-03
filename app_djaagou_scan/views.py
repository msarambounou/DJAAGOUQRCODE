from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login
from .models import Categorie_article, Article, UserConfirmation, Entreprise, Categorie_ets, Devises, user_qrcode, Option_tables,\
    user_flyer, All_social_media, Entreprise_social_media, Option_commande_intermediaire, Option_commande, Business_card_social_media
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import make_password
import random
import string
from app_djaagou_scan.generate_qrcode import new_qrcode
from app_djaagou_scan.generate_flyer import new_flyer, custom_flyer
import stripe
from datetime import datetime
from app_djaagou_scan.random_tools import generate_random_string
from app_djaagou_scan.tools_email import my_email_new_user
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from django.db.models import Avg, Count, Min, Sum

# ------------------------------------------------------------- EMAIL -------------------------------------------------------------
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

def home(request):

    #return render(request, '06_QRCODE/test/test_superposer_2_div.html')

   return render(request, '00_Home/home.html')


def inscription(request):
    letters = string.ascii_lowercase
    random_code = ''.join(random.choice(letters) for i in range(8))

    if request.method == "POST":
        first_name = request.POST["first_name"].capitalize()
        last_name = request.POST["last_name"].upper()
        email = request.POST["email"].lower()
        password = request.POST["password"]
        password_confirmation = request.POST["confirme_password"]

        if password_confirmation != password:
            messages.error(request, "Mot de passe de confirmation différent du mot de passe")
            return redirect("/inscription/")

        my_email_new_user('app_djaagou_scan/templates/email_inscription_code.html', "msarambounou11@gmail.com", random_code)

        User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password,
                                 username=email, is_active=0)

        UserConfirmation.objects.create(email=email, code_confirmation=random_code)

        messages.success(request, "Un code de confirmation vous à été envoyé par email")
        return redirect("/inscription_code/"+email)

    return render(request, '01_Authentification/inscription.html')

# ------------------------------------------------------- AUTHENTIFICATION -------------------------------------------------------

def inscription_code(request, email):
    new_user = UserConfirmation.objects.values_list("email", "code_confirmation").get(email=email)
    #users = list(User.objects.values_list("username", flat=True))
    print(new_user)
    if request.method == "POST":
        code_confirmation = request.POST["code_confirmation"]

        if new_user[0] == email and new_user[1] == code_confirmation:
            User.objects.filter(username=email).update(is_active=1)

            messages.success(request,"Votre compte à été créer !")
            return redirect("/connexion/")
        else:
            messages.error(request, "Code de confirmation incorrecte")
            return redirect("/inscription_code/"+email)

    return render(request, '01_Authentification/inscription_code.html', {"email":email})

def connexion(request):
    if request.method == "POST":
        email = request.POST["email"].lower()
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            messages.success(request, "Bienvenu !")
            return redirect("/")
        else :
            messages.error(request, "Email ou mot de passe incorrect")
            redirect("/connexion/")
    return render(request, '01_Authentification/login2.html')

@login_required(login_url="/connexion/")
def logout(request):
    auth.logout(request)
    messages.error(request, "Vous êtes déconnecté")
    return redirect('/')

#--------------------------------------------------------------- CREATE ---------------------------------------------------------------

@login_required(login_url="/connexion/")
def add_article(request):
    current_user = request.user
    current_user_id = current_user.id

    if request.method == "POST":
        nom_entreprise = request.POST['my_entreprise']
        name = request.POST['article_name'].capitalize()
        input_categorie = request.POST['categorie_article'].capitalize()
        price = request.POST['price']
        description = request.POST['description'].capitalize()
        image = request.FILES['image']

        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        image_url = fss.url(file)

        print("NOM CATEGORIE : ", input_categorie)

        categorie = Categorie_article.objects.all().get(id_user=current_user_id,
                                                        nom_categorie_article=input_categorie,
                                                        nom_entreprise=nom_entreprise)
        #nom_entreprise = Categorie_article.objects.values_list("nom_entreprise").filter(id_user=current_user_id,nom_categorie_article=categorie)

        #id_entreprise = id_entreprise[0]
        #nom_entreprise = nom_entreprise[0]

        Article.objects.create(nom_article=name, nom_categorie=input_categorie, prix=price, description=description,
                               image_path=image_url, id_user=current_user.id, id_entreprise=categorie.id_ets,
                               nom_entreprise=categorie.nom_entreprise, statut=1)

        id_ets = str(categorie.id_ets)

        messages.success(request, "Ajout résussit !")

        redirect("/manage_entreprise/")

        return redirect("/manage_entreprise/manage_menu/"+id_ets)

    return render(request, '06_QRCODE/01_Manage/manage_menu.html')

@login_required(login_url="/connexion/")
def add_categorie(request):
    current_user = request.user
    current_user_id = current_user.id

    #my_entreprise = Entreprise.objects.all().get(id_user=current_user_id)

    if request.method == "POST":
        nom_entreprise = request.POST['my_entreprise']
        name = request.POST['nom_categorie'].capitalize()

        print(nom_entreprise)
        entreprise = Entreprise.objects.all().get(nom_ets=nom_entreprise, id_user=current_user_id, statut=1)

        categories = Categorie_article.objects.values_list("nom_categorie_article", flat=True).filter(id_user=current_user.id, id_ets=entreprise.id)
        for i in categories:
            if i == name:
                messages.error(request, "Cette catégorie existe déjà pour la même entreprise")
                return redirect('/manage_categorie/'+str(entreprise.id))

        Categorie_article.objects.create(nom_categorie_article=name, id_user=current_user_id, id_ets=entreprise.id,nom_entreprise=entreprise.nom_ets, statut=1)

        messages.success(request, "Ajout réussit !")
        return redirect('/manage_categorie/'+str(entreprise.id))

    return render(request, 'index.html')

def add_ets(request):
    current_user = request.user
    current_user_id = current_user.id


    if request.method == "POST":
        name_entreprise = request.POST['name_entreprise'].capitalize()
        categorie_entreprise = request.POST['categorie_entreprise'].capitalize()
        image = request.FILES['image_logo']
        my_devise = request.POST['devise']
        nb_places = request.POST['nb_places']

        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        image_url = fss.url(file)

        new_entreprise = Entreprise.objects.create(secteur=categorie_entreprise, nom_ets=name_entreprise,
                                                   id_user=current_user.id, logo_ets=image_url,
                                                   nom_devise=my_devise, nb_places=nb_places, statut=1)
        for i in range(int(nb_places)):
            Option_tables.objects.create(id_user=current_user_id,
                                     id_entreprise=new_entreprise.id,
                                     numero_table=i+1,
                                     statut_table=1)

        new_qrcode(current_user_id, "https://www.instagram.com/itsmams.sb/", str(new_entreprise.id), new_entreprise.nom_ets)
        new_flyer(current_user_id, str(new_entreprise.id), new_entreprise.nom_ets)

        return redirect('/manage_entreprise/')

    return render(request, '06_QRCODE/01_Manage/manage_ets.html')


#--------------------------------------------------------------- DELETE ---------------------------------------------------------------

@login_required(login_url="/connexion/")
def masquer_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    id_entreprise = Article.objects.values_list("id_entreprise").get(id=article_id)

    id_ets = str(id_entreprise[0])

    if request.method == "POST":
        Article.objects.filter(pk=article_id).update(statut=0)

        return redirect("/manage_entreprise/manage_menu/"+id_ets)

    return render(request, '06_QRCODE/04_Delete/masquer_article.html', {'article': article, 'article_id': article_id})

@login_required(login_url="/connexion/")
def delete_article(request, article_id):
    article = Article.objects.get(pk=article_id)

    if request.method == "POST":
        Article.objects.filter(pk=article_id).delete()

        return redirect("/historique_article/")

    return render(request, '06_QRCODE/04_Delete/delete_article2.html', {'article': article, 'article_id': article_id})


def masquer_categorie(request, categorie_id):
    categorie = Categorie_article.objects.get(pk=categorie_id)

    if request.method == "POST":
        Categorie_article.objects.filter(pk=categorie_id).update(statut=0)

        messages.success(request, "La catégorie à bien été supprimée !")
        return redirect('/manage_categorie/'+str(categorie.id_ets))

    return render(request, '06_QRCODE/04_Delete/masquer_categorie.html', {'categorie':categorie, "categorie_id":categorie_id})

def delete_categorie(request, id_categorie):
    categorie = Categorie_article.objects.get(pk=id_categorie)

    if request.method == "POST":
        Categorie_article.objects.filter(pk=id_categorie).delete()

        messages.success(request, "La catégorie à bien été supprimée !")
        return redirect('/historique_categorie')

    return render(request, '06_QRCODE/04_Delete/delete_categorie.html', {'categorie':categorie, "categorie_id":id_categorie})


def masquer_entreprise(request, id_entreprise):
    entreprise = Entreprise.objects.get(pk=id_entreprise)

    if request.method == "POST":
        Entreprise.objects.filter(pk=id_entreprise).update(statut=0)
        Categorie_article.objects.filter(id_ets=id_entreprise).update(statut=0)
        Article.objects.filter(id_entreprise=id_entreprise).update(statut=0)

        return redirect('/manage_entreprise/')

    return render(request, '06_QRCODE/04_Delete/masquer_entreprise.html', {'entreprise':entreprise})


def delete_business_card(request, id_reseau_social):
    current_user_rs = social_media_link.objects.get(pk=id_reseau_social)

    if request.method == "POST":
        social_media_link.objects.filter(pk=id_reseau_social).delete()

        messages.success(request, "Suppression réussit !")
        return redirect("/manage_business_card/")

    return render(request, '07_BUSINESS_CARD/delete_reseau_social.html', {"current_user_rs": current_user_rs})

#--------------------------------------------------------------- UPDATE ---------------------------------------------------------------

def update_user(request):
    current_user = request.user
    current_user_id = current_user.id


    if request.method == "POST":
        new_firstname = request.POST["new_firstname"]
        new_lastname = request.POST["new_lastname"]

        User.objects.filter(id=current_user_id).update(first_name=new_firstname, last_name=new_lastname)

        return redirect("/my_account/")


    return render(request, '01_Authentification/update_user.html')

@login_required(login_url="/connexion/")
def update_article(request, article_id):
    categorie_articles = Categorie_article.objects.all()
    article = Article.objects.get(pk=article_id)

    if request.method == "POST":
        name = request.POST['article_name']
        category = request.POST['categorie_article']
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES['image']

        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        image_url = fss.url(file)

        if image is None:
            Article.objects.filter(pk=article_id).update(nom_article=name, nom_categorie=category, prix=price, description=description)
        else:
            #Product.objects.filter(name=name,category_name=category, Price=price, Description=description, image=image)
            Article.objects.filter(pk=article_id).update(nom_article=name, nom_categorie=category, prix=price, description=description, image_path=image_url)

        id_entreprise = article.id_entreprise
        return redirect('/manage_entreprise/manage_menu/'+str(id_entreprise))

    return render(request, '06_QRCODE/05_Update/update_article3.html', {'article': article, 'categorie_articles': categorie_articles, 'article_id': article_id})

def update_categorie(request, categorie_id):
    categorie = Categorie_article.objects.get(pk=categorie_id)
    id_entreprise = Categorie_article.objects.values_list("id_ets").filter(pk=categorie_id)
    id_entreprise = id_entreprise[0]

    if request.method == "POST":
        categorie_name = request.POST["categorie_name"]
        Categorie_article.objects.filter(pk=categorie_id).update(nom_categorie_article=categorie_name)

        messages.success(request, "Modification résussit !")
        return redirect('/manage_categorie/'+str(id_entreprise[0]))

    return render(request, '06_QRCODE/05_Update/update_categorie.html', {'categorie':categorie, 'categorie_id':categorie_id})

def update_entreprise(request, entreprise_id):
    current_user = request.user
    current_user_id = current_user.id

    entreprise = Entreprise.objects.get(pk=entreprise_id)
    categorie_entreprise = Categorie_ets.objects.all().exclude(nom_categorie_ets=entreprise.secteur)
    devise = Devises.objects.all()

    if request.method == "POST":
        name_ets = request.POST['name_ets']
        categorie_ets = request.POST['categorie_ets']
        my_devise = request.POST['devise']
        nb_places = request.POST['nb_places']

        if entreprise.nb_places != nb_places:
            Option_tables.objects.filter(id_user=current_user_id, id_entreprise=entreprise.id).delete()

            for i in range(int(nb_places)):
                Option_tables.objects.create(id_user=current_user_id,
                                             id_entreprise=entreprise.id,
                                             numero_table=i + 1,
                                             statut_table=1)

        if (len(request.FILES) != 0):
            image = request.FILES["image"]

            fss = FileSystemStorage()
            file = fss.save(image.name, image)
            image_url = fss.url(file)

            Entreprise.objects.filter(pk=entreprise_id).update(secteur=categorie_ets, nom_ets=name_ets,
                                                               nom_devise=my_devise, logo_ets=image_url, nb_places=nb_places)

        else:

            Entreprise.objects.filter(pk=entreprise_id).update(secteur=categorie_ets, nom_ets=name_ets,
                                                               nom_devise=my_devise, nb_places=nb_places)


        return redirect("/manage_entreprise/")

    return render(request, '06_QRCODE/05_Update/update_entreprise2.html', {'entreprise':entreprise, 'categorie_entreprise':categorie_entreprise, 'entreprise_id':entreprise_id, 'devise':devise})

def update_reseau_social(request, id_reseau_social):
    current_user_rs = social_media_link.objects.get(pk=id_reseau_social)

    if request.method == "POST":
        link = request.POST["link"]
        social_media_link.objects.filter(pk=id_reseau_social).update(link=link)

        messages.success(request, "Modification réussit !")
        return redirect("/manage_business_card/")

    return render(request, '07_BUSINESS_CARD/update_reseau_social.html', {"current_user_rs":current_user_rs})
#--------------------------------------------------------------- ABONNEMENT ---------------------------------------------------------------
def manage_abonnement(request):
    return render(request, '06_QRCODE/07_Abonnement/manage_abonnement.html')

#--------------------------------------------------------------- HISTORIQUE ---------------------------------------------------------------
def manage_historique(request):
    return render(request, '06_QRCODE/06_Historique/manage_historique.html')

def historique_entreprise(request):
    current_user = request.user
    current_user_id = current_user.id

    entreprises = Entreprise.objects.all().filter(id_user=current_user_id, statut=0)
    len_entreprises = len(entreprises)

    return render(request, '06_QRCODE/06_Historique/historique_entreprise.html', {'entreprises':entreprises, 'len_entreprises':len_entreprises})

def historique_categorie(request):
    current_user = request.user
    current_user_id = current_user.id

    categories = Categorie_article.objects.all().filter(id_user=current_user_id, statut=0)
    len_categories = len(categories)

    return render(request, '06_QRCODE/06_Historique/historique_categorie.html', {'categories':categories, 'len_categories':len_categories})

def historique_article(request):
    current_user = request.user
    current_user_id = current_user.id

    articles = Article.objects.all().filter(id_user=current_user_id, statut=0)
    len_articles = len(articles)

    return render(request, '06_QRCODE/06_Historique/historique_article.html', {'articles':articles, 'len_articles':len_articles})

def recuperer_entreprise(request, id_entreprise):
    entreprise = Entreprise.objects.all().get(id=id_entreprise)

    if request.method == "POST":
        Entreprise.objects.filter(id=id_entreprise).update(statut=1)
        Categorie_article.objects.filter(id_ets=id_entreprise).update(statut=1)
        Article.objects.filter(id_entreprise=id_entreprise).update(statut=1)

        return redirect("/gestion_des_historiques/")
    return render(request, '06_QRCODE/Recuperer/recuperer_entreprise.html', {"entreprise":entreprise})

def recuperer_categorie(request, id_categorie):
    categorie = Categorie_article.objects.all().get(id=id_categorie)
    entreprise = Entreprise.objects.all().get(id=categorie.id_ets)

    if request.method == "POST":
        if entreprise.statut == 0:
            messages.error(request, "Impossible de récupérer cette catégorie car l'entreprise correspond n'existe plus.")
        else :
            Categorie_article.objects.filter(id=id_categorie).update(statut=1)

        return redirect("/gestion_des_historiques/")
    return render(request, '06_QRCODE/Recuperer/recuperer_categorie.html', {"categorie":categorie})

def recuperer_article(request, id_article):
    article = Article.objects.all().get(id=id_article)
    entreprise = Entreprise.objects.all().get(id=article.id_entreprise)

    if request.method == "POST":
        if entreprise.statut == 0:
            messages.error(request, "Impossible de récupérer cette catégorie car l'entreprise correspond n'existe plus.")
        else :
            Article.objects.filter(id=id_article).update(statut=1)


        return redirect("/gestion_des_historiques/")
    return render(request, '06_QRCODE/Recuperer/recuperer_article.html', {"article":article})


def delete_entreprise(request, id_entreprise):
    entreprise = Entreprise.objects.all().get(id=id_entreprise)

    if request.method == "POST":
        Entreprise.objects.filter(id=id_entreprise).delete()
        Categorie_article.objects.filter(id_ets=id_entreprise).delete()
        Article.objects.filter(id_entreprise=id_entreprise).delete()

        return redirect("/historique_entreprise/")
    return render(request, '06_QRCODE/04_Delete/delete_entreprise2.html', {"entreprise":entreprise})



#--------------------------------------------------------------- MANAGE ---------------------------------------------------------------
@login_required(login_url="/connexion/")
def manage_menu(request, entreprise_id):
    current_user = request.user
    current_user_id = current_user.id

# QUERY
    articles = Article.objects.all().filter(id_user=current_user_id, id_entreprise=entreprise_id, statut=1)
    len_articles = len(articles)
    #print("NOMBRE ARTICLE : ", len_articles)

    for i in articles:
        if i.prix.is_integer():
            i.prix = int(i.prix)

    categorie_article = Categorie_article.objects.all().filter(id_user=current_user_id, id_ets=entreprise_id, statut=1)
    list_categorie = Categorie_article.objects.all().distinct()
    my_entreprise = Entreprise.objects.all().get(id=entreprise_id)

    nom_entreprise = my_entreprise.nom_ets


    return render(request, '06_QRCODE/01_Manage/manage_menu.html', {"categorie_article": categorie_article, "articles":articles, 'entreprise_id':entreprise_id, "nom_entreprise":my_entreprise.nom_ets, "len_articles":len_articles, 'list_categorie':list_categorie, 'nom_entreprise':nom_entreprise})


@login_required(login_url="/connexion/")
def manage_categorie(request, id_entreprise):
    current_user = request.user
    current_user_id = current_user.id

    categorie_article = Categorie_article.objects.all().filter(id_user=current_user_id, id_ets=id_entreprise, statut=1)
    len_categories = len(categorie_article)
    my_entreprise = Entreprise.objects.all().get(id=id_entreprise)

    return render(request, '06_QRCODE/01_Manage/manage_categorie.html',
                  {"categorie_article": categorie_article, 'entreprise':my_entreprise.nom_ets, 'len_categories':len_categories})

def manage_entreprise(request):
    current_user = request.user
    current_user_id = current_user.id

    entreprises = Entreprise.objects.all().filter(id_user=current_user_id, statut=1)
    len_entreprises = len(entreprises)
    categorie_entreprises = Categorie_ets.objects.all()
    devise = Devises.objects.all()

    return render(request, '06_QRCODE/01_Manage/manage_ets.html',
                  {'entreprises':entreprises, 'categorie_entreprises':categorie_entreprises, 'devise':devise, 'len_entreprises':len_entreprises})

def manage_qrcode(request, id_entreprise):
    current_user = request.user
    current_user_id = current_user.id

    my_qrcode = user_qrcode.objects.all().filter(id_user=current_user_id, id_entreprise=id_entreprise)

    flyers = user_flyer.objects.filter(id_entreprise=id_entreprise)

    path_modele = list(flyers.values_list("path_modele", flat=True).filter(name_modele="perso", id_entreprise=id_entreprise))
    len_path_modele = len(path_modele)

    if len_path_modele != 0:
        path_modele = path_modele[0]

    entreprise = Entreprise.objects.get(pk=id_entreprise)

    categorie_article = Categorie_article.objects.all().filter(id_user=current_user_id, id_ets=id_entreprise)
    nom_entreprise = Entreprise.objects.values_list("nom_ets").filter(id=id_entreprise)
    nom_entreprise = nom_entreprise[0]

    return render(request, '06_QRCODE/01_Manage/manage_qrcode.html',
                  {"categorie_article": categorie_article, 'nom_entreprise': nom_entreprise[0], 'id_entreprise':entreprise.id, "my_qrcode": my_qrcode, "flyers":flyers, "path_modele":path_modele, "len_path_modele":len_path_modele})


def manage_business_card(request):
    current_user = request.user
    current_user_id = current_user.id
    return 0;
#--------------------------------------------------------------- DISPLAY ---------------------------------------------------------------

def diplay_from_qrcode(request, current_user_id):
    all_categorie_article = Categorie_article.objects.all()
    entreprise = Entreprise.objects.filter(pk=current_user_id)
    if request.method == "POST":
        categorie_article = request.POST["categorie_article"]
        print(categorie_article)
    articles = Article.objects.all().filter(id_user=current_user_id)

    return render(request, '06_QRCODE/display_from_qrcode5.html', {"articles": articles, "all_categorie_article":all_categorie_article, 'entreprise':entreprise})

def diplay_from_qrcode2(request, id_entreprise):
    all_categorie_article = Categorie_article.objects.all().filter(id_ets=id_entreprise)
    entreprise = Entreprise.objects.get(id=id_entreprise)

    articles = Article.objects.all().filter(id_entreprise=id_entreprise)

    return render(request, '06_QRCODE/11_Display/display_ultimate_acces.html', {"articles": articles, "all_categorie_article":all_categorie_article, 'entreprise':entreprise})

def display_menu_prenium_membership(request, id_entreprise, id_commande=generate_random_string(), total_price=0):

    all_categorie_article = Categorie_article.objects.all().filter(id_ets=id_entreprise)
    entreprise = Entreprise.objects.get(id=id_entreprise)

    if request.method == "POST":
        if "add_menu" in request.POST:
            id_menu = request.POST["id_menu"]
            name = request.POST["name"]
            prix = request.POST["prix"]
            quantite = request.POST["quantite"]
            path_image = request.POST["path_image"]
            description = request.POST["description"]

            #sum_distinct = Option_commande_intermediaire.objects.filter(id_commande=id_commande, id_menu=id_menu).count()

            #if sum_distinct >= 1:
                #list_quantite = list(Option_commande_intermediaire.objects.filter(id_commande=id_commande, id_menu=id_menu).values_list("quantite",flat=True))
                #print("list_quantite : ", list_quantite)

                #new_quantite = sum((list(list_quantite))) + 1
                #print("new_quantite : ", new_quantite)
                #Option_commande_intermediaire.objects.filter(id_commande=id_commande, id_menu=id_menu).update(quantite=new_quantite)
            #else:

                #Option_commande_intermediaire.objects.create(
                    #id_commande=id_commande,
                    #id_entreprise=id_entreprise,
                    #name=name,
                    #id_menu=id_menu,
                    #price=prix,
                    #quantite=quantite,
                    #description=description,
                    #image_path=path_image,
                    #date_transaction=datetime.now().strftime("%H:%M")
            #)

            #current_commande_price = list(Option_commande_intermediaire.objects.filter(id_commande=id_commande).values_list("price", flat=True))
            current_commande_quantite = list(Option_commande_intermediaire.objects.filter(id_commande=id_commande).values_list("quantite",flat=True))

            #price = (list(current_commande_price))
            #print(price)

            #for i in price:
                #total_price += i

            try:
                curent_achat = Option_commande_intermediaire.objects.get(id_commande=id_commande, id_menu=id_menu)
                this_quantite = curent_achat.quantite
                Option_commande_intermediaire.objects.filter(id_commande=id_commande, id_menu=id_menu).update(quantite=this_quantite+1)

            except:

                Option_commande_intermediaire.objects.create(
                    id_commande=id_commande,
                    id_entreprise=id_entreprise,
                    name=name,
                    id_menu=id_menu,
                    price=prix,
                    quantite=quantite,
                    description=description,
                    image_path=path_image,
                    date_transaction=datetime.now().strftime("%H:%M")
                )

            current_achat = list(Option_commande_intermediaire.objects.all().filter(id_commande=id_commande))

            for achat in current_achat:
                total_price += achat.price * achat.quantite


        if "finish" in request.POST:
            return redirect("/valider_ma_commande/" + id_commande)

    articles = Article.objects.all().filter(id_entreprise=id_entreprise, statut=1)

    return render(request, '06_QRCODE/11_Display/display_prenium_membership.html', {"articles": articles, "all_categorie_article":all_categorie_article, 'entreprise':entreprise, 'total_price':total_price})



def display_menu_prenium_membership2(request, id_entreprise, list_commande = [], price=0):
    all_categorie_article = Categorie_article.objects.all().filter(id_ets=id_entreprise)
    entreprise = Entreprise.objects.get(id=id_entreprise)

    print("PRIX TOTAL = ", price)

    if request.method == "POST":
        if "add_menu" in request.POST:
            id_menu = request.POST["id_menu"]
            menu = request.POST["menu"]
            prix = request.POST["prix"]
            quantite = request.POST["quantite"]

        if "finish" in request.POST:
            #url = reverse('/valider_ma_commande/')
            return redirect(valider_commande_menu, list_commande=list_commande)

        list_commande.append([id_menu, menu, prix, quantite])

    for prix in list_commande:
        price += float(prix[2])

    print(list_commande)

    articles = Article.objects.all().filter(id_entreprise=id_entreprise, statut=1)

    return render(request, '06_QRCODE/11_Display/display_prenium_membership.html', {"articles": articles, "all_categorie_article":all_categorie_article, 'entreprise':entreprise, 'price':price})

def display_from_business_card(request, id_user):

    #rs_link = social_media_link.objects.all().filter(id_user=id_user)
    return render(request, '07_BUSINESS_CARD/display_from_business_card.html', {"rs_link": rs_link})

#--------------------------------------------------------------- QRCODE ---------------------------------------------------------------

def add_custom_qrcode(request, id_ets):
    current_user = request.user
    current_user_id = current_user.id

    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(8))

    entreprise = Entreprise.objects.get(pk=id_ets)
    #user_qrcode_initial = User_qrcode_initial.objects.get(id_user=current_user_id, id_entreprise=id_ets)


    if request.method == "POST":
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save("flyer/cutom/background/"+random_string+"custom_flyer_"+str(id_ets)+"_" + ".png", image)
        image_url = fss.url(file)

        print("IMAGE URL : ", image_url)

        custom_flyer(image_url, current_user_id,
                     str(entreprise.id), entreprise.nom_ets)

        return redirect("/manage_qrcode/"+str(id_ets))

    return render(request, '06_QRCODE/03_Create/add_qrcode.html', {'entreprise': entreprise})

def my_account(request):
    current_user = request.user
    current_user_id = current_user.id

    entreprises = Entreprise.objects.all().filter(id_user=current_user_id)

    return render(request, '01_Authentification/my_account.html', {'entreprises':entreprises})

#--------------------------------------------------------------- PASSWORD ---------------------------------------------------------------

def update_password_forget(request):
    if request.method == "POST":
        email = request.POST["Email"]
        password = request.POST["password"]
        password_confirmation = request.POST["password_confirme"]

        if password_confirmation != password:
            messages.error(request, "Mot de passe de confirmation différent du mot de passe")
            return redirect("/update_password/")

        User.objects.filter(email=email).update(password=make_password(password))
        messages.success(request, "Votre mot de passe à été changé")

        return redirect("/connexion/")

    return render(request, '01_Authentification/update_password_forget.html')

def update_password(request):
    current_user = request.user
    current_user_id = current_user.id

    user = User.objects.get(id=current_user_id)
    print("USER ID :", user.id)
    #user_password = user.password

    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirme_new_password = request.POST["confirme_new_password"]

        if user.check_password(current_password):

            if confirme_new_password != new_password:
                messages.error(request, "Mot de passe de confirmation différent du mot de passe")
                return redirect("/modifier_mot_de_passe/")

            User.objects.filter(id=current_user_id).update(password=make_password(new_password))

            messages.success(request, "Votre mot de passe à été changé")

            return redirect("/connexion/")

        else:
            messages.error(request, "Mot de passe actuel incorrect")
            return redirect("/modifier_mot_de_passe/")


        #if make_password(current_password) != user_password:
         #   print("current_password : ", make_password(current_password))
          #  print("user_password : ", user_password)
           # messages.error(request, "Mot de passe actuel incorrect")
            #return redirect("/modifier_mot_de_passe/")

        #if confirme_new_password != new_password:
         #   messages.error(request, "Mot de passe de confirmation différent du mot de passe")
          #  return redirect("/modifier_mot_de_passe/")

       # User.objects.filter(id=current_user_id).update(password=make_password(new_password))
        #messages.success(request, "Votre mot de passe à été changé")

        #return redirect("//")

    return render(request, '01_Authentification/update_password.html')




#------------------------------------ ACHAT ENTREPRISE -----------------------------------------

#------------------------------------ ACHAT ENTREPRISE -----------------------------------------
def info_qrcode(request):
    return render(request, '06_QRCODE/info_qrcode.html')

#------------------------------------ PRODUITS ------------------------------------
def nos_produits(request):
    return render(request, '06_QRCODE/08_Produits/nos_produits.html')

def commander_qrcode(request):
    return render(request, '06_QRCODE/08_Produits/commander_qrcode.html')

#------------------------------------ PAYMENT ------------------------------------
def checkout_success(request):
    return render(request, '00_stripe/checkout_success.html')

def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1MS1vKEh0F6VKvKtG3ImmzDG',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='http://127.0.0.1:8000/checkout_sucess/',
            cancel_url='http://127.0.0.1:8000/',
        )



    return redirect(checkout_session.url, code=303)

#------------------------------------ TABLES ------------------------------------
def manage_tables_case_entreprise(request):
    current_user = request.user
    current_user_id = current_user.id

    entreprises = Entreprise.objects.all().filter(id_user=current_user_id, statut=1)

    return render(request, '06_QRCODE/10_Options/Tables/case_entreprise.html', {'entreprises':entreprises})

def manage_tables(request, id_entreprise):
    entreprise = Entreprise.objects.all().get(id=id_entreprise)

    tables = Option_tables.objects.all().filter(id_entreprise=id_entreprise)

    tables_dispo = Option_tables.objects.all().filter(id_entreprise=id_entreprise, statut_table=1)
    len_tables_dispo = len(tables_dispo)

    tables_indispo = Option_tables.objects.all().filter(id_entreprise=id_entreprise, statut_table=0)
    len_tables_indispo = len(tables_indispo)

    list_nb_places = []
    nb_places = entreprise.nb_places
    for i in range(nb_places):
        list_nb_places.append(1)

    print("NOMBRE DE PLACE : ", nb_places)

    return render(request, '06_QRCODE/10_Options/Tables/manage_tables.html',
                  {'tables':tables,
                   'len_tables_dispo':len_tables_dispo,
                   'len_tables_indispo':len_tables_indispo,
                   'list_nb_places':list_nb_places,
                   })

def update_table(request, id_entreprise, numero_table):

    table = Option_tables.objects.get(id_entreprise=id_entreprise, numero_table=numero_table)

    if request.method == "POST":
        #numero_table = request.POST["numero_table"]
        nb_places = request.POST["nb_places"]
        statut = request.POST["statut"]

        if statut == "Disponible":
            table_statut = 1
        else:
            table_statut = 0

        Option_tables.objects.filter(id_entreprise=id_entreprise, numero_table=numero_table).update(nb_places=nb_places, statut_table=table_statut)

        return redirect('/gestion_tables/' + str(id_entreprise))

    return render(request, '06_QRCODE/10_Options/Tables/update_table.html', {'table':table})


#------------------------------------ SOCIAL MEDIA ------------------------------------
def manage_social_media_case_entreprise(request):
    current_user = request.user
    current_user_id = current_user.id

    entreprises = Entreprise.objects.all().filter(id_user=current_user_id, statut=1)
    return render(request, '06_QRCODE/10_Options/social_media/case_entreprise.html', {'entreprises':entreprises})

def manage_social_media(request, id_entreprise):
    current_user = request.user
    current_user_id = current_user.id

    list_entreprise_social_media = Entreprise_social_media.objects.values_list("name", flat=True).filter(
        id_entreprise=id_entreprise,
        id_user=current_user_id)
    active_social_media = list(list_entreprise_social_media)

    all_social_media = All_social_media.objects.exclude(name__in=active_social_media)

    entreprise_social_media = Entreprise_social_media.objects.all().filter(id_entreprise=id_entreprise)
    len_entreprise_social_media = len(entreprise_social_media)

    return render(request, '06_QRCODE/10_Options/social_media/manage_entreprise_social_media.html',
                  {
                      'id_entreprise':id_entreprise,
                      'all_social_media': all_social_media,
                      'entreprise_social_media':entreprise_social_media,
                      'len_entreprise_social_media':len_entreprise_social_media
                   })

def add_social_media(request, id_entreprise):
    current_user = request.user
    current_user_id = current_user.id

    if request.method == "POST":
        name = request.POST["name"]
        link = request.POST["link"]
        country = request.POST["country"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]

        print("name :", name)
        #print("email : ", email)

        full_phone_number = "0000"

        if (link == "" and phone_number == "" and email == ""):

            return redirect("/gestion_resaux_sociaux/"+str(id_entreprise))

        elif name == "WhatsApp":
            full_phone_number = country + phone_number
            link = "https://wa.me/" + full_phone_number

        elif name == "Email":
            print("email : ", email)
            link = email

        print("phone_number  : ", phone_number)
        print("full_phone_number : ", full_phone_number)

        social_media = All_social_media.objects.all().get(name=name)

        Entreprise_social_media.objects.create(
            path_logo=social_media.path_logo,
            name=name,
            id_user=current_user_id,
            link=link,
            id_entreprise=id_entreprise,
            phone_number=full_phone_number
        )

        return redirect("/gestion_resaux_sociaux/"+str(id_entreprise))

    return render(request, '06_QRCODE/03_Create/02_add_reseau_social.html')

def display_entreprise_social_media(request, id_entreprise):
    current_user = request.user
    current_user_id = current_user.id

    social_media = Entreprise_social_media.objects.all().filter(
        id_entreprise=id_entreprise,
        id_user=current_user_id
    )

    return render(request, '06_QRCODE/10_Options/social_media/display_entreprise_social_media.html',
                  {'social_media':social_media})

#------------------------------------ BUSINESS CARD ------------------------------------

def manage_social_media_bs(request, id_user):

    list_user_social_media = Business_card_social_media.objects.values_list("name", flat=True).filter(
        id_user=id_user)
    active_social_media = list(list_user_social_media)

    all_social_media = All_social_media.objects.exclude(name__in=active_social_media)

    bs_social_media = Business_card_social_media.objects.all().filter(id_user=id_user)
    len_bs_social_media = len(bs_social_media)

    return render(request, '06_QRCODE/10_Options/Business_card/manage_business_card.html',
                  {
                      'all_social_media': all_social_media,
                      'bs_social_media':bs_social_media,
                      'len_bs_social_media':len_bs_social_media
                   })

def add_social_media_bs(request, id_user):

    if request.method == "POST":
        name = request.POST["name"]
        link = request.POST["link"]
        country = request.POST["country"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]

        full_phone_number = "0000"

        if (link == "" and phone_number == "" and email == ""):

            return redirect("/gestion_reseaux_sociaux_business_card/"+str(id_user))

        elif name == "WhatsApp":
            full_phone_number = country + phone_number
            link = "https://wa.me/" + full_phone_number

        elif name == "Email":
            link = email

        social_media = All_social_media.objects.all().get(name=name)

        Business_card_social_media.objects.create(
            path_logo=social_media.path_logo,
            name=name,
            id_user=id_user,
            link=link,
            phone_number=full_phone_number
        )

        return redirect("/gestion_reseaux_sociaux_business_card/"+str(id_user))

    return render(request, '06_QRCODE/03_Create/02_add_reseau_social.html')

def display_bs_social_media(request, id_user):

    social_media = Business_card_social_media.objects.all().filter(
        id_user=id_user
    )

    return render(request, '06_QRCODE/10_Options/Business_card/display_from_business_card.html',
                  {'social_media':social_media})

#------------------------------------ COMMANDE MENU ------------------------------------
def valider_commande_menu(request,id_commande, total_price=0):

    user_commande = Option_commande_intermediaire.objects.all().filter(id_commande=id_commande)

    for achat in user_commande:
        total_price += achat.price * achat.quantite

    id_entreprise = list(user_commande.values_list("id_entreprise", flat=1))[0]

    if request.method == "POST":
        if "annuler" in request.POST:
            Option_commande_intermediaire.objects.all().filter(id_commande=id_commande).delete()
            return redirect("/afficher_menu_prenium_membership/"+str(id_entreprise))

        if "delete_menu" in request.POST:
            id_menu = request.POST["delete_menu"]
            print("id_menu : ", id_menu)

            Option_commande_intermediaire.objects.all().filter(id_commande=id_commande, id_menu=id_menu).delete()
            return redirect("/valider_ma_commande/"+str(id_commande))




    return render(request, '06_QRCODE/10_Options/Commande/panier.html',
                  {"user_commande":user_commande,
                   "id_commande" : id_commande,
                   "total_price": total_price
                   })

def update_quantite_menu(request, id_commande, id_menu):
    commande = Option_commande_intermediaire.objects.get(id_commande=id_commande, id_menu=id_menu)
    if request.method == "POST":
        new_quantite = request.POST["quantite"]

        Option_commande_intermediaire.objects.filter(id_commande=id_commande, id_menu=id_menu).update(
            quantite=new_quantite
        )

        return redirect("/valider_ma_commande/" + str(id_commande))

    return render(request, '06_QRCODE/10_Options/Commande/update_quantite_menu.html',
                  {"commande":commande})

def confirmer_commande(request, id_commande, total_price=0):

    user_commande = Option_commande_intermediaire.objects.all().filter(id_commande=id_commande)

    for this_commande in user_commande:
        total_price += this_commande.price * this_commande.quantite

    if request.method == "POST":
        numero_table = request.POST["numero_table"]
        customer_name = request.POST["customer_name"]

        for commande in user_commande:
            Option_commande.objects.create(
                id_menu=commande.id_menu,
                id_entreprise=commande.id_entreprise,
                price=commande.price,
                quantite=commande.quantite,
                date_transaction=commande.date_transaction,
                numero_table=numero_table,
                custumer_name=customer_name,
                id_commande=id_commande,
                statut=0
            )

        Option_commande_intermediaire.objects.all().filter(id_commande=id_commande).delete()

        return redirect("/commande_finalise/" + str(commande.id_entreprise))

    return render(request, "06_QRCODE/10_Options/Commande/confirmer_commande.html",
                  {"total_price": total_price})

def remerciement(request, id_entreprise):

    return render(request, '06_QRCODE/10_Options/Commande/remerciement.html', {
        'id_entreprise':id_entreprise

    })

def manage_commande(request, id_entreprise):

    distinct_commandes = list(Option_commande.objects.values_list('id_commande', 'numero_table', 'custumer_name', 'date_transaction', 'statut', 'id_entreprise').distinct().filter(id_entreprise=id_entreprise))

    commandes = Option_commande.objects.all().filter(id_entreprise=id_entreprise)
    achats = Option_commande.objects.all().filter(id_entreprise=id_entreprise)
    articles = Article.objects.all().filter(id_entreprise=id_entreprise)

    return render(request, '06_QRCODE/10_Options/Commande/manage_commande.html',
                  {"commandes":commandes,
                   "achats":achats,
                   "articles":articles,
                   "distinct_commandes":distinct_commandes})

def confirmer_livraison(request, id_commande, prix_total=0):

    current_commande = Option_commande.objects.values_list("custumer_name", "numero_table", "id_entreprise").filter(id_commande=id_commande)[0]
    achats = Option_commande.objects.all().filter(id_commande=id_commande)
    id_entreprise = Option_commande.objects.values_list("id_entreprise").filter(id_commande=id_commande)[0][0]
    articles = Article.objects.all().filter(id_entreprise=id_entreprise)

    this_commande = Option_commande.objects.all().filter(id_commande=id_commande)

    for commande in this_commande:
        prix_total += commande.price * commande.quantite

    if request.method == "POST":
        Option_commande.objects.all().filter(id_commande=id_commande).update(statut=1)


        return redirect("/suivi_commandes/"+str(current_commande[2]))

    return render(request, '06_QRCODE/10_Options/Commande/confirmer_livraison.html',
                  {"current_custumer_name": current_commande[0],
                   "current_numero_table": current_commande[1],
                   "id_commande": id_commande,
                   "achats": achats,
                   "articles": articles,
                   "prix_total": prix_total
                   })
#------------------------------------ TEST ------------------------------------
def test(request):
    return render(request, '06_QRCODE/test/test_carousel.html')

#------------------------------------ RESTE A FAIRE ------------------------------------

#https://fr.moonbooks.org/Articles/Comment-afficher-dans-un-template-le-nombre-de-visiteurs-en-ligne-sous-Django-/
# Ajouter un email de confirmation

import requests

def lancer_paiement(request):
    url = "https://api.orange.com/orange-money-webpay/cm/v1/webpayment"
    headers = {
        "Authorization": "Bearer <votre_token_d'API>",
        "Content-Type": "application/json"
    }
    payload = {
        "merchant_key": "<votre_clé_marchand>",
        "currency": "XAF",
        "order_id": "<votre_identifiant_de_commande>",
        "amount": "10000",
        "return_url": "https://votre-site.com/paiement-reussi/",
        "cancel_url": "https://votre-site.com/paiement-annule/",
        "notif_url": "https://votre-site.com/paiement-notification/"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return render(request, "paiement.html", {"message": "Votre paiement a été lancé."})
    else:
        return render(request, "paiement.html", {"message": "Une erreur s'est produite lors du lancement du paiement."})
