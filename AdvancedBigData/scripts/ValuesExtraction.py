import json
import re
import requests
from bs4 import BeautifulSoup

def extract_values_from_webpage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            fixed_width_div = soup.find('div', class_='fixed-width document-details-wrapper')
            if fixed_width_div:
                disp_doc2_divs = fixed_width_div.find_all('div', class_='disp_doc2')
                values = {}

                for disp_doc2_div in disp_doc2_divs:
                    disp_elm_title_div = disp_doc2_div.find('div', class_='disp_elm_title')
                    disp_elm_text_div = disp_doc2_div.find('div', class_='disp_elm_text')

                    if disp_elm_title_div and disp_elm_text_div:
                        title_text = disp_elm_title_div.get_text().strip()
                        text_text = disp_elm_text_div.get_text().strip()
                        values[title_text] = text_text
                    elif not disp_elm_title_div and disp_elm_text_div:
                        id_text = disp_elm_text_div.get_text().strip()
                        patent_pattern = re.search(r'(.+?)\s+Patent\s+\d{5,}', id_text)
                        if patent_pattern:
                            values["ID"] = patent_pattern.group()
                            #break
 

                return values
            else:
                print(f"No div with class='fixed-width document-details-wrapper' found in the webpage {url}")
        else:
            print(f"Failed to retrieve the webpage ({url}). Status code:", response.status_code)
    except requests.RequestException as e:
        print(f"An error occurred while processing ({url}):", e)
    return None

def process_url1(url):
    try:
        data = extract_values_from_webpage(url)
        if data is None:
            print("data is none")
            return   
        #print(data)
        words = []
        transformed_patent_number = ""
        number=""
        initials=""
        if data.get("ID") is not None and data.get("ID") != "":
            words = data.get("ID").split()
            initials = ''.join(word[0] for word in words if word.isalpha())
            number = ''.join(filter(str.isdigit, words))
            transformed_patent_number = (initials.upper()[:2] + number)

        if data.get("Title:") is not None and data.get("Title:").strip() != "":
            extracted_data = {
                'title': data.get("Title:").strip(),
                'inventors': [part.strip() for part in data.get("Inventors:").split('\n') if part.strip()],
                'description': [part.strip() for part in data.get("Abstract:").split('\n') if part.strip()],
                'publication_date': data.get("Publication Date:").strip(),
                'country': words[0]+" "+words[1] if words else "",
                'current_assignees': data.get('Assignee:').strip(),
                'pdf_link': url.strip(),
                'ID': transformed_patent_number,
                'application date': data.get("Filing Date:").strip(),
                'claims': [part.strip() for part in data.get("Claims:").split('\n') if part.strip()],
            }

            with open(f'metadata.json', 'a', encoding='utf-8') as json_file:
                json_file.write(json.dumps(extracted_data, ensure_ascii=False, indent=4))
                json_file.write(",\n")
    except Exception as e:
        print("OOps")

def extract_values_from_webpage2(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            container_fluid_div = soup.find('div', class_='container-fluid')
            if container_fluid_div:
                fixed_width_div = container_fluid_div.find('div', class_='fixed-width document-details-wrapper')
                if fixed_width_div:
                    disp_doc2_divs = fixed_width_div.find_all('div', class_='disp_doc2')
                    values = {}
                    first_found = False
                    for disp_doc2_div in disp_doc2_divs:
                        disp_elm_text_div = disp_doc2_div.find('div', class_='disp_elm_text')
                        disp_elm_title_div = disp_doc2_div.find('div', class_='disp_elm_title')

                        if disp_elm_title_div and disp_elm_text_div:
                            title_text = disp_elm_title_div.get_text().strip()
                            text_text = disp_elm_text_div.get_text().strip()
                            values[title_text] = text_text

                        if disp_elm_text_div and not disp_elm_title_div:
                            float_left_divs = disp_elm_text_div.find_all('div', class_='float_left')
                            labels = soup.find_all('label', class_='float_left')
                            for label in labels:
                                extracted_text0 = label.get_text().strip()
                                values["ID1"]=extracted_text0
                            for float_left_div in float_left_divs:
                                extracted_text = float_left_div.get_text().strip()
                                if 'Kind' in extracted_text or 'Code' in extracted_text:
                                    continue
                                if not first_found:
                                    values["ID2"] = extracted_text
                                    first_found = True
                                
                                else:
                                    break 

                    return values
                else:
                    print(f"No div with class='fixed-width document-details-wrapper' found in the webpage {url}")
            else:
                print(f"No div with class='container-fluid' found in the webpage {url}")
                #values = extract_values_from_webpage(url)
                #return  values
        else:
            print(f"Failed to retrieve the webpage ({url}). Status code:", response.status_code)
    except requests.RequestException as e:
        print(f"An error occurred while processing ({url}):", e)
    return None

def process_url2(url):
    try:
        data = extract_values_from_webpage2(url)
        if data is None:
            return 

        words = []
        #transformed_patent_number=""
        initials=""
        number=""
        if data.get("ID1") is not None and data.get("ID1") != "":
            words = data.get("ID1").split()
            filtered_words = [word for word in words if word.lower() not in ["Patent", "Application"]]

            initials = ''.join(word[0] for word in filtered_words if word.isalpha())
            number = ''.join(filter(str.isdigit, ''.join(filtered_words)))

            #transformed_patent_number = (initials.upper()[:2] + number)
          

        if data.get("Title:") is not None and data.get("Title:").strip() != "":
            extracted_data = {
                'title': data.get("Title:", "").strip(),
                'inventors': [part.strip() for part in data.get("Inventors:", "").split('\n') if part.strip()],
                'description': [part.strip() for part in data.get("Abstract:", "").split('\n') if part.strip()],
                'publication_date': data.get("Publication Date:", "").strip(),
                'country': words[0]+" "+words[1] if words else "",
                'current_assignees': data.get('Assignee:', "").strip(),
                'pdf_link': url.strip(),
                'ID': str(initials.upper()[:2] + number)+data.get("ID2"),
                'application_date': data.get("Filing Date:", "").strip(),
                'claims': [part.strip() for part in data.get("Claims:", "").split('\n')[:10] if part.strip()],
            }

            with open(f'metadata.json', 'a', encoding='utf-8') as json_file:
                json_file.write(json.dumps(extracted_data, ensure_ascii=False, indent=4))
                json_file.write(",\n")
    except Exception as e:
        print(f"Oops")
        with open("html.txt", "a") as html1 :
            html1.write(url+"\n")

line_number=1
with open('html.txt', 'r') as htmls:
    for line in htmls:
        
            print("************************************************")
            print(line_number)
            print(line.strip())
            process_url1(line.strip())
            line_number += 1  
#print(extract_values_from_webpage2("https://www.freepatentsonline.com/y2014/0024528.html").get("ID1"))