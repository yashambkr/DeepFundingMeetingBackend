from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

def get_google_sheet_data():
    # Set up Google Sheets API credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('appscript.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Spreadsheet using its title
    spreadsheet = client.open('deep_funding_meeting_execl')
    
    # Select the desired sheet
    sheet = spreadsheet.sheet1  # You may need to change this to the correct sheet

    # Get all values from the sheet
    values = sheet.get_all_values()

    # Convert the data into the desired format
    output = []
    headers = values[0]

    for row in values[1:]:
        row_data = dict(zip(headers, row))
        output.append(row_data)

    return output

@app.route('/api/get_sheet_data', methods=['GET'])
def api_get_sheet_data():
    data = get_google_sheet_data()
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(debug=True)