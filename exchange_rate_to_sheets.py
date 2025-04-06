import os
import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from banamex_scraper import get_dollar_rate
from supabase_client import save_exchange_rates

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = "TRM!A:C"  # Updated to include Column C for EUR


def update_sheets(usd_rate, eur_rate, bank):
    print(f"Updating sheets with rates from {bank}: USD={usd_rate}, EUR={eur_rate}")
    try:
        # Load credentials from service account file
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

        service = build("sheets", "v4", credentials=creds)

        # Prepare the data
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        adjusted_usd = round(float(usd_rate) + 0.50, 4)  # Adding 0.50 to USD rate
        adjusted_eur = round(float(eur_rate) + 0.50, 4)  # Adding 0.50 to EUR rate
        values = [[today, adjusted_usd, adjusted_eur]]

        # Debugging: Print values to ensure correct structure
        print(f"Appending values: {values}")

        body = {"values": values}

        # Append the data to the sheet
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()

        print(f"Data updated successfully: {today} - USD: {adjusted_usd} - EUR: {adjusted_eur}")

        # Guardar en Supabase
        save_exchange_rates(usd_rate, eur_rate, bank)

        return True

    except HttpError as error:
        print(f"An error occurred: {error}")
        return False


if __name__ == "__main__":
    usd, eur, bank = get_dollar_rate()
    if usd and eur:
        update_sheets(usd, eur, bank)
    else:
        print("Failed to fetch exchange rates")
