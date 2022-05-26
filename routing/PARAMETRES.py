# -*- coding: utf-8 -*-
"""
Created on Sun May  1 20:46:18 2022

@author: Matthieu
"""

import flask
import sqlite3
import random
from time import *
from Plugins_E2000 import entete, basdepage, morceau_entete, entete_parametre, interface, demarrer_on, demarrer_off, erreur_12, erreur_2a, erreur_2b, popup_info

app = flask.Flask(__name__) # Création de l'application

#@app.route('/parametres', methods = ['GET']) # Bureau Ferry 2000
def parametres():
    page=entete

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

    #On affiche simplement le Panneau de configuration

    page+="""
    <img class="control_pannel" src="static/images/system/parametres/control_pannel.png" alt="Panneau de configuration">
    <h1 class="explorateur">Panneau de<br> configuration</h1>
    <p class="explorateur">Utiliser les paramètres du Panneau<br>de configuration pour personnaliser<br>l'ordinateur.</p>
    <p class="addresse">Panneau de configuration</p>
    """

    page+="""
    <div style="position: absolute; top:90px; left:280px">
        <a href="ouverture_fenetre?ouvrir=controle_utilisateur?acces=parametre_session" target="_parent" onmouseover="session.src='static/images/system/icons/parametre_session_on.png'" onmouseout="session.src='static/images/system/icons/parametre_session.png'">
            <img class="fichiers" id="session" src="static/images/system/icons/parametre_session.png" alt="Paramètre de la session">
        </a>

        <a href="ouverture_fenetre?ouvrir=parametre_graphique" target="_parent" onmouseover="graphique.src='static/images/system/icons/parametre_graphique_on.png'" onmouseout="graphique.src='static/images/system/icons/parametre_graphique.png'">
            <img class="fichiers" id="graphique" src="static/images/system/icons/parametre_graphique.png" alt="Paramètre graphique">
        </a>

        <a href="ouverture_fenetre?ouvrir=controle_utilisateur?acces=parametre_admin" target="_parent" onmouseover="admin.src='static/images/system/icons/msagent-4_on.png'" onmouseout="admin.src='static/images/system/icons/msagent-4.png'">
            <img class="fichiers" id="admin" src="static/images/system/icons/msagent-4.png" alt="Paramètre d'administration'">
        </a>

        <a href="ouverture_fenetre?ouvrir=parametre_dossiers" target="_parent" onmouseover="dossier.src='static/images/system/icons/parametre_dossier_on.png'" onmouseout="dossier.src='static/images/system/icons/parametre_dossier.png'">
            <img class="fichiers" id="dossier" src="static/images/system/icons/parametre_dossier.png" alt="Paramètre des documents">
        </a>
    </div>

    <div style="position: absolute; top:130px; left:255px;">
        <p class="fichiers">Paramètre de la session</p>
        <p class="fichiers">Paramètre graphique</p>
        <p class="fichiers">Paramètre d'administration</p>
        <p class="fichiers">Paramètre des dossiers</p>
    </div>
    """

    page+=basdepage
    return page


