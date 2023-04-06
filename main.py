from bs4 import BeautifulSoup
import requests
from slugify import slugify
import csv
from pathlib import Path
import os

session = requests.session()


def bs_get(url_to_scrape):
    """Fonction qui reçoit une URL en paramètre et qui retourne un objet BeautifulSoup"""
    try:
        response = session.get(url_to_scrape)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except Exception as err:
        print(f"Une erreur est survenue : {err} ")


def load_img(img, nom_img, categ):
    """Fonction qui télécharge l'image d'une URL donnée et la stock dans le répertoire courant"""
    response = session.get(img)
    file_img = os.path.join(slugify(categ, separator="_"), nom_img)
    with open(file_img, "wb") as f:
        f.write(response.content)


def load_csv(csv_path: str, books_datas: list):
    """Fonction qui reçoit en paramètre le chemin du fichier CSV à créer et la liste des dictionnaires contenant les
    données à écrire, et qui écrit ces données dans le fichier CSV"""
    champs = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax',
              'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    with open(csv_path, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(books_datas)


def convert_rating(txt):
    """Fonction qui convertit le texte de la classe de l'élément HTML en nombre"""
    ratings = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    return ratings.get(txt, 0)


def convert_stock(txt: str) -> int:
    """Fonction qui convertit le texte de la quantité en stock en nombre"""
    stock = ""
    for char in txt:
        if char.isdigit():
            stock += char

    if stock:
        stock = int(stock)
        return stock
    else:
        return 0


def scrape_url(url_to_scrape: str) -> dict:
    """Fonction qui reçoit une URL en paramètre et qui retourne un dictionnaire contenant
    l'ensemble des éléments demandés"""
    soup = bs_get(url_to_scrape)
    if soup is None:
        exit()
    datas = {}
    # Recuperation des different donnes demandées et stockage dans des variables
    datas['product_page_url'] = url_to_scrape
    datas['universal_product_code'] = soup.find('th', string='UPC').find_next_sibling('td').get_text()
    title = soup.find('h1').get_text()
    datas['title'] = title
    datas['price_including_tax'] = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').get_text()
    datas['price_excluding_tax'] = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').get_text()

    datas['number_available'] = convert_stock(soup.find('th', string='Availability').find_next_sibling('td').get_text())
    try:
        datas['product_description'] = soup.find('div', id='product_description').find_next('p').get_text()
    except:
        datas['product_description'] = "Ce livre n'a pas de description"
    category = soup.select('.breadcrumb > li > a')[-1].get_text()
    datas['category'] = category
    rating_init = soup.find('p', class_='star-rating')  # Renvoie tout le code HTML
    rating_class = rating_init['class']  # Je récupère le nom de la classe qui est en fait une liste
    datas['review_rating'] = convert_rating(rating_class[1])  # Je récupère le second élément de la liste
    img = 'http://books.toscrape.com/' + soup.select('img')[0]['src']
    datas['image_url'] = img

    nom_img = slugify(title, separator="_") + ".jpg"
    try:
        load_img(img, nom_img, category)
    except Exception as err:
        print(f"Une erreur est survenue dans le téléchargement de l'image: {err} ")

    return datas


def get_books_from_category(base_url: str, category_name: str):
    """Fonction qui parcourt toutes les pages d'une catégorie et extrait les informations de chaque livre"""
    print(f'Récupération de la catégorie {category_name} en cours. Veuillez patitenter...')
    csv_path = os.path.join(slugify(category_name, separator="_"), f'{category_name}.csv')
    books_datas = []

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
            data = scrape_url(url_book)
            books_datas.append(data)

        # Récupération du lien de la page suivante
        next_page = soup.select_one('li.next a')
        if next_page:
            # Construction de l'URL absolue de la page suivante
            url = base_url + next_page['href']
        else:
            url = None

    load_csv(csv_path, books_datas)
    print(f'Catégorie {category_name} récupérée.')


def main():
    """Fonction principale"""
    base_url = 'http://books.toscrape.com/'
    soup = bs_get(base_url)
    # Récupération des liens de chaque catégorie sur la page d'accueil
    category_links = soup.select('ul.nav-list > li > ul > li > a')

    for category_link in category_links:
        category_name = category_link.get_text().strip()
        categ_slugged = slugify(category_name, separator="_")
        directory = Path(f'./{categ_slugged}')
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

        url = base_url + category_link['href']
        get_books_from_category(url[:-10], category_name)


if __name__ == "__main__":
    main()
    print("Fin d'exécution du programme")
