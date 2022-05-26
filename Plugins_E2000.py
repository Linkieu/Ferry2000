# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 08:13:49 20222

@author: Matthieu
"""

#-----------------------------------------------------------------------------
#COMMUNE A TOUTE LES PAGES
#-----------------------------------------------------------------------------

entete="""<!DOCTYPE html> <!--Entête de la page HTML-->

    <html lang="fr">
            <head>
                <meta charset="UTF-8" >
                <title>Ferry 2000 - Projet NSI</title>
                <link rel="icon" href="/static/images/autres/W2000.png" />
                <link rel="stylesheet" href="static/style.css" type="text/css">
                <link rel="stylesheet" href="static/fonts.css" type="text/css">
                <link rel="stylesheet" href="static/messages.css" type="text/css">
                <link rel="stylesheet" href="static/explorateur.css" type="text/css">
                <link rel="stylesheet" href="static/demarrage_et_session.css" type="text/css">
                <link rel="stylesheet" href="static/ferryword.css" type="text/css">
    </head>
    <body>

"""

morceau_entete="""<!DOCTYPE html> <!--Entête de la page HTML-->

    <html lang="fr">
            <head>
                <meta charset="UTF-8" >
                <title>Ferry 2000 - Projet NSI</title>
                <link rel="icon" href="/static/images/autres/W2000.png" />
                <link rel="stylesheet" href="static/style.css" type="text/css">
                <link rel="stylesheet" href="static/fonts.css" type="text/css">
                <link rel="stylesheet" href="static/messages.css" type="text/css">
                <link rel="stylesheet" href="static/demarrage_et_session.css" type="text/css">
    """

entete_parametre="""<!DOCTYPE html> <!--Entête de la page HTML-->

    <html lang="fr">
            <head>
                <meta charset="UTF-8" >
                <title>Ferry 2000 - Projet NSI</title>
                <link rel="icon" href="/static/images/autres/W2000.png" />
                <link rel="stylesheet" href="static/parametres.css" type="text/css">
                <link rel="stylesheet" href="static/messages.css" type="text/css">
                <link rel="stylesheet" href="static/fonts.css" type="text/css">
    </head>
    <body>

"""


basdepage="""
<!--Bas de la page HTML + Information sur le projet sur le côté-->
    </body>
