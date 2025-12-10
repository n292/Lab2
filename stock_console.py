
from datetime import datetime
from os import path

from stock_class import Stock, DailyData
from utilities  import clear_screen, display_stock_chart, sortStocks, sortDailyData
import stock_data

def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer")
        print("1 Manage Stocks")
        print("2 Add Daily Data")
        print("3 Show Report")
        print("4 Show Chart")
        print("5 Manage Data (Save / Load / Retrieve / Import)")
        print("0  Exit")
        option = input("Choice: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)

def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks")
        print("1 Add")
        print("2 Buy / Sell")
        print("3 Delete")
        print("4 List")
        print("0 Back")
        option = input("Choice: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
            input("Press Enter to return")

def add_stock(stock_list):
    clear_screen()
    symbol = input("Ticker symbol: ").strip().upper()      

   
    if any(s.symbol == symbol for s in stock_list):
        input("That ticker is already in the portfolio — use Buy/Sell instead.  Enter")
        return
    

    name = input("Company name: ")
    try:
        shares = float(input("Initial shares: "))
    except ValueError:
        input("Invalid number. Enter to continue")
        return

    stock_list.append(Stock(symbol, name, shares))


def update_shares(stock_list):
    if not stock_list:
        input("No stocks yet. Enter"); return
    list_stocks(stock_list)
    symbol = input("Which ticker? ").upper()
    op     = input("Buy (b) or Sell (s)? ").lower()
    try:
        qty = float(input("# shares: "))
    except ValueError:
        input("Invalid number. Enter"); return

    stock = next((s for s in stock_list if s.symbol == symbol), None)
    if not stock:
        input("Symbol not found. Enter"); return
    if op.startswith("b"):
        stock.buy(qty)
    else:
        stock.sell(qty)
    input("Updated! Enter")

def delete_stock(stock_list):
    if not stock_list:
        input("Portfolio empty. Enter"); return
    list_stocks(stock_list)
    symbol = input("Delete which ticker? ").upper()
    stock_list[:] = [s for s in stock_list if s.symbol != symbol]
    input("Deleted (if it existed). Enter")

def list_stocks(stock_list):
    clear_screen()
    print("Symbol   Name                              Shares")
    print("-" * 50)
    for s in stock_list:
        print(f"{s.symbol:6}   {s.name[:30]:30}   {s.shares:9,.2f}")
    print()

def add_stock_data(stock_list):
    if not stock_list:
        input("Add a stock first. Enter"); return
    list_stocks(stock_list)
    symbol = input("Enter ticker to add data for: ").upper()
    stock  = next((s for s in stock_list if s.symbol == symbol), None)
    if not stock:
        input("Not found. Enter "); return
    try:
        date   = datetime.strptime(input("Date (m/d/yy): "), "%m/%d/%y")
        price  = float(input("Close price: "))
        volume = float(input("Volume: "))
    except Exception:
        input("Bad input. Enter"); return
    stock.add_data(DailyData(date, price, volume))
    input("Record added. Enter")


def display_report(stock_list):
    clear_screen()
    sortStocks(stock_list)
    sortDailyData(stock_list)
    if not stock_list:
        print("Portfolio Report")
        print("=================")
        print("No stocks to report.\n")
        input("Enter")
        return
    print("Portfolio Report")
    print("Symbol  Name                      Shares   Last Price     Volume    Value ($)  P/L ($)     P/L (%)")
    print("=" * 90)

    for s in stock_list:
     if s.DataList:
       
        latest = s.DataList[-1]           
        last_close = latest.close
        total_value = last_close * s.shares
        last_vol   = int(latest.volume)

     
        start_price = s.DataList[0].close
        change_per_share = last_close - start_price
        change_total     = change_per_share * s.shares
        pct_change       = (change_per_share / start_price) * 100

        print(f"{s.symbol:5}  {s.name[:24]:24} "
              f"{s.shares:8,.2f}  ${last_close:10,.2f}  "
              f"{last_vol:10,}  "
              f"${total_value:11,.2f} "
              f"${change_total:+11,.2f}  {pct_change:+8.2f}%")
     else:
            print(f"{s.symbol:5}  {s.name[:24]:24} "
              f"{s.shares:8,.2f}  (no history)")
    input("\nEnter")

def display_chart(stock_list):
    if not stock_list:
        input("No stocks. Enter"); return
    list_stocks(stock_list)
    symbol = input("Show chart for which ticker? ").upper()
    display_stock_chart(stock_list, symbol)


def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data")
        print("1  Save to DB")
        print("2  Load from DB")
        print("3  Retrieve from Web")
        print("4  Import CSV")
        print("0  Back")
        option = input("Choice: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            input("Saved. Enter")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            input("Loaded. Enter")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)

def retrieve_from_web(stock_list):
    if not stock_list:
        input("Add stocks first. Enter"); return
    dateFrom = input("Start date (m/d/yy): ")
    dateTo   = input("End   date (m/d/yy): ")
    try:
        cnt = stock_data.retrieve_stock_web(dateFrom, dateTo, stock_list)
        input(f"{cnt} records added. Enter")
    except RuntimeWarning as e:
        input(str(e) + "  Enter")

def import_csv(stock_list):
    if not stock_list:
        input("Add stocks first. Enter…"); return
    symbol   = input("Ticker symbol: ").upper()
    filename = input("Full path to CSV: ")
    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        input("Import done. Enter")
    except FileNotFoundError:
        input("File not found. Enter")


def main():
    if not path.exists("stocks.db"):
        stock_data.create_database()
    main_menu([])

if __name__ == "__main__":
    main()
