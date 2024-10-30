import requests
from bs4 import BeautifulSoup
import html

def wiki_artykul(nazwa):

    url = f'https://pl.wikipedia.org{nazwa}'

    response = requests.get(url)

    if response.status_code == 200:
        
        html_content = response.text

        full = []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        main_div = soup.find("div", class_="mw-body-content")

        # Nazwy artykułów do których prowadzą odnośniki (wewnętrzne) w artykule wraz z treścią odnośników (pierwsze 5)
        wew = [a['title'] for a in main_div.find_all('a', href=True) 
                if a['href'].startswith('/wiki/') and ':' not in a['href'][6:]][:5]
        
        wew_full = " | ".join(wew)
        full.append(wew_full)

        # Adresy URL wykorzystanych obrazków (pierwsze 3)
        all_img = main_div.find_all("img")
        img_src = [link["src"] for link in all_img if '/wiki/' not in link['src']][:3]
        if len(img_src) > 0:
            img_full = " | ".join(img_src)
        else:
            img_full = ""
        
        full.append(img_full)

        # # Adresy URL źródeł (zewnętrzne) (pierwsze 3)
        refs_div = soup.find("div", class_="mw-references-wrap mw-references-columns")
        if refs_div == None:
            refs_div = soup.find("div", class_="do-not-make-smaller refsection")

        if refs_div != None:
            refs_a = refs_div.find_all("li")
            hrefs = [a['href'] for ref in refs_a for span in ref.find_all("span", class_="reference-text") for a in span.find_all("a", href=True) if "http" in a['href']][:3]
            
            hrefs_escaped = [html.escape(href) for href in hrefs]
            hrefs_full = " | ".join(hrefs_escaped)
        else:
            hrefs_full = ""

        full.append(hrefs_full)

        # # Nazwy przypisanych kategorii do artykułu (pierwsze 3)
        kat_div = soup.find("div", class_="mw-normal-catlinks")
        ul = kat_div.find('ul')
        kategorie = [kats.text.strip() for kats in ul.find_all("a")[:3]]

        kategorie_full = " | ".join(kategorie)

        full.append(kategorie_full)

        return full

    else:
        print("Błąd podczas pobierania strony:", response.status_code)

def main():

    slowo = input().replace(" ", '_')

    base = 'https://pl.wikipedia.org/wiki/Kategoria:'
    url = base+slowo
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        main_div = soup.find("div", class_="mw-category mw-category-columns")
        all_a = main_div.find_all("a")
        hrefs = [link["href"] for link in all_a[:2]]

        for i in hrefs:
            for j in wiki_artykul(i):
                print(j)

    else:
        print("Błąd podczas pobierania strony:", response.status_code)

main()

#   Miasta na prawach powiatu
#   Państwa członkowskie Unii Europejskiej
#   Python
#   Biblioteki Pythona