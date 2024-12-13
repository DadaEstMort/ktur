from rapidfuzz import fuzz
import pandas as pd
import requests
import json
from datetime import datetime

#fonction qui regarde si une date est au format Y-m-d
def is_valid_date(date_string):
    try:
        # Essayer de parser la date selon le format Y-m-d
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        # Retourne False si la date ne correspond pas au format
        return False

# Fonction qui permet de rechercher les informations d'un livre via l'api de google
# Sans utiliser de token pour l'utiliser
# on l'utilise quand un utilisateur donne un livre mais qu'il ne se trouve pas dans le csv

def get_book_info_google_books(title):
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            return data["items"][0]["volumeInfo"]
        else:
            return "Aucun livre trouvé."
    else:
        return f"Erreur : {response.status_code}"



# Potentiel fonction pour fuzzy wooooooooodzy !!!
def corespondance_text(text, tab_element, Item_not_found, ratio1, ratio2):
    if pd.isna(text):
        return None

    text_strip = str(text).strip()  # Récupérer et nettoyer le champ
    trouve = False

    if text_strip and text_strip.lower() not in not_valid:
        
        # Comparaison directe avec tab_author
        for elem in tab_element:
            score = fuzz.ratio(text_strip.lower(), elem.lower())
            if score > ratio1:  # Si le score est suffisant
                trouve = True
                break
        if trouve:
            TabVal.append(text_strip)
            return elem
        else:
            # Comparaison mot à mot
            text_split = text_strip.split(" ")
            for elem in tab_element:
                elem_split = elem.split(" ")
                nb_good = sum(
                    1 for i in text_split 
                    if any(fuzz.ratio(i.lower(), j.lower()) > ratio2 for j in elem_split)
                )

                if nb_good == len(text_split):  # Si tous les mots correspondent
                    TabVal.append(text_strip)
                    return elem
                   
            
            # Ajouter dans Author_not_found si non trouvé
            if not trouve:
                Item_not_found.append(text)
                
                
# Charger les fichiers CSV
df_authors = pd.read_csv('CSV_Author_clean copy.csv', encoding='utf-8', header=None, skiprows=1)
df_data = pd.read_csv('data copy.csv', encoding='utf-8')
df_data = df_data[df_data['Quel est votre âge ?'] >= 18]
df_books = pd.read_csv('CSV_Books_clean copy.csv', encoding='utf-8', header=None, skiprows=1)
df_genre = pd.read_csv('listes_genres_translate.csv', encoding='utf-8', header=None, skiprows=1)
df_publisher = pd.read_csv('unique_publishers.csv', encoding='utf-8', header=None, skiprows=1)

# Convertir les colonnes necessaire en liste pour effectuer des recherches
tab_author = df_authors[1].tolist()
tab_books = df_books[1].tolist()
tab_genre = df_genre[0].tolist()
tab_publisher = df_publisher[1].tolist()
tab_publisher_id = df_publisher[0].tolist()

# Initialisation de liste pour stocker des données et faire des liaisons
TabVal = list()
Author_not_found = list()
Book_not_found = list()
No_Genre = list()
book_info_list = list()
publisher_info_list = list()
titles_set = set()

# liste contenant des mots qui ne sont pas valides pour traitement
# exemple :  personnes qui mettent "je ne sais pas" lors de la question "livre préféré"
not_valid = [
    'pareil',
    'je n’en ai pas',
    '',
    'aucun',
    'rien',
    'jsp',
    'jen ai pas',
    'j\'en ai pas',
    'je n\'en ai pas',
    'je n\'ai pas',
    'personne',
    'rien du tout',   
]

# 10 genres que les personnes peuvent choisir dans notre questionnaire
# Permet de gagner en rapidité de traitement que de devoir rechercher dans le csv
genre_questionnaire = {
    'fantasy' : 'Fantaisie',
    'romance': 'Romance',
    'nonfiction' : 'non-fiction',
    'science-fiction' : 'La-science-fiction',
    'mystère' : 'Mystère',
    'historical' : 'Historique',
    'bande déssinée' : 'Bandes-dessinées',
    'adolescent' : 'les-adolescents',
    'fiction': 'Fiction',
    'classiques': 'Classiques'
}