#@app.route('/parametre_session', methods = ['POST'])
def parametre_session():
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

    resultat = flask.request.form
    utilisateur = resultat.get('utilisateur',"")
    mdp = resultat.get('mdp',"")
    changer_user = resultat.get('changer_user',"")
    changer_mdp = resultat.get('changer_mdp',"")
    changer_mdp_conf = resultat.get('changer_mdp_conf',"")


    titre="Modification des informations de sessions"
    info="Vous pouvez modifier votre nom d'utilisater ainsi que votre mot de passe."

    connexion = sqlite3.connect("Ferry2000.db")
    requete=list(connexion.execute("SELECT nom,mdp,MAX(jeton) FROM utilisateur"))[0]
    connexion.close()

    if requete[0]==utilisateur and requete[1]==mdp and (changer_user=="" and changer_mdp=="" and changer_user==""):
        #Situation où l'utilisateur ne donne aucune information à modifier.
        #Soit car il vient tout juste d'arrivé sur cette page, et que
        #précédemment il était sur la page de contrôle d'utilisateur.

        #Soit car il n'a pas rempli les formulaires de cette page précédemment,
        #et alors cette page se recharge.

        #Dans tout les cas, on vérifie que l'utilisateur connecté est bien
        #le propriétaire de la session.


        img="parametre_session.png"
        description="Attention: veuillez intéragir uniquement avec cette fenêtre au risque de devoir vous reconnecter. Entrez uniquement les informations que vous souhaitez modifier."

        page+="""
            <div class="connexion">
            <form action ="/parametre_session" method="post">

            <br>
            <label for="changer_user" class="connexion" title="Veuillez saisir votre nouveau nom d'utilisateur">Nouveau nom:</label>
            <input class="connexion1" type="text" maxlength="15" name="changer_user" id="changer_user" size="32"> <!--Emplacement nom utilisateur-->
            <br><br>
            <label for="changer_mdp" class="connexion" title="Veuillez saisir votre nouveau mot de passe">Nouveau mot de passe:</label>
            <input class="connexion2" type="password" maxlength="30" name="changer_mdp" id="changer_mdp" size="32"> <!--Emplacement nom utilisateur-->
            <br><br>
            <label for="changer_mdp_conf" class="connexion" title="Veuillez saisir votre nouveau mot de passe de nouveau">Confirmer le mot de passe:</label>
            <input class="connexion3" type="password" maxlength="30" name="changer_mdp_conf" id="changer_mdp_conf" size="32"> <!--Emplacement nom utilisateur-->


            <input class="bouton1" type="submit" value="          OK          ">\n <!--Renvoi le formulaire-->

            <input name="utilisateur" type="hidden" value='"""+utilisateur+"""'>
            <input name="mdp" type="hidden" value='"""+mdp+"""'>

            </form>
            </div>
        """
    elif changer_mdp!=changer_mdp_conf:
        #Cas où la confirmation du mot de passe ne correspond pas.
        #Il n'y a alors aucune modification de la base de donnée, même pour le
        #nom d'utilisateur.


        img="Error.png"
        description="Le mot de passe et sa confirmation ne correspond pas. Il n'y a eu aucune modification sur votre session, vous pouvez recommencer."
        page+="""
        <div class="connexion">
        <form action ="/parametre_session" method="post">
            <input name="utilisateur" type="hidden" value='"""+utilisateur+"""'>
            <input name="mdp" type="hidden" value='"""+mdp+"""'>
            <input class="bouton1" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
        </form>
        </div>
        """
    elif changer_mdp==changer_mdp_conf and (changer_mdp!="" or changer_user!=""):
        #Dans cette situation, les formulaires pour modifier la session ont été
        #bien rempli.
        #On peut donc modifier les informations de la session.


        message=[]

        if "'" in (changer_mdp or changer_user):
            #Il n'est pas possible d'utiliser ces caractères, puisqu'ils
            #pourraient causer des soucis avec la base de donnée, ou certains
            #formulaire.

            #On pourrait faire une convertion, mais vu qu'on utilise très
            #régulièrement les identifiants de connexion, cela deviendrait
            #assez compliqué.

            img="Error.png"
            description="""Erreur: le caractère ' n'est pas pas acceptés."""
            page+="""
                <div class="connexion">
                <form action ="controle_utilisateur" method="get">
                <input name="acces" type="hidden" value='parametre_session'>
                <input class="bouton1" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
                </form>
                </div>
            """
            page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

            page+=basdepage
            connexion.close()
            return page


        if changer_user!="":
            connexion = sqlite3.connect("Ferry2000.db")
            dejautiliser=list(connexion.execute("SELECT COUNT(nom) FROM utilisateur WHERE nom=='"+str(changer_user)+"'"))[0][0]
            connexion.close()


            if dejautiliser!=0 or (len(changer_user)>15 or len(changer_user)<=0): #Impossible de modifier le nom d'utilisateur
                #Si le nouveau nom est déjà utilisé, ou s'il y a plus de 15 caractères.
                #Remarque: le "len(changer_user)<=0" peut-être facultatif, mais ça présence ne change pas grand chose.

                img="Error.png"
                description="Impossible de changer le nom de session. Soit il est déjà utilisé par un autre utilisateur, soit vous avez dépassé la limite des 15 caractères."
                page+="""
                <div class="connexion">
                <form action ="controle_utilisateur" method="get">
                <input name="acces" type="hidden" value='parametre_session'>
                <input class="bouton1" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
                </form>
                </div>
                """
                page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

                page+=basdepage
                connexion.close()
                return page


            else: #Modification du nom d'utilisateur
                #Les paramètres indiquer par l'utilisateur sont valides

                #On met à jour tout élément ayant un lien de près ou de loin
                #avec l'utilisateur.
                connexion = sqlite3.connect("Ferry2000.db")
                connexion.execute("UPDATE documents SET user_doc='"+str(changer_user)+"' WHERE user_doc=='"+str(utilisateur)+"'")
                connexion.execute("UPDATE utilisateur SET nom='"+str(changer_user)+"' WHERE nom=='"+str(utilisateur)+"'")
                connexion.commit()
                connexion.close()
                flask.session['utilisateur']=str(changer_user)
                message.append(True)

        else: #L'utilisateur n'a pas demandé à modifier le nom de session
            message.append(None)

        if changer_mdp!="":
            if len(changer_mdp)>0 and len(changer_mdp)<=30:
                #Si le mot de passe fait bien au maximum 30 caractères, alors
                #on valide le changement.
                utilisateur=flask.session['utilisateur']
                connexion = sqlite3.connect("Ferry2000.db")
                connexion.execute("UPDATE utilisateur SET mdp='"+str(changer_mdp)+"' WHERE nom=='"+str(utilisateur)+"'")
                connexion.commit()
                connexion.close()
                message.append(True)
            else:
                #Sinon, les paramètres entrées ne sont pas valide

                img="Error.png"
                description="Impossible de changer mot de passe, vous avez dépassé la limite des 30 caractères."
                page+="""
                <div class="connexion">
                <form action ="controle_utilisateur" method="get">
                <input name="acces" type="hidden" value='parametre_session'>
                <input class="bouton1" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
                </form>
                </div>
                """
                page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

                page+=basdepage
                connexion.close()
                return page
        else:
            #Les cases n'ont pas été remplis, il n'y a aucun changement.
            message.append(False)

        connexion = sqlite3.connect("Ferry2000.db")
        connexion.commit()
        connexion.close()
        if message[0]==message[1] and message[0]==True:
            img="tools.png"
            description="Le nom d'utilisateur et le mot de passe de la session ont été modifié."
        elif message[0]==message[1] and (message[0]==False or message[0]==None):
            img="Error.png"
            description="Une erreur est survenue, il n'y a eu aucune modification."
        elif message[0]==True and (message[1]==False or message[1]==None):
            img="tools.png"
            description="Le nom d'utilisateur de la session a été modifié."
        elif message[1]==True and (message[0]==False or message[0]==None):
            img="tools.png"
            description="Le mot de passe de la session a été modifié."
        else:
            img="Error.png"
            description="Une erreur est survenue, veuillez recommencer"
        page+="""
        <div class="connexion">
        <form action ="fermeture_fenetre" target="_parent" method="get">
            <input name="fermer" type="hidden" value='controle_utilisateur?acces=parametre_session'>
            <input class="bouton1" type="submit" value="        Fermer        ">\n <!--Renvoi le formulaire-->
        </form>
        </div>
        """




    else:
        #Situation où les informations envoyés par l'utilisateur ne
        #correspondent pas aux informations attendus par le système.

        img="Error.png"
        description="Une erreur est survenu, les informations entrées ne correspondent pas."
        page+="""
        <div class="connexion">
        <form action ="controle_utilisateur" method="get">
            <input name="acces" type="hidden" value='parametre_session'>
            <input class="bouton1" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
        </form>
        </div>
        """



    page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

    page+=basdepage
    connexion.close()
    return page