</html>
"""

#-----------------------------------------------------------------------------
#FOND D'ECRAN ET BARRE DES TÂCHES
#-----------------------------------------------------------------------------

interface="""
    <img class="bureau" src="static/images/system/wallpaper/WP_sonic.jpg" alt="Fond d'écran">
    <img class="interface" src="static/images/system/taskbar.png" alt="Barre des tâches Ferry 2000">
    """


#-----------------------------------------------------------------------------
#ETAT DU MENU DEMARRER: OUVERT OU REFERMER
#-----------------------------------------------------------------------------

demarrer_on="""
        <a href="javascript:history.go(-1)">
        <img class="filtre_démarrer" src="static/images/system/filtre_burreau_pour_menu_démarrer.png" alt="Menu démarrer" height="558" width="790">
        </a>
        <a href="javascript:history.go(-1)">
            <img class="démarrer" src="static/images/system/démarrer_clickon.png" alt="Bouton démarrer avec click">
        </a>


        <img usemap="#menu_dem" class="menu_démarrer" src="static/images/system/menu_démarrer.gif" alt="Menu démarrer">

                <a href="ouverture_fenetre?ouvrir=bibliotheque_logiciels&retour=2" onmouseover="programmes.src='static/images/system/menu_démarrer/programmes_on.png'" onmouseout="programmes.src='static/images/system/menu_démarrer/programmes_off.png'">
                <img class="démarrer_programmes" id="programmes" src="static/images/system/menu_démarrer/rien.png" alt="Menu Démarrer: Programmes"></a>

                <a href="ouverture_fenetre?ouvrir=bibliotheque_docs&retour=2" onmouseover="documents.src='static/images/system/menu_démarrer/documents_on.png'" onmouseout="documents.src='static/images/system/menu_démarrer/documents_off.png'">
                <img class="démarrer_documents" id="documents" src="static/images/system/menu_démarrer/rien.png" alt="Menu Démarrer: Documents"></a>


                <a href="ouverture_fenetre?ouvrir=parametres&retour=2" onmouseover="parametres.src='static/images/system/menu_démarrer/parametres_on.png'" onmouseout="parametres.src='static/images/system/menu_démarrer/parametres_off.png'">
                <img class="démarrer_parametres" id="parametres" src="static/images/system/menu_démarrer/rien.png" alt="Menu Démarrer: Paramètres"></a>

                <a href="ouverture_fenetre?ouvrir=Ferry_Explorer&retour=2" onmouseover="EExplorer.src='static/images/system/menu_démarrer/EExplorer_on.png'" onmouseout="EExplorer.src='static/images/system/menu_démarrer/EExplorer_off.png'">
                <img class="démarrer_EExplorer" id="EExplorer" src="static/images/system/menu_démarrer/rien.png" alt="Menu Démarrer: EExplorer"></a>

                <a href="ouverture_fenetre?ouvrir=aide&retour=2" onmouseover="aide.src='static/images/system/menu_démarrer/aide_on.png'" onmouseout="aide.src='static/images/system/menu_démarrer/aide_off.png'">
                <img class="démarrer_aide" id="aide" src="static/images/system/menu_démarrer/rien.png" alt="Menu Démarrer: Aide"></a>

                <a href="ouverture_fenetre?ouvrir=executer&retour=2" onmouseover="executer.src='static/images/system/menu_démarrer/executer_on.png'" onmouseout="executer.src='static/images/system/menu_démarrer/executer_off.png'">
                <img class="démarrer_executer" id="executer" src="static/images/system/menu_démarrer/rien.png" alt="Menu Démarrer: Exécuter"></a>

                <a href="deconnexion_session" onmouseover="arrêter.src='static/images/system/menu_démarrer/arrêter_on.png'" onmouseout="arrêter.src='static/images/system/menu_démarrer/arrêter_off.png'">
                <img class="démarrer_arrêter" id="arrêter" src="static/images/system/menu_démarrer/rien.png" alt="Menu Démarrer: Arrêter"></a>


        <form action ="/ouverture_fenetre" method="get">
            <div style="position:absolute; bottom:280px; left:65px;">
            <input name="ouvrir" type="hidden" value='bibliotheque_docs'>
            <input name="retour" type="hidden" value='2'>
            <input type="text" name="recherche" size="8" placeholder="Rechercher"> <!--Barre de recherche-->
            <input type="submit" value=">">
            </div>
        </form>

        """

demarrer_off="""
        <a href="?demarrer=on">
        <img class="démarrer" src="static/images/system/démarrer_clickoff.png" alt="Bouton démarrer sans click">
        </a>
        """

#-----------------------------------------------------------------------------
#MESSAGES
#-----------------------------------------------------------------------------

#Simple pop-up qui apparaît pour prévenir l'utilisateur sur une action en cours.
popup_info="""
                <!--<audio src="static/musique/chord.mp3" autoplay></audio>-->
                <img class="message" src="static/images/system/messages/msgbox1.png" alt="Ecran de démarrage">

            """



#Message d'erreur redirigeant vers l'ouverture de la session.
erreur_12="""
                <audio src="static/musique/chord.mp3" autoplay></audio>
                <img class="message" src="static/images/system/messages/msgbox1.png" alt="Message d'erreur">
                <div class="refermer_message">
                    <form action ="/demarrage" method="get">
                        <input type="submit" value="          OK          ">\n <!--Referme le message-->
                    </form>
                </div>

            """

#Message d'erreur faisant un retour arrière dans l'historique (revient à la page -1)
erreur_2a="""
                <audio src="static/musique/chord.mp3" autoplay></audio>
                <img class="message" src="static/images/system/messages/msgbox1.png" alt="Message d'erreur">
                <div class="refermer_message">
                    <form action ="javascript:history.go(-1)" method="get">
                        <input type="submit" value="          OK          ">\n <!--Referme le message-->
                    </form>
                </div>

            """
#Message d'erreur faisant un retour arrière dans l'historique (revient à la page -2)
erreur_2b="""
                <audio src="static/musique/chord.mp3" autoplay></audio>
                <img class="message" src="static/images/system/messages/msgbox1.png" alt="Message d'erreur">
                <div class="refermer_message">
                    <form action ="javascript:history.go(-2)" method="get">
                        <input type="submit" value="          OK          ">\n <!--Referme le message-->
                    </form>
                </div>

            """