#inverse les clés / valeurs du dictionnaire pour permettre un traitement ultérieurment
genre_questionnaire_inverted = {v.lower(): k for k, v in genre_questionnaire.items()}

'''
PARTIE RECUPERATION DE DONNES
'''
#On parcours le fichier data.csv qui contient les réponses des utilisateurs
for i, row in df_data.iterrows():
    
    #Traitement du genre
    for col in ['Quel genre de livre lisez-vous ?']:
        if pd.isna(row[col]):
            continue
        current_genre = [g.strip() for g in str(row[col]).replace("/", ",").strip().split(",")]

        for genre in current_genre:
            genre_lower = genre.strip().lower()

            # Vérifier dans les clés de genre_questionnaire
            if genre_lower in genre_questionnaire:
                df_data.at[i, col] = genre_questionnaire[genre_lower]

            # Vérifier dans les valeurs de genre_questionnaire
            elif genre_lower in genre_questionnaire_inverted:
                df_data.at[i, col] = genre_questionnaire_inverted[genre_lower]

            else:
                trouve = False
                if genre and genre_lower not in not_valid:
                    
                    # Comparaison directe avec les genres du csv
                    for genre_csv in tab_genre:
                        score = fuzz.ratio(genre_lower, genre_csv.lower())
                        if score > 80:
                            trouve = True
                            TabVal.append(genre)
                            df_data.at[i, col] = genre_csv
                            break

                    # Comparaison mot à mot
                    if not trouve:
                        current_genre_split = genre.split(" ")
                        for genre_csv in tab_genre:
                            genre_csv_words = genre_csv.split("-")
                            nb_good = sum(
                                1 for word in current_genre_split 
                                if any(fuzz.ratio(word.lower(), j.lower()) > 80 for j in genre_csv_words)
                            )

                            if nb_good == len(current_genre_split):
                                TabVal.append(genre)
                                df_data.at[i, col] = genre_csv
                                trouve = True
                                break

                    # Ajouter au No_Genre si non trouvé
                    if not trouve:
                        No_Genre.append(genre)


    #Transformation donnée qualitative en donnée quantitative
    for col in ['A quelle fréquence lisez vous des livres']:
        match row[col]:
                case "Rarement":
                    df_data.at[i, col] = 0
                case "Quelques fois par semaine":
                    df_data.at[i, col] = 1
                case "Quelques fois par mois":
                    df_data.at[i, col] = 2
                case "Tous les jours":  
                    df_data.at[i, col] = 3
                case _:
                    df_data.at[i, col] = -1
                    
    #Transformation donnée qualitative en donnée quantitative     
    for col in ['Comme lecteur vous considérez vous comme :']:
        match row[col]:
            case "Non lecteur":
                df_data.at[i, col] = 0
            case "Modeste":
                df_data.at[i, col] = 1
            case "Moyen":
                df_data.at[i, col] = 2
            case "Passionné":
                df_data.at[i, col] = 3
            case _:
                df_data.at[i, col] = -1


    # On parcours tous les livres favoris
    # On essaye de voir si des livres match avec le csv
    # Si oui on modifie le fichier data.csv avec le livre trouvé 
    # Au cas où si l'utilisateur avait fait une faute d'orthographe
    # Si non on ajoute le livre mis par l'utilisateur dans une liste
    # Pour pouvoir ajouter les livres dans le csv livre
    for col in ['Livre n°1','Livre n°2','Livre n°3']:
       
        # Vérification de la précence dans les csv et modification du csv en conséquence
        val = corespondance_text(row[col], tab_books, Book_not_found, 85,90)

        if val == -1:
            continue
        else:
            df_data.at[i, col] = val
            
        
    # On parcours tous les auteurs favoris
    # On essaye de voir si des auteurs match avec le csv
    # Si oui on modifie le fichier data.csv avec l'auteur trouvé 
    # Au cas où si l'utilisateur avait fait une faute d'orthographe
     # Si non on ajoute l'auteur mis par l'utilisateur dans une liste
    # Pour pouvoir ajouter les auteurs dans le csv des auteurs
    
    for col in ['Auteur n°1', 'Auteur n°2', 'Auteur n°3']:

        # Vérification de la précence dans les csv et modification du csv en conséquence
        val = corespondance_text(row[col], tab_author, Author_not_found, 85,90)

        if val == -1:
            continue
        else:
            df_data.at[i, col] = val

        # FIN DE L'UTILISATION

