from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categorie_ets(models.Model):
    nom_categorie_ets = models.CharField(max_length=25)

class Entreprise(models.Model):
    id_user = models.IntegerField(null=False, default=None)
    secteur = models.CharField(max_length=25)
    nom_ets = models.CharField(max_length=40)
    logo_ets = models.CharField(max_length=255, null=False, default=None)
    nom_devise = models.CharField(max_length=10, null=False, default=None)
    statut = models.IntegerField(null=False, default=None)
    nb_places = models.IntegerField(null=True, default=None)

class Categorie_article(models.Model):
    nom_categorie_article = models.CharField(max_length=25)
    id_user = models.IntegerField(null=False, default=None)
    id_ets = models.IntegerField(null=False, default=None)
    nom_entreprise = models.CharField(max_length=40, null=False, default=None)
    statut = models.IntegerField(null=False, default=None)

class Article(models.Model):
    id_user = models.IntegerField(null=False, default=None)
    nom_categorie = models.CharField(max_length=25)
    nom_article = models.CharField(max_length=35)
    description = models.CharField(max_length=65)
    prix = models.FloatField(max_length=4)
    image_path = models.CharField(max_length=255, null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)
    nom_entreprise = models.CharField(max_length=40, null=False, default=None)
    statut = models.IntegerField(null=False, default=None)

class UserConfirmation(models.Model):
    email = models.EmailField(null=False, default=None)
    code_confirmation = models.TextField(max_length=8)

class All_social_media(models.Model):
    path_logo = models.CharField(max_length=255, null=False, default=None)
    name = models.CharField(max_length=25)

class Entreprise_social_media(models.Model):
    path_logo = models.CharField(max_length=255, null=False, default=None)
    name = models.CharField(max_length=25)
    id_user = models.IntegerField(null=False, default=None)
    link = models.CharField(max_length=80, null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)
    phone_number = models.BigIntegerField(null=True, default=None)

class Business_card_social_media(models.Model):
    path_logo = models.CharField(max_length=255, null=False, default=None)
    name = models.CharField(max_length=25)
    id_user = models.IntegerField(null=False, default=None)
    link = models.CharField(max_length=80, null=False, default=None)
    phone_number = models.BigIntegerField(null=True, default=None)

class Devises(models.Model):
    nom_devise = models.CharField(max_length=35, null=False, default=None)
    symbole = models.CharField(max_length=15, null=False, default=None)

class Abonnement(models.Model):
    id_user = models.IntegerField(null=False, default=None)
    flag_en_vigeur = models.IntegerField(max_length=2, null=False, default=None)
    periodicite = models.IntegerField(max_length=2, null=False, default=None)
    date_effet = models.DateTimeField(null=False, default=None)
    date_fin = models.DateTimeField(null=False, default=None)

class user_qrcode(models.Model):
    id_user = models.IntegerField(null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)
    path_white_qrcode = models.CharField(max_length=255, null=False, default=None)
    path_black_qrcode = models.CharField(max_length=255, null=False, default=None)

class user_flyer(models.Model):
    id_user = models.IntegerField(null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)
    name_modele = models.CharField(max_length=8)
    path_modele = models.CharField(max_length=255, null=False, default=None)

class user_custom_flyer(models.Model):
    id_user = models.IntegerField(null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)
    name_modele = models.CharField(max_length=8)
    path_modele = models.CharField(max_length=255, null=False, default=None)

class Option_tables(models.Model):
    id_user = models.IntegerField(null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)
    numero_table = models.IntegerField(null=False, default=None)
    statut_table = models.IntegerField(null=False, default=1)
    nb_places = models.IntegerField(null=False, default=0)

class Option_commande(models.Model):
    id_menu = models.IntegerField(null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)
    price = models.FloatField(null=False, default=None)
    quantite = models.IntegerField(null=False, default=None)
    date_transaction = models.CharField(max_length=65, null=False, default=None)
    numero_table = models.IntegerField(null=False, default=None)
    custumer_name = models.CharField(max_length=25,null=False, default=None)
    id_commande = models.CharField(max_length=25,null=False, default=None)
    statut = models.IntegerField(null=False, default=None)

class Option_commande_intermediaire(models.Model):
    id_commande = models.CharField(max_length=255, null=False, default=None)
    id_menu = models.IntegerField(null=False, default=None)
    id_entreprise = models.IntegerField(null=False, default=None)
    price = models.FloatField(null=False, default=None)
    quantite = models.IntegerField(null=False, default=None)
    date_transaction = models.CharField(max_length=65, null=False, default=None)
    image_path = models.CharField(max_length=255, null=False, default=None)
    description = models.CharField(max_length=65, null=False, default=None)
    name = models.CharField(max_length=65, null=False, default=None)

