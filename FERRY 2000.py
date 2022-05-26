# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 19:00:24 2022

@author: Matthieu
"""

import flask
import sqlite3
import random
from time import *
from Plugins_E2000 import entete, basdepage, morceau_entete, entete_parametre, interface, demarrer_on, demarrer_off, erreur_12, erreur_2a, erreur_2b, popup_info

app = flask.Flask(__name__) # Création de l'application

from routing.BUREAU import bureau, fermer_tte_fenetres, fermeture_fenetre, ouverture_fenetre, controle_utilisateur
from routing.AIDE_EXECUTER import aide, executer, executer_conf
from routing.FERRY_WORD import ferryword, ew_supprimer, ew_sauvegarde, ew_confirm
from routing.BIBLIOTHEQUES import bibliotheque_docs, bibliotheque_logiciels
from routing.PARAMETRES import parametres, parametre_session, parametre_graphique, parametre_dossiers, parametre_sauvegarder, parametre_admin
from routing.PARAMETRES_ADMIN import admin_creersession, admin_modifsession, admin_supprsession, admin_modif_session_sauvegarder
from routing.FERRY_EXPLORER import Ferry_Explorer, Explorer_web

#BUREAU.py
app.add_url_rule('/bureau', 'bureau', bureau, methods=['GET'])
app.add_url_rule('/fermer_tte_fenetres', 'fermer_tte_fenetres', fermer_tte_fenetres, methods=['GET'])
app.add_url_rule('/fermeture_fenetre', 'fermeture_fenetre', fermeture_fenetre, methods=['GET'])
app.add_url_rule('/ouverture_fenetre', 'ouverture_fenetre', ouverture_fenetre, methods=['GET'])
app.add_url_rule('/controle_utilisateur', 'controle_utilisateur', controle_utilisateur, methods=['GET'])

#AIDE_EXECUTER.py
app.add_url_rule('/aide', 'aide', aide, methods=['GET'])
app.add_url_rule('/executer', 'executer', executer, methods=['GET'])
app.add_url_rule('/executer_conf', 'executer_conf', executer_conf, methods=['POST'])

#FERRY_WORD.py
app.add_url_rule('/ferryword', 'ferryword', ferryword, methods=['GET'])
app.add_url_rule('/ew_supprimer', 'ew_supprimer', ew_supprimer, methods=['GET'])
app.add_url_rule('/ew_sauvegarde', 'ew_sauvegarde', ew_sauvegarde, methods=['GET'])
app.add_url_rule('/ew_confirm', 'ew_confirm', ew_confirm, methods=['GET'])


#BIBLIOTHEQUES.py
app.add_url_rule('/bibliotheque_docs', 'bibliotheque_docs', bibliotheque_docs, methods=['GET'])
app.add_url_rule('/bibliotheque_logiciels', 'bibliotheque_logiciels', bibliotheque_logiciels, methods=['GET'])

#PARAMETRES.py
app.add_url_rule('/parametres', 'parametres', parametres, methods=['GET'])
app.add_url_rule('/parametre_session', 'parametre_session', parametre_session, methods=['POST'])
app.add_url_rule('/parametre_graphique', 'parametre_graphique', parametre_graphique, methods=['GET'])
app.add_url_rule('/parametre_dossiers', 'parametre_dossiers', parametre_dossiers, methods=['GET'])
app.add_url_rule('/parametre_sauvegarder', 'parametre_sauvegarder', parametre_sauvegarder, methods=['POST'])
app.add_url_rule('/parametre_admin', 'parametre_admin', parametre_admin, methods=['POST'])

#PARAMETRES_ADMIN.py
app.add_url_rule('/admin_creersession', 'admin_creersession', admin_creersession, methods=['GET'])
app.add_url_rule('/admin_modifsession', 'admin_modifsession', admin_modifsession, methods=['GET'])
app.add_url_rule('/admin_supprsession', 'admin_supprsession', admin_supprsession, methods=['GET'])
app.add_url_rule('/admin_modif_session_sauvegarder', 'admin_modif_session_sauvegarder', admin_modif_session_sauvegarder, methods=['POST'])

#FERRY_EXPLORER.py
app.add_url_rule('/Ferry_Explorer', 'Ferry_Explorer', Ferry_Explorer, methods=['GET'])
app.add_url_rule('/Explorer_web', 'Explorer_web', Explorer_web, methods=['POST'])

###############
"""
Pour ce projet, nous avons besoin d'utiliser le système de session qu'utilise flask.
Les cookies serviront à garder en mémoire sur quelle session l'utilisateur est actuellement connecté.
Mais également pour garder en mémoire les fenêtres ouvertes, ou tout simplement pour
stocker temporairement une information.
Les cookies permettent également d'éviter d'envoyer certaines informations via des formulaires.
"""


#guide session flask: https://ressources.magicmakers.fr/ressources-python-webapp-lycee-flask-session/

#Mot de passe d'accès aux cookies:
app.secret_key = "J'aimelespâtes!123"





@app.route('/') # Accueil
def index():
    #Affichage du fond du site web.
    #+ Affichage dans l'iframe qui comportera Ferry 2000.

    page="""
    <!DOCTYPE html> <!--Entête de la page HTML-->

    <html lang="fr">
    <head>
        <meta charset="UTF-8" >
        <title>Ferry 2000 - Projet NSI</title>
        <link rel="icon" href="/static/images/autres/W2000.png" />
        <link rel="stylesheet" href="static/fond.css" type="text/css">
    </head> 
    """

    page+="""
    <!--Fond de la page HTML + Information sur le projet sur le côté-->
    <body>
        <img class="logo_fond" src="static/images/autres/Ferry2000_logo.png" width="250" alt="Logo Ferry 2000">
        <iframe class="incrustation" src="demarrage" width="804" height="605"></iframe>
        <div style="position: absolute; left: 1%; top: 100px; font-family: KOMIKAX; color: yellow; font-size: 13px;">
            <p class="centrer">Par Matthieu Linkieu</p>
            <p>Projet de NSI pour le 09/05/2022</p>
            <br><br>
        </div>
    
            
        </body>
    </html>
    """

    return page

@app.route('/demarrage', methods = ['GET']) # Bureau Ferry 2000
def demarrage():
    #Une simple image de redirection.
    
    entete="""<!DOCTYPE html> <!--Entête de la page HTML-->

    <html lang="fr">
            <head>
                <meta charset="UTF-8" >
                <meta http-equiv="refresh" content="0.5; URL=ouverture_session">
                <link rel="stylesheet" href="static/style.css" type="text/css">
                <link rel="stylesheet" href="static/demarrage_et_session.css" type="text/css">
            </head> 
    <body>
        
    """
    page=entete
    
    page+="""
    <img class="interface" src="static/images/system/demarrage/demarrage.png" alt="Ecran de démarrage">
    """
    
    page+=basdepage
    return page

@app.route('/ouverture_session', methods = ['GET']) # Bureau Ferry 2000
def ouverture_session():
    #Ecran de connexion à la session
    page=entete
    
    page+="""
    <img class="interface" src="static/images/system/demarrage/demarrage.png" alt="Ecran de démarrage">
    """
    
    page+="""
    
    <img class="pop_up_ouverture_session" src="static/images/system/demarrage/ouverturesession.png" alt="Pop up ouverture session">
    
    <form action ="/ouverture_verif_session" method="post">
    
        <div class="connexion_session_utilisateur" >
            <input type="text" name="utilisateur" size="32" required> <!--Emplacement nom utilisateur-->
            </div>
    
        <div class="connexion_session_mdp" >
            <input type="password" name="mdp" size="32" required> <!--Emplacement mot de passe-->
        </div>
        
        <div class="connexion_session_ok">
            <input type="submit" value="          OK          ">\n <!--Renvoi le formulaire-->
        </div>
    </form>
    """
    
    page+=basdepage
    return page

@app.route('/ouverture_verif_session', methods = ['POST']) # S'occupe de vérifier la connexion vers la session, et redirection vers le bureau.
def ouverture_verif_session():
    #On vérifie le formulaire afin de laisser accéder ou non l'utilisateur à
    #Ferry 2000.
    #Si l'accès est autorisé, alors on assigne à la session un jeton qu'on
    #sauvegardera dans la Base de donnée. En plus de sauvegarder le nom de
    #session, on créer une liste "taskbar" dans les cookies.
    #Une variable sera également créer dans l'unique but d'indiquer si la
    #l'utilisateur vient tout juste de se connecter.
    
    page=morceau_entete
    
    resultat = flask.request.form
    utilisateur = resultat.get('utilisateur',None)
    mdp = resultat.get('mdp',None)

    connexion = sqlite3.connect("Ferry2000.db")
    if utilisateur=='' or mdp=='':
        #Si l'une des deux cases n'est pas remplis, alors on affiche un
        #message d'erreur.
        
        
        requete=list(connexion.execute("SELECT type,erreur,icon FROM erreurs WHERE id_erreur==3")) #On recherche dans la base de donnée le message d'erreur associé
        page+="""
            </head>
            <body>
            """
        page+=erreur_12
        page+="""<h1 class="titre_message">"""+str(requete[0][0])+"""</h1><p class="message">"""+str(requete[0][1])+"""</p><img class="msg_icon" src="static/images/system/icons/"""+str(requete[0][2])+""".png" alt="Icon du message">"""
        #↑↑↑ On affiche le type d'erreur, ainsi que le message d'erreur.
        connexion.close()
        
        page+="""
            <img class="interface" src="static/images/system/demarrage/demarrage.png" alt="Ecran de démarrage">
            """
        
        ##############################################
        page+=basdepage
        return page
    
    
    
    else: 
        #Les cases sont remplis, donc on va devoir vérifier si quelqu'un
        #est déjà connecté ou non
    
        
        #On cherche le jeton le plus récent: le plus grand.
        #Un jeton est représenté par un nombre qui s'incrémente toute les milisecondes.
        dejaconnecter=list(connexion.execute("SELECT MAX(jeton) FROM utilisateur"))[0][0]
        
        #On vérifie que le jeton le plus récent a expiré.
        #Remarque: un jeton peut être représenté par la valeur 0, dans le cas
        #où l'utilisateur s'est déconnecté de lui même.
        if dejaconnecter>int(time()):
            #Le jeton le plus récent n'a pas expiré, on ne peut pas se connecter.
            
            
            requete=list(connexion.execute("SELECT type,erreur,icon FROM erreurs WHERE id_erreur==6")) #On recherche dans la base de donnée le message d'erreur associé
            page+="""
                </head>
                <body>
                """
            page+=erreur_12
            page+="""<h1 class="titre_message">"""+str(requete[0][0])+"""</h1><p class="message">"""+str(requete[0][1])+"""</p><img class="msg_icon" src="static/images/system/icons/"""+str(requete[0][2])+""".png" alt="Icône du message">"""
            #↑↑↑ On affiche le type d'erreur, ainsi que le message d'erreur.
            page+=basdepage
            connexion.close()
            return page
        
        
        
    
        #Sinon, le jeton a expiré, donc on peut essayer de se connecter.
        
        
        
    
        #On se connecte à la BDD, puis on récupérer les info de connexion sur les utilisateurs
        connexion = sqlite3.connect("Ferry2000.db") #Connexion à la BDD
        requete="SELECT nom, mdp FROM utilisateur" #Requete pour récupérer nom utilisateur et mots de passe
        
        #On insère les résultat dans un dictionnnaire
        resultat={}
        for element in(list(connexion.execute(requete))): #Transforme le résultat en dictionnaire ({'nom': 'mdp'})
            resultat[element[0]]=element[1]
        
        
        
        
        #On parcours le dictonnaire, dans le but de retrouver le nom
        #d'utilisateur et le mot de passe mis dans le formulaire.
        for BDD_users,BDD_password in resultat.items():
            if BDD_users==utilisateur and BDD_password==mdp: #L'utilisateur a été retrouvé
                page+="""
                <meta http-equiv="refresh" content="0.1; URL=bureau?startup=oui">
                """
                #On va voir si c'est la première fois que la session s'ouvre.
                #Dans ce cas, le jeton initialisé dans la BDD serait "-1"   
                premiereconnexion=list(connexion.execute("SELECT jeton FROM utilisateur WHERE nom=='"+str(utilisateur)+"'"))[0][0]
                
                
                #On assigne à l'utilisateur un jeton qui sera valide durant
                #15 minutes. Ce jeton sera mis à jour régulièrement, donc
                #son horaire d'expiration sera régulièrement repoussé.
                jeton=int(time())+900 #15min pour 900
                
                #On sauvegarde ce jeton, dans la base de donnée.
                connexion.execute("UPDATE utilisateur SET jeton="+str(jeton)+" WHERE nom=='"+utilisateur+"'")
                
                #On le sauvegarde une deuxième fois, mais cette celui-ci ne
                #sera pas mis à jour.
                
                #Supposon que l'utilisateur A se connecte à la session SESSION1.
                #Que son jeton expire, et que l'utilisateur B se connecte sur la
                #même session. Il en a la possibilité.
                #Sauf que vu que le SESSION1 est toujours la dernière session
                #de connecter d'après la BDD, l'utilisateur A peut utiliser
                #la session bien que l'utilisateur B soit également connecté.
                
                #Par ce système, vu que l'ident_jeton sera remplacé suite à la
                #connexion de l'utilisateur B, l'utilisateur A sera
                #déconnecté à son retour.
                connexion.execute("UPDATE utilisateur SET ident_jeton="+str(jeton)+" WHERE nom=='"+utilisateur+"'")
                
                connexion.commit()
                #On prépare l'arriver de l'utilisateur sur Ferry 2000:
                flask.session['utilisateur']=utilisateur #On créer un cookie contenant le nom de session.
                flask.session['ident_jeton']=jeton #On créer un cookie "ident_jeton".
                flask.session['taskbar']=[] #On créer un cookie indiquant les fenêtres ouvertes du Ferry 2000
                
                
                if premiereconnexion==-1:
                    flask.session['musique_ouverture_session']='premiereconnexion'
                    #On créer un cookie indiquant qu'il faut jouer la musique
                    #de première connexion. On va également faire apparaître
                    #la fenêtre d'aide sur le bureau.
                else:
                    flask.session['musique_ouverture_session']=True
                    #On créer un cookie indiquant qu'il faut jouer la musique
                    #au démarrage de session. 
                
                
                connexion.close()
                page+=basdepage
                return page
        
        
        #Sorti de boucle --> L'utilisateur s'est trompé de nom d'utilisateur ou
        #de mot de passe. Ou encore, la session n'existe pas.
        #Note, pour la session Admin: Nom: ADMIN /// Mot de passe: ADMIN123
        
        ########GENERATION DU MESSAGE D'ERREUR
        connexion = sqlite3.connect("Ferry2000.db")
        requete=list(connexion.execute("SELECT type,erreur,icon FROM erreurs WHERE id_erreur==2")) #On recherche dans la base de donnée le message d'erreur associé
        page+="""
            </head>
            <body>
            """
        page+=erreur_12
        page+="""<h1 class="titre_message">"""+str(requete[0][0])+"""</h1><p class="message">"""+str(requete[0][1])+"""</p><img class="msg_icon" src="static/images/system/icons/"""+str(requete[0][2])+""".png" alt="Icône du message">"""
        #↑↑↑ On affiche le type d'erreur, ainsi que le message d'erreur.
        connexion.close()
        
        ##############################################
        
        page+=basdepage
    

    
    
    return page



