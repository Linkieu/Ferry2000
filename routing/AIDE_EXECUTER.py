# -*- coding: utf-8 -*-
"""
Created on Sun May  1 20:35:15 2022

@author: Matthieu
"""

import flask
import sqlite3
import random
from time import *
from Plugins_E2000 import entete, basdepage, morceau_entete, entete_parametre, interface, demarrer_on, demarrer_off, erreur_12, erreur_2a, erreur_2b, popup_info

app = flask.Flask(__name__) # Création de l'application


#@app.route('/aide', methods = ['GET'])
def aide():
    #Page d'aide
    
    resultat = flask.request.args
    afficher = resultat.get('afficher',"")    
    
    #On génère en premier lieu la structure de la page: le logo, le menu à
    #gauche, les textes, les fonds colorés...
    page=morceau_entete
    page+="""
    <link rel="stylesheet" href="static/parametres.css" type="text/css">
    <link rel="stylesheet" href="static/aide.css" type="text/css">
    </head><body>
    """
    page+="""
    <div class="blochaut">
    </div>
    <a href="aide">
    <img src="static/images/autres/Ferry2000_logo.png" alt="logo" class="logohaut_aide">
    </a>
    
    <div class="blocgauche_aide">
    </div>
    
    <div class="barremilieu_aide">
    </div>
    
    <div style="position:absolute; top:85px; left:0px;">
    <a href="aide?afficher=presentation" class="bleu_aide">
    <p class="menu_aide">Présentation d'Ferry 2000</p>
    </a>
    <img src="static/images/system/aide/bleu.png" alt="barrebleu" class="bleu_aide" width="205" height="2"><br>
    
    <a href="aide?afficher=config" class="bleu_aide">
    <p class="menu_aide">Configuration requise</p>
    </a>
    <img src="static/images/system/aide/bleu.png" alt="barrebleu" class="bleu_aide" width="205" height="2"><br>
    
    <a href="aide?afficher=fenetres" class="bleu_aide">
    <p class="menu_aide">Le système de fenêtre</p>
    </a>
    <img src="static/images/system/aide/bleu.png" alt="barrebleu" class="bleu_aide" width="205" height="2"><br>
    
    <a href="aide?afficher=admin" class="bleu_aide">
    <p class="menu_aide">La session Administrateur</p>
    </a>
    <img src="static/images/system/aide/bleu.png" alt="barrebleu" class="bleu_aide" width="205" height="2"><br>
    
    <a href="aide?afficher=connexion" class="bleu_aide">
    <p class="menu_aide">Connexion et écran de veille</p>
    </a>
    <img src="static/images/system/aide/bleu.png" alt="barrebleu" class="bleu_aide" width="205" height="2"><br>
    
    <a href="aide?afficher=EExplorer" class="bleu_aide">
    <p class="menu_aide">A propos d'Ferry Explorer</p>
    </a>
    <img src="static/images/system/aide/bleu.png" alt="barrebleu" class="bleu_aide" width="205" height="2"><br>
    <img src="static/images/system/aide/bleu.png" alt="barrebleu" class="bleu_aide" width=205" height="2">
        
    </div>
    """
    
    #On affiche désormais la partie de droite: la description des sections.
    #En fonction de la section demandé par l'utilisateur.
    page+="""<div style="position:absolute; top:80px; left:250px;">"""
    
    if afficher=="presentation": #Présentation d'Ferry 2000
        page+="""
        <div style="background-color: blue; width:205px; height:37px; position:absolute; top:5px; left:-250px; opacity: 0.2;">
        </div>

        """
        page+="""
        <img src="static/images/system/aide/fond0b.png" alt="fond_aide" class="fond_aide">
        
        <h1 class="titre_aide">Présentation d'Ferry 2000</h1>
        
        <p class="texte_aide">
        Projet de Terminal NSI 2022 par Matthieu Linkieu.<br>
        <br>
        Inspiré du projet de 1ère NSI <a href="https://cdn.discordapp.com/attachments/549205743564226570/970246545851179008/nsi1ereE98.jpg" target="_blank">"Escape 98"</a>,
        Ferry 2000 se veut aller plus loin dans le principe de "clône de Windows".<br>
        L'utilisation d'iframes, des formulaires et des sessions FLASK permettent l'existence du système de fenêtre.
        SQLite3 permet de rendre le projet "vivant": customisable, utile et pratique.<br>
        Le tout avec un travail plus poussé côté HTML/CSS.<br>
        <br>
        Pourquoi choisir Windows 2000 après Windows 98 ?<br>
        Car je n'étais pas certain que <a href="bsod" target="_parent">Windows ME</a> soit une bonne idée...
        
        </p>
        """
    
    elif afficher=="config": #Configuration requise
        page+="""
        <div style="background-color: blue; width:205px; height:37px; position:absolute; top:40px; left:-250px; opacity: 0.2;">
        </div>

        """
        page+="""
        <img src="static/images/system/aide/office.webp" alt="fond_aide" class="fond_aide">
        
        <h1 class="titre_aide">Configuration requise</h1>
        
        <p class="texte_aide">
        Pour le bon fonctionnement du site web, vérifiez que les options suivantes
        soient bien activées sur votre navigateur:<br>
        - Javascript<br>
        - Images<br>
        - Cookies de navigations<br>
        <br>
        Navigateurs recommandés:<br>
            - Google Chrome ⭐⭐⭐⭐⭐<br>
            - Microsoft Edge ⭐⭐⭐⭐⭐<br>
            - Mozilla Firefox ⭐⭐⭐⭐<br>
        </p>
        """  
    
    elif afficher=="fenetres": #Le système de fenêtres
        page+="""
        <div style="background-color: blue; width:205px; height:37px; position:absolute; top:76px; left:-250px; opacity: 0.2;">
        </div>

        """
        page+="""
        <img src="static/images/system/aide/fenetres.webp" alt="logo" class="fond_aide">
        
        <h1 class="titre_aide">Le système de fenêtre</h1>
        
        <p class="texte_aide">
        FLASK a permis l'existence de ce système.<br>
        Dans les cookies, il existe une liste indiquant les fenêtres ouvertes par l'utilisateur.
        A partir de cette liste, on incruste au bureau les pages associés aux fenêtres avec les iframes.
        Des pages web spéciaux sont consacrées à la gestion de cette liste, grâce aux formulaires reçus.<br>
        <br>
        Le Javascript est principalement utilisé pour la navigation dans l'historique.
        Ce moyen permet de régénérer telles quelles les pages web précédemment ouvertes.
        Comme après avoir ouvert le menu démarré.<br>
        Les fenêtres fermées sont gardé en mémoire, penser à retourner sur le bureau régulièrement.
        </p>
        """     
    elif afficher=="admin": #La session Administrateur
        page+="""
        <div style="background-color: blue; width:205px; height:37px; position:absolute; top:112px; left:-250px; opacity: 0.2;">
        </div>

        """
        page+="""
        <img src="static/images/system/aide/console.webp" alt="fond_aide" class="fond_aide">
        
        <h1 class="titre_aide">La session Administrateur</h1>
        
        <p class="texte_aide">
        L'administrateur d'Ferry 2000 peut accéder à tous les
        documents d'Ferry Word existants, et même les supprimers.<br>
        Il peut également créer, modifier ou supprimer des sessions utilisateurs.<br>
        <br>
        Toutefois, l'administrateur n'a pas la permission de supprimer sa session,
        ou créer une autre session administrateur.<br>
        Pour modifier la session, l'administrateur est obligé de se connecter à
        sa session dès l'ouverture d'Ferry 2000.<br>
        <br>
        Pour des mesures de sécurité, pensez à vous déconnecter lorsque vous n'utilisez plus la session.
        </p>
        """  
    
    elif afficher=="connexion": #Connexion et écran de veille
        page+="""
        <div style="background-color: blue; width:205px; height:37px; position:absolute; top:150px; left:-250px; opacity: 0.2;">
        </div>

        """
        page+="""
        <img src="static/images/system/demarrage/demarrage.png" alt="fond_aide" class="fond_aide">
        
        <h1 class="titre_aide">Connexion et écran de veille</h1>
        
        <p class="texte_aide">
        Afin d'éviter que deux utilisateurs soient connectés en même temps,
        il existe un système de jeton.<br>
        Lorsqu'un utilisateur se connecte, un jeton valide durant 15 minutes est créé.
        Il est régulièrement mis à jour durant votre utilisation.<br>
        Lorsque le jeton n'est plus valide, vous n'êtes pas déconnecté.
        Toutefois, un autre utilisateur peut se connecter et vous serez alors déconnecté.<br>
        <br>
        S'il n'y a aucune interaction avec Ferry 2000 en dehors de l'utilisation
        des fenêtres pendant 15 minutes, alors l'écran de veille s'activera.<br>
        Vous pourrez reprendre vos activités sur Ferry 2000, si le jeton le permet.

        </p>
        """  
        
    elif afficher=="EExplorer": #A propos d'Ferry Explorer
        page+="""
        <div style="background-color: blue; width:205px; height:37px; position:absolute; top:185px; left:-250px; opacity: 0.2;">
        </div>

        """
        page+="""
        <img src="static/images/system/aide/EExplorer.webp" alt="fond_aide" class="fond_aide">
        
        <h1 class="titre_aide">A propos d'Ferry Explorer</h1>
        
        <p class="texte_aide">
        Jusqu'où irez-vous aujourd'hui ?<br>
        <br>
        Certains sites internet ne sont pas compatibles.<br>
        Toutefois, il peut-être très utilise si vous utilisez Ferry Word.<br>
        Vous pouvez l'ouvrir assez rapidement pour y faire une simple recherche.
        Vous pourrez ensuite refermer le navigateur, et reprendre là où vous en étier.<br>
        <br>
        Pas besoin de sauvegarder juste avant, vos modifications resteront en mémoire !
        </p>
        """  
    
    else: #Si aucune section est demandé, on affiche par défaut ce message:
        page+="""
        <img src="static/images/system/aide/fond_ferry.webp" alt="fond_aide" class="fond_aide">
        
        <h1 class="titre_aide">Démarrer avec Ferry 2000</h1>
        
        <p class="texte_aide">
        Bienvenue sur Ferry 2000 !<br>
        <br>        
        Cliquez sur la section qui vous intéresse, afin d'être aidé et d'en savoir plus.<br>
        Le système comporte quelques bruitages audio et musiques. N'hésitez pas à activé légèrement
        le son pour la meilleur expérience possible.
        </p>
        """

        
    page+="""</div>"""
    
    page+=basdepage
    return page


