# -*- coding: utf-8 -*-
"""
Created on Sun May  1 20:49:39 2022

@author: Matthieu
"""

import flask
import sqlite3
import random
from time import *
from Plugins_E2000 import entete, basdepage, morceau_entete, entete_parametre, interface, demarrer_on, demarrer_off, erreur_12, erreur_2a, erreur_2b, popup_info

app = flask.Flask(__name__) # Création de l'application


#@app.route('/admin_creersession', methods = ['GET']) # Bureau Ferry 2000
def admin_creersession():
    page=entete_parametre
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


    #On vérifie que l'utilisateur est toujours connecté aux paramètres en tant
    #qu'administrateur.
    #Remarque: lorsque les paramètres d'administration sont fermés, les cookies
    #concernés sont supprimés.
    if "admin_nom" in flask.session and "admin_mdp" in flask.session:
        connexion = sqlite3.connect("Ferry2000.db")
        verif_admin=list(connexion.execute("SELECT nom,mdp FROM utilisateur WHERE type==2"))[0]
        connexion.close()

        if flask.session["admin_nom"]!=verif_admin[0] or flask.session["admin_mdp"]!=verif_admin[1]: ############################# A REMPLIR
            description="Une erreur est survenue, les identifiants stockés en mémoire ne correspondent pas."
            msgbas="Cliquez sur retour pour vous connecter."
            page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

            page+="""
            <form action="controle_utilisateur" method="get">
            <input name="acces" type="hidden" value='parametre_admin'>
            <input class="bouton3c" type="submit" value="    Retour     ">\n
            </form>
            """
            connexion.close()
            page+=basdepage
            return page
    else:
        description="Une erreur est survenue, vous devez vous connecter en tant qu'administrateur pour poursuivre."
        msgbas="Cliquez sur retour pour vous connecter."
        page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)
        page+=basdepage

        page+="""
        <form action="controle_utilisateur" method="get">
        <input name="acces" type="hidden" value='parametre_admin'>
        <input class="bouton3c" type="submit" value="    Retour     ">\n
        </form>
        """
        return page


    resultat = flask.request.args
    afficher = resultat.get('afficher',"")








    description="Entrez les informations de base concernant cet utilisateur, puis confirmez un mot de passe."
    msgbas="Pour continuer, cliquez sur Suivant."
    if afficher=="marchepas":
        #Message d'erreur
        description="""
        Impossible d'effectuer l'action demandé. Vérifiez que votre demande est conforme.
        Il est possible que le paramètre demander est indisponible, comme un nom de session
        déjà utilisé par exemple.
        <br>
        Veuillez recommencer.
        """
        msgbas="Cliquez sur précédent pour retourner en arrière."

        page+="""
        <form>
        <input class="bouton3b" type="submit" value="   Suivant >   " disabled>\n
        </form>

        <form action="javascript:history.go(-1)" method="get">
        <input class="bouton3a" type="submit" value="  < Précédent  ">\n
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Annuler    ">\n
        </form>
        """

    elif afficher=='creersession_2':
        #Affichage des possibilités d'arrière-plan pour la nouvelle session.

        #Redirection:
        #    admin_modif_session_sauvegarder → afficher=creersession_3

        description="Choisissez un fond d'écran qui sera associé à la session."
        msgbas="Pour continuer, cliquez sur Suivant."
        page+="""<div style="position: absolute; top:90px; left:186px; width:400px;">"""
        style1="position: absolute; top:104px; left:181px; width:400px;"
        page+=flask.render_template("parametre_wallpaper.html",lien1='admin_modif_session_sauvegarder',name1='creersession_WP',style1=style1)

        page+="""
        </div>
        <input name="afficher" type="hidden" value='creersession_3'>
        <input class="bouton3b" type="submit" value="   Suivant >   ">\n
        </form>


        <form action="javascript:history.go(-1)" method="get">
        <input class="bouton3a" type="submit" value="  < Précédent  ">\n
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Annuler    ">\n
        </form>
        """

    elif afficher=='creersession_3':
        #Affichage des paramètres du thème de la nouvelle session.

        #Redirection:
        #    admin_modif_session_sauvegarder → afficher=creersession_4

        description="Choisissez comment sera représenté la barre des titres des fenêtres."
        msgbas="Pour continuer, cliquez sur Suivant."

        pos2="position: relative; top:253px; left:6px;"
        class_bt,nom_bt="bouton3b","   Suivant >   "
        page+="""<form action="admin_modif_session_sauvegarder" method="post">"""
        page+=flask.render_template("parametre_themes.html",pos1="modif_session_themes",pos2=pos2,pos3="modif_session_pointeur",pos4="modif_session_police",class_bt=class_bt,nom_bt=nom_bt,theme_c1="#191970",theme_c2="#87ceeb",theme_titre="#ffffff",theme_opa="100",theme_police="windowsfont")
        page+="""<input name="afficher" type="hidden" value='creersession_4'>"""
        page+="</form>"

        page+="""
        <form action="javascript:history.go(-1)" method="get">
        <input class="bouton3a" type="submit" value="  < Précédent  ">\n
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Annuler    ">\n
        </form>
        """
    elif afficher=='creersession_4':
        #Affichage des possibilités d'écran de veille pour la nouvelle session.

        #Redirection:
        #    admin_modif_session_sauvegarder → afficher=creersession_fin
        description="Choisissez un écran de veille qui s'enclenchera après 15 minutes d'inactivité du bureau."
        msgbas="Pour terminer, cliquez sur suivant."

        style1="position: absolute; top:100px; left:186px; width:400px;"
        style2="position: absolute; top:114px; left:181px; width:400px;"
        action="/admin_modif_session_sauvegarder"
        page+=flask.render_template("parametre_scr.html",style1=style1,style2=style2,action=action)
        page+="""
            </div>
            <input name="afficher" type="hidden" value='creersession_fin'>
            <input class="bouton3b" type="submit" value="   Suivant >   ">\n
        </form>

        <form action="javascript:history.go(-1)" method="get">
        <input class="bouton3a" type="submit" value="  < Précédent  ">\n
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Annuler    ">\n
        </form>
        """
    elif afficher=='creersession_fin':
        #Affichage du message de confirmation et enregistrement de la nouvelle
        #session.
        tour=-1
        for requete in flask.session["requetes"]:
            tour+=1
            if tour!=0:
                connexion = sqlite3.connect("Ferry2000.db")
                connexion.execute(requete)
                connexion.commit()
                connexion.close()
        description="La création de la nouvelle session s'est terminé avec succès !"
        msgbas="Vous pouvez refermer cette fenêtre."

        page+="""
        <form action="fermeture_fenetre" target="_parent" method="get">
        <input name="fermer" type="hidden" value='controle_utilisateur?acces=parametre_admin'>
        <input class="bouton3b" type="submit" value="    Fermer    ">\n
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Retour    ">\n
        </form>

        """
    else:
        #Affichage de la première page, où on demande le nom et le mot de passe
        #de la nouvelle session.

        #Redirection:
        #    admin_modif_session_sauvegarder → afficher=creersession_2


        flask.session["requetes"]=["","","","",""]
        #On va stocker les requetes pour créer (et aussi personnalisé) la session
        #dans cette liste en associant une requete à un emplacement spécifique.
        #1 → nom de la nouvelle session
        #2 → requête pour créer la session
        #3 → requête pour mettre un fond d'écran
        #4 → requête pour mettre un thème
        #5 → requête pour mettre un écran de veille
        #Elle seront toute exécutées plus tard, à la fin de la création de la session.

        #Il existe donc une possibilité que l'utilisateur en profite pour faire
        #de l'injection SQL. D'autres possibilités doivent exister, mais je juge
        #que c'est la plus simple, et la plus rapide à mettre en place.


        description="Entrez les informations de base concernant cet utilisateur, puis confirmez un mot de passe."
        msgbas="Pour continuer, cliquez sur Suivant."
        page+="""

        <form action ="/admin_modif_session_sauvegarder" method="post">
        <div class="disposition_creersession">

        <br>
        <label for="new_user" class="connexion" title="Veuillez saisir votre nouveau nom d'utilisateur">Nom d'utilisateur:</label>
        <input class="connexion1" type="text" name="new_user" id="new_user" size="32"> <!--Emplacement nom utilisateur-->
        <br><br>
        <label for="new_mdp" class="connexion" title="Veuillez saisir votre nouveau mot de passe">Mot de passe:</label>
        <input class="connexion2" type="password" name="new_mdp" id="new_mdp" size="32"> <!--Emplacement nom utilisateur-->
        <br><br>
        <label for="new_mdp_conf" class="connexion" title="Veuillez saisir votre nouveau mot de passe de nouveau">Confirmation:</label>
        <input class="connexion3" type="password" name="new_mdp_conf" id="new_mdp_conf" size="32"> <!--Emplacement nom utilisateur-->

        </div>
        <input name="afficher" type="hidden" value='creersession_2'>
        <input class="bouton3b" type="submit" value="   Suivant >   ">\n
        </form>

        <form action="parametre_admin" method="post">
        <input class="bouton3a" type="submit" value="  < Précédent  " disabled>\n
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Annuler    ">\n
        </form>

        """



    page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

    connexion.close()
    page+=basdepage
    return page

