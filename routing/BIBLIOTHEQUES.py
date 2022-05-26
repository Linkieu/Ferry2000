# -*- coding: utf-8 -*-
"""
Created on Sun May  1 20:42:36 2022

@author: Matthieu
"""

import flask
import sqlite3
import random
from time import *
from Plugins_E2000 import entete, basdepage, morceau_entete, entete_parametre, interface, demarrer_on, demarrer_off, erreur_12, erreur_2a, erreur_2b, popup_info

app = flask.Flask(__name__) # Création de l'application

#@app.route('/bibliotheque_docs', methods = ['GET'])
def bibliotheque_docs():
    page=morceau_entete
    page+="""
    <link rel="stylesheet" href="static/explorateur.css" type="text/css">
    <link rel="stylesheet" href="static/explorateur_fond.css" type="text/css">
    <link rel="stylesheet" href="static/ferryword.css" type="text/css">
    </head>
    <body>
    """




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

    #Mise à jour du jeton, car page rechargé
    connexion = sqlite3.connect("Ferry2000.db")
    jeton=int(time())+900 #15min pour 900
    connexion.execute("UPDATE utilisateur SET jeton="+str(jeton)+" WHERE nom=='"+str(flask.session['utilisateur'])+"'")
    connexion.commit()
    connexion.close()
    ##########################################################################

    resultat = flask.request.args
    ouvrir_doc = resultat.get('ouvrir_doc',"")


    if ouvrir_doc!="":
        #Si on demande à la page d'ouvrir un document.
        #Par exemple, l'utilisateur clique sur l'un des enregistrements affichés,
        #Alors la page se recharge avec la valeur associé à ouvrir_doc adéquate.
        #Et donc, nous préparons l'ouverture du document dans Ferry Word.

        flask.session['document']=ouvrir_doc
        page+="""
            <script type="text/javascript">
            var delai=0; // Delai en secondes
            var url='ouverture_fenetre?ouvrir=ferryword&retour=2'; // Url de destination
            setTimeout("parent.document.location.href=url", delai + '000');
            </script>
            """

        ########RESERVER A L'EASTER EGG The Ferry 2000 Product Team!########

        if ouvrir_doc=="The Ferry 2000 Product Team!":
            #Indique lorsqu'on génère le bureau qu'il faut jouer la musique
            #de l'easter egg.
            #Si le nom du document à ouvrir correspond à:
            #"The Ferry 2000 Product Team!"

            #Remarque:  cela bug un peu...
            #           Si on ouvre tout de suite après un autre document
            #           la musique se joue quand même.
            #           Et si après ça, on réouvre le document crédit,
            #           la musique de ne se joue pas.

            #Il est impossible d'intégrer directement cette fonction à
            #Ferry Word au risque qu'elle soit joué plusieurs fois.

            #La solution actuel est un compromis, pour essayer de reproduire
            #l'easter egg de Windows 95.
            flask.session['dejajouer_easteregg_EW']=True
        elif 'dejajouer_easteregg_EW' in flask.session:
            #Au cas où on ouvre le documents easter egg, et qu'on ouvre
            #ensuite un autre document, on efface le cookie afin d'éviter
            #que la musique de joue.
            del flask.session['dejajouer_easteregg_EW']

        #######################################################################

    if 'recherche' in flask.session:
        #Si l'utilisateur a utilisé la barre de recherche du menu démarré
        #pour rechercher un document, alors on affiche ce qui correspond à
        #son mot clé.
        #On remplace les caractères problématique par des caractères juger
        #inutile. Ils sont utiliser à la place de ' et " dans la BDD.
        recherche=str(flask.session['recherche'])
        recherche=recherche.replace("'","ऐ")
        recherche=recherche.replace('"','ऑ')
        selection="AND nom_doc LIKE '%"+recherche+"%'"
    else:
        #Dans ce cas là, on sélectionne tout les documents que peut accéder
        #l'utilisateur. Donc il n'y a pas de sélection.
        selection=""

    #On affiche l'interface qui s'adaptera au cas où il y a beaucoup de docs
    #à afficher.
    page+="""
    <img class="explorateur" src="static/images/system/bibliotheques/docs.png" alt="Bibliothèque">
    <img class="adroite" src="static/images/system/bibliotheques/adroite.png" alt="côté">
    <img class="enbas" src="static/images/system/bibliotheques/enbas.png" alt="tout en bas">




    <h1 class="explorateur">Mes<br>documents</h1>
    <p class="explorateur">Retrouvez facilement vos documents<br>personnels.</p>
    <p class="addresse">Mes documents</p>

    <img class="barre_classer_docs" src="static/images/system/bibliotheques/barre.png" alt="Barre classer docs">

    """

    page+="""<div class="classement_docs">"""

    #On récupère l'ordre indiqué par l'utilisateur dans les paramètres des dossiers.
    connexion = sqlite3.connect("Ferry2000.db")
    ordre=list(connexion.execute("SELECT ordre_docs FROM utilisateur WHERE nom=='"+str(flask.session['utilisateur'])+"'"))[0][0]


    #On récupère la totalité les documents accessible.
    #C'est à dire:
    #   - Ceux dont l'utilisateur en est l'auteur
    #   - Ceux qui sont accessible à tous
    #   - Ou la totalité des documents si c'est une session administrateur.
    morceau_code=str(flask.session['utilisateur'])+"' IN (SELECT nom FROM utilisateur WHERE type==2))"+selection+"ORDER BY "+str(ordre)
    liste_docs=list(connexion.execute("SELECT * FROM documents WHERE (user_doc=='"+str(flask.session['utilisateur'])+"' OR (proteger_doc==2 OR proteger_doc==3) OR '"+morceau_code))
    connexion.close()

    #On parcours les enregistrements
    for enregistrement in liste_docs:
        #On récupère les informations à afficher dans la bibliothèque.
        nom_doc,user_doc,date_doc,proteger_doc=enregistrement[0],enregistrement[1],enregistrement[2],enregistrement[3]

        #On réajuste la date pour l'affichage.
        date_doc=date_doc[6:8]+"/"+date_doc[4:6]+"/"+date_doc[:4]+date_doc[8:14] #On affiche correctement la date


        #On affiche l'état du document en fonction de ce qui est inscrit dans la BDD.
        if proteger_doc%2==0:
            proteger_doc="Modifiable"
        else:
            proteger_doc="Finaliser"

        #Création de la mise en page pour l'affichage des informations liées
        #au document.

        page+="""
        <div class="docs">
            <a href='bibliotheque_docs?ouvrir_doc="""+str(nom_doc)+"""'>
            <img class="classement_docs" src="static/images/system/icons/word2mini.png" alt="Icone Word">
            """
        nom_doc=nom_doc.replace("ऐ","'")
        nom_doc=nom_doc.replace('ऑ','"')
        page+="""
            <p class="classement_docs_nom">"""+str(nom_doc)+"""</p>
            </a>
            <p class="classement_docs_protection">"""+str(proteger_doc)+"""</p>
            <p class="classement_docs_auteur">"""+str(user_doc)+"""</p>
            <p class="classement_docs_date">"""+str(date_doc)+"""</p>
        </div>
        """
    page+="""
    <div style="height:30px;">
    </div>
    """
    #Le div permet d'éviter que l'image qu'on met au premier plan tout en bas
    #cache les derniers documents affichés, s'il y en a plusieurs


    page+="</div>"






    return page