# On modifie le fichier de réponses des utilisateurs avec la correction orthographique des valeurs
df_data['id_lecteur '] = range(1, len(df_data) + 1)
df_data.to_csv('data_updated.csv', index=False, encoding='utf-8')


'''
-------------------------------------------------------------------------------------------------------
'''

'''
PARTIE AJOUT DONNEES MANQUANTES
'''


'''
On rajoute les auteurs inconnus aux csv
'''
# On calcule l'id max pour en avoir un unique
id_max = max(df_authors[0].tolist())

new_authors = pd.DataFrame({
    'id_author': range(id_max + 1, id_max + 1 + len(Author_not_found)),
    'author_name': Author_not_found,
    'author_gender' : None,
    'birthplace' : None,
    'author_average_rating' : None,

})
new_authors.to_csv('CSV_Author_clean copy.csv', mode='a', index=False, header=False, encoding='utf-8')


'''
On essaye de voir si les livres non trouvé existe grace à l'api google
'''
# On recalcule l'id max mais cette fois si pour les livres 
id_max = max(df_books[0].tolist()) if not df_books.empty else 0

id_publisher_max = max(tab_publisher_id) + 1
id_publisher = None
for book in Book_not_found:
    if pd.isna(book):  
        continue

    # On récupère les informations du livre donné par l'utilisateur si il existe
    book_info = get_book_info_google_books(book)
    
    if isinstance(book_info, str):
        try:
            book_info = json.loads(book_info)  
        except json.JSONDecodeError:
            continue  

    if not isinstance(book_info, dict) or 'title' not in book_info:
        continue

    score = fuzz.ratio(book.lower(), book_info['title'].lower())
    if score > 80:
        # Conditionpour éviter d'importer 2 fois le même livre
        if book_info['title'] in titles_set:
            continue 

        '''
        On regarder si un publisher existe pour le livre trouvé 
        '''
        # parfois il n'y a pas de publisher
        try:
            publisher = book_info['publisher']
        except:
            publisher = False
            
        if(publisher):
            
            '''
                On regarde si le publisher existe dans le fichier publisher
            '''
            trouve = False
            
            for ligne in range (1,len(tab_publisher)):
                if not tab_publisher:
                    continue
            
                if (isinstance(tab_publisher[ligne],str)):
                    score = fuzz.ratio(tab_publisher[ligne].lower().strip(),publisher.lower().strip())
                    if (score > 85):
                        trouve = True
                        break
                
            if trouve :
                id_publisher = tab_publisher_id[ligne]
            
            else:
                # si il existe pas on le créer
                nouvelle_ligne = {'id_publisher': id_publisher_max, 'nom': publisher}
                publisher_info_list.append(nouvelle_ligne)
                id_publisher_max += 1                  

            titles_set.add(book_info['title'])
            book_info_list.append({
                'id_book': id_max + 1,  
                'title': book_info.get('title', ''),
                'number_of_pages': book_info.get('pageCount', ''),
                'date_published': book_info.get('publishedDate', '') if is_valid_date(book_info.get('publishedDate', '')) else None,
                'original_title': None,
                'isbn': None,
                'isbn13': next(
                    (identifier['identifier'] for identifier in book_info.get('industryIdentifiers', [])
                    if identifier.get('type') == 'ISBN_13'),  
                    None 
                ),
                'description': book_info.get('description', ''),
                'id_publisher': id_publisher if not None else id_publisher_max,
                'id_serie': None,
            })
            id_max += 1
            id_publisher = None


