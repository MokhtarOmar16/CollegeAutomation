from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrowserHandler:
    def __init__(self):
        self.driver = webdriver.Firefox(options=self.get_webdriver_options())
    

    def get_webdriver_options(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--incognito")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")

        return options

    def login_to(self,url: str,username: str,password: str) -> bool:
        """
        This method is designed to login into your url using the username and password 
        """


        self.driver.get(url)

        username_field = self.driver.find_element(By.XPATH, '//*[@id="user_id"]')
        username_field.send_keys(username)

        password_field = self.driver.find_element(By.XPATH, '//*[@id="password"]')
        password_field.send_keys(password)

        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'تسجيل الدخول')]")
        login_button.click()

        termsMsg = self.driver.find_element(By.XPATH, '//*[@id="btnYes"]')
        termsMsg.click()
        time.sleep(3)

        return self.is_account_correct(username,password)
            
        

    def is_account_correct(self,username,password):
        """
        Valdator For The Account
        """
        try:
            wait = WebDriverWait(self.driver, 3)
            wait.until(lambda driver: driver.current_url == "https://bblms.kfu.edu.sa/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1")
        except Exception:
            print(f"This {username} , {password} are wrong , Skipping...")

            return False

        try:
            termsMsg = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="agree_button"]'))
            )
            termsMsg.click()

        except:
            pass
        return True


    def get_subjects(self) -> dict:
        """
            Retrieve a dictionary of subjects and their corresponding URLs.

            Returns:
            dict: A dictionary where keys are the names of subjects and values are their associated URLs.

            Example:
            If there are subjects like {'Math': 'https://math-subject.com', 'History': 'https://history-subject.com'},
            the returned dictionary would be {'Math': 'https://math-subject.com', 'History': 'https://history-subject.com'}.
        """


        ul = self.driver.find_element(By.CSS_SELECTOR, '.portletList-img.courseListing.coursefakeclass')
        li = ul.find_elements(By.TAG_NAME, 'li')
        links = {}
        for element in li:
            links[element.find_element(By.TAG_NAME, 'a').text]= element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        return links


    def get_classes_links(self,number:int = 0) -> list:
        
        """
            Get a list of class links.

            :param number: The last index of the list. By default, it is set to zero.
            :type number: int

            :return: A list of class links.
            :rtype: list
        """
        
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'courseMenuPalette_contents'))
        )
        self.driver.get(element.find_elements(By.TAG_NAME, 'li')[8].find_element(
            By.TAG_NAME, 'a').get_attribute('href'))

        ul = WebDriverWait(self.driver, 10).until(
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
        return links[-number:]


    def get_lectures(self, link:str) -> list:
        """
            Get a list of links associated with a specific  subject.

            :param link: link or url of the subject.
            :type subject_code: str

            :return: A list of links associated with the scientific subject.
            :rtype: list
        """
        self.driver.get(link)
        ul = self.driver.find_element(By.XPATH, '//*[@id="content_listContainer"]')
        li = ul.find_elements(By.TAG_NAME, 'li')
        li = li[1:-1]
        links = []

        for element in li:

            try:
                div = element.find_element(By.CSS_SELECTOR, '.item.clearfix')
                link_of_video = div.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('href')
                label_of_video = div.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME,'span').text
                links.append({"link": link_of_video, "label": label_of_video})
            except Exception as e:
                pass
        return links
    

    def video(self ,link:str) -> None:
        """
            Listen to the video associated with a specific lesson or lecture.

            :param link: The link or identifier of the lesson or lecture.
            :type link: str

            :return: None.
            :rtype: None
        """
        self.driver.get(link)
        self.driver.get(self.driver.find_element(By.ID, 'content_listContainer').find_elements(By.TAG_NAME, 'li')[3].find_element(By.TAG_NAME, 'a').get_attribute('href'))

        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )

        while True:
            current_time = self.driver.execute_script("return arguments[0].currentTime", element)
            if current_time >= 6 :
                break
            time.sleep(1)

    
    
    def listen_to_audio(self ,link:str)-> bool:
        """
            Listen to the audio associated with a specific lesson or lecture.

            :param link: The link or identifier of the lesson or lecture.
            :type link: str

            :return: True if the audio was successfully listened to for 5 seconds, False if the audio dose not exist.
            :rtype: bool
        """
        try:
            self.driver.get(link)


            self.driver.get(self.driver.find_element(By.ID, 'content_listContainer').find_elements(By.TAG_NAME, 'li')[2].find_element(By.TAG_NAME, 'a').get_attribute('href'))
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )

            while True:
                current_time = self.driver.execute_script("return arguments[0].currentTime", element)
                if current_time >= 6:
                    break
                time.sleep(1)
            return True
        except Exception as e:
            return False
    
    def logout(self):
        """
            Logout from the educational platform.

            This method navigates to the main page of the educational platform and performs the logout action.

            Returns:
            None

            Example:
            If the user is currently logged in, calling this method will navigate to the main page
            and perform the logout action, ending the user's session.

            Note:
            This method assumes that the educational platform's main page URL is 'https://bblms.kfu.edu.sa/'
            and that the logout element has the ID 'topframe.logout.label'.
        """
        self.driver.get('https://bblms.kfu.edu.sa/')
        self.driver.find_element(By.ID, "topframe.logout.label").click()


