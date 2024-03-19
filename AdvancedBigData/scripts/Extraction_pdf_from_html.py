import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pyautogui

import requests
from bs4 import BeautifulSoup

def extract_pdf_from_html(url):
    pdf_link = ""  # Initialize pdf_link variable
    try:
        response = requests.get(str(url), allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.endswith('.pdf'):
                    pdf_link = href
                    break
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
    except requests.RequestException as e:
        print("An error occurred:", e)

    return str(pdf_link)


    
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

i=1
# Open the input file ('text.txt') and the output file ('text2.txt')
with open('html_links.txt', 'r') as input_file, open('pdf_links.txt', 'a') as output_file:
    # Read each line in the input file
    for line in input_file:
        # Call extract_pdf_from_html and write the result to the output file
        var =  extract_pdf_from_html(line.strip())
        try:
            output_file.write("https://www.freepatentsonline.com" + var + '\n')
            print(var,"was added to the text2 successfully")
            print(i)
            i=i+1
        except Exception as e :
            print(e)














