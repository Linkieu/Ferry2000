# -*- coding: utf-8 -*-
"""
Created on Sun May  1 20:36:37 2022

@author: Matthieu
"""

import flask
import sqlite3
import random
from time import *
from Plugins_E2000 import entete, basdepage, morceau_entete, entete_parametre, interface, demarrer_on, demarrer_off, erreur_12, erreur_2a, erreur_2b, popup_info

app = flask.Flask(__name__) # Création de l'application


@app.route('/ferryword', methods = ['GET']) # Bureau Ferry 2000
def ferryword():
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

    #Initialisation des variable
    nom_doc="Document non enregistré" #Contiendra le nom du document en cours // Ou ce message si le document n'est pas enregistré.
    #texte=""
    icon="fichier.png" #Icone par défaut montrant l'état du document.


    resultat = flask.request.args

    #Si on a stocké le nom d'un document dans les cookies, on le récupère.
    if 'document' in flask.session:
        document = flask.session['document']

    #On récupère le nom de la session actuellement ouverte.
    utilisateur=flask.session['utilisateur']


    #En cas de sauvegarde ou de suppression du document
    save = resultat.get('save',"") #Action à faire


    texte = resultat.get('texte',"") #On récupère le texte du formulaire ou on l'initialise.
    #Lorsqu'on clique sur "enregistrer" on envoie un formulaire contenant le
    #texte écrit. Ce formulaire est reçus par la page ferryword.

    #Il y a donc 2 système pour charger le texte:
    #    - Soit via les cookies (ex: ouverture depuis Mes Documents)
    #    - Soit via les formulaires (ex: récupération du formulaire pour sauvegarder)


    if save=='True':
        #Si on souhaite sauvegarder le document, on affiche la fenêtre de
        #sauvegarde.

        #On stocke le texte dans les cookies, pour pouvoir le récupérer plus
        #tard.
        flask.session['FerryWord']=texte

        #Ouverture de la fenêtre de sauvegarde.
        page+="""
        <script type="text/javascript">
        var delai=0; // Delai en secondes
        var url='ouverture_fenetre?ouvrir=ew_sauvegarde&retour=2'; // Url de destination
        setTimeout("parent.document.location.href=url", delai + '000');
        </script>
        """
    elif save=='Suppr':
        #Ouverture de la fenêtre de suppression du document ouvert.
        page+="""
        <script type="text/javascript">
        var delai=0; // Delai en secondes
        var url='ouverture_fenetre?ouvrir=ew_supprimer&retour=2'; // Url de destination
        setTimeout("parent.document.location.href=url", delai + '000');
        </script>
        """

    """
    Rappel:
        proteger_doc=0 ► Modifiable, et accessible pour l'utilisateur
        proteger_doc=1 ► Finaliser, et accessible pour l'utilisateur
        proteger_doc=2 ► Modifiable, et accessible pour tous les utilisateurs
        proteger_doc=3 ► Faliser, et accessible pour tous les utilisateurs


    Ainsi, la suite du code va se structurer ainsi.

    Si "document" contient quelque chose:
        → Si proteger_doc == 1 ou 3
            ► Ouvre l'éditeur, sans la possibilité de le modifier.
        → Si proteher_doc == 0, 2 ou ""
            ► Ouvre l'éditeur, en prennant en compte des paramètres s'ils existent.
    """


    if 'document' in flask.session:
        connexion = sqlite3.connect("Ferry2000.db")
        #Si on a un document semblant être disponible dans les cookies, on le charge.
        info_doc=list(connexion.execute("SELECT nom_doc, user_doc, date_doc, proteger_doc, doc FROM documents JOIN utilisateur WHERE nom_doc=='"+str(document)+"'"))
        liste_admin=list(connexion.execute("SELECT nom FROM utilisateur WHERE type==2"))[0]
        connexion.close()

        #Si ce document peut être correctement pris en charge, alors on va le
        #charger et adapter Ferry Word à la situation.
        #Sinon, on ne le charge pas et on créer un document vierge.
        if info_doc!=[]:
            info_doc=info_doc[0]
            nom_doc,user_doc,date_doc,proteger_doc,texte2=info_doc[0],info_doc[1],info_doc[2],info_doc[3],info_doc[4]



            if texte=="":
                #Si on a pas précédemment chargé un texte, alors on charge
                #celui contenu dans la base de donnée.
                #Remarque:  Il y a toute les chances que la variable texte soit
                #           vide, mais par précaution, pour éviter qu'on remplace
                #           par mégarde un document en cours d'écriture.
                texte=texte2

                #On converti le texte pour qu'il soit présentable.
                #Cette conversion était dû pour éviter tout problème avec la
                #sauvegarde dans la base de donnée.
                texte=texte.replace("ऐ","'")
                texte=texte.replace('ऑ','"')
                texte=texte.replace("क","-")
                texte=texte.replace("ष","=")
                nom_doc=nom_doc.replace("ऐ","'")
                nom_doc=nom_doc.replace('ऑ','"')


            ##################################################################
            # LE DOCUMENT EST MODIFIABLE                                     #
            ##################################################################
            #Si l'utilisateur est le créateur du document, alors on l'ouvre.
            #Si l'utilisateur est un administrateur, alors on l'ouvre
            #Si le créateur a autorisé tous les utilisateurs à l'ouvrir, alors on l'ouvre.
            if (proteger_doc==0 and (user_doc==utilisateur or utilisateur in liste_admin)) or proteger_doc==2:
                icon="fichier_nonproteger.png"
                page+=flask.render_template("ferryword.html",nom_doc=nom_doc, texte=texte,icon=icon)

                #Seul le créateur ou l'administrateur possède la possibilité de
                #supprimer le document. Il est donc inutile de faire croire
                #à l'utilisateur, si ce n'est ni l'admin, ni le créateur, de lui
                #faire croire cette possibilité.
                if utilisateur in liste_admin or user_doc==utilisateur:
                    page+="""
                    <form action="ferryword" method="get">
                        <div style="position: absolute; top:5px; left: 160px;">
                            <input name="save" type="hidden" value='Suppr'>
                            <input type="submit" value="       Supprimer      ">
                        </div>
                    </form>
                    """
                else:
                    page+="""
                    <form action="" method="get">
                    <div style="position: absolute; top:5px; left: 160px;">
                    <input type="submit" value="       Supprimer      " disabled>
                    </div>
                    </form>
                    """
            ##################################################################
            ##################################################################




            ##################################################################
            # LE DOCUMENT N'EST PAS MODIFIABLE                               #
            ##################################################################
            #Si l'utilisateur est le créateur du document, alors on l'ouvre.
            #Si l'utilisateur est un administrateur, alors on l'ouvre
            #Si le créateur a autorisé tous les utilisateurs à l'ouvrir, alors on l'ouvre.
            elif (proteger_doc==1 and (user_doc==utilisateur or utilisateur in liste_admin)) or proteger_doc==3:
                icon="fichier_proteger.png"
                page+=flask.render_template("ferryword.html",nom_doc=nom_doc, texte=texte,icon=icon,parametre_input='disabled',parametre_input2='readonly')


                #Seul le créateur ou l'administrateur possède la possibilité de
                #supprimer le document. Il est donc inutile de faire croire
                #à l'utilisateur, si ce n'est ni l'admin, ni le créateur, de lui
                #faire croire cette possibilité.
                if utilisateur in liste_admin or user_doc==utilisateur:
                    page+="""
                    <form action="ferryword" method="get">
                    <div style="position: absolute; top:5px; left: 160px;">
                    <input name="save" type="hidden" value='Suppr'>
                    <input type="submit" value="       Supprimer      ">
                    </div>
                    </form>
                    """
                else:
                    page+="""
                    <form action="" method="get">
                    <div style="position: absolute; top:5px; left: 160px;">
                    <input type="submit" value="       Supprimer      " disabled>
                    </div>
                    </form>
                    """
            ##################################################################
            ##################################################################

            #Le document ne possède aucune information concernant sa protection.
            #Ou les valeurs enregistré ne sont pas valide.
            else:
                icon="erase_file-0.png"
                page+=flask.render_template("ferryword.html",nom_doc=nom_doc, texte=texte,icon=icon)

            ###########################################################################
            # EASTER EGG PAS TRES CACHER: The Ferry 2000 Product Team!             #
            ###########################################################################

            if nom_doc!="The Ferry 2000 Product Team!" and 'dejajouer_easteregg_EW' in flask.session:
                #Au cas où on ouvre le documents easter egg, et qu'on ouvre
                #ensuite un autre document, on efface le cookie afin d'éviter
                #que la musique de joue.
                del flask.session['dejajouer_easteregg_EW']

            page+=basdepage
            connexion.close()
            return page




    ###########################################################################
    # CREATION D'UN DOCUMENT VIERGE                                           #
    ###########################################################################

    if 'dejajouer_easteregg_EW' in flask.session:
        #Au cas où on ouvre le documents easter egg, et qu'on ouvre
        #ensuite un autre document, on efface le cookie afin d'éviter
        #que la musique de joue.
        del flask.session['dejajouer_easteregg_EW']


    flask.session['document']=""
    page+=flask.render_template("ferryword.html",nom_doc=nom_doc, texte=texte,icon=icon)
    page+="""
    <form action="" method="get">
    <div style="position: absolute; top:5px; left: 160px;">
    <input type="submit" value="       Supprimer      " disabled>
    </div>
    </form>
    """

    page+=basdepage
    connexion.close()
    return page


