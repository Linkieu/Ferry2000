# -*- coding: utf-8 -*-
"""
Created on Sun May  1 19:27:16 2022

@author: Matthieu
"""

import flask
import sqlite3
import random
from time import *
from Plugins_E2000 import entete, basdepage, morceau_entete, entete_parametre, interface, demarrer_on, demarrer_off, erreur_12, erreur_2a, erreur_2b, popup_info

app = flask.Flask(__name__) # Création de l'application

#@app.route('/bureau', methods = ['GET']) # Bureau Ferry 2000
def bureau():

    resultat = flask.request.args
    page=entete

    demarrer,startup = resultat.get('demarrer',None),resultat.get('startup',None)



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


    ##########################################################################
    # ECRAN DE VEILLE                                                        #
    ##########################################################################
    #Génère un décompte avant l'apparition de l'écran de veille.
    #Est réinitialiser dès que FLASK recharge cette page.

    page+="""
    <script type="text/javascript">
    var delai=900; // Delai en secondes
    var url='veille'; // Url de destination
    setTimeout("document.location.href=url", delai + '000');
    </script>
        """

    ##########################################################################
    ##########################################################################


    ##########################################################################
    #AFFICHAGE DE L'HEURE DANS LA BARRE DES TÂCHES                           #
    ##########################################################################
    #Vu qu'Ferry 2000 pour fonctionné a besoin de naviguer dans l'historique,
    #L'heure affiché sera celui du dernier chargement de cette page.
    #Par ce système de cookie, on vérifie que l'heure qu'on souhaite affiché est
    #bien la plus récente ou non.
    #Afin que l'heure affiché soit la plus récente possible.

    if 'horloge' not in flask.session:
        flask.session['horloge']=str(strftime("%y%m%d %H:%M", localtime()))
    else:
        if str(strftime("%y%m%d %H:%M", localtime()))>flask.session['horloge']:
            #Permet de s'assurer que l'heure affiché à l'écran est toujours la
            #plus récente.
            flask.session['horloge']=str(strftime("%y%m%d %H:%M", localtime()))

    page+="""
    <div style="position:absolute; bottom:0px; right:27px; font-family: windowsfont; font-size: 14px;">
    <p>"""+str(flask.session['horloge'])[7:]+"""</p>
    </div>
    """
    ##########################################################################
    ##########################################################################
    connexion = sqlite3.connect("Ferry2000.db")

    #On charge le thème de la session
    themes=list(connexion.execute("SELECT theme_c1,theme_c2,theme_opa,theme_titre,theme_police FROM utilisateur WHERE nom=='"+str(flask.session['utilisateur'])+"'"))
    theme_c1,theme_c2,theme_opa, theme_titre, theme_police = themes[0][0],themes[0][1],themes[0][2],themes[0][3],themes[0][4]






    ##########################################################################
    #AFFICHAGE DES ICÔNES SUR LE BUREAU                                      #
    ##########################################################################
    page+="""
    <div class="icones_bureau" style="font-family:"""+str(theme_police)+"""; font-size: 12px;">
    """
    #On parcours la liste des logiciels qu'on autorise l'apparition sur le
    #bureau, dans l'ordre indiqué dans la BDD.
    liste_icones_bureau=list(connexion.execute("SELECT nom,titre,icon FROM logiciels WHERE dispo_bureau>0 ORDER BY dispo_bureau ASC"))

    for icone_bureau in liste_icones_bureau:
        icone_nom=icone_bureau[0]
        icone_titre=icone_bureau[1]
        icone_icon=icone_bureau[2]
        page+="""
        <a href='ouverture_fenetre?ouvrir="""+str(icone_nom)+"""' class="icone_bureau">
            <p class="nom_icone_bureau">"""+str(icone_titre)+"""</p>
            <img class="icone_bureau" src='static/images/system/icons/"""+str(icone_icon)+"""' alt="Icone sur le bureau">
        </a>
        """

    page+="</div>"


    ##########################################################################
    ##########################################################################



    ##########################################################################
    #SUPPERPOSITION DES IFRAMES SUR LE BUREAU                                #
    ##########################################################################
    for e in flask.session['taskbar']: #e représente une page, qui va être généré dans une iframe


        if e!="refermer":
            #Récupération des informations sur le logiciel pour son apparition
            taille=list(connexion.execute("SELECT fenetre FROM logiciels WHERE nom=='"+str(e)+"'"))[0][0]
            titre_fenetre=list(connexion.execute("SELECT titre FROM logiciels WHERE nom=='"+str(e)+"'"))[0][0]
            icone=list(connexion.execute("SELECT icon FROM logiciels WHERE nom=='"+str(e)+"'"))[0][0]


            if taille=='grande':
                #Cas où on génère la page dans une grande fenêtre

                #Affichage de la page web
                page+='<iframe class="grande_fenetre" src='+str(e)+' width="784" height="535"></iframe>'

                #Génération de la barre des titres juste au dessus de l'iframe:
                page+="""
                <div style="position: absolute; background: linear-gradient(to right,"""+str(theme_c1)+""","""+str(theme_c2)+"""); opacity:"""+str(theme_opa)+"""; width: 788px; height: 20px;">
                </div>
                """
                page+='<a href="fermeture_fenetre?fermer='+str(e)+'">'
                page+="""
                <img class="fermer_grande" src="static/images/system/titlebar/bouton_fermer.png" alt="X">
                </a>
                """
                page+='<img class="icone_grande" src="static/images/system/icons/'+str(icone)+'" alt="icône">'

                page+='<div style="color:'+str(theme_titre)+'; font-family:'+str(theme_police)+';">'
                page+='<p class="titre_grande">'+str(titre_fenetre)+'</p>'
                page+='</div>'
            elif taille=='moyenne':
                page+='<iframe class="moyenne_fenetre" src='+str(e)+' width="586" height="400"></iframe>'

                page+='<div style="position: absolute; left: 110px; top: 72px; ">'
                page+="""
                <div style="position: absolute; background: linear-gradient(to right,"""+str(theme_c1)+""","""+str(theme_c2)+"""); opacity:"""+str(theme_opa)+"""; width: 590px; height: 20px; box-shadow: 2px -2px 12px #555;">
                </div>
                """
                page+='<a href="fermeture_fenetre?fermer='+str(e)+'">'
                page+="""
                <img class="fermer_moyenne" src="static/images/system/titlebar/bouton_fermer.png" alt="X">
                </a>
                """
                page+='<img class="icone_fenetre" src="static/images/system/icons/'+str(icone)+'" alt="icône">'

                page+='<div style="color:'+str(theme_titre)+'; font-family:'+str(theme_police)+'">'
                page+='<p class="titre_fenetre">'+str(titre_fenetre)+'</p>'
                page+="</div></div>"
            elif taille=='petite':
                page+='<iframe class="petite_fenetre" src='+str(e)+' width="366" height="250"></iframe>'

                page+='<div style="position: absolute; left: 230px; top: 172px; ">'
                page+="""
                <div style="position: absolute; background: linear-gradient(to right,"""+str(theme_c1)+""","""+str(theme_c2)+"""); opacity:"""+str(theme_opa)+"""; width: 370px; height: 20px; box-shadow: 2px -2px 12px #555;">
                </div>
                """
                page+='<a href="fermeture_fenetre?fermer='+str(e)+'">'
                page+="""
                <img class="fermer_petite" src="static/images/system/titlebar/bouton_fermer.png" alt="X">
                </a>
                """
                page+='<img class="icone_fenetre" src="static/images/system/icons/'+str(icone)+'" alt="icône">'

                page+='<div style="color:'+str(theme_titre)+'; font-family:'+str(theme_police)+'">'
                page+='<p class="titre_fenetre">'+str(titre_fenetre)+'</p>'
                page+="</div></div>"


        elif e=="refermer":
            #Situation où on doit placer une iframe invisible pour que le
            #navigateur puisse y "vider" son câche dessus.
            #(et donc éviter qu'une nouvelle iframe recharge une ancienne page).

            #Il est recommander d'aller régulièrement sur le bureau pour
            #recharger le cache, et ainsi alléger le navigateur.
            page+='<iframe class="fenêtre_caché" src='' width="0" height="0"></iframe>'

    ##########################################################################
    ##########################################################################



    ##########################################################################
    #VERIFICATION DE L'ETAT DE CERTAINS PROGRAMMES                           #
    ##########################################################################
    #Si on a en mémoire les informations de connexion de la session
    #administrateur, mais que pourtant aucune page en ayant besoin est affiché,
    #Alors on supprime.
    #Cela ne concerne pas le stockage du nom d'utilisateur de la session.
    if ("admin_nom" in flask.session or "admin_mdp" in flask.session) and "controle_utilisateur?acces=parametre_admin" not in flask.session['taskbar']:
        del flask.session["admin_nom"]
        del flask.session["admin_mdp"]
        #Lorsqu'on paramètre les sessions en passant par la fenêtre "parametre_admin",
        #nous stockons le nom et le mot de passe de la session admin.
        #J'ai préféré les mettre dans les cookies, plutôt de l'envoyer par formulaire
        #lorsqu'on charge une page paramètre, par principe de sécuriter.
        #Vu que qu'il est impossible de retourner en arrière par l'historique et
        #d'envoyer en même temps un formulaire.

        #Malgré tout, lorsque l'utilisateur n'utilise plus les paramètres administrateurs,
        #on en profite pour détruire en quelque sorte le cookie, ce qu'on fait ici.


    #On supprime le nom du document gardé en mémoire si Ferry Word n'est pas
    #ouvert.
    #Cela permet d'éviter que l'utilisateur y accède en voulant créer un
    #document vierge.
    if 'document' in flask.session and 'ferryword' not in flask.session['taskbar']:
        del flask.session['document']

    #Situation où on a un terme de recherche gardé en mémoire, mais que
    #le dossier Mes Documents n'est pas ouvert.
    #Permets d'éviter qu'au moment d'ouvrir le dossier Mes Documents, la
    #recherche soit réexécuté.
    if 'recherche' in flask.session and 'bibliotheque_docs' not in flask.session['taskbar']:
        del flask.session['recherche']


    #Uniquement si Ferry Word indique de la jouer. et si la fenêtre est
    #ouverte, alors, on joue la musique.

    if 'dejajouer_easteregg_EW' in flask.session and 'ferryword' in flask.session['taskbar']:
        page+="""<audio src="static/musique/clouds.mp3" autoplay loop></audio>"""

    ##########################################################################
    ##########################################################################



    ##########################################################################
    #AFFICHAGE DES PROGRAMMES DANS LA BARRE DES TÂCHES                       #
    ##########################################################################
    page+='<div style="	position:absolute; top:571px; left:185px;">'

    nb_emplacement=1 #Permet de compter le nombre de fenêtre à afficher dans la barre des tâches.
    espace_nom_taskbar=23 #Malheureusement, je n'ai pas réussis à utiliser en css le "position:relative" pour espacer les noms des fenêtres... J'ai du le faire manuellement.

    for e in flask.session['taskbar']: #On parcours les fenêtres ouvertes
        if e!="refermer":
            if nb_emplacement<=3: #S'il reste de la place dans la barre des tâches

                #Récupération des informations
                titre_fenetre=list(connexion.execute("SELECT titre FROM logiciels WHERE nom=='"+str(e)+"'"))[0][0]
                icone=list(connexion.execute("SELECT icon FROM logiciels WHERE nom=='"+str(e)+"'"))[0][0]

                #Mise en page
                page+='<img class="emplacement_taskbar" src="static/images/system/emplacement_taskbar.png" alt="Emplacement de la barre des tâches">'
                page+='<img class="icone_taskbar" src="static/images/system/icons/'+str(icone)+'" alt="Icone">'
                page+='<div style="position:absolute; left:'+str(espace_nom_taskbar)+'px; bottom:-7px;">'
                page+='<p class="nom_taskbar">'+str(titre_fenetre)+'</p>'
                page+='</div>'

                #On indique l'emplacement de la prochaine case dans la barre
                #des tâches
                espace_nom_taskbar+=163

            #On compte la fenêtre dans la liste des fenêtres ouverte.
            nb_emplacement+=1
    if nb_emplacement>4:
        #S'il y a d'autres fenêtres en plus de celle affiché dans la barre des
        #tâches.

        #On ajoute une petite case indiquant le nombre de fenêtres supplémentaire
        #ouvertes.
        page+='<img class="emplacement_taskbar" src="static/images/system/emplacement+_taskbar.png" alt="Affiche le nombre de plage supplémentaire.">'
        page+='<div style="position:absolute; left:'+str(espace_nom_taskbar-20)+'px; bottom:-7px;">'
        page+='<p class="plus_taskbar">+'+str(nb_emplacement-4)+'</p>'
        page+='</div>'
    page+="</div>"

    ##########################################################################
    ##########################################################################



    ##########################################################################
    #RECHARGEMENT DU BUREAU                                                  #
    ##########################################################################
    if nb_emplacement==1 and flask.session['taskbar']!=[]:
        #Si aucune fenêtre (iframe) n'est ouverte à l'utilisateur,
        #Alors on vide la liste représentant les fenêtres précédemment ouverte.
        #Lorsqu'une iframe va apparaître, vu que la liste est vide,
        #"ouvrir fenêtre" renverra l'utilisateur directement vers le bureau.
        #Au lieu de renvoyer dans l'historique.
        #
        #Le fait de renvoyer dans l'historique permet de récupérer les entrées
        #des iframes précédemment ouverte, en cas de besoin par l'utilisateur.
        #
        #Sauf que dans ce cas, c'est complètement inutile. Et recharger la page
        #permet de vider le cache, donc supprimer les iframes gardé en mémoire
        #ce qui allège le navigateur.
        flask.session['taskbar']=[]

    ##########################################################################
    ##########################################################################



    ##########################################################################
    #OUVERTURE DU BUREAU... BIENVENUE SUR FERRY 2000 !                    #
    ##########################################################################
    #On affiche ou non le menu démarré en fonction de ce qui est demandé.
    if demarrer=='on':
        etat_menu_démarrer=demarrer_on
        page+='<audio src="static/musique/start.wav" autoplay></audio>'
    else:
        etat_menu_démarrer=demarrer_off


    #On va jouer la musique de démarrage
    if flask.session['musique_ouverture_session']==True:
        #Démarrage habituel

        page+="""<audio src="static/musique/startup.mp3" autoplay></audio>"""
        flask.session['musique_ouverture_session']=False #Afin d'éviter que la musique se rejoue, alors qu'on a déjà démarré la session.

    elif flask.session['musique_ouverture_session']=='premiereconnexion':
        #Toute première connexion à la session, on joue une musique différente
        #(celle de connexion à Windows 95, pour le simple plaisir de l'entendre)
        #Et on redirige l'utilisateur vers la page d'aide.

        #Remarque:  Même si on ouvre une fenêtr/menu démarré, la fenêtre
        #           d'aide s'ouvre.

        page+="""<audio src="static/musique/The Microsoft Sound.wav" autoplay></audio>"""
        flask.session['musique_ouverture_session']='premiereconnexion2'
        page+="""
        <script type="text/javascript">
            var delai=5; // Delai en secondes
            var url='bureau'; // Url de destination
            setTimeout("document.location.href=url", delai + '000');
        </script>
        """

    elif flask.session['musique_ouverture_session']=='premiereconnexion2':
        #On affiche le menu d'aide qui en s'ouvrant va lire la musique
        #juste en dessous (premiereconnexion3)

        flask.session['musique_ouverture_session']='premiereconnexion3'
        page+="""
        <script type="text/javascript">
            var delai=1; // Delai en secondes
            var url='ouverture_fenetre?ouvrir=aide'; // Url de destination
            setTimeout("document.location.href=url", delai + '000');
        </script>
        """

    elif flask.session['musique_ouverture_session']=='premiereconnexion3':
        #Désactive le cookie de démarrage, et joue un thème étendu de
        #Windows ME/2000 (non officiel: https://www.youtube.com/watch?v=TU_UF9FMcZE)
        page+="""<audio src="static/musique/Windows ME Extended Theme.mp3" autoplay></audio>"""
        flask.session['musique_ouverture_session']=False


    ##########################################################################
    ##########################################################################



    ##########################################################################
    #MISE EN PLACE DE L'ARRIERE PLAN ET DE LA BARRE DES TÂCHES               #
    ##########################################################################
    arriere_plan=list(connexion.execute("SELECT wallpaper FROM utilisateur WHERE jeton=='"+str(jeton)+"'"))[0][0]
    interfacee="""
            <img class="bureau" src="static/images/system/wallpaper/"""+str(arriere_plan)+"""" alt="Fond d'écran">
            <img class="interface" src="static/images/system/taskbar.png" alt="Barre des tâches Ferry 2000">

            <div style="position: absolute; bottom:11.5px; left:102.5px;">
                <a href="fermer_tte_fenetres">
                <img class="mini_icones" src="static/images/system/icons/bureaumini.png" alt="Icone retour bureau"></a>

                <a href="ouverture_fenetre?ouvrir=Ferry_Explorer">
                <img class="mini_icones" src="static/images/system/icons/iemini.png" alt="Icone Ferry Explorer"></a>

                <a href="ouverture_fenetre?ouvrir=ferryword">
                <img class="mini_icones" src="static/images/system/icons/wordmini.png" alt="Icone Ferry Word"></a>
            </div>
            """

    ##########################################################################
    ##########################################################################

    page+=interfacee
    page+=etat_menu_démarrer
    page+=basdepage
    connexion.close()
    return page

