from data_handler import DataSheetHandler
from browserhandler import BrowserHandler
import time


def main():
    URL = 'https://bblms.kfu.edu.sa/'
    browser = BrowserHandler()
    data_handler = DataSheetHandler()
    file_path = "users.xlsx"

    users = data_handler.parse_excel_sheet(file_path=file_path, username_col="college no", password_col='college pass')

    for username , password in users.items():
        
        # check if this account is correct
        if not browser.login_to(url=URL, username=username, password=password):
            print("This Account Incorrect... ")
            print("Skipping... ")
            data_handler.report_to_csv(file_path="UserAccounts.csv", username=username, data="this account is incorrect")
            continue
        errors_in_audio = []

        # get all the subjects in this account
        subjects = browser.get_subjects()
        for subject_label , subject_url in subjects.items():
            
            # get the urls of the classes of this subject
            classes_urls = browser.get_classes_links(subject_url=subject_url, number=3)
            for class_url in classes_urls:
            
                #get all lectures in this class
                lectures_urls = browser.get_lectures(link=class_url)
                for lecture_url in lectures_urls : 

                    # cheack if the audio of this lecture is work if not will watch it video
                    if not browser.listen_to_audio(lecture_url['link']):
                            browser.watch_video(lecture_url['link'])
                            errors_in_audio.append(f"{subject_label} : {lecture_url["label"]}")
        data_handler.report_to_csv(file_path="LecturesErrors.csv",username=username, data=errors_in_audio)
        browser.logout()
        time.sleep(2)

if __name__ == "__main__":
    main()