#@app.route('/admin_modifsession', methods = ['GET']) # Bureau Ferry 2000
def admin_modifsession():
    page=entete_parametre
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


    #On vérifie que l'utilisateur est toujours connecté aux paramètres en tant
    #qu'administrateur.
    #Remarque: lorsque les paramètres d'administration sont fermés, les cookies
    #concernés sont supprimés.
    if "admin_nom" in flask.session and "admin_mdp" in flask.session:
        connexion = sqlite3.connect("Ferry2000.db")
        verif_admin=list(connexion.execute("SELECT nom,mdp FROM utilisateur WHERE type==2"))[0]
        connexion.close()
        if flask.session["admin_nom"]!=verif_admin[0] or flask.session["admin_mdp"]!=verif_admin[1]: ############################# A REMPLIR
            description="Une erreur est survenue, les identifiants stockés en mémoire ne correspondent pas."
            msgbas="Cliquez sur retour pour vous connecter."
            page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

            page+="""
            <form action="controle_utilisateur" method="get">
            <input name="acces" type="hidden" value='parametre_admin'>
            <input class="bouton3c" type="submit" value="    Retour     ">\n
            </form>
            """
            connexion.close()
            page+=basdepage
            return page
    else:
        description="Une erreur est survenue, vous devez vous connecter en tant qu'administrateur pour poursuivre."
        msgbas="Cliquez sur retour pour vous connecter."
        page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

        page+="""
        <form action="controle_utilisateur" method="get">
        <input name="acces" type="hidden" value='parametre_admin'>
        <input class="bouton3c" type="submit" value="    Retour     ">\n
        </form>
        """
        connexion.close()
        page+=basdepage
        return page

    resultat = flask.request.args
    afficher = resultat.get('afficher',"")
    message = resultat.get('message',"")


    if afficher=="modifsession_2":
        #Affichage de la première page, où on demande à l'administrateur
        #d'entrer un nouveau nom ou/et nouveau mot de passe à la session
        #sélectionné.

        #Redirection:
        #    admin_modif_session_sauvegarder → afficher=modif_sessionfin
        description="Entrez seulement les informations que vous souhaitez modifier."
        msgbas="Pour continuer, cliquez sur Suivant."
        page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)
        page+="""

        <form action ="/admin_modif_session_sauvegarder" method="post">
            <div style="position:absolute; top:100px; left:370px;">
                <br>
                <label for="changer_user" class="connexion" title="Veuillez saisir votre nouveau nom d'utilisateur">Nouveau nom:</label>
                <input class="connexion1" type="text" name="changer_user" id="changer_user" size="32" placeholder="15 caractères max"> <!--Emplacement nom utilisateur-->
                <br><br>
                <label for="changer_mdp" class="connexion" title="Veuillez saisir votre nouveau mot de passe">Nouveau mot de passe:</label>
                <input class="connexion2" type="password" name="changer_mdp" id="changer_mdp" size="32" placeholder="30 caractères max"> <!--Emplacement nom utilisateur-->
                <br><br>
                <label for="changer_mdp_conf" class="connexion" title="Veuillez saisir votre nouveau mot de passe de nouveau">Confirmer le mot de passe:</label>
                <input class="connexion3" type="password" name="changer_mdp_conf" id="changer_mdp_conf" size="32"> <!--Emplacement nom utilisateur-->
            </div>
            <input name="afficher" type="hidden" value='modifsession_fin'>
            <input class="bouton3b" type="submit" value="   Suivant >   ">\n <!--Renvoi le formulaire-->
        </form>

        <form action="admin_modifsession" method="get">
        <input class="bouton3a" type="submit" value="  < Précédent  ">\n
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Annuler    ">\n
        </form>

        """



        connexion.close()
        page+=basdepage
        return page


    elif afficher=="modifsession_fin":
        #Affichage du message de confirmation.
        if message=='1':
            description="Le mot de passe a été modifé avec succès !"
        elif message=='2':
            description="Le nom d'utilisateur a été modifé avec succès !"
        elif message=='3':
            description="Le nom d'utilisateur, et le mot de passe de cette session, a été modifé avec succès !"
        else:
            description="""Un problème est survenue, vérifiez que vous n'avez pas
            dépassé la limite de caractère, que tout correspond. Et que s'il y a un nom,
            qu'il n'est pas déjà utilisé."""
        msgbas="Vous pouvez refermer cette fenêtre."
        page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

        page+="""
        <form action="fermeture_fenetre" target="_parent" method="get">
        <input name="fermer" type="hidden" value='controle_utilisateur?acces=parametre_admin'>
        <input class="bouton3b" type="submit" value="    Fermer    ">
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Retour    ">
        </form>
        """

        return page

    elif afficher=='marchepas':
        #Message d'erreur
        titre="Administration des sessions"
        info="Modification des informations de connexion d'une session."
        description="Il n'existe aucune session à ce nom. Cliquez sur retour pour réessayer."
        img="Error.png"
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

        page+="""
        <form action="fermeture_fenetre" target="_parent" method="get">
        <input name="fermer" type="hidden" value='controle_utilisateur?acces=parametre_admin'>
        <input class="bouton3b" type="submit" value="    Fermer    ">
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Retour    ">
        </form>
        """
        return page
    else:
        #Affichage de la première page, où on demande de sélectionner
        #la session d'utilisateur a modifier.

        #Redirection:
        #    admin_modif_session_sauvegarder → afficher=modif_session2

        titre="Administration des sessions"
        info="Modification d'une session utilisateur."
        img="change_users.png"
        description="Sélectionnez la session à modifier."
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

        page+="""
        <form action ="admin_modif_session_sauvegarder" method="post">
            <div style="position:absolute; top:170px; left:370px">
                <label for="utilisateur" class="connexion" title="Veuillez saisir votre nom d'utilisateur">Utilisateur:</label>
                <div style="position:relative; right:130px; bottom:20px;">
                <select name="modif_user" id="utilisateur">
        """
        connexion = sqlite3.connect("Ferry2000.db")
        liste_session=list(connexion.execute("SELECT nom,type FROM utilisateur"))
        connexion.close()
        for nom_session in liste_session:
            if nom_session[1]!=2:
                page+="<option value='"+str(nom_session[0])+"'>"+str(nom_session[0])+"</option>"

        page+="""
                </select>
                </div>


                <input name="afficher" type="hidden" value='modifsession_2'>
            </div>
            <input class="bouton3b" type="submit" value="   Suivant >   ">\n <!--Renvoi le formulaire-->
        </form>

        <form action="parametre_admin" method="post">
        <input class="bouton3a" type="submit" value="  < Précédent  " disabled>\n
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Annuler    ">\n
        </form>
        """


        connexion.close()
        page+=basdepage
        return page