#@app.route('/executer', methods = ['GET'])
def executer():
    #La fenêtre executer permet de lancer directement un logiciel, ou d'ouvrir
    #un document.
    
    page=morceau_entete
    page+="""
    <link rel="stylesheet" href="static/executer.css" type="text/css">
    </head><body>
    """

    #Structure de la page comportant les formulaires.
    page+="""
    <div style="position:absolute; top:20px; left:20px;">
    <img src="static/images/system/icons/executer.png" alt="Îcone executer">
    </div>
    
    <div style="position:absolute; top:5px; left:70px; font-family: windowsfont; font-size: 15px;">
    <p>Tapez le nom d'un programme ou d'un document, et Ferry 2000 l'ouvrira pour vous.</p>
    </div>
    
    <p style="position:absolute; top:80px; left:50px; font-family: windowsfont; font-size: 15px;">
    <u>Que souhaitez vous ouvrir ?</u>
    </p>
    
    
    <div style="position:absolute; top:95px;left:230px; width:10px;">
    <form action="executer_conf" method="post">
    <input name="executer_type" type="radio" value="programme" checked="checked">
    <input name="executer_type" type="radio" value="document">
    <input name="executer" type="texte" size="25" style="position:absolute; top:70px; right:-70px;">
    <input value="       OK       " type="submit" style="position:absolute; top:120px; right:-5px;">
    </div>
    </form>
    
    <div style="position:absolute; top:81px; left:255px; width:10px; font-family: windowsfont; font-size: 15px;">
    <p style="margin-bottom:-12px;">programme</p>
    <p style="margin-bottom:-12px;">document</p>
    </div>
    
    <p style="position:absolute; top:150px; left:50px; font-family: windowsfont; font-size: 15px;">
    <u>Ouvrir : </u>
    </p>
    
    <form action="fermeture_fenetre" target="_parent" method="get">
    <input name="fermer" type="hidden" value='executer'>
    <input value="    Annuler    " type="submit" style="position:absolute; top:215px; right:20px;">
    </form>
    
    """
    page+=basdepage
    
    return page

