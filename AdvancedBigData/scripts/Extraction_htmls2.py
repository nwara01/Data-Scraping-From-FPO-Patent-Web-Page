import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pyautogui

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
    

def extract_pdf_from_html(url):
    pdf_link = None  # Initialize pdf_link variable
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.pdf'):
                pdf_link = href
                break
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

    return pdf_link

    
def download_pdf_with_selenium(url):
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)
        print("Waiting for the web page to load...")
        
        time.sleep(20)
        print("Web page loaded!")

        button_position = pyautogui.locateCenterOnScreen('pic.png')  
        if button_position:
            print("Button found!")
            pyautogui.click(button_position.x, button_position.y)
            print("Button clicked!")
            
            time.sleep(2)
            
            save_button_position = pyautogui.locateCenterOnScreen('save.png')  # Replace 'save.png' with the actual filename of the save button image
            
            if save_button_position:
                print("Save button found!")
                pyautogui.click(save_button_position.x, save_button_position.y)
                print("Save button clicked!")
                time.sleep(2)
            else:
                print("Unable to locate save button")
        else:
            print("Unable to locate download button")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

all_html_urls = [] #liste qui va contenir tous les liens html

#extraction de tous les lien html
for i in range(100,200):
    html_urls = extract_html_urls_from_page("https://www.freepatentsonline.com/result.html?p="+str(i)+"&sort=relevance&srch=top&query_txt=portable+sensors+for+plants&patents_us=on")
    html_urls = [html_url for html_url in html_urls if not any(substring in html_url for substring in ["services", "register", "tools", "contact", "privacy", "search"])]
    all_html_urls.extend(html_urls)
    print("HTML URLs found on all pages till now:" ,len(all_html_urls))

#stocker les liens html dans un fichier text ("text.txt")
with open('text.txt', 'a') as file:
    for html in all_html_urls :
        file.write("https://www.freepatentsonline.com"+html+"\n")
        print("the html link "+html+" is printed to the file")