#@app.route('/admin_supprsession', methods = ['GET']) # Bureau Ferry 2000
def admin_supprsession():
    page=entete_parametre
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
    afficher = resultat.get('afficher',"")

    #On vérifie que l'utilisateur est toujours connecté aux paramètres en tant
    #qu'administrateur.
    #Remarque: lorsque les paramètres d'administration sont fermés, les cookies
    #concernés sont supprimés.
    if "admin_nom" in flask.session and "admin_mdp" in flask.session:
        connexion = sqlite3.connect("Ferry2000.db")
        verif_admin=list(connexion.execute("SELECT nom,mdp FROM utilisateur WHERE type==2"))[0]
        connexion.close()
        if flask.session["admin_nom"]!=verif_admin[0] or flask.session["admin_mdp"]!=verif_admin[1]: ############################# A REMPLIR
            description="Une erreur est survenue, les identifiants stockés en mémoire ne correspondent pas."
            msgbas="Cliquez sur retour pour vous connecter."
            page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

            page+="""
            <form action="controle_utilisateur" method="get">
            <input name="acces" type="hidden" value='parametre_admin'>
            <input class="bouton3c" type="submit" value="    Retour     ">\n
            </form>
            """
            connexion.close()
            page+=basdepage
            return page
    else:
        description="Une erreur est survenue, vous devez vous connecter en tant qu'administrateur pour poursuivre."
        msgbas="Cliquez sur retour pour vous connecter."
        page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

        page+="""
        <form action="controle_utilisateur" method="get">
        <input name="acces" type="hidden" value='parametre_admin'>
        <input class="bouton3c" type="submit" value="    Retour     ">\n
        </form>
        """
        connexion.close()
        page+=basdepage
        return page


    if afficher=='supprsession_2':
        #Affichage de la page de confirmation de la suppression de la session.

        #Redirection:
        #    admin_modif_session_sauvegarder → afficher=supprsession_fin
        if 'nom_session_a_suppr' in flask.session:
            nom_session_a_suppr=flask.session['nom_session_a_suppr']
        else:
            nom_session_a_suppr='missingno'
        description="Êtes vous sûr de supprimer définitivement la session nommé: "+str(nom_session_a_suppr)+" ?"
        msgbas="Cliquez sur suivant pour supprimer la session."
        page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

        page+="""
        <p class="supprsession1">
        Supprimer une session implique:<br>
        <span class='tab'>- Supprimer les paramètres associés<br>
        <span class='tab'>- Supprimer l'ensemble des données associés<br>
        <span class='tab'>- L'impossibilité d'annuler l'action<br>

        </p>
        """

        page+="""
        <p class="supprsession2">
        Réécrivez le nom d'utilisateur pour confirmer la suppression:
        </p>

        <form action ="admin_modif_session_sauvegarder" method="post">
            <div style="position:absolute; top:190px; left:300px;">
                <input type="text" name="conf_suppr_user" id="utilisateur" size="16"> <!--Emplacement nom utilisateur-->
            </div>
                <input name="afficher" type="hidden" value='supprsession_fin'>
                <input class="bouton3b" type="submit" value="   Suivant >   ">\n <!--Renvoi le formulaire-->
        </form>
        """


        page+="""
        <form action="admin_supprsession" method="get">
        <input name="fermer" type="hidden" value='controle_utilisateur?acces=parametre_admin'>
        <input class="bouton3a" type="submit" value="  < Précédent  ">
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Annuler    ">
        </form>
        """

        return page

    elif afficher=='supprsession_fin':
        #Affichage de la page de confirmation de la suppression de la session.

        #On souhaite afficher le nom de la session qui vient d'être supprimé.
        #On l'importe donc
        if 'nom_session_a_suppr' in flask.session:
            nom_session_a_suppr=flask.session['nom_session_a_suppr']
        else:
            #Si la variable n'existe pas... On affiche "missingno" à cause
            #du fait qu'il manque la variable.
            #Et pour éviter un plantage.
            nom_session_a_suppr='missingno'

        titre="Administration des sessions"
        info="Suppression d'une session utilisateur."
        description="La suppression de la session "+str(nom_session_a_suppr)+" s'est achevé avec succès !"
        img="valider.png"
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

        page+="""
        <form action="fermeture_fenetre" target="_parent" method="get">
        <input name="fermer" type="hidden" value='controle_utilisateur?acces=parametre_admin'>
        <input class="bouton3b" type="submit" value="    Fermer    ">
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Retour    ">
        </form>
        """
        connexion.close()
        page+=basdepage
        return page

    elif afficher=='marchepas':
        #Message d'erreur
        titre="Administration des sessions"
        info="Suppression d'une session utilisateur."
        description="Une erreur est survenue, Ferry 2000 n'a pas pu supprimer la session."
        img="Error.png"
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

        page+="""
        <form action="fermeture_fenetre" target="_parent" method="get">
        <input name="fermer" type="hidden" value='controle_utilisateur?acces=parametre_admin'>
        <input class="bouton3b" type="submit" value="    Fermer    ">
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Retour    ">
        </form>
        """

        connexion.close()
        page+=basdepage
        return page



    else:
        #Affichage de la première page, où on demande de sélectionner
        #la session d'utilisateur a supprimer.

        #Redirection:
        #    admin_modif_session_sauvegarder → afficher=suppr_session2

        titre="Administration des sessions"
        info="Suppression d'une session utilisateur"
        img="change_users.png"
        description="Sélectionner la session à supprimer."
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

        page+="""
        <form action ="admin_modif_session_sauvegarder" method="post">
            <div style="position:absolute; top:170px; left:370px">
                <label for="utilisateur" class="connexion" title="Veuillez saisir votre nom d'utilisateur">Utilisateur:</label>
                <div style="position:relative; right:130px; bottom:20px;">
                <select name="nom_session_a_suppr" id="utilisateur">
        """
        connexion = sqlite3.connect("Ferry2000.db")
        liste_session=list(connexion.execute("SELECT nom,type FROM utilisateur"))
        connexion.close()
        for nom_session in liste_session:
            if nom_session[1]!=2:
                page+="<option value='"+str(nom_session[0])+"'>"+str(nom_session[0])+"</option>"

        page+="""
                </select>
                </div>


                <input name="afficher" type="hidden" value='supprsession_2'>
            </div>
            <input class="bouton3b" type="submit" value="   Suivant >   ">\n <!--Renvoi le formulaire-->
        </form>

        <form action="parametre_admin" method="post">
        <input class="bouton3a" type="submit" value="  < Précédent  " disabled>\n
        </form>

        <form action="parametre_admin" method="post">
        <input name="utilisateur" type="hidden" value='"""+str(flask.session["admin_nom"])+"""'>
        <input name="mdp" type="hidden" value='"""+str(flask.session["admin_mdp"])+"""'>
        <input class="bouton3c" type="submit" value="    Annuler    ">\n
        </form>
        """
        connexion.close()
        page+=basdepage
        return page