#@app.route('/executer_conf', methods = ['POST'])
def executer_conf():
    #Page qui reçois les formulaires et traite la demande de l'utilisateur.
    page=morceau_entete
    page+="""
    <link rel="stylesheet" href="static/executer.css" type="text/css">
    </head><body>
    """
    
    resultat = flask.request.form
    executer_type = resultat.get('executer_type',"")
    executer = resultat.get('executer',"")
    

    if executer_type!="" and executer!="":
        #Les formulaires ont été remplis, donc on peut essayer de traiter la
        #demande.
        #(Sinon, on redirige vers la page exécuter.)
        
        #Pour éviter tout problème avec la base de donnée et le traitement de
        #la demande, on remplace les caractères problématique par d'autres.
        
        #Il n'y aura pas besoin de reconversion à faire par la suite, puisque
        #les documents enregistrés comporte sont ces lettres au lieu de: ' et ".
        #De plus, aucun nom de logiciel dans la BDD comporte ces caractères.
        executer=executer.replace("'","ऐ")
        executer=executer.replace('"','ऑ')
        
        #Si on souhaite afficher un document
        if executer_type=="document":
            connexion = sqlite3.connect("Ferry2000.db")

            morceau_requete="(documents.user_doc=='"+str(flask.session['utilisateur'])+"' OR documents.proteger_doc>=2 OR '"+str(flask.session['utilisateur'])+"' IN (SELECT nom FROM utilisateur WHERE type==2))"
            recup_nom_doc=list(connexion.execute("SELECT COUNT(documents.nom_doc) FROM documents JOIN utilisateur ON utilisateur.nom=documents.user_doc WHERE documents.nom_doc=='"+str(executer)+"' AND "+morceau_requete))[0][0]
            connexion.close()

            #On vérifie que le document demandé existe, et qu'Ferry Word
            #n'est pas déjà ouvert
            if recup_nom_doc>0 and 'ferryword' not in flask.session['taskbar']:
                #Le doc existe, et Ferry Word est bien fermer.
                
                #On stock le nom du document afin qu'à l'ouverture
                #d'Ferry Word, celui-ci prenne en charge immédiatement le
                #document.
                flask.session['document']=str(executer)

                #On ajoute Ferry Word à la liste des fenêtres ouverte par
                #l'utilisateur.
                taskbar=flask.session['taskbar']
                taskbar.append('ferryword')
                flask.session['taskbar']=taskbar
                #Note:  Il n'est pas possible d'ajouter la valeur directement
                #       à la liste. Il faut faire ce détour, comme vous me
                #       l'avez proposer, quand j'étais confronté à ce problème.
                
                #Redirection pour fermer la fenêtre Executer
                page+="""
                    <script type="text/javascript">
                    var delai=0; // Delai en secondes
                    var url='fermeture_fenetre?fermer=executer'; // Url de destination
                    setTimeout("parent.document.location.href=url", delai + '000');
                    </script>          
                """
                
                #Note:  On est obligé de passer par une redirection pour éviter
                #       de recréer un formulaire demandant à l'utilisateur de
                #       le faire manuellement.
                #       Cependant, cela nous livre à divers problèmes:
                #           - Impossible d'ouvrir en même temps Ferry Word
                #           - Impossible d'envoyer un formulaire comportant le
                #             nom du document à ouvrir à Ferry Word.
                #       Ce qui explique la manipulation qui pourrait parraître
                #       inutile (car il existe ouverture_fenêtre), plus haut.
                page+=basdepage
                return page
            else:
                #Impossible d'ouvrir le document
                
                page+="""
                <img src="static/images/system/icons/no.png" alt="valider" style="position:absolute; top:20px; left:20px;">
                
                <p style="position:absolute; top:15px; left:70px; font-family:windowsfont; font-size:15px;">
                Impossible d'ouvrir le document.<bR>
                <br>
                Soit celui-ci n'existe pas, où encore Ferry Word est déjà ouvert<br>
                Il est également possible que vous n'ayez pas les permissions
                d'accès, dans le cas où il existe.
                </p>
                
                <div style="position:absolute; top:95px;left:230px; width:10px;">
                <form action="executer" method="get">
                <input value="     Retour     " type="submit" style="position:absolute; top:120px; right:-5px;">
                </div>
                </form>
                
                <form action="fermeture_fenetre" target="_parent" method="get">
                <input name="fermer" type="hidden" value='executer'>
                <input value="    Fermer    " type="submit" style="position:absolute; top:215px; right:20px;">
                </form>
                
                """
                
                page+=basdepage
                return page

        #Si on souhaite afficher un programme
        elif executer_type=="programme":
            
            connexion = sqlite3.connect("Ferry2000.db")
            recup_nom_prog=list(connexion.execute("SELECT COUNT(logiciels.nom) FROM logiciels WHERE logiciels.nom=='"+str(executer)+"' AND logiciels.dispo_bureau>=0"))[0][0]
            connexion.close()
            
            #On vérifie que le programme demandé existe, et qu'il n'est pas
            #déjà ouvert
            if recup_nom_prog>0 and str(executer) not in flask.session['taskbar']:
                #Si c'est le cas
                taskbar=flask.session['taskbar']
                taskbar.append(str(executer))
                flask.session['taskbar']=taskbar
                page+="""
                    <script type="text/javascript">
                    var delai=0; // Delai en secondes
                    var url='fermeture_fenetre?fermer=executer'; // Url de destination
                    setTimeout("parent.document.location.href=url", delai + '000');
                    </script>          
                """
                #Note:  On est obligé de passer par une redirection pour éviter
                #       de recréer un formulaire demandant à l'utilisateur de
                #       le faire manuellement.
                #       Cependant, cela nous livre à un problème:
                #           - Impossible d'ouvrir en même temps le programme
                #       Ce qui explique la manipulation qui pourrait parraître
                #       inutile (car il existe ouverture_fenêtre), plus haut.
                
                
                page+=basdepage
                return page
            else:
                #Impossible d'ouvrir le programme
                page+="""
                <img src="static/images/system/icons/no.png" alt="valider" style="position:absolute; top:20px; left:20px;">
                
                <p style="position:absolute; top:15px; left:70px; font-family:windowsfont; font-size:15px;">
                Impossible d'ouvrir le programme.<bR>
                <br>
                Soit celui-ci n'existe pas, où encore il est déjà ouvert.<br>
                Il est aussi possible qu'il ne puisse pas être exécuter de cette manière.
                </p>
                
                <div style="position:absolute; top:95px;left:230px; width:10px;">
                <form action="executer" method="get">
                <input value="     Retour     " type="submit" style="position:absolute; top:120px; right:-5px;">
                </div>
                </form>
                
                <form action="fermeture_fenetre" target="_parent" method="get">
                <input name="fermer" type="hidden" value='executer'>
                <input value="    Fermer    " type="submit" style="position:absolute; top:215px; right:20px;">
                </form>
                
                """
                page+=basdepage
                return page

    #S'il n'est pas possible de subvenie à la demande de l'utilisateur, alors
    #on le ramène au formulaire. Vu que la demande n'a pas marché.
        page+="""
        <script type="text/javascript">
            var delai=0; // Delai en secondes
            var url='executer'; // Url de destination
            setTimeout("document.location.href=url", delai + '000');
        </script>          
        """
        page+=basdepage
        return page