from bs4 import BeautifulSoup
import requests

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


def scrape_url(url_to_scrape) -> list:
    """Fonction qui reçoit une URL en paramètre et qui retourne une liste contenant l'ensemble des éléments demandés"""
    soup = bs_get(url_to_scrape)

    # Recuperation des different donnes demandées et stockage dans des variables
    upc = soup.find('th', string='UPC').find_next_sibling('td').get_text()
    title = soup.find('h1').get_text()
    price_notax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').get_text()
    price_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').get_text()
    availability = soup.find('th', string='Availability').find_next_sibling('td').get_text()
    description = soup.find('div', id='product_description').find_next('p').get_text()
    category = soup.select('.breadcrumb > li > a')[-1].get_text()
    rating_init = soup.find('p', class_='star-rating')  # Renvoie tout le code HTML
    rating_class = rating_init['class']  # Je récupère le nom de la classe qui est en fait une liste
    rating = rating_class[1]  # Je récupère le second élément de la liste
    img = 'http://books.toscrape.com/' + soup.select('img')[0]['src']

    nom_img = category + "_" + title + ".jpg"
    try:
        load_img(img, nom_img)
    except Exception as err:
        print(f"Une erreur est survenue dans le téléchargement de l'image: {err} ")

    datas = [upc, title, price_notax, price_tax, availability, description, category, rating, img]

    return datas


def main():
    url_to_scrape = 'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'
    print(scrape_url(url_to_scrape))


if __name__ == "__main__":
    main()
