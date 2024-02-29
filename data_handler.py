import pandas as pd


class DataSheetHandler:
    def parse_excel_sheet(self, file_path: str, username_col: str, password_col: str) -> dict:
        """
            Parse login credentials from an Excel sheet.

            :param file_path: Path to the Excel file.
            :type file_path: str

            :param username_col: Column name for usernames.
            :type username_col: str

            :param password_col: Column name for passwords.
            :type password_col: str

            :return: A dictionary containing login credentials.
            :rtype: dict
        """
        
        data = pd.read_excel(file_path)

        usernames = data[username_col].tolist()
        passwords = data[password_col].tolist()

        
        login_data = dict(zip(usernames, passwords))

        return login_data


    def report_to_csv(self, file_path: str, username: str, data: list | str) -> None:
        """
            Append or create a CSV file with a new entry for the given username and interaction data.

            :param file_path: The path to the CSV file.
            :type file_path: str
            :param username: The username associated with the report.
            :type username: str
            :param data: The interaction data to be reported.
            :type data: list | str
            :return: None
            :rtype: None

            This method attempts to read the existing CSV file at the specified path. If the file exists,
            it appends a new entry with the provided username and interaction data. If the file does not
            exist, it creates a new CSV file with the entry.

            Example:
            ```python
            handler = DataSheetHandler()
            handler.report_to_csv("path/to/report.csv", "john_doe", ["error", "audio issue"])
            ```
        """

        report_data = {username: data}
        try:
            df = pd.read_csv(file_path)
            df_new = pd.DataFrame(report_data)
            merged_df = pd.concat([df, df_new], axis=1)
            merged_df.to_csv(file_path, index=False, encoding="utf-8-sig")
        except FileNotFoundError:
            df = pd.DataFrame(report_data)
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