#@app.route('/fermer_tte_fenetres', methods = ['GET'])
def fermer_tte_fenetres():
    #Permet de fermer immédiatement toute les fenêtres. Actuellement ouverte
    #comme précédemment ouverte.
    #On vide la barre des tâches et on en profite pour rafraichir le bureau.
    page=morceau_entete

    if 'taskbar' in flask.session:
        flask.session['taskbar']=[]

    page+="""
    <meta http-equiv="refresh" content="0.1; URL=bureau">
    </head>
    <body>
    """
    page+=basdepage
    return page

#@app.route('/fermeture_fenetre', methods = ['GET']
def fermeture_fenetre():
    #Fait fermer la fenêtre demander, en remplaçant le nom du programme dans
    #la barre des tâches par "refermer".
    #Si le bureau n'est pas rafraichi, la page web devra quand même être chargé
    #à cause du navigateur, mais elle sera invisible pour l'utilisateur.
    #De plus, cela n'influe pas sur l'expérience utilisateur.
    #Elles n'enverrons pas de formulaire pouvant poser problème.

    connexion = sqlite3.connect("Ferry2000.db")
    resultat = flask.request.args
    fermer = resultat.get('fermer',None)

    #On retourne en arrière dans le navigateur afin de recharger les entrées
    #des formulaires et l'état des pages juste avant la fermeture de la fenêtre.
    #(sinon, si on tape du texte dans Ferry Word, fermer une fenêtre
    #provoquerais sa disparition, par exemple.)
    page=morceau_entete
    page+="""
          <script language="javascript" type="text/javascript">
              window.history.go(-1);
          </script>
          </head>
          <body>
          """



    ################## On charge la liste des logiciel existant
    requete=list(connexion.execute("SELECT nom FROM logiciels"))
    liste_logiciels=[]
    for logiciel in requete:
        liste_logiciels.append(logiciel[0])
    #######################################


    #On vérifie que tout est correct pour la fermeture du programme.
    if fermer in liste_logiciels and fermer in flask.session['taskbar']:

        #On vérifie que la liste n'est pas vide
        if len(flask.session['taskbar'])!=0:
            a=flask.session['taskbar']
            a[a.index(fermer)]='refermer'
            flask.session['taskbar']=a

            #Ce sorte de détour à été fait car il est impossible de mettre à
            #jour directement la liste depuis les cookies.
            #C'était la solution que vous m'avez conseillée lorsque j'ai
            #rencontré ce problème.

    else:
        #On affiche un message d'erreur
        page=entete
        requete=list(connexion.execute("SELECT type,erreur,icon FROM erreurs WHERE id_erreur==11")) #On recherche dans la base de donnée le message d'erreur associé
        page+=erreur_2a
        page+="""<h1 class="titre_message">"""+str(requete[0][0])+"""</h1><p class="message">"""+str(requete[0][1])+"""</p><img class="msg_icon" src="static/images/system/icons/"""+str(requete[0][2])+""".png" alt="Icon du message">"""
        page+=basdepage

    page+=basdepage
    connexion.close()
    return page