#@app.route('/parametre_graphique', methods = ['GET'])
def parametre_graphique():
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
    titre="Modification des paramètres graphique de votre session"
    info="Vous pouvez modifier votre fond d'écran, le thème ainsi que l'écran de veille de la session."

    resultat = flask.request.args
    parametre = resultat.get('parametre',"None")

    if parametre=="wallpaper":
        #Si l'utilisateut souhaite modifier sont fond d'écran.
        #Génère le menu adéquat

        description="Sélectionnez le fond d'écran que vous souhaitez mettre à votre session."
        img="monitor_windows.png"
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)
        page+="""<div style="position: absolute; top:150px; left:186px; width:400px;">"""
        style1="position: absolute; top:164px; left:181px; width:400px;"
        page+=flask.render_template("parametre_wallpaper.html",lien1='parametre_sauvegarder',name1='WP',style1=style1)

        page+="""
        <input class="bouton2a" type="submit" value="     Enregistrer      ">
        </div>
        </form>
        """

        page+="""
        <div style="position: absolute; top:164px; left:181px; width:400px;">
            <form action="/parametre_graphique" method="get">
                <input class="bouton2b" type="submit" value="        Retour        ">
            </form>
        </div>
        """

    elif parametre=="themes":
        #Si l'utilisateur souhaite modifier le thème de sa session.
        #Génère le menu adéquat
        connexion = sqlite3.connect("Ferry2000.db")
        themes=list(connexion.execute("SELECT theme_c1,theme_c2,theme_opa,theme_titre,theme_police FROM utilisateur WHERE nom=='"+str(flask.session['utilisateur'])+"'"))
        theme_c1,theme_c2,theme_opa, theme_titre, theme_police = themes[0][0],themes[0][1],themes[0][2],themes[0][3],themes[0][4]
        description="Personnalisez la barre des titres d'Ferry 2000."
        img="shell_window3.png"
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)
        page+=""""<form action ="parametre_sauvegarder" method="post">"""

        pos2="position:absolute; top:-16px; left:371px;"
        class_bt,nom_bt="bouton2a","     Enregistrer      "
        page+=flask.render_template("parametre_themes.html",pos1="themes",pos2=pos2,pos3="pointeur",pos4="police",class_bt=class_bt,nom_bt=nom_bt,theme_c1=str(theme_c1),theme_c2=str(theme_c2),theme_titre=str(theme_titre),theme_opa=str(float(theme_opa)*100),theme_police=str(theme_police))
        page+="""
        </form>
        <div style="position: absolute; top:164px; left:181px; width:400px;">
            <form action="/parametre_graphique" method="get">
                <input class="bouton2b" type="submit" value="        Retour        ">
            </form>
        </div>
        """
        connexion.close()
    elif parametre=="screensaver":
        #Si l'utilisateur souhaite modifier le l'écran de veille de sa session.
        #Génère le menu adéquat

        description="Sélectionnez l'écran de veille qui s'affichera au bout de 15 minutes pour votre session."
        img="screensaver.png"
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)
        style1="position: absolute; top:150px; left:186px; width:400px;"
        style2="position: absolute; top:164px; left:181px; width:400px;"
        action="/parametre_sauvegarder"
        page+=flask.render_template("parametre_scr.html",style1=style1,style2=style2,action=action)
        page+="""
                <input class="bouton2a" type="submit" value="     Enregistrer      ">
            </div>
        </form>
        <div style="position: absolute; top:164px; left:181px; width:400px;">
            <form action="/parametre_graphique" method="get">
                <input class="bouton2b" type="submit" value="        Retour        ">
            </form>
        </div>
        """

    elif parametre=="confirmation_camarche":
        #Message de confirmation que le changement à fonctionné

        description="Votre modification a bien été prise en compte. Vous pouvez refermer cette fenêtre."
        img="valider.png"
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

        page+="""
        <div style="position: absolute; top:164px; left:181px; width:400px;">
            <form action ="fermeture_fenetre" target="_parent" method="get">
                <input name="fermer" type="hidden" value='parametre_graphique'>
                <input class="bouton2a" type="submit" value="        Fermer        ">\n <!--Renvoi le formulaire-->
            </form>
            <form action ="parametre_graphique" method="get">
                <input class="bouton2b" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
            </form>
        </div>
        """
    elif parametre=="confirmation_camarchepas":
        #Message de indiquant que le changement n'a pas fonctionné

        description="Une erreur est survenue. Impossible de prendre en compte votre modification. Vérifiez que votre choix est bien valide."
        img="no.png"
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

        page+="""
        <div style="position: absolute; top:164px; left:181px; width:400px;">
            <form action ="fermeture_fenetre" target="_parent" method="get">
                <input name="fermer" type="hidden" value='parametre_graphique'>
                <input class="bouton2a" type="submit" value="        Fermer        ">\n <!--Renvoi le formulaire-->
            </form>
            <form action ="parametre_graphique" method="get">
                <input class="bouton2b" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
            </form>
        </div>
        """
    else:
        #Sinon, aucune option ou message doit être affiché, donc on affiche le
        #menu principal des paramètres graphique.

        #Afin que l'utilisateur puisse faire le choix dans ce qu'il souhaite
        #modifier.

        description="Sélectionner l'option auquel vous souhaitez accéder."
        img="parametre_graphique2.png"

        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

        page+="""
        <div style="position: absolute; top:200px; right:35px">
        <a href="parametre_graphique?parametre=wallpaper" onmouseover="monitorw.src='static/images/system/icons/monitor_windows_on.png'" onmouseout="monitorw.src='static/images/system/icons/monitor_windows.png'">
        <img class="parametre_pos" id="monitorw" src="static/images/system/icons/monitor_windows.png" alt="Fond d'écran">
        </a>
        <a href="parametre_graphique?parametre=themes" onmouseover="themes.src='static/images/system/icons/shell_window3_on.png'" onmouseout="themes.src='static/images/system/icons/shell_window3.png'">
        <img class="parametre_pos" id="themes" src="static/images/system/icons/shell_window3.png" alt="Thèmes">
        </a>
        <a href="parametre_graphique?parametre=screensaver" onmouseover="screensaver.src='static/images/system/icons/screensaver_on.png'" onmouseout="screensaver.src='static/images/system/icons/screensaver.png'">
        <img class="parametre_pos" id="screensaver" src="static/images/system/icons/screensaver.png" alt="Ecran de veille">
        </a>
        </div>

        <div style="position: absolute; top:242px; left:230px;">
            <p class="parametre_pos">Fond d'écran</p>
            <p class="parametre_pos">Thèmes</p>
            <p class="parametre_pos">Ecran de veille</p>
        </div>


        """

    page+=basdepage

    connexion.close()
    return page

