from selenium import webdriver
import time
import pyautogui


def download_pdf_with_selenium(url):

    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)
        print("Waiting for the web page to load...")
        
        time.sleep(3)
        print("Web page loaded!")

        button_position = pyautogui.locateCenterOnScreen('images/pic.png')  
        if button_position:
            print("Button found!")
            pyautogui.click(button_position.x, button_position.y)
            print("Button clicked!")
            
            time.sleep(1)
            
            save_button_position = pyautogui.locateCenterOnScreen('images/save.png')  # Replace 'save.png' with the actual filename of the save button image
            
            if save_button_position:
                print("Save button found!")
                pyautogui.click(save_button_position.x, save_button_position.y)
                print("Save button clicked!")
                time.sleep(1)
            else:
                print("Unable to locate save button")
        else:
            print("Unable to locate download button")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()


with open('pdf_links_finale.txt', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        print(line.strip()) 
        download_pdf_with_selenium(line.strip())