@app.route('/deconnexion_session') #Déconnecte la session actuellement connecté
def deconnexion_session():
    connexion = sqlite3.connect("Ferry2000.db")
    page=morceau_entete   
    
    #On cherche le dernier utilisateur connecté à Ferry 2000.
    dernierutilisateur=list(connexion.execute("SELECT nom,ident_jeton,MAX(jeton) FROM utilisateur WHERE jeton>=0"))[0]
    

    if flask.session['utilisateur']==dernierutilisateur[0] and flask.session['ident_jeton']==dernierutilisateur[1]:
        #L'utilisateur est belle est bien le dernier à s'être connecté.
        #Alors on affiche l'écran de déconnexion habituel.
        
        #On réinitialise le jeton, pour montrer la déconnexion de l'utilisateur.
        connexion.execute("UPDATE utilisateur SET jeton=0 WHERE nom=='"+str(flask.session['utilisateur'])+"'")
        
        #On prépare la redirection.
        #Note:  les 4 secondes permettent de laisser le temps à la musique de
        #       déconnexion de se jouer.
        page+="""<meta http-equiv="refresh" content="4; URL=demarrage">"""
        page+="""</head><body>"""  
            

        page+=popup_info
        page+="""
                <audio src="static/musique/shutdown.mp3" autoplay></audio>
                <h1 class="titre_message">Ferry 2000</h1>
                <p class="message">Fermeture de session...</p>
                <img class="msg_icon" src="static/images/system/icons/computer.png" alt="Icône du message">
                """
        #↑↑↑ On affiche le type de message et le message.
        
    else:
        #Un autre utilisateur s'est connecté entre temps.
        #Sur une autre session, ou la même session.
        
        #Dans le doute que ce soit la même, pour éviter de déconnecter
        #l'autre utilisateur, on affiche que l'utilisateur était déjà
        #déconnecté.
        page+="""</head><body>"""
        requete=list(connexion.execute("SELECT type,erreur,icon FROM erreurs WHERE id_erreur==8"))
        page+=erreur_12
        page+="""
                <audio src="static/musique/shutdown.mp3" autoplay></audio>
                <h1 class="titre_message">"""+str(requete[0][0])+"""</h1>
                <p class="message">"""+str(requete[0][1])+"""</p>
                <img class="msg_icon" src="static/images/system/icons/"""+str(requete[0][2])+""".png" alt="Icon du message">
                """
        #↑↑↑ On affiche le type d'erreur, ainsi que le message d'erreur.
        
    connexion.commit()
    connexion.close()
    page+=basdepage
    return page

