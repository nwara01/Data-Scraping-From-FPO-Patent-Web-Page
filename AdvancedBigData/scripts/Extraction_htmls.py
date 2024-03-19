import requests
from bs4 import BeautifulSoup


def extract_html_urls_from_page(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            html_urls = set()

            for link in soup.find_all('a', href=True):
                href = link['href']

                if href.endswith('html'):
                    html_urls.add(href)

            return html_urls
        else:
            print("Failed to fetch page:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None


all_html_urls = [] #liste qui va contenir tous les liens html

#extraction de tous les lien html
for i in range(3,100):
    html_urls = extract_html_urls_from_page("https://www.freepatentsonline.com/result.html?p="+str(i)+"&sort=relevance&srch=top&query_txt=portable+sensors+for+plants&patents_us=on")
    html_urls = [html_url for html_url in html_urls if not any(substring in html_url for substring in ["services", "register", "tools", "contact", "privacy", "search"])]
    all_html_urls.extend(html_urls)
    print("HTML URLs found on all pages till now:" ,len(all_html_urls))
    

#stocker les liens html dans un fichier text ("text.txt")
with open('text.txt', 'w') as file:
    for html in all_html_urls :
        file.write("https://www.freepatentsonline.com"+html+"\n")
        print("the html link "+html+" is printed to the file")

