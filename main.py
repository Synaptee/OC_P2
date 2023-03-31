from bs4 import BeautifulSoup
import requests
from slugify import slugify
import csv

session = requests.session()


def bs_get(url_to_scrape):
    try:
        response = session.get(url_to_scrape)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except Exception as err:
        print(f"Une erreur est survenue : {err} ")


def load_img(img, nom_img):
    """Fonction qui télécharge l'image d'une URL donnée et la stock dans le répertoire courant"""
    response = requests.get(img)
    with open(nom_img, "wb") as f:
        f.write(response.content)


def convert_rating(txt):
    if txt == "One":
        return 1
    elif txt == "Two":
        return 2
    elif txt == "Three":
        return 3
    elif txt == "Four":
        return 4
    elif txt == "Five":
        return 5
    else:
        return 0


def scrape_url(url_to_scrape) -> list:
    """Fonction qui reçoit une URL en paramètre et qui retourne une liste contenant l'ensemble des éléments demandés"""
    soup = bs_get(url_to_scrape)

    # Recuperation des different donnes demandées et stockage dans des variables
    upc = soup.find('th', string='UPC').find_next_sibling('td').get_text()
    title = soup.find('h1').get_text()
    price_notax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').get_text()
    price_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').get_text()
    availability = soup.find('th', string='Availability').find_next_sibling('td').get_text()
    try:
        description = soup.find('div', id='product_description').find_next('p').get_text()
    except:
        description = "Ce livre n'a pas de description"
    category = soup.select('.breadcrumb > li > a')[-1].get_text()
    rating_init = soup.find('p', class_='star-rating')  # Renvoie tout le code HTML
    rating_class = rating_init['class']  # Je récupère le nom de la classe qui est en fait une liste
    rating = convert_rating(rating_class[1])  # Je récupère le second élément de la liste
    img = 'http://books.toscrape.com/' + soup.select('img')[0]['src']

    nom_img = slugify(category + " " + title, separator="_") + ".jpg"
    try:
        load_img(img, nom_img)
    except Exception as err:
        print(f"Une erreur est survenue dans le téléchargement de l'image: {err} ")

    datas = [upc, title, price_notax, price_tax, availability, description, category, rating, img]

    return datas


def categ_to_scrape(base_url, categ):
    filecsv = categ + ".csv"
    with open(filecsv, 'a') as f:

        nb = 0

        # URL de la première page de la catégorie de livres
        url = base_url + 'index.html'

        basik_url = 'https://books.toscrape.com/catalogue'

        # Boucle pour parcourir toutes les pages de livres
        while url:

            soup = bs_get(url)

            # Récupération des informations de chaque livre sur la page
            books = soup.select('article.product_pod')
            for book in books:
                url_book = basik_url + book.h3.a['href'][8:]
                nb += 1
                datas = scrape_url(url_book)
                writer = csv.writer(f)
                writer.writerow(datas)

            # Récupération du lien de la page suivante
            next_page = soup.select_one('li.next a')
            if next_page:
                # Construction de l'URL absolue de la page suivante
                url = base_url + next_page['href']
            else:
                url = None

        print(nb)


def main():
    base_url = 'http://books.toscrape.com/'
    soup = bs_get(base_url)
    # Récupération des liens de chaque catégorie sur la page d'accueil
    category_links = soup.select('ul.nav-list > li > ul > li > a')

    for category_link in category_links:
        categ = category_link.get_text().strip()
        url = base_url + category_link['href']
        # print(url)
        categ_to_scrape(url[:-10], categ)


if __name__ == "__main__":
    main()
