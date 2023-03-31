#Import des différents modules

import requests
from bs4 import BeautifulSoup


def scrape_url(url)->list:
    """Fonction qui reçoit une URL en paramètre et qui retourne une liste contenant l'ensemble des éléments demandés"""

    # Obtenir la page en utilisant requests
    response = requests.get(url)

    # Analyser la page avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    #Récupération des différentes données demandées et stockage dans des variables
    upc = soup.find('th', text='UPC').find_next_sibling('td').get_text()
    title = soup.find('h1').get_text()
    price_notax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').get_text()
    price_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').get_text()
    availability = soup.find('th', text='Availability').find_next_sibling('td').get_text()
    description = soup.find('div', id='product_description').find_next('p').get_text()
    category = soup.select('.breadcrumb > li > a')[-1].get_text()
    rating_init = soup.find('p', class_='star-rating') #Renvoie tout le code HTML 
    rating_class = rating_init['class'] #Je récupéère le nom de la classe qui est en fait une liste
    rating = rating_class[1] #Je récupère le second élément de la liste
    img = 'http://books.toscrape.com/' + soup.select('img')[0]['src']
    
    datas = [upc,title,price_notax,price_tax,availability,description,category,rating,img]
    
    return datas

# URL de la page à scraper
url = 'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'

#On fait un print dans la console pour vérification du résultat
print(scrape_url(url))