#@app.route('/bibliotheque_logiciels', methods = ['GET'])
def bibliotheque_logiciels():
    page=morceau_entete

    page+="""
    <link rel="stylesheet" href="static/explorateur.css" type="text/css">
    <link rel="stylesheet" href="static/programmes.css" type="text/css">
    </head><body>
    """

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

    #Mise à jour du jeton, car page rechargé
    connexion = sqlite3.connect("Ferry2000.db")
    jeton=int(time())+900 #15min pour 900
    connexion.execute("UPDATE utilisateur SET jeton="+str(jeton)+" WHERE nom=='"+str(flask.session['utilisateur'])+"'")
    connexion.commit()
    connexion.close()
    ##########################################################################

    #Mise en page
    page+="""
    <img class="control_pannel" src="static/images/system/bibliotheques/logiciels.png" alt="Panneau de configuration">
    <h1 class="explorateur">Bibliothèque de<br> programmes</h1>
    <p class="explorateur">Exécutez le logiciel que vous <br> souhaitez utiliser depuis cette page.</p>
    <p class="addresse">Bibliothèque de programmes</p>
    """

    page+="""
    <div class="icones_programmes" style="font-family:windowsfont; font-size: 12px;">
    """

    #On récupère la liste des logiciels qu'on autorise à apparaître dans cette liste.
    connexion = sqlite3.connect("Ferry2000.db")
    liste_icones_bureau=list(connexion.execute("SELECT nom,titre,icon FROM logiciels WHERE dispo_bureau>=0 ORDER BY dispo_bureau ASC"))
    connexion.close()

    #Mise en page de la sélection
    for icone_bureau in liste_icones_bureau:
        #On affiche les icones dans la bibliothèque en parcourant la liste de logiciels.
        #Elles apparaissent dans l'ordre indiqué dans la BDD.
        icone_nom=icone_bureau[0]
        icone_titre=icone_bureau[1]
        icone_icon=icone_bureau[2]
        if icone_nom!="bibliotheque_logiciels":
            page+="""
            <a href='ouverture_fenetre?ouvrir="""+str(icone_nom)+"""' target="_parent" class="icone_bureau">
                <p class="icones_programmes">"""+str(icone_titre)+"""</p>
                <img class="icone_bureau" src='static/images/system/icons/"""+str(icone_icon)+"""' alt="Icone sur le bureau">
            </a>
            """

    page+="</div>"

    page+=basdepage
    return page
