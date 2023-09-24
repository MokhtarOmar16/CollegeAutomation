from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from random import randint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import pyfiglet
import os

def get_Chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach",True)
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless")
    return options


# getting data from sheet
def data():
    data = pd.read_excel('users.xlsx')
    collage_numbers = data['الرقم الجامعي'].tolist()
    paswordat = data['الرقم السري'].tolist()
    usernames = collage_numbers
    passwords = paswordat
    login_data = zip(usernames, passwords)
    return dict(login_data)


# le.py >>>
def login(driver, username, password):
    driver.get(url)

    username_field = driver.find_element(By.XPATH, '//*[@id="user_id"]')
    username_field.send_keys(username)

    password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_field.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'تسجيل الدخول')]")
    login_button.click()

    accept1 = driver.find_element(By.XPATH, '//*[@id="btnYes"]')
    accept1.click()
    time.sleep(3)


def get_subject(driver):
    ul = driver.find_element(By.CSS_SELECTOR, '.portletList-img.courseListing.coursefakeclass')
    li = ul.find_elements(By.TAG_NAME, 'li')
    links = {}
    for element in li:
        links[element.find_element(By.TAG_NAME, 'a').text]= element.find_element(By.TAG_NAME, 'a').get_attribute('href')
    return links


# return the class of lessons
def classes_links(driver) -> list:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'courseMenuPalette_contents'))
    )
    driver.get(element.find_elements(By.TAG_NAME, 'li')[8].find_element(
        By.TAG_NAME, 'a').get_attribute('href'))

    ul = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'contentList'))
        )
    li = ul.find_elements(By.TAG_NAME, 'li')
    links = []
    del li[0:3]

    for element in li:
        try:
            div = element.find_element(By.CSS_SELECTOR, '.item.clearfix')
            link = div.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('href')
            links.append(link)
        except Exception as e:
            pass
    # print(links)
    return links


def lecture(driver, link):
    driver.get(link)
    ul = driver.find_element(By.XPATH, '//*[@id="content_listContainer"]')
    li = ul.find_elements(By.TAG_NAME, 'li')
    li = li[1:-1]
    links = []

    for element in li:

        try:
            div = element.find_element(By.CSS_SELECTOR, '.item.clearfix')
            l = div.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('href')
            s = div.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME,'span').text
            links.append({"link": l, "label": s})
        except Exception as e:
            pass
    return links


#  watch video
def video(driver ,link):

    driver.get(link)
    driver.get(driver.find_element(By.ID, 'content_listContainer').find_elements(By.TAG_NAME, 'li')[3].find_element(By.TAG_NAME, 'a').get_attribute('href'))

    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "video"))
    )

    while True:
        current_time = driver.execute_script("return arguments[0].currentTime", element)
        if current_time >= 6 :
            break
        time.sleep(1)


# listen audio
def audio(driver ,link):
    try:
        driver.get(link)


        driver.get(driver.find_element(By.ID, 'content_listContainer').find_elements(By.TAG_NAME, 'li')[2].find_element(By.TAG_NAME, 'a').get_attribute('href'))
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )

        while True:
            current_time = driver.execute_script("return arguments[0].currentTime", element)
            if current_time >= 6:
                break
            time.sleep(1)
        return True
    except Exception as e:
        return False


def logout(driver):
    driver.get('https://bblms.kfu.edu.sa/')
    driver.find_element(By.ID, "topframe.logout.label").click()


def info():
    os.system('cls')
    islam_fb = 'https://www.facebook.com/islam.badran.77/'
    mekha_fb = 'https://www.facebook.com/mokhtar.omar.961/'
    use = input("1- Islam FaceBook \n2- Mokhtar Facebook\n")
    if use == "1":
        driver = webdriver.Chrome(options=get_Chrome_options())
        driver.get(islam_fb)
    elif use == "2":
        driver = webdriver.Chrome(options=get_Chrome_options())
        driver.get(mekha_fb)


def report(username, inter):
    if inter:
        for n in range(len(inter)):
            medhet = {username: "error",
            f"{n} -": inter}
    else:
        medhet = {username: ["هذا الحساب جيد"]}

    try:
        df = pd.read_csv("REPORT.csv")
        df_new = pd.DataFrame(medhet)
        merged_df = pd.concat([df, df_new], axis=1)
        merged_df.to_csv("REPORT.csv", index=False, encoding="utf-8-sig")

    except FileNotFoundError:
        df = pd.DataFrame(medhet)
        df.to_csv("REPORT.csv", index=False, encoding="utf-8-sig")
def report_user(username, inter):
    medhet = {username: [inter]}
    try:
        df = pd.read_csv("REPORT-USER.csv")
        df_new = pd.DataFrame(medhet)
        merged_df = pd.concat([df, df_new], axis=1)
        merged_df.to_csv("REPORT-USER.csv", index=False, encoding="utf-8-sig")

    except FileNotFoundError:
        df = pd.DataFrame(medhet)
        df.to_csv("REPORT-USER.csv", index=False, encoding="utf-8-sig")


def main(number = 0):
    users = data()
    # users = {"221481326":"Saud#4810","223062399":"Nnnn@899"}
    for username, password in users.items():
        # print(username, password)
        driver = webdriver.Chrome(options=get_Chrome_options())
        login(driver, username, password)
        try:
            wait = WebDriverWait(driver, 3)
            wait.until(lambda driver: driver.current_url == "https://bblms.kfu.edu.sa/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1")
        except Exception:
            print(f"This {username} , {password} are wrong , Skipping...")
            driver.close()
            report_user(username,"حساب خاطيء")

            continue
        try:
            accept2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="agree_button"]'))
            )
            accept2.click()

        except:
            pass

        listError = []
        # get subjects >>>
        subjects = get_subject(driver)
        for label_S, subject in subjects.items():
            driver.get(subject)
            driver.refresh()
            for link in classes_links(driver)[-number:]:
                lectureLinks = lecture(driver, link)
                driver.refresh()
                # innerlecture يعني كسم المحاضره اللي جوا
                for innerLicture in lectureLinks:


                    if audio(driver,innerLicture['link']):
                        pass
                    else:
                        video(driver,innerLicture['link'])
                        listError.append(f"{label_S} >> {innerLicture['label']} صوت   ")

        report(username, listError)
        logout(driver)
        time.sleep(3)
        print(f"this user : {username} is done .....")
        driver.close()


if __name__ == "__main__":
    Use = input("1- DO YOU WANT TO START THE TASK ?\n2- Specific Classes ? \n3 - Info \n\n ")
    url = "https://bblms.kfu.edu.sa/"
    if Use == "1":
        try:
            main()
            print("your sheet is done")
            print("get a good day :)")
            time.sleep(5400)

        except Exception as ex:
            print(ex)
    elif Use == "2":
        os.system('cls')
        time.sleep(1)
        x = int(input('Enter The Number Of Classes : \n'))
        main(x)
    else:
        info()
    os.system('cls')
    time.sleep(1)