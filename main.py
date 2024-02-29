from data_handler import DataSheetHandler
from browserhandler import BrowserHandler


URL = 'https://bblms.kfu.edu.sa/'
browser = BrowserHandler()
data_handler = DataSheetHandler()
file_path = "users.xlsx"

data_handler.parse_excel_sheet(file_path=file_path, username_col="college no", password_col='college pass')
browser.login_to(url=URL, )