#@app.route('/ouverture_fenetre', methods = ['GET'])
def ouverture_fenetre():
    connexion = sqlite3.connect("Ferry2000.db")
    resultat = flask.request.args
    ouvrir = resultat.get('ouvrir',None)
    retour = str(resultat.get('retour',None)) #Permet de savoir vers quel page de l'historique on redirige l'utilisateur.


    ##########################################################################
    #AFFICHAGE DES DOCUMENTS DEPUIS LA BARRE DE RECHERCHE DU MENU DEMARRER   #
    ##########################################################################
    recherche = resultat.get('recherche',"")

    #Si on a bien demandé de faire une recherche de documents
    if recherche!="":
        #On stock la recherche dans les cookies temporairement
        flask.session['recherche']=recherche

        #Si bibliotheque_docs est déjà ouvert, alors on le ferme.
        if 'bibliotheque_docs' in flask.session['taskbar']:
            #Problème également présent ici, impossible de mettre à jour le
            #cookie "taskbar" directement... On doit passer par cette manière.
            index=flask.session['taskbar'].index('bibliotheque_docs')
            taskbar=flask.session['taskbar']
            taskbar[index]="refermer"
            flask.session['taskbar']=taskbar

    #EXPLICATIONS:
    #Vu qu'on ne peut pas envoyer un formulaire depuis cette page, et qu'en
    #réalité l'apparition des fenêtres sur le bureau est du au cookie "taskbar",
    #on doit faire autrement.
    #La solution la plus évidente est de repasser par les cookies.
    #Ce cookie sera détruit lorsque la fenêtre sera refermer (donc quand elle
    #ne sera plus dans la taskbar)
    #On en profite pour refermer la fenêtre bibliotheque_docs si elle est déjà
    #ouverte, pour laisser permettre la recherche.

    ###########################################################################
    ###########################################################################


    ################## On charge la liste des logiciels existant
    requete=list(connexion.execute("SELECT nom FROM logiciels"))
    liste_logiciels=[]
    for logiciel in requete:
        liste_logiciels.append(logiciel[0])
    #######################################""



    if ouvrir!=None and ouvrir not in flask.session['taskbar'] and ouvrir in liste_logiciels:
        page=morceau_entete

        """
        Explication du 'window.location.replace("bureau");'
        Si la fenêtre apparaît (ou non) alors que le bureau est vide,
        il est inutile de charger l'historique. Car on a aucune entrée de
        formulaire à regénérer.
        Cela alourdirait inutilement le site web, il faut donc profiter de
        l'occasion pour actualiser le bureau.
        """



        if retour=='2':
            #On fait une redirection de -2 dans l'historique.

            if flask.session['taskbar']==[]:
                #Aucune fenêtre est ouverte
                redirection="""window.location.replace("bureau");"""
            else:
                #Il y a des fenêtres ouvertes, on revient dans l'historique.
                #Ainsi, on les réaffiches dans le même état que juste avant
                #l'ouverture de la fenêtre.
                redirection="""window.history.go(-2);"""

            """
            On peut supposer que l'utilisateur ai fait la demande d'ouverture
            depuis le menu démarré.
            Donc, la page précédente comporte le menu démarré ouvert.
            Or, on aimerais qu'il soit fermé à l'apparition de la fenêtre.
            Donc on retourne à la page avant la précédente, là où il est fermé.
            """

            page+="""
            <script language="javascript" type="text/javascript">
            """+redirection+"""
            </script>
            </head>
            <body>
            """
        else:
            #Sinon, on fait un simple retour en arrière.

            if flask.session['taskbar']==[]:
                redirection="""window.location.replace("bureau");"""
            else:
                redirection="""window.history.go(-1);"""
            """
            On peut supposer ici que l'utilisateur a fait la demande
            d'ouverture depuis l'explorateur de fichier par exemple.
            Donc la page précédente est celle qu'on souhaite recharger, car
            elle comporte les entrées les plus récente des formulaire.
            """

            page+="""
            <script language="javascript" type="text/javascript">
            """+redirection+"""
            </script>
            </head>
            <body>
            """

        l=flask.session['taskbar']
        l.append(str(ouvrir))
        flask.session['taskbar']=l

        #Remarque: création de la liste "l" par votre conseil, vu que faire
        #flask.session['taskbar'].append(str(ouvrir)) ne marche pas.
        page+=basdepage
    else:
        #On affiche un message d'erreur
        page=entete
        requete=list(connexion.execute("SELECT type,erreur,icon FROM erreurs WHERE id_erreur==10")) #On recherche dans la base de donnée le message d'erreur associé

        #En fonction du pop-up, le bouton Retour est différent.
        if retour=='2':
            page+=erreur_2b
        else:
            page+=erreur_2a
        page+="""<h1 class="titre_message">"""+str(requete[0][0])+"""</h1><p class="message">"""+str(requete[0][1])+"""</p><img class="msg_icon" src="static/images/system/icons/"""+str(requete[0][2])+""".png" alt="Icon du message">"""
        page+=basdepage


    connexion.close()
    return page

