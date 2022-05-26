# -*- coding: utf-8 -*-
"""
Created on Sun May  1 20:50:47 2022

@author: Matthieu
"""
import flask
import sqlite3
import random
from time import *
from Plugins_E2000 import entete, basdepage, morceau_entete, entete_parametre, interface, demarrer_on, demarrer_off, erreur_12, erreur_2a, erreur_2b, popup_info

app = flask.Flask(__name__) # Création de l'application

@app.route('/Ferry_Explorer', methods = ['GET'])
def Ferry_Explorer():
    page="""
    <html lang="fr">
            <head>
                <meta charset="UTF-8" >
                <title>Ferry 2000 - Projet NSI</title>
                <link rel="stylesheet" href="static/fonts.css" type="text/css">
                <link rel="stylesheet" href="static/ferryexplorer.css" type="text/css">
            </head>
    <body>
    """




    #Affiche le menu d'accès entre Google.fr, francetvinfo.fr et wikipedia.fr.
    page+="""

    <div class="bloc">
    </div>
    <img class="logoferry" src="static/images/autres/Ferry2000_logo.png" alt="logo ferry">

    <h1>Jusqu'où irez vous aujourd'hui ?</h1>

    <div class="emplacements">
        <form action="Explorer_web" method="post">
            <input name="pageweb" type="hidden" value='google'>

            <a onmouseover="google.src='static/images/ferryxplorer/google_select.png'" onmouseout="google.src='static/images/ferryxplorer/google.png'">
            <input type="image" class="emplacements" id="google" src="static/images/ferryxplorer/google.png" alt="Menu Démarrer: Programmes"></a>
        </form>

        <div style="position:absolute; bottom:0px; left:240px;">
        <form action="Explorer_web" method="post">
            <input name="pageweb" type="hidden" value='finfo'>

            <a onmouseover="finfo.src='static/images/ferryxplorer/finfo_select.png'" onmouseout="finfo.src='static/images/ferryxplorer/finfo.png'">
            <input type="image" class="emplacements" id="finfo" src="static/images/ferryxplorer/finfo.png" alt="Menu Démarrer: Programmes"></a>
        </form></div>

        <div style="position:absolute; bottom:0px; left:480px;">
        <form action="Explorer_web" method="post">
            <input name="pageweb" type="hidden" value='wiki'>

            <a onmouseover="wiki.src='static/images/ferryxplorer/wiki_select.png'" onmouseout="wiki.src='static/images/ferryxplorer/wiki.png'">
            <input type="image" class="emplacements" id="wiki" src="static/images/ferryxplorer/wiki.png" alt="Menu Démarrer: Programmes"></a>
        </form></div>
    </div>

    """

    page+=basdepage
    return page

@app.route('/Explorer_web', methods = ['POST'])
def Explorer_web():
    page=entete

    resultat = flask.request.form
    pageweb = resultat.get('pageweb',"")

    liste_pageweb=("finfo","wiki")

    #On redirige l'utilisateur vers la page souhaité.
    if pageweb=="finfo":
        pageafficher="https://www.francetvinfo.fr/"
    elif pageweb=="wiki":
        pageafficher="https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal"
    elif pageweb=="google":
        pageafficher="https://www.google.com/webhp?igu=1"
    else:
        #Sinon, on considère qu'il souhaite faire une recherche Google.
        pageweb=pageweb.replace("'","%27")
        pageafficher="https://www.google.com/search?q="+str(pageweb)+"&igu=1"

    #Affichage de la barre d'outil juste au dessus de l'iframe affichant la
    #page web.
    page+="""

    <div style="background-color: silver; width: 100%; height: 100%; position:absolute; top:0px; left:0px;">
    </div>

    <div style="position:absolute; top:2px; left:10px;">
        <form>
            <input type="button" value="< Précédent" onclick="parent.history.go(-1)">
            <input type="button" value=" Suivant > " onclick="parent.history.go(+1)">
            <a href="Ferry_Explorer"><input type="button" value="  Accueil  " onclick="Ferry_Explorer"></a>

        </form>

    </div>

    <div style="position:absolute; top:2px; left:280px;">
        <form action ="/Explorer_web" method="post">
            <input type="text" name="pageweb" size="20" placeholder="Recherche Google"> <!--Barre de recherche-->
            <input type="submit" value=">">
        </form>
    </div>

    <div style="position:absolute; bottom:0px; left:0px;">
    <iframe src='"""+str(pageafficher)+"""' width="780" height="500"></iframe>
    </div>
    """
    page+=basdepage
    return page