@app.route('/ew_supprimer', methods = ['GET']) # Bureau Ferry 2000
def ew_supprimer():
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

    #FENETRE POUR SUPPRIMER LE DOCUMENT OUVERT
    ##########################################################################


    resultat = flask.request.args
    save_nom_doc = resultat.get('save_doc_nom',"")
    #Remarque:  on utilise le nom de variable "save_nom_doc" bien que la
    #           fenêtre s'occupe d'une suppression.


    if 'document' in flask.session:
        nom_doc=flask.session['document']
    else:
        #Impossible de supprimer un document s'il n'est pas chargé au
        #préalable.
        page+="""
        <script type="text/javascript">
        var delai=0; // Delai en secondes
        var url='fermeture_fenetre?fermer=ew_supprimer'; // Url de destination
        setTimeout("document.location.href=url", delai + '000');
        </script>
        """


    if 'ferryword' not in flask.session['taskbar']:
        #On vérifie qu'Ferry Word soit bien ouvert pour afficher la page.
        #Car il est impossible de supprimer quelque chose sinon.
        #Vu qu'il supprime seulement les documents ouvert.

        page+="""
            <div class="ew_save_fond1">
            </div>
            <div class="ew_save_fond2">
            </div>
            <img class="barre2" src="static/images/system/barre.png" alt="barre">
            <img class="ew_save_clippyb" src="static/images/ferryword/clippy3.gif" alt="Clippy">
            <img class="ew_save_msgclippy" src="static/images/ferryword/message_clippy.png" alt="message de Clippy">
            <img class="ew_logoword" src="static/images/system/icons/word.png" alt="Logo Word">
            <h1 class="ew_save_titre"><b><i>Ferry Word n'est pas ouvert !</i></b></h1>

            <p class="ew_save_msgclippy">
            Il n'est pas possible d'effacer un document,
            s'il n'est pas déjà ouvert...<br>
            <br>
            Fermez cette fenêtre puis ouvrez le document avec Ferry Word pour supprimer celui-ci
            </p>


        <form action ="fermeture_fenetre" target="_parent" method="GET">
            <input name="fermer" type="hidden" value='ew_supprimer'>
            <input class="ew_save_fermer" type="submit" value="     Fermer     ">
        </form>
        """

        page+=basdepage
        return page


    if save_nom_doc!="":
        #Pour éviter tout problème avec la base de donnée, on converti le texte.
        save_nom_doc=save_nom_doc.replace("'","ऐ")
        save_nom_doc=save_nom_doc.replace('"','ऑ')

        connexion = sqlite3.connect("Ferry2000.db")
        compteadmin=list(connexion.execute("SELECT nom FROM utilisateur WHERE type==2"))[0]
        user_doc=list(connexion.execute("SELECT user_doc FROM documents WHERE nom_doc=='"+str(save_nom_doc)+"'"))
        connexion.close()



        if user_doc!=[]:
            user_doc=user_doc[0][0]

        #On vérifie que le document a supprimé a bien son nom chargé dans la
        #mémoire, et que l'utilisateur est autorisé à le supprimer.
        if save_nom_doc==flask.session['document'] and (flask.session['utilisateur']==user_doc or flask.session['utilisateur'] in compteadmin):
            connexion = sqlite3.connect("Ferry2000.db")
            connexion.execute("DELETE FROM documents WHERE nom_doc=='"+str(save_nom_doc)+"'")
            connexion.commit()
            connexion.close()

            save_nom_doc=save_nom_doc.replace("'","ऐ")
            save_nom_doc=save_nom_doc.replace('"','ऑ')

            #On affiche le message de confirmation
            page+="""
            <script type="text/javascript">
            var delai=0; // Delai en secondes
            var url='ew_confirm?nom_doc="""+str(save_nom_doc)+"""&afficher_msg_save=suppr_reussit'; // Url de destination
            setTimeout("document.location.href=url", delai + '000');
            </script>
            """
            page+=basdepage
            return page
        else:
            #Sinon, on affiche un message d'erreur.
            page+="""
            <script type="text/javascript">
            var delai=0; // Delai en secondes
            var url='ew_confirm?afficher_msg_save=suppr_echec'; // Url de destination
            setTimeout("document.location.href=url", delai + '000');
            </script>
            """
            page+=basdepage
            return page

    ##########################################################################
    #PAGE D'ACCUEIL POUR LA SUPPRESSION D'UN DOCUMENT.                       #
    ##########################################################################

    nom_doc=nom_doc.replace("ऐ","'")
    nom_doc=nom_doc.replace('ऑ','"')

    page+="""
    <div class="ew_save_fond1">
    </div>
    <div class="ew_save_fond2">
    </div>

    <h1 class="ew_save_titre"><b><i>Supprimer le document...</i></b></h1>
    <img class="ew_logoword" src="static/images/system/icons/word.png" alt="Logo Word">


    <p class="ew_nomtxt_entier">
    <u>Nom entier du document :</u><br>
    """+str(nom_doc)+"""
    </p>

    <p class="ew_emplacementtxt2">
    <b><u>Attention !</b></u><br>
    C'est une suppression définitive et irréversible.
    </p>

    <p class="ew_suppr_form1">Confirmation du nom :</p>
    <form action ="/ew_supprimer" method="GET">
        <input type="text" class="ew_supprform1" name="save_doc_nom" id="save_doc_nom" size="20" maxlength="30" placeholder="Document à supprimer">
        <div class="ew_form2">
        <input class="ew_save_envoie" type="submit" value="  Supprimer  ">
        </div>
    </form>

    <form action ="/fermeture_fenetre" target="_parent" method="GET">
        <div class="ew_form2">
            <input name="fermer" type="hidden" value='ew_supprimer'>
            <input class="ew_save_annuler" type="submit" value="    Annuler    ">
        </div>
    </form>
    <img class="barre2" src="static/images/system/barre.png" alt="barre">
    """


    page+=basdepage
    return page


