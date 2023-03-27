import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figure input from the user
    """
    while True:
        print('Please enter your sales data from the last market')
        print('Data should be six numbers, seperated by commas')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Enter your data here: ')

        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print('Data is valid!')
            break
    return sales_data


def calculate_surplus_data(sales_row):
    """
    Compare sales data with stock data and calculate the surplus for each data type.

    The surplus is defined as the as the sales sigure subtracted from the stock. 
    -  Positive surplus indicates a waste. 
    -  Negative surplus indicates that extar stock was made when the stock ran out.  
    """
    print("Calculating Surplus Data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    # pprint(stock)
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row,sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def update_worksheet(data,worksheet):
    """
    Recieves a list of integers and updates worksheets accordingly
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet has been successfully updated.\n')


def validate_data(values):
    """
    Inside the try,converts all string data into integers.
    Raise ValueError if strings can not be converted into int, 
    or if there is not exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 vlaues required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True


    """
    Update surplus worksheet, adding a new row after calculations
    """
    print('Updating surplus worksheet\n')
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    print('Surplus worksheet updated successfully\n')


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    update_worksheet(new_surplus_data, "surplus") 

print('Welcome To Love Sandwiches Automation\n')
main()