#@app.route('/admin_modif_session_sauvegarder', methods = ['POST']) # Bureau Ferry 2000
def admin_modif_session_sauvegarder():
    #Enregistre les paramètres administrateurs si un formulaire est reçus.
    #Elle permet d'éviter d'afficher un message d'erreur correspondant aux pages
    #"parametre_graphique", mais joue le même rôle que parametre_sauvegarder.
    #
    #Cependant, il peut aussi jouer le rôle de redirecteur, tout en sauvegardant
    #quelques informations.


    connexion = sqlite3.connect("Ferry2000.db")
    page=morceau_entete
    page+="""<link rel="stylesheet" href="static/parametres.css" type="text/css">"""


    #On vérifie que l'utilisateur est toujours connecté aux paramètres en tant
    #qu'administrateur.
    #Remarque: lorsque les paramètres d'administration sont fermés, les cookies
    #concernés sont supprimés.
    if "admin_nom" in flask.session and "admin_mdp" in flask.session:
        verif_admin=list(connexion.execute("SELECT nom,mdp FROM utilisateur WHERE type==2"))[0]
        if flask.session["admin_nom"]!=verif_admin[0] or flask.session["admin_mdp"]!=verif_admin[1]: ############################# A REMPLIR
            description="Une erreur est survenue, les identifiants stockés en mémoire ne correspondent pas."
            msgbas="Cliquez sur retour pour vous connecter."
            page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

            page+="""
            </head><body>
            <form action="controle_utilisateur" method="get">
            <input name="acces" type="hidden" value='parametre_admin'>
            <input class="bouton3c" type="submit" value="    Retour     ">\n
            </form>
            """
            connexion.close()
            page+=basdepage
            return page
    else:
        description="Une erreur est survenue, vous devez vous connecter en tant qu'administrateur pour poursuivre."
        msgbas="Cliquez sur retour pour vous connecter."
        page+=flask.render_template("creersession.html",description=description,msgbas=msgbas)

        page+="""
        </head><body>
        <form action="controle_utilisateur" method="get">
        <input name="acces" type="hidden" value='parametre_admin'>
        <input class="bouton3c" type="submit" value="    Retour     ">\n
        </form>
        """
        connexion.close()
        page+=basdepage
        return page

    ############

    resultat = flask.request.form

    afficher = resultat.get('afficher',"")

    ############################
    #Admin créer session
    new_user = resultat.get('new_user',"")
    new_mdp = resultat.get('new_mdp',"")
    new_mdp_conf = resultat.get('new_mdp_conf',"")

    creersession_WP = resultat.get('creersession_WP',"")
    liste_WP=["WP_default.png","WP_E2000.png","WP_lycee.jpg","WP_linuxmint.jpg","WP_windows.jpg","WP_windows10.gif","WP_chambre.gif","WP_sonic.jpg","WP_sonicXP.gif","WP_pokésoft98.png","WP_pokésoft7.png","WP_minecraft.png","WP_art.png","WP_gobou.jpg","WP_marissonlegrand.jpg"]

    liste_police=["windowsfont","ComicSansMS", "Arial", "TimesNewRoman", "Impact", "Ubuntu", "NiseSegaSonic", "HyliaSerifBeta", "Ketchum"]
    themes_c1 = resultat.get('themes_c1',"")
    themes_c2 = resultat.get('themes_c2',"")
    themes_titre = resultat.get('themes_titre',"")
    themes_opa = resultat.get('themes_fondu',"")
    themes_police = resultat.get('themes_police',"")

    SCR = resultat.get('SCR',"")
    liste_scr=["3dmaze.gif","nyancat.gif","retrowave.gif","windows.gif","windows2.gif","flowerbox.gif","pokemon.gif","sega.gif"]

    ############################
    #Admin modif session
    modif_user = resultat.get('modif_user',"")

    changer_user = resultat.get('changer_user','')
    changer_mdp = resultat.get('changer_mdp','')
    changer_mdp_conf = resultat.get('changer_mdp_conf','')

    message_a_afficher=0

    ############################
    #Admin suppression de session
    nom_session_a_suppr= resultat.get('nom_session_a_suppr',"")
    conf_suppr_user=resultat.get('conf_suppr_user',"")


    ##########################################################################
    #VERIFICATION QU'AUCUN CARACTERE NE PEUT DERANGER                        #
    ##########################################################################


    #---------//    ADMIN CREER SESSION: IDENT  //-----//                      CREER SESSION: THEMES                       //--//                MODIF SESSION              //---//           SUPPRIMER SESSION            //----
    if "'" in (new_user or new_mdp or new_mdp_conf or themes_c1 or themes_c2 or themes_titre or themes_opa or themes_police or changer_user or changer_mdp or changer_mdp_conf or nom_session_a_suppr or conf_suppr_user):
        #Il n'est pas possible d'utiliser ces caractères, puisqu'ils
        #pourraient causer des soucis avec la base de donnée, ou certains
        #formulaire.

        #On pourrait faire une convertion, mais vu qu'on utilise très
        #régulièrement les identifiants de connexion, cela deviendrait
        #assez compliqué.

        img="Error.png"
        description="""Erreur: le caractère ' n'est pas accepté."""
        titre="Administration des sessions"
        info="Echec de l'exécution de l'action demandée."
        page+="""
        <div class="connexion">
        <form action ="javascript:history.go(-1)" method="get">
            <input name="acces" type="hidden" value='parametre_session'>
            <input class="bouton1" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
        </form>
        </div>
        """
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

        page+=basdepage
        connexion.close()
        return page







    ##########################################################################
    ##########################################################################


    if afficher=="supprsession_2":
        flask.session['nom_session_a_suppr']=nom_session_a_suppr
        page+="""
        <meta http-equiv="refresh" content="0.1; URL=admin_supprsession?afficher=supprsession_2">
        </head><body>
        """
        page+=basdepage
        connexion.close()
        return page

    elif afficher=="supprsession_fin":
        etatadmin=list(connexion.execute("SELECT COUNT(nom) FROM utilisateur WHERE type!=2 AND nom=='"+str(flask.session['nom_session_a_suppr'])+"'"))[0][0]

        if etatadmin==1 and flask.session['nom_session_a_suppr']==conf_suppr_user:
            connexion.execute("DELETE FROM utilisateur WHERE nom=='"+str(conf_suppr_user)+"'")
            connexion.execute("DELETE FROM documents WHERE user_doc=='"+str(conf_suppr_user)+"'")
            connexion.commit()
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_supprsession?afficher=supprsession_fin">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page
        else:
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_supprsession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page


    elif afficher=="modifsession_2":
        existence=list(connexion.execute("SELECT COUNT(nom) FROM utilisateur WHERE nom=='"+str(modif_user)+"'"))[0][0]

        if existence==1:
            flask.session['admin_modif_user']=modif_user
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_modifsession?afficher=modifsession_2">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page
        else:
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_modifsession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page

    elif afficher=="modifsession_fin":
        if changer_user=='' and (changer_mdp=='' and (changer_mdp==changer_mdp_conf)):
            """
            Situation où toute les entrées sont vide.
            """
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_modifsession?afficher=modifsession_2">
            </head><body>
            """

            connexion.close()
            page+=basdepage
            return page

        if changer_mdp==changer_mdp_conf and changer_mdp!='' and len(changer_mdp)<=30:
            connexion.execute("UPDATE utilisateur SET mdp='"+str(changer_mdp)+"' WHERE nom=='"+str(flask.session['admin_modif_user'])+"'")
            connexion.commit()
            message_a_afficher+=1


        if changer_user!='' and len(changer_user)<=15:
            dejautiliser=list(connexion.execute("SELECT COUNT(nom) FROM utilisateur WHERE nom=='"+str(changer_user)+"'"))[0][0]
            if dejautiliser==0:
                connexion.execute("UPDATE utilisateur SET nom='"+str(changer_user)+"' WHERE nom=='"+str(flask.session['admin_modif_user'])+"'")
                connexion.execute("UPDATE documents SET user_doc='"+str(changer_user)+"' WHERE user_doc=='"+str(flask.session['admin_modif_user'])+"'")
                connexion.commit()
                message_a_afficher+=2
                
                #Rafraichissement des cookies uniquement si la session utilisée est
                #concernée par la modification.
                
                if flask.session['utilisateur']==flask.session['admin_modif_user']:
                    flask.session['utilisateur']=str(changer_user)

        page+="""
        <meta http-equiv="refresh" content='0.1; URL=admin_modifsession?afficher=modifsession_fin&message="""+str(message_a_afficher)+"""'>
        </head><body>
        """
        connexion.close()
        page+=basdepage
        return page

    elif afficher=="creersession_2":
        if new_user!="" and new_mdp==new_mdp_conf and new_mdp!="":
            dejautiliser=list(connexion.execute("SELECT COUNT(nom) FROM utilisateur WHERE nom=='"+str(new_user)+"'"))[0][0]
            if (len(new_user)<=15 and len(new_mdp)<=30) and dejautiliser==0:

                requetestab=flask.session["requetes"]
                requetestab[0]=new_user
                requetestab[1]="INSERT INTO utilisateur VALUES ('"+str(new_user)+"','"+str(new_mdp)+"',0,-1,-1,'WP_E2000.png','flowerbox.gif','#191970','#87ceeb','1.0','#ffffff','windowsfont','nom_doc DESC')"
                flask.session["requetes"]=requetestab
                page+="""
                <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=creersession_2">
                </head><body>
                """
                page+=basdepage
                connexion.close()
                return page
            else:
                page+="""
                <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
                </head><body>
                """
                page+=basdepage
                connexion.close()
                return page
        else:
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page
    elif afficher=='creersession_3':
        if creersession_WP in liste_WP:
            requetestab=flask.session["requetes"]
            requetestab[2]="UPDATE utilisateur SET wallpaper='"+str(creersession_WP)+"' WHERE nom=='"+str(requetestab[0])+"'"
            flask.session["requetes"]=requetestab

            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=creersession_3">

            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page
        else:
            requetestab=flask.session["requetes"]
            requetestab[2]="UPDATE utilisateur SET wallpaper='E2000.png' WHERE nom=='"+str(requetestab[0])+"'"
            flask.session["requetes"]=requetestab
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page

    elif afficher=='creersession_4' and (themes_c1 or themes_c2 or themes_titre or themes_opa or themes_police)!="":
        if themes_c1=="" or len(themes_c1)!=7:
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page

        if themes_c2=="" or len(themes_c2)!=7:
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page

        if themes_titre=="" or len(themes_titre)!=7:
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page

        if themes_opa=="" or (int(themes_opa)>100 or int(themes_opa)<0):
            #On est pas censer convertir le texte en nombre, puisque l'utilisateur
            #pourrait trafiquer le formulaire pour envoyer des lettres.
            #Dans une utilisation normal, la conversion ne pose pas de problème.
            #Malgré cette connaissance de cause, on va ne pas vérifier l'entrée.
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page
        else:
            themes_opa=str(int(themes_opa)/100)

        if themes_police=="" or themes_police not in liste_police:
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page
        requetestab=flask.session["requetes"]
        requetestab[3]="UPDATE utilisateur SET theme_c1='"+themes_c1+"',theme_c2='"+themes_c2+"',theme_titre='"+themes_titre+"',theme_opa='"+themes_opa+"',theme_police='"+themes_police+"' WHERE nom=='"+str(requetestab[0])+"'"
        flask.session["requetes"]=requetestab
        page+="""
        <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=creersession_4">
        </head><body>
        """
        page+=basdepage
        connexion.close()
        return page
    elif afficher=='creersession_fin':
        if SCR in liste_scr:
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=creersession_fin">

            </head><body>
            """
            requetestab=flask.session["requetes"]
            requetestab[4]="UPDATE utilisateur SET screensaver='"+str(SCR)+"' WHERE nom='"+str(requetestab[0])+"'"
            flask.session["requetes"]=requetestab
            page+=basdepage
            connexion.close()
            return page
        else:
            page+="""
            <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
            </head><body>
            """
            page+=basdepage
            connexion.close()
            return page

    page+="""
    <meta http-equiv="refresh" content="0.1; URL=admin_creersession?afficher=marchepas">
    </head><body>
    """
    page+=basdepage
    connexion.close()
    return page