# on créer les nouveau csv nettoyé
new_books = pd.DataFrame(book_info_list)
new_books.to_csv('CSV_Books_clean copy.csv', mode='a', index=False, header=False, encoding='utf-8')

new_publisher = pd.DataFrame(publisher_info_list)
new_publisher.to_csv('unique_publishers.csv', mode='a', index=False, header=False, encoding='utf-8')

'''
-------------------------------------------------------------------------------------------------------
'''

'''
PARTIE CREATION DES CSV POUR INTEGRATION
'''




'''
Création du CSV des Users
'''
# on créer un dictionnaire pour stocker les informations des utilisateurs
colonnes_a_garder_users = ["Achetez vous vos livres neufs ou d'occasion ?",'Quand vous achetez un livre quel est le plus important ?', 'Pour quelles raisons vous arrive-t-il de lire ?','Comment sélectionnez-vous un livre ?','Où achetez vous vos livres ?','Quelle est votre situation professionnelle ?','Quel est votre genre ?','Quel est votre âge ?','A quelle fréquence lisez vous des livres','Comme lecteur vous considérez vous comme :', 'id_lecteur ']

data_users = df_data[colonnes_a_garder_users]

# renommage
nouveaux_noms = {
    'Quel est votre âge ?': 'age',
    'Quel est votre genre ?': 'gender',
    'Quelle est votre situation professionnelle ?' : 'profession',
    'A quelle fréquence lisez vous des livres' : 'frequence_lecture',
    'Comme lecteur vous considérez vous comme :' : 'interet_lecture',
    'Où achetez vous vos livres ?' : 'achat_livre',
    'Comment sélectionnez-vous un livre ?' : 'methode_selection',
    'Pour quelles raisons vous arrive-t-il de lire ?' : 'raison_lecture',
    'Quand vous achetez un livre quel est le plus important ?' : 'preference_achat',
    "Achetez vous vos livres neufs ou d'occasion ?" : 'type_achat'
}

data_users = data_users.rename(columns=nouveaux_noms)

# ajout champs manquants
data_users['nom'] = '' 
data_users['prenom'] = '' 
data_users.to_csv('CSV_Users_FINI.csv', index=False)






'''
Création du CSV user aime livre
'''

# on récupère encore les données des livres pour avoir ceux ajouter si il y en a eu
df_books = pd.read_csv('CSV_Books_clean copy.csv', encoding='utf-8', header=None, skiprows=1)
df_books.columns = [
    'id_book', 'title', 'number_of_pages', 'date_published', 
    'original_title', 'isbn', 'isbn13', 'description', 
    'id_publisher', 'id_serie'
]  

# nettoyage + renommage
colonnes_a_garder_livre = ['id_lecteur ', 'Livre n°1', 'Livre n°2', 'Livre n°3']
data_aime_livre = df_data[colonnes_a_garder_livre]
nouveaux_noms = {
    'id_lecteur ': 'id_lecteur',
}
data_aime_livre = data_aime_livre.rename(columns=nouveaux_noms)

#  horizontalisation des livres
data_aime_livre_transformee = data_aime_livre.melt(
    id_vars=['id_lecteur'], 
    value_vars=['Livre n°1', 'Livre n°2', 'Livre n°3'], 
    var_name='Type de Livre', 
    value_name='Livre'
)

# suppression des ligne non conforme
data_aime_livre_transformee = data_aime_livre_transformee[
    data_aime_livre_transformee['Livre'].notna() & (data_aime_livre_transformee['Livre'] != '')
]

# suppression de la colone temp
data_aime_livre_transformee = data_aime_livre_transformee.drop(columns=['Type de Livre'])

# joiture pour récupérer les id à la place des titre
data_aime_livre_finale = pd.merge(
    data_aime_livre_transformee, 
    df_books, 
    left_on='Livre',   
    right_on='title', 
    how='left'        
)
data_aime_livre_finale = data_aime_livre_finale.dropna(subset=['id_book'])

# passage des id en int
data_aime_livre_finale['id_book'] = data_aime_livre_finale['id_book'].astype(int)