#@app.route('/parametre_dossiers', methods = ['GET'])
def parametre_dossiers():
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
    para_dossiers_ordre = resultat.get('para_dossiers_ordre',"")

    titre="Ordre des documents"
    info="Choisissez de quel manière apparaissent les documents"
    img="parametre_dossier.png"
    description="Sélectionner l'option d'ordre des documents qui vous convient"

    liste_options=["nom_doc ASC","nom_doc DESC","date_doc ASC","date_doc DESC","user_doc ASC","user_doc DESC"]


    #On vérifie l'authenticité du formulaire reçus.
    ##########################################################################
    if para_dossiers_ordre!="":
        if para_dossiers_ordre in liste_options:
            #MODIFICATION DES PARAMETRES
            ##################################################################

            img="valider.png"
            description="Le paramètre sélectionné a été enregistré."

            page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

            connexion = sqlite3.connect("Ferry2000.db")
            connexion.execute("UPDATE utilisateur SET ordre_docs='"+str(para_dossiers_ordre)+"' WHERE nom=='"+str(flask.session['utilisateur'])+"'")
            connexion.commit()
            connexion.close

            page+="""
            <div style="position: absolute; top:164px; left:181px; width:400px;">
                <form action ="fermeture_fenetre" target="_parent" method="get">
                    <input name="fermer" type="hidden" value='parametre_dossiers'>
                    <input class="bouton2a" type="submit" value="        Fermer        ">\n <!--Renvoi le formulaire-->
                </form>
                <form action ="parametre_dossiers" method="get">
                    <input class="bouton2b" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
                </form>
            </div>
            """

            page+=basdepage
            return page
        else:
            img="no.png"
            description="Le paramètre sélectionné n'est pas valide."

            page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)

            page+="""
            <div style="position: absolute; top:164px; left:181px; width:400px;">
                <form action ="fermeture_fenetre" target="_parent" method="get">
                    <input name="fermer" type="hidden" value='parametre_dossiers'>
                    <input class="bouton2a" type="submit" value="        Fermer        ">\n <!--Renvoi le formulaire-->
                </form>
                <form action ="parametre_dossiers" method="get">
                    <input class="bouton2b" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
                </form>
            </div>
            """

            page+=basdepage
            return page


    page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)
    #checked="checked"


    #CHARGEMENT DU PARAMETRE ACTUEL
    ##########################################################################

    connexion = sqlite3.connect("Ferry2000.db")
    cocher_par_defaut=list(connexion.execute("SELECT ordre_docs FROM utilisateur WHERE nom=='"+str(flask.session['utilisateur']+"'")))[0][0]
    connexion.close()

    c1,c2,c3,c4,c5,c6="","","","","",""

    if liste_options[0]==cocher_par_defaut:
        c1='checked="checked"'
    elif liste_options[1]==cocher_par_defaut:
        c2='checked="checked"'
    elif liste_options[2]==cocher_par_defaut:
        c3='checked="checked"'
    elif liste_options[4]==cocher_par_defaut:
        c5='checked="checked"'
    elif liste_options[5]==cocher_par_defaut:
        c6='checked="checked"'
    else:
        c4='checked="checked"'


    #AFFICHAGE DE LA PAGE DES PARAMETRES DES DOSSIERS
    ##########################################################################

    page+="""
    <form action ="/parametre_dossiers" method="GET">

        <div class="posform_para_dossiers1">
            <input name="para_dossiers_ordre" type="radio" value="nom_doc ASC" """+c1+""">
            <input name="para_dossiers_ordre" type="radio" value="nom_doc DESC" """+c2+""">
            <input name="para_dossiers_ordre" type="radio" value="date_doc ASC" """+c3+""">
            <input name="para_dossiers_ordre" type="radio" value="date_doc DESC" """+c4+""">
            <input name="para_dossiers_ordre" type="radio" value="user_doc ASC" """+c5+""">
            <input name="para_dossiers_ordre" type="radio" value="user_doc DESC" """+c6+""">

        </div>

        <div class="posform_para_dossiers2">
        <p class="pos_para_dossiers1">Nom des documents: ASCENDANT.</p>
        <p class="pos_para_dossiers1">Nom des documents: DESCENDANT.</p>
        <p class="pos_para_dossiers1">Date des documents: ASCENDANT.</p>
        <p class="pos_para_dossiers1">Date des documents: DESCENDANT.</p>
        <p class="pos_para_dossiers1">Créateur des documents: ASCENDANT.</p>
        <p class="pos_para_dossiers1">Créateur des documents: DESCENDANT.</p>
        </div>

        <div style="position: absolute; top:164px; left:181px; width:400px;">
            <input class="bouton2a" type="submit" value="     Enregistrer      ">
        </div>
    </form>

    <form action="/fermeture_fenetre" target="_parent" method="get">
        <input name="fermer" type="hidden" value='parametre_dossiers'>
        <div style="position: absolute; top:164px; left:181px; width:400px;">
            <input class="bouton2b" type="submit" value="        Fermer        ">
        </div>
    </form>
    """

    page+=basdepage
    return page

