import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
import time
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import shutil
from os import path
from threading import Thread

start_time = time.time()

def parser(url):
    try:
        data = []
        ua = dict(DesiredCapabilities.CHROME)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
        # driver = webdriver.Chrome(chrome_options=options)

        wait = WebDriverWait(driver, 20, StaleElementReferenceException)
        driver.get(url=url)
        time.sleep(5)
        len_str = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[2]').text.split(' ')[-2]

        for lst in range(2, int(len_str)+1):

            print('___________________', lst-1, '___________________')
            time.sleep(2)
            for i in range(1, 13):
                move = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[2]/div[{i}]/div/div[2]/div[1]/p[4]')))
                webdriver.ActionChains(driver).move_to_element(move).perform()
                image = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[2]/div[{i}]/div/div[1]/a/img'))).get_attribute('src')
                link = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="content"]/div/div[2]/div[{i}]/div/div[1]/a'))).get_attribute('href')
                try:
                    text = driver.find_element(By.XPATH, f'//*[@id="content"]/div/div[2]/div[{i}]').get_attribute('innerText').split('\n\n')
                    print(text)
                    print(len(text))
                    if text[0] == '%':
                        text = text.remove('%')
                    if len(text) <= 4:


                        time.sleep(15)
                        move = wait.until(EC.visibility_of_element_located(
                            (By.XPATH, f'//*[@id="content"]/div/div[2]/div[{i}]/div/div[2]/div[1]/p[4]')))

                        webdriver.ActionChains(driver).move_to_element(move).perform()

                        text = driver.find_element(By.XPATH, f'//*[@id="content"]/div/div[2]/div[{i}]').get_attribute(
                            'innerText').split('\n\n')
                        size = text[-1].split('\n')[1]
                    else:
                        size = text[-1].split('\n')[1]
                except:
                    continue

                data.append({
                    'manufacturer': text[-5].split(':')[1].strip(),
                    'name': text[-4],
                    'vendor code': text[-3].split(':')[1].strip(),
                    'price': text[-2].replace(' ', '').split('.')[0],
                    'image': image,
                    'size': size.split(' '),
                    'link': link
                })
            if 'https://brand-in-hand.ru/krossovki/krossovki-muzhskie' in url:
                name_file = 'male'
            else:
                name_file = 'female'
            with open(f'{name_file}_sneakers_data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            driver.find_element(By.CSS_SELECTOR, f'[data-page="{lst}"]').click()

    except Exception as ex:
        print(ex)

    finally:
        driver.quit()
        print("--- %s seconds ---" % (time.time() - start_time))




def main():
    while True:

        url_female = 'https://brand-in-hand.ru/krossovki/krossovki-zhenskie/#?page=1&price_min=1450.0000&price_max=9900.0000'
        parser(url_female)
        source_path_female = "female_sneakers_data.json"
        time.sleep(60)
        url_male = 'https://brand-in-hand.ru/krossovki/krossovki-muzhskie/#?page=1&price_min=1370.0000&price_max=11390.0000'
        parser(url_male)
        source_path_male = "male_sneakers_data.json"





        destination_path = "filters"
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'filters/female_sneakers_data.json')
        os.remove(path)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'filters/male_sneakers_data.json')
        os.remove(path)
        shutil.move(source_path_female, destination_path)
        shutil.move(source_path_male, destination_path)
        time.sleep(10800)



if __name__ == '__main__':
    main()