# nettoyage
data_aime_livre_finale = data_aime_livre_finale[['id_lecteur', 'id_book']]

# suppression doublon
data_aime_livre_finale = data_aime_livre_finale.drop_duplicates()

# enregistrement
data_aime_livre_finale.to_csv('CSV_Aime_livre_FINI.csv', index=False)








'''
Création du CSV user aime author
'''

# Exactement la même procédure que pour user aime livre

# Author
df_authors = pd.read_csv('CSV_Author_clean copy.csv', encoding='utf-8', header=None, skiprows=1)
df_authors.columns = [
    'id_author', 'author_name', 'author_gender', 'birthplace', 
    'author_average_rating'
]  
colonnes_a_garder_auteur = ['id_lecteur ', 'Auteur n°1', 'Auteur n°2', 'Auteur n°3']
data_aime_auteur = df_data[colonnes_a_garder_auteur]
nouveaux_noms = {
    'id_lecteur ': 'id_lecteur',
}

data_aime_auteur = data_aime_auteur.rename(columns=nouveaux_noms)
data_aime_auteur_transformee = data_aime_auteur.melt(
    id_vars=['id_lecteur'], 
    value_vars=['Auteur n°1', 'Auteur n°2', 'Auteur n°3'], 
    var_name='Type de Auteur', 
    value_name='Auteur'
)
data_aime_auteur_transformee = data_aime_auteur_transformee[
    data_aime_auteur_transformee['Auteur'].notna() & (data_aime_auteur_transformee['Auteur'] != '')
]
data_aime_livre_finale = data_aime_livre_finale.drop_duplicates()
data_aime_auteur_transformee = data_aime_auteur_transformee.drop(columns=['Type de Auteur'])
data_aime_auteur_finale = pd.merge(
    data_aime_auteur_transformee, 
    df_authors, 
    left_on='Auteur',   
    right_on='author_name', 
    how='left'        
)
data_aime_auteur_finale = data_aime_auteur_finale.dropna(subset=['id_author'])
data_aime_auteur_finale['id_author'] = data_aime_auteur_finale['id_author'].astype(int)
data_aime_auteur_finale = data_aime_auteur_finale[['id_lecteur', 'id_author']]
data_aime_auteur_finale.to_csv('CSV_Aime_Auteur_FINI.csv', index=False)








'''
Création du CSV user aime genre
'''

# Exactement la même procédure que pour user aime livre
df_genre = pd.read_csv('listes_genres_translate_with_ids.csv', encoding='utf-8', header=None, skiprows=1)
df_genre.columns = ['id_genre','genre_name'] 
colonnes_a_garder_genre = ['id_lecteur ', 'Quel genre de livre lisez-vous ?']
data_aime_genre = df_data[colonnes_a_garder_genre]
nouveaux_noms = {
    'id_lecteur ': 'id_lecteur',
}
data_aime_genre = data_aime_genre.rename(columns=nouveaux_noms)
data_aime_genre_transformee = data_aime_genre.melt(
    id_vars=['id_lecteur'], 
    value_vars=['Quel genre de livre lisez-vous ?'], 
    var_name='Type de Genre', 
    value_name='Genre'
)
data_aime_genre_transformee = data_aime_genre_transformee[
    data_aime_genre_transformee['Genre'].notna() & (data_aime_genre_transformee['Genre'] != '')
]
data_aime_genre_transformee = data_aime_genre_transformee.drop(columns=['Type de Genre'])
data_aime_genre_finale = pd.merge(
    data_aime_genre_transformee, 
    df_genre, 
    left_on='Genre',   
    right_on='genre_name', 
    how='left'        
)
data_aime_genre_finale = data_aime_genre_finale.dropna(subset=['id_genre'])
data_aime_genre_finale['id_genre'] = data_aime_genre_finale['id_genre'].astype(int)
data_aime_genre_finale = data_aime_genre_finale[['id_lecteur', 'id_genre']]
data_aime_genre_finale = data_aime_genre_finale.drop_duplicates()
data_aime_genre_finale.to_csv('CSV_Aime_Genre_FINI.csv', index=False)