#@app.route('/parametre_sauvegarder', methods = ['POST'])
def parametre_sauvegarder():
    """
    Enregistre les paramètres utilisateurs si un formulaire est reçus.
    Les paramètres de la session n'ont aucun lien avec cette page en
    revanche.
    """
    connexion = sqlite3.connect("Ferry2000.db")
    page=morceau_entete
    resultat = flask.request.form
    WP = resultat.get('WP',"")

    liste_WP=["WP_default.png","WP_E2000.png","WP_lycee.jpg","WP_linuxmint.jpg","WP_windows.jpg","WP_windows10.gif","WP_chambre.gif","WP_sonic.jpg","WP_sonicXP.gif","WP_pokésoft98.png","WP_pokésoft7.png","WP_minecraft.png","WP_art.png","WP_gobou.jpg","WP_marissonlegrand.jpg"]
    liste_police=["windowsfont","ComicSansMS", "Arial", "TimesNewRoman", "Impact", "Ubuntu", "NiseSegaSonic", "HyliaSerifBeta", "Ketchum"]
    themes_c1 = resultat.get('themes_c1',"")
    themes_c2 = resultat.get('themes_c2',"")
    themes_titre = resultat.get('themes_titre',"")
    themes_opa = resultat.get('themes_fondu',"")
    themes_police = resultat.get('themes_police',"")

    SCR = resultat.get('SCR',"")
    liste_scr=["3dmaze.gif","nyancat.gif","retrowave.gif","windows.gif","windows2.gif","flowerbox.gif","pokemon.gif","sega.gif"]

    ##########################################################################
    #CHANGEMENT FOND D'ECRAN                                                 #
    ##########################################################################
    if WP in liste_WP:
        #Si la page a reçus un formulaire indiquant un changement de fond
        #d'écran (donc que WP ≠ "", et qu'il est valide).

        page+="""
        <meta http-equiv="refresh" content="0.1; URL=parametre_graphique?parametre=confirmation_camarche">

        </head><body>
        """
        connexion.execute("UPDATE utilisateur SET wallpaper='"+str(WP)+"' WHERE nom='"+str(flask.session['utilisateur'])+"'")
        connexion.commit()


    ##########################################################################
    #CHANGEMENT DU THEME DE LA SESSION                                       #
    ##########################################################################
    elif (themes_c1 or themes_c2 or themes_titre or themes_opa or themes_police)!="":
        #Si la page a reçus un formulaire indiquant un changement de theme
        #(donc que l'une des options n'est pas vide).
        page+="""
        <meta http-equiv="refresh" content="0.1; URL=parametre_graphique?parametre=confirmation_camarche">

        </head><body>
        """
        if themes_c1!="" and len(themes_c1)==7:
            #Couleur dégrader 1
            connexion.execute("UPDATE utilisateur SET theme_c1='"+str(themes_c1)+"' WHERE nom='"+str(flask.session['utilisateur'])+"'")
            connexion.commit()
        if themes_c2!="" and len(themes_c2)==7:
            #Couleur dégrader 2
            connexion.execute("UPDATE utilisateur SET theme_c2='"+str(themes_c2)+"' WHERE nom='"+str(flask.session['utilisateur'])+"'")
            connexion.commit()
        if themes_titre!="" and len(themes_titre)==7:
            #Couleur du titre
            connexion.execute("UPDATE utilisateur SET theme_titre='"+str(themes_titre)+"' WHERE nom='"+str(flask.session['utilisateur'])+"'")
            connexion.commit()
        if themes_opa!="":
            #On est pas censer convertir le texte en nombre, puisque l'utilisateur
            #pourrait trafiquer le formulaire pour envoyer des lettres.
            #Dans une utilisation normal, la conversion ne pose pas de problème.
            #Malgré ce risque, on va ne pas vérifier l'entrée.

            #Faire directement "themes_opa=int(themes_opa)" ne marche pas sur Firefox.
            #Par contre, sur d'autre navigateur si, comme paradoxalement Internet Explorer 11.
            #Pour palier à ce problème, et faire quand même une conversation, j'ai fais ça:
            themes_opa=int(str(themes_opa)[:len(themes_opa)-1])*10
            if themes_opa<=100 and themes_opa>=0:
                #Opaciter du fond de la barre des titres
                connexion.execute("UPDATE utilisateur SET theme_opa='"+str(themes_opa/100)+"' WHERE nom='"+str(flask.session['utilisateur'])+"'")
                connexion.commit()
        if themes_police!="" and themes_police in liste_police:
            #Police d'écriture
            connexion.execute("UPDATE utilisateur SET theme_police='"+str(themes_police)+"' WHERE nom='"+str(flask.session['utilisateur'])+"'")
            connexion.commit()


    ##########################################################################
    #CHANGEMENT DE L'ECRAN DE VEILLE                                       #
    ##########################################################################
    elif SCR in liste_scr:
        #Si la page a reçus un formulaire indiquant un changement d'écran de
        #veille (donc que SCR ≠ "", et qu'il est valide).
        page+="""
        <meta http-equiv="refresh" content="0.1; URL=parametre_graphique?parametre=confirmation_camarche">

        </head><body>
        """
        connexion.execute("UPDATE utilisateur SET screensaver='"+str(SCR)+"' WHERE nom='"+str(flask.session['utilisateur'])+"'")
        connexion.commit()

    else:
        page+="""
        <meta http-equiv="refresh" content="0.1; URL=parametre_graphique?parametre=confirmation_camarchepas">

        </head><body>
        """

    page+=basdepage
    connexion.close()
    return page