@app.route('/bsod')
def bsod():
    #Simple Blue Screen Of the Dead, sans aucune utilité apparente.
    
    texte=entete
    texte+="""
    <img src="static/images/system/bsod2.png" width="788" height="585" alt="Blue Screen">
    """
    texte+=basdepage
    return texte   


@app.route('/veille', methods = ['GET'])
def veille():
    ##########################################################################
    #VERIFICATION QUE L'UTILISATEUR EST BIEN TOUJOURS CONNECTé               #
    ##########################################################################
    connexion = sqlite3.connect("Ferry2000.db")
    nom=list(connexion.execute("SELECT nom, ident_jeton, MAX(jeton) FROM utilisateur WHERE jeton>0"))[0]
    
    if ('utilisateur' in flask.session) != True:
        """
        L'utilisateur a accédé à la page sans avoir de jeton dans son navigateur.
        
        2 causes:
            - Soit le navigateur a supprimé les cookies, et donc le jeton a
              disparu.
              
             - Soit, l'utilisateur cherche à accéder directement à la page.
             
        Dans les deux cas, l'accès à la page est impossible.
        """
        
        page+=erreur_12
        page+="""
                <h1 class="titre_message">"""+str(requete[0][0])+"""</h1>
                <p class="message">"""+str(requete[0][1])+"""</p>
                <img class="msg_icon" src="static/images/system/icons/"""+str(requete[0][2])+""".png" alt="Icon du message">
                """
        #↑↑↑ On affiche le type d'erreur, ainsi que le message d'erreur.
        connexion.close()
        page+=basdepage
        return page
    
    if flask.session['utilisateur']!=nom[0] or flask.session['ident_jeton']!=nom[1]:
        """
        Situation où le jeton stocké dans la base de donnée et le jeton
        stockée dans les cookies ne correspond pas.
        
        Soit quelqu'un s'est connecté à Ferry 2000 entre temps, et a pris
        sa place.
        Soit la personne s'est déconnecté sur une autre page du navigateur,
        et donc sur celle-ci, elle est aussi déconnecté.
        """
        page+="""
            <script type="text/javascript">
            var delai=0; // Delai en secondes
            var url='bureau'; // Url de destination
            setTimeout("parent.document.location.href=url", delai + '000');
            </script>          
            """

        connexion.close()
        page+=basdepage
        return page
    ##########################################################################
    
    
    #Fait afficher un écran de veille.
    #L'utilisateur peut immédiatemment retourner à là où il était.
    #Mais cela permet au cas où durant les 15 minutes, le jeton de connexion
    #n'a pas été mis à jour par l'utilisateur, de le mettre à jour.
    #Ainsi, s'il a été intérrompu sur Ferry Word, il aura la garanti de ne
    #pas perdre son travail si entre temps quelqu'un se connecte à Ferry 2000.
    
    #Toutefois, pour éviter tout abus, on vérifie que l'utilisateur est bien
    #connecté avant de générer l'écran de veille.
    
    page=entete

    resultat = flask.request.args
    sortiveille = resultat.get('sortiveille',None)

    if sortiveille=='oui':
        #Si l'utilisateur demande de sortir de veille, alors on met à jour le
        #jeton, et on le redirige à là où il en était avant la mise en veille.
        connexion = sqlite3.connect("Ferry2000.db")
        jeton=int(time())+900 #15min pour 900
        connexion.execute("UPDATE utilisateur SET jeton="+str(jeton)+" WHERE nom=='"+str(flask.session['utilisateur'])+"'")
        connexion.commit()
        connexion.close()
        page+="""
        <script type="text/javascript">
        var delai=0; // Delai en secondes
        var url="javascript:history.go(-2)"; // Url de destination
        setTimeout("document.location.href=url", delai + '000');
        </script>
        """
        page+=basdepage
        return page
    
    if "utilisateur" in flask.session:
        connexion = sqlite3.connect("Ferry2000.db")
        ecranveille=list(connexion.execute("SELECT screensaver FROM utilisateur WHERE nom=='"+str(flask.session['utilisateur'])+"'"))[0][0]

        page+="""
        <a href="veille?sortiveille=oui">
        <img src='static/images/system/screensaver/"""+str(ecranveille)+"""' width="788" height="585" alt="Ecran de veille">
        </a>
        """    

        connexion.close()
        
    else:
        page+="""
        <script type="text/javascript">
        var delai=1; // Delai en secondes
        var url='demarrage'; // Url de destination
        setTimeout("document.location.href=url", delai + '000');
        </script>
        """

    page+=basdepage
    return page

app.run(debug=True)