"""DJAAGOU_SCAN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_djaagou_scan.views import home,logout
from app_djaagou_scan import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
#------------------- AUTHENTIFICATION -------------------
    path("inscription/", views.inscription),
    path("connexion/", views.connexion),
    path("logout/", logout, name="logout"),
    path("my_account/", views.my_account),
    path("mot_de_passe_oublie/", views.forget_password),
    path("update_password/", views.update_password_forget),
    path("modifier_mot_de_passe/", views.update_password),
    path("inscription_code/<email>", views.inscription_code),

#------------------- MANAGE -------------------
    path("manage_entreprise/", views.manage_entreprise),
    path('manage_entreprise/manage_menu/<int:entreprise_id>', views.manage_menu),
    path("manage_categorie/<int:id_entreprise>", views.manage_categorie),
    path("manage_business_card/", views.manage_business_card),
    path("manage_qrcode/<int:id_entreprise>", views.manage_qrcode),

#------------------- ADD -------------------
    path("ajouter_article/", views.add_article),
    path('ajouter_categorie/', views.add_categorie),
    path('ajouter_entreprise/', views.add_ets),


#------------------- UPDATE -------------------
    path('modfifier_confidentialite/', views.update_user),

    path('manage_menu/update_article/<int:article_id>', views.update_article),
    path('manage_categorie/update_categorie/<int:categorie_id>', views.update_categorie),
    path('manage_entreprise/update_entreprise/<int:entreprise_id>', views.update_entreprise),

    path('manage_business_card/update_business_card/<int:id_reseau_social>', views.update_reseau_social),

#------------------- MASQUER -------------------
    path('manage_menu/masquer_article/<int:article_id>',views.masquer_article),
    path('manage_categorie/masquer_categorie/<int:categorie_id>',views.masquer_categorie),
    path('manage_entreprise/masquer_entreprise/<int:id_entreprise>', views.masquer_entreprise),


    path('manage_business_card/delete_business_card/<int:id_reseau_social>', views.delete_business_card),

#------------------- DISPLAY -------------------
    path("display_from_qrcode/<int:current_user_id>", views.diplay_from_qrcode),
    path("display_from_qrcode2/<int:id_entreprise>", views.diplay_from_qrcode2),

    path("display_from_business_card/<int:id_user>", views.display_from_business_card),
    path("afficher_menu_prenium_membership/<id_entreprise>", views.display_menu_prenium_membership),

#------------------- COMMANDE -------------------
    path("valider_ma_commande/<id_commande>", views.valider_commande_menu),
    path("commande_finalise/<id_entreprise>", views.remerciement),
    path("suivi_commandes/<int:id_entreprise>", views.manage_commande),
    path("confirmer_commande/<id_commande>", views.confirmer_commande),
    path("confirmer_livraison/<id_commande>", views.confirmer_livraison),
    path("modifier_quantite/<id_commande>/<id_menu>", views.update_quantite_menu),

#------------------- QRCODE -------------------
    path("ajouter_qrcode/<int:id_ets>", views.add_custom_qrcode),
    path("info_qrcode/", views.info_qrcode),
    path("commander_qrcode/", views.commander_qrcode),

#------------------- HISTORIQUE -------------------
    path("gestion_des_abonnements/", views.manage_abonnement),

#------------------- HISTORIQUE -------------------
    path("gestion_des_historiques/", views.manage_historique),

    path("historique_entreprise/", views.historique_entreprise),
    path("recuperer_entreprise/<int:id_entreprise>", views.recuperer_entreprise),
    path("supprimer_entreprise/<int:id_entreprise>", views.delete_entreprise),

    path("historique_categorie/", views.historique_categorie),
    path("recuperer_categorie/<int:id_categorie>", views.recuperer_categorie),
    path("supprimer_categorie/<int:id_categorie>", views.delete_categorie),

    path("historique_article/", views.historique_article),
    path("recuperer_article/<int:id_article>", views.recuperer_article),
    path("supprimer_article/<int:article_id>", views.delete_article),


#------------------- NOS PRODUITS -------------------
    path("nos_produits/", views.nos_produits),

#------------------- PAYMENT -------------------
    path("checkout/", views.checkout),
    path("checkout_sucess/", views.checkout_success),

#------------------- TABLES -------------------
    path("gestion_tables/", views.manage_tables_case_entreprise),
    path("gestion_tables/<int:id_entreprise>", views.manage_tables),
    path("modifier_table/<int:id_entreprise>/<int:numero_table>", views.update_table),

#------------------- SOCIAL MEDIA -------------------
    path("gestion_reseaux_sociaux/", views.manage_social_media_case_entreprise),
    path("gestion_resaux_sociaux/<int:id_entreprise>", views.manage_social_media),
    path("ajouter_reseau_social/<int:id_entreprise>", views.add_social_media),
    path("nos_reseaux_sociaux/<int:id_entreprise>", views.display_entreprise_social_media),

#------------------- BUSINESS CARD -------------------
    path("gestion_reseaux_sociaux_business_card/<int:id_user>", views.manage_social_media_bs),
    path("ajouter_reseau_social_business_card/<int:id_user>", views.add_social_media_bs),
    path("mes_reseaux_sociaux/<int:id_user>", views.display_bs_social_media),

#------------------- test -------------------
    path("test/", views.test),


    path('lancer_paiement/', views.lancer_paiement),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