#@app.route('/parametre_admin', methods = ['POST']) # Bureau Ferry 2000
def parametre_admin():
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

    resultat = flask.request.form
    utilisateur = resultat.get('utilisateur',"")
    mdp = resultat.get('mdp',"")
    action = resultat.get('action',"")



    connexion = sqlite3.connect("Ferry2000.db")
    info_admin=list(connexion.execute("SELECT nom, mdp FROM utilisateur WHERE type==2"))[0]
    connexion.close()
    admin_nom=info_admin[0]
    admin_mdp=info_admin[1]

    titre="Administration des sessions"
    info="Vous pouvez créer de nouvelles sessions, les modifier ou encore les supprimer."
    img="msagent-4.png"
    description="Choisissez l'action que vous souhaitez faire."
    if utilisateur!=admin_nom or mdp!=admin_mdp:
        #Si les informations de connexion ne correspondent pas à ceux de la
        #session admin, alors il n'est pas possible d'ouvrir les paramètres
        #d'administration.

        #Remarque:  avant d'accéder à cette page, l'utilisateur a été redirigé
        #           vers la page d'authentification.

        img="Error.png"
        description="Les informations rentrées ne correspondent pas à la session Administrateur."
        page+="""
        <div class="connexion">
        <form action ="controle_utilisateur" method="get">
            <input name="acces" type="hidden" value='parametre_admin'>
            <input class="bouton1" type="submit" value="        Retour        ">\n <!--Renvoi le formulaire-->
        </form>
        </div>
        """
        page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)
        page+=basdepage
        connexion.close()
        return page

    #On stock en mémoire les informations pour la session administrateur.
    #C'est pour éviter de devoir s'assurer à chaque fois qu'on a bien transmis
    #le nom et le mot de passe à chaque envoie de formulaire.
    #Pour que ce soit plus simple à créer.

    #Cependant, mieux vaut éviter d'envoyer des informations aussi importante,
    #aussi régulièrement via internet. C'est sûrement plus sécurisé de stocker
    #ce type d'information en mémoire. Dans tous les cas, lorsque les
    #paramètres d'administration sont refermé, les variables sont réinitialisés.
    flask.session["admin_nom"]=admin_nom
    flask.session["admin_mdp"]=admin_mdp

    #REDIRECTION
    ##########################################################################
    #En fonction du bouton cliqué par l'utilisateur.
    if action=="    Créer une session    ":
        page+="""
        <script type="text/javascript">
        var delai=0; // Delai en secondes
        var url='admin_creersession'; // Url de destination
        setTimeout("window.location.href=url", delai + '000');
        </script>
        """
        page+=basdepage
        connexion.close()
        return page

    elif action=="  Modifier une session  ":
        page+="""
        <script type="text/javascript">
        var delai=0; // Delai en secondes
        var url='admin_modifsession'; // Url de destination
        setTimeout("window.location.href=url", delai + '000');
        </script>
        """
        page+=basdepage
        connexion.close()
        return page

    elif action=="Supprimer une session":
        page+="""
        <script type="text/javascript">
        var delai=0; // Delai en secondes
        var url='admin_supprsession'; // Url de destination
        setTimeout("window.location.href=url", delai + '000');
        </script>
        """
        page+=basdepage
        connexion.close()
        return page

    #AFFICHAGE PAR DEFAUT DE LA PAGE:

    page+="""

        <div class="admin">
            <p class="admin">Créer et personnaliser une nouvelle session</p>
            <p class="admin">Modifier une session déjà existente</p>
            <p class="admin">Supprimer définitivement l'intégralité d'une session</p>
        </div>

        <div class="admin">
            <form action ="parametre_admin" method="post">
                <input name="utilisateur" type="hidden" value="""+str(utilisateur)+""">
                <input name="mdp" type="hidden" value="""+str(mdp)+""">
                <input class="admin" type="submit" name="action" value="    Créer une session    ">
                <input class="admin" type="submit" name="action" value="  Modifier une session  ">
                <input class="admin" type="submit" name="action" value="Supprimer une session">
            </form>
        </div>


        <div class="connexion">
        <form action ="fermeture_fenetre" target="_parent" method="get">
            <input name="fermer" type="hidden" value='controle_utilisateur?acces=parametre_admin'>
            <input class="bouton1" type="submit" value="        Fermer        ">\n <!--Renvoi le formulaire-->
        </form>
        </div>
        """

    page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)
    page+=basdepage
    connexion.close()
    return page