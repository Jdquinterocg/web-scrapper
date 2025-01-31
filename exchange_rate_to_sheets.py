from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from banamex_scraper import get_dollar_rate

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'  # You'll need to replace this
RANGE_NAME = 'Sheet1!A:C'  # Updated to include Column C for EUR

def update_sheets(rate_usd, rate_eur):
    print(rate_usd, rate_eur)
    try:
        # Load credentials from service account file
        creds = Credentials.from_service_account_file(
            'credentials.json',
            scopes=SCOPES
        )

        service = build('sheets', 'v4', credentials=creds)
        
        # Prepare the data
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        adjusted_eur = round(float(rate_eur) + 0.50, 4)  # Adding 0.50 to EUR rate
        values = [[today, rate_usd, adjusted_eur]]
        
        # Debugging: Print values to ensure correct structure
        print(f"Appending values: {values}")
        
        body = {
            'values': values
        }

        # Append the data to the sheet
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()

        print(f"Data updated successfully: {today} - USD: {rate_usd} - EUR: {adjusted_eur}")
        return True

    except HttpError as error:
        print(f"An error occurred: {error}")
        return False

if __name__ == "__main__":
    rate_usd, rate_eur = get_dollar_rate()
    if rate_usd and rate_eur:
        update_sheets(rate_usd, rate_eur)
    else:
        print("Failed to fetch exchange rates") 