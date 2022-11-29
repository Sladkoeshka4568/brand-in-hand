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



start_time = time.time()
def size_filter(a):
    num_list = []
    num = ''
    for char in a:
        if char.isdigit():
            num = num + char
        else:
            if num != '':
                num_list.append(int(num))
                num = ''
                if num != '':
                    num_list.append(int(num))
    return num_list
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
                if 'https://brand-in-hand.ru/krossovki/krossovki-muzhskie' in url:
                    name_file = 'male'
                else:
                    name_file = 'female'


                if '%D0%9B%D0%B5%D1%82%D0%BE' in url:
                    season = 'summer'
                elif '%D0%97%D0%B8%D0%BC%D0%B0' in url:
                    season = 'winter'
                elif '%D0%94%D0%B5%D0%BC%D0%B8%D1%81%D0%B5%D0%B7%D0%BE%D0%BD' in url:
                    season = 'demi'


                data.append({
                    'manufacturer': text[-5].split(':')[1].strip(),
                    'name': text[-4],
                    'vendor code': text[-3].split(':')[1].strip(),
                    'price': text[-2].replace(' ', '').split('.')[0],
                    'image': image,
                    'size': size_filter(size),
                    'link': link,
                    'sex': name_file,
                    'season':  season
                })

            with open(f'{name_file}_{season}_sneakers_data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            driver.find_element(By.CSS_SELECTOR, f'[data-page="{lst}"]').click()

    except Exception as ex:
        print(ex)

    finally:
        driver.quit()
        print("--- %s seconds ---" % (time.time() - start_time))




def main():
    while True:

        url_female_demi = 'https://brand-in-hand.ru/krossovki/krossovki-zhenskie/#?page=1&attribute=2_%D0%94%D0%B5%D0%BC%D0%B8%D1%81%D0%B5%D0%B7%D0%BE%D0%BD&price_min=1450.0000&price_max=9900.0000'
        parser(url_female_demi)
        source_path_female_demi = "female_demi_sneakers_data.json"
        dest_path_female_demi = "filters/female_demi_sneakers_data.json"
        os.replace(source_path_female_demi, dest_path_female_demi)
        time.sleep(30)

        url_female_summer = 'https://brand-in-hand.ru/krossovki/krossovki-zhenskie/#?page=1&attribute=2_%D0%9B%D0%B5%D1%82%D0%BE&price_min=1450.0000&price_max=9900.0000'
        parser(url_female_summer)
        source_path_female_summer = "female_summer_sneakers_data.json"
        dest_path_female_summer = "filters/female_summer_sneakers_data.json"
        os.replace(source_path_female_summer, dest_path_female_summer)
        time.sleep(30)

        url_female_winter = 'https://brand-in-hand.ru/krossovki/krossovki-zhenskie/#?page=1&attribute=2_%D0%97%D0%B8%D0%BC%D0%B0&price_min=1450.0000&price_max=9900.0000'
        parser(url_female_winter)
        source_path_female_winter = "female_winter_sneakers_data.json"
        dest_path_female_winter = "filters/female_winter_sneakers_data.json"
        os.replace(source_path_female_winter, dest_path_female_winter)
        time.sleep(30)






        url_male_demi = 'https://brand-in-hand.ru/krossovki/krossovki-muzhskie/#?page=1&attribute=2_%D0%94%D0%B5%D0%BC%D0%B8%D1%81%D0%B5%D0%B7%D0%BE%D0%BD&price_min=1370.0000&price_max=11390.0000'
        parser(url_male_demi)
        source_path_male_demi = "male_demi_sneakers_data.json"
        dest_path_male_demi = "filters/male_demi_sneakers_data.json"
        os.replace(source_path_male_demi, dest_path_male_demi)
        time.sleep(30)

        url_male_summer = 'https://brand-in-hand.ru/krossovki/krossovki-muzhskie/#?page=1&attribute=2_%D0%9B%D0%B5%D1%82%D0%BE&price_min=1370.0000&price_max=11390.0000'
        parser(url_male_summer)
        source_path_male_summer = "male_summer_sneakers_data.json"
        dest_path_male_summer = "filters/male_summer_sneakers_data.json"
        os.replace(source_path_male_summer, dest_path_male_summer)
        time.sleep(30)

        url_male_winter = 'https://brand-in-hand.ru/krossovki/krossovki-muzhskie/#?page=1&attribute=2_%D0%97%D0%B8%D0%BC%D0%B0&price_min=1370.0000&price_max=11390.0000'
        parser(url_male_winter)
        source_path_male_winter = "male_winter_sneakers_data.json"
        dest_path_male_winter = "filters/male_winter_sneakers_data.json"
        os.replace(source_path_male_winter, dest_path_male_winter)
        time.sleep(30)







        time.sleep(10800)



if __name__ == '__main__':
    main()