#@app.route('/controle_utilisateur', methods = ['GET']
def controle_utilisateur():
    #Page permettant de confirmant que la personne qui souhaite faire l'action
    #soit bien le propriétaire de la session. Ou un administrateur, dans le
    #cas d'un accès aux paramètres d'aministration.

    page=entete_parametre

    resultat = flask.request.args
    acces = resultat.get('acces',"")

    titre="Contrôle de compte utilisateur"
    info="Entrez vos informations de connexions pour poursuivre."
    img="clef.png"

    #Message s'affichant en fonction de la redirection.
    if acces=='parametre_session':
        description="Vous serez redirigé vers les paramètres de votre session juste après."
    elif acces=='parametre_admin':
        description="Vous devez être connecté en tant qu'administrateur pour poursuivre."
    else:
        page+="""<p>Une erreur s'est produite, veuillez refermer cette page.</p>"""
        page+=basdepage
        return page




    page+=flask.render_template("parametre.html",titre=titre,info=info,description=description,img=img)
    page+="""

    <div class="connexion">
    <form action ="/"""+acces+"""" method="post">

        <label for="utilisateur" class="connexion" title="Veuillez saisir votre nom d'utilisateur">Utilisateur:</label>
        <input class="connexion1" type="text" name="utilisateur" id="utilisateur" size="32"> <!--Emplacement nom utilisateur-->
        <br><br>
        <label for="mdp" class="connexion" title="Veuillez saisir votre mot de passe">Mot de passe:</label>
        <input class="connexion2" type="password" name="mdp" id="mdp" size="32"> <!--Emplacement nom utilisateur-->
        <input class="bouton1" type="submit" value="       Continuer      ">\n <!--Renvoi le formulaire-->
    </form>
    </div>
    """
    page+=basdepage
    return page