@app.route('/ew_sauvegarde', methods = ['GET']) # Bureau Ferry 2000
def ew_sauvegarde():

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

    #FENETRE POUR ENREGISTRER LE DOCUMENT OUVERT
    ##########################################################################

    resultat = flask.request.args
    save_doc_protection = resultat.get('save_doc_protection',"")
    nom_doc = resultat.get('save_doc_nom',"")


    if 'ferryword' not in flask.session['taskbar']:
        #On vérifie qu'Ferry Word soit bien ouvert pour afficher la page.
        #Car il est impossible de sauvegarder quelque chose sinon.
        #Vu qu'il enregistre seulement le texte inscrit dans Ferry Word.

        page+="""
            <div class="ew_save_fond1">
            </div>
            <div class="ew_save_fond2">
            </div>
            <img class="barre2" src="static/images/system/barre.png" alt="barre">
            <img class="ew_save_clippyb" src="static/images/ferryword/clippy3.gif" alt="Clippy">
            <img class="ew_save_msgclippy" src="static/images/ferryword/message_clippy.png" alt="message de Clippy">
            <img class="ew_logoword" src="static/images/system/icons/word.png" alt="Logo Word">
            <h1 class="ew_save_titre"><b><i>Ferry Word n'est pas ouvert !</i></b></h1>

            <p class="ew_save_msgclippy">
            Il n'est pas possible d'enregistrer un document,
            s'il n'est pas déjà ouvert...<br>
            <br>
            Fermez cette fenêtre puis ouvrez Ferry Word pour enregistrer<br>
            un document.

        <form action ="fermeture_fenetre" target="_parent" method="GET">
            <input name="fermer" type="hidden" value='ew_sauvegarde'>
            <input class="ew_save_fermer" type="submit" value="     Fermer     ">
        </form>
        """

        page+=basdepage
        return page

    if nom_doc!="": #Si le document est bien nommé
        #On vérifie que le nom de document n'est pas déjà utilisé.
        connexion = sqlite3.connect("Ferry2000.db")

        #On protège notre texte contre l'injection SQL
        nom_doc=nom_doc.replace("'","ऐ")
        nom_doc=nom_doc.replace('"','ऑ')


        dejautiliser = list(connexion.execute("SELECT count(nom_doc) FROM documents WHERE nom_doc=='"+str(nom_doc)+"'"))[0][0]

        #Le nom de document est déjà utilisé
        if dejautiliser>0:
            #Nous allons différencier 2 cas:
            #   - Le document ayant le même nom, est celui qu'on vient de modifier et qu'on souhaite sauvegarder
            #   - Le document ayant le même nom n'a rien à voir avec celui d'ouvert.

            createur = list(connexion.execute("SELECT user_doc FROM documents WHERE nom_doc=='"+str(nom_doc)+"'"))[0][0]
            nom_admin = list(connexion.execute("SELECT nom FROM utilisateur WHERE type==2"))[0][0]

            #On vérifie que cela correspond à la première situation, et que
            #celui qui cherche à le remplacer est bien le créateur, ou un
            #administrateur.
            if (flask.session['utilisateur']==createur or flask.session['utilisateur'] in nom_admin) and str(nom_doc)==flask.session['document']:
                connexion.execute("DELETE FROM documents WHERE nom_doc=='"+str(nom_doc)+"'")
                connexion.commit()

            else:
                #Sinon, cas 2 (ou encore l'utilisateur ne peut pas remplacer le document)
                nom_doc=nom_doc.replace("'","ऐ")
                nom_doc=nom_doc.replace('"','ऑ')

                page+="""
                    <script type="text/javascript">
                    var delai=0; // Delai en secondes
                    var url='ew_confirm?nom_doc="""+str(nom_doc)+"""&afficher_msg_save=echec_dejautiliser'; // Url de destination
                    setTimeout("document.location.href=url", delai + '000');
                    </script>
                """

                connexion.close()
                page+=basdepage
                return page
    if save_doc_protection!="" and nom_doc!="":
        named_tuple = localtime() # get struct_time

        #Le nom du document est déjà associé à la variable nom_doc
        user_doc = flask.session['utilisateur']
        date_doc = strftime("%Y%m%d %H:%M", named_tuple)
        doc = flask.session['FerryWord']



        """
        Pour éviter l'injection SQL depuis le texte, on remplace les caractères
        problématique par des caractères très rarement utilisé.

        ' → ऐ
        " → ऑ
        - → क
        = → ष
        """
        doc=doc.replace("'","ऐ")
        doc=doc.replace('"','ऑ')
        doc=doc.replace("-","क")
        doc=doc.replace("=","ष")

        nom_doc=nom_doc.replace("'","ऐ")
        nom_doc=nom_doc.replace('"','ऑ')

        #Nous allons enregistrer en fonction des 4 protections possible.

        if save_doc_protection=="non":
            #Ouverture: Uniquement au créateur ou à l'admin
            #Modification: autorisé

            connexion.execute("INSERT INTO documents VALUES('"+str(nom_doc)+"','"+str(user_doc)+"','"+str(date_doc)+"',0,'"+str(doc)+"')")
            connexion.commit()
            info_parametre="Il est uniquement accessible par votre session, et vous pouvez le modifier."
            flask.session['document']=str(nom_doc)


        elif save_doc_protection=="oui":
            #Ouverture: Uniquement au créateur ou à l'admin
            #Modification: non autorisé

            connexion.execute("INSERT INTO documents VALUES('"+str(nom_doc)+"','"+str(user_doc)+"','"+str(date_doc)+"',1,'"+str(doc)+"')")
            connexion.commit()
            info_parametre="Il est uniquement accessible par votre session, et il a été finalisé."
            flask.session['document']=str(nom_doc)


        elif save_doc_protection=="nonlibre":
            #Ouverture: A tous les utilisateurs
            #Modification: autorisé (note: seul l'admin et le créateur peut remplacer le fichier original)

            connexion.execute("INSERT INTO documents VALUES('"+str(nom_doc)+"','"+str(user_doc)+"','"+str(date_doc)+"',2,'"+str(doc)+"')")
            connexion.commit()
            info_parametre="Il est en accès libre, et tous les utilisateurs peuvent le modifier."
            flask.session['document']=str(nom_doc)


        if save_doc_protection=="ouilibre":
            #Ouverture: A tous les utilisateurs
            #Modification: non autorisé

            connexion.execute("INSERT INTO documents VALUES('"+str(nom_doc)+"','"+str(user_doc)+"','"+str(date_doc)+"',3,'"+str(doc)+"')")
            connexion.commit()
            info_parametre="Il est en accès libre, et a été finalisé."
            flask.session['document']=str(nom_doc)

        nom_doc=nom_doc.replace("'","ऐ")
        nom_doc=nom_doc.replace('"','ऑ')


        #On redirige vers le message de confirmation de l'enregistrement.
        page+="""
            <script type="text/javascript">
            var delai=0; // Delai en secondes
            var url='ew_confirm?nom_doc="""+str(nom_doc)+"""&info_parametre="""+str(info_parametre)+"""&afficher_msg_save=confirm'; // Url de destination
            setTimeout("document.location.href=url", delai + '000');
            </script>
        """

        connexion.close()
        page+=basdepage
        return page

    ##########################################################################
    #PAGE D'ACCUEIL POUR L' ENREGISTREMENT D'UN DOCUMENT.                    #
    ##########################################################################

    page+="""
    <div class="ew_save_fond1">
    </div>
    <div class="ew_save_fond2">
    </div>

    <h1 class="ew_save_titre"><b><i>Enregistrer le document...</i></b></h1>
    <img class="ew_logoword" src="static/images/system/icons/word.png" alt="Logo Word">

    <p class="ew_save_form1">Nom de fichier :</p>
    <p class="ew_save_form2">Protection :</p>

    <form action ="/ew_sauvegarde" method="GET">
        <input type="text" class="ew_form1" name="save_doc_nom" id="save_doc_nom" size="20" maxlength="30">
        <div class="ew_form2">
            <input name="save_doc_protection" type="radio" value="non" checked="checked">
            <input name="save_doc_protection" type="radio" value="oui">
            <input name="save_doc_protection" type="radio" value="nonlibre">
            <input name="save_doc_protection" type="radio" value="ouilibre">

            <input class="ew_save_envoie" type="submit" value="  Enregistrer  ">
        </div>

        <div class="ew_txtform2">
        <p class="ew_txtform2">Modification et accès réservé à l'auteur.</p>
        <p class="ew_txtform2">Document finalisé, réservé à l'auteur.</p>
        <p class="ew_txtform2">Modification et accès réservé à tous.</p>
        <p class="ew_txtform2">Document finalisé, accessible à tous.</p>
        </div>
    </form>

    <form action ="/fermeture_fenetre" target="_parent" method="GET">
        <div class="ew_form2">
            <input name="fermer" type="hidden" value='ew_sauvegarde'>
            <input class="ew_save_annuler" type="submit" value="    Annuler    ">
        </div>

    </form>
    <img class="barre2" src="static/images/system/barre.png" alt="barre">
    """

    page+=basdepage
    return page

@app.route('/ew_confirm', methods = ['GET']) # Bureau Ferry 2000
def ew_confirm():
    """
    L'idéal est de pouvoir sauvegarder un document qu'on a modifier, sans
    devoir le créer sous un autre nom.
    Le problème est, que vu qu'on garde les iframes dans le cache du navigateur,
    l'url est rééxécuté. Si on ouvre un document, et que l'url stocké le concerne,
    on peut le modifier involontairement.
    Pour éviter ça, il faut éviter de placer une commande dans l'url de l'iframe
    au moment de la fermer.
    Donc on créer cette page dédier, pour qu'il n'y ai aucun problème.

    Exemple de problème:
        J'ai un fichier A, B et C.
        Je modifie A, je demande de l'enregistrer sous le nom "C".
        Il refuse.

        J'ouvre B, A... Aucun problème

        MAIS

        Si j'ouvre C, vu que j'ai toujours en mémoire ma demande d'enregistrement,
        et qu'elle est valide cette fois-ci, elle va écraser mes données.
    """


    resultat = flask.request.args
    info_parametre = resultat.get('info_parametre',"")
    nom_doc = resultat.get('nom_doc',"")
    afficher_msg_save = resultat.get('afficher_msg_save',"")



    nom_doc=nom_doc.replace("ऐ","'")
    nom_doc=nom_doc.replace('ऑ','"')


    page=entete

    #ENREGISTREMENT
    ###############################################

    if afficher_msg_save=='confirm':

        page+="""
        <div class="ew_save_fond1">
        </div>
        <div class="ew_save_fond3a">
        </div>
        <img class="barre2" src="static/images/system/barre.png" alt="barre">
        <img class="ew_save_clippya" src="static/images/ferryword/clippy.gif" alt="Clippy">
        <img class="ew_save_msgclippy" src="static/images/ferryword/message_clippy.png" alt="message de Clippy">
        <img class="ew_logoword" src="static/images/system/icons/word.png" alt="Logo Word">
        <h1 class="ew_save_titre"><b><i>Enregistrement du document</i></b></h1>

        <p class="ew_save_msgclippy">
        Votre document <u><b>"""+str(nom_doc)+"""</b></u> a bien été enregistré.<br>
        <br>
        """+str(info_parametre)+"""
        </p>

        <form action ="fermeture_fenetre" target="_parent" method="GET">
            <input name="fermer" type="hidden" value='ew_sauvegarde'>
            <input class="ew_save_fermer" type="submit" value="     Fermer     ">
        </form>

        """
    elif afficher_msg_save=='echec_dejautiliser':
        page+="""
        <div class="ew_save_fond1">
        </div>
        <div class="ew_save_fond3b">
        </div>
        <img class="barre2" src="static/images/system/barre.png" alt="barre">
        <img class="ew_save_clippyb" src="static/images/ferryword/clippy2.gif" alt="Clippy">
        <img class="ew_save_msgclippy" src="static/images/ferryword/message_clippy.png" alt="message de Clippy">
        <img class="ew_logoword" src="static/images/system/icons/word.png" alt="Logo Word">
        <h1 class="ew_save_titre"><b><i>L'enregistrement du document a échoué</i></b></h1>

        <p class="ew_save_msgclippy">
        Le nom <u><b>"""+str(nom_doc)+"""</b></u> a déjà été utilisé pour un autre document.<br>
        <br>
        Veuillez essayer un autre nom.
        </p>

        <form action ="ew_sauvegarde" method="GET">
        <input class="ew_save_fermer" type="submit" value="     Retour     ">
        </form>

        """

    #SUPPRESSION
    ###############################################

    elif afficher_msg_save=='suppr_reussit':
        page+="""
        <div class="ew_save_fond1">
        </div>
        <div class="ew_save_fond3a">
        </div>
        <img class="barre2" src="static/images/system/barre.png" alt="barre">
        <img class="ew_save_clippya" src="static/images/ferryword/clippy.gif" alt="Clippy">
        <img class="ew_save_msgclippy" src="static/images/ferryword/message_clippy.png" alt="message de Clippy">
        <img class="ew_logoword" src="static/images/system/icons/word.png" alt="Logo Word">
        <h1 class="ew_save_titre"><b><i>Suppression du document</i></b></h1>

        <p class="ew_save_msgclippy">
        Votre document <u><b>"""+str(nom_doc)+"""</b></u> a bien été supprimé.<br>
        <br>
        """+str(info_parametre)+"""
        </p>

        <form action ="fermeture_fenetre" target="_parent" method="GET">
            <input name="fermer" type="hidden" value='ew_supprimer'>
            <input class="ew_save_fermer" type="submit" value="     Fermer     ">
        </form>

        """
    elif afficher_msg_save=='suppr_echec':
        page+="""
        <div class="ew_save_fond1">
        </div>
        <div class="ew_save_fond3b">
        </div>
        <img class="barre2" src="static/images/system/barre.png" alt="barre">
        <img class="ew_save_clippyb" src="static/images/ferryword/clippy2.gif" alt="Clippy">
        <img class="ew_save_msgclippy" src="static/images/ferryword/message_clippy.png" alt="message de Clippy">
        <img class="ew_logoword" src="static/images/system/icons/word.png" alt="Logo Word">
        <h1 class="ew_save_titre"><b><i>La suppression du document a échoué</i></b></h1>

        <p class="ew_save_msgclippy">
        Il est possible que vous ne soyez pas le créateur de celui-ci.<br>
        Ou que vous vous êtes trompez durant la confirmation du nom.<br>
        Voir que le document n'existe plus en réalité.
        </p>

        <form action ="ew_supprimer" method="GET">
        <input class="ew_save_fermer" type="submit" value="     Retour     ">
        </form>

        """

    page+=basdepage
    return page