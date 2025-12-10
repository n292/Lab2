

import matplotlib.pyplot as plt

from os import system, name


def clear_screen():
    if name == "nt": 
        _ = system('cls')
    else: 
        _ = system('clear')


def sortStocks(stock_list):
    stock_list.sort(key=lambda s: s.symbol.upper())


def sortDailyData(stock_list):
   for s in stock_list:
        s.DataList.sort(key=lambda d: d.date)


def display_stock_chart(stock_list,symbol):
    stock = next((s for s in stock_list if s.symbol == symbol), None)
    if not stock or not stock.DataList:
        print("No data to chart for", symbol)
        input("Press Enter to return…")
        return
    sortDailyData([stock])

    dates  = [d.date for d in stock.DataList]
    closes = [d.close for d in stock.DataList]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes)
    plt.title(f"{stock.name} ({stock.symbol})  Close Price")
    plt.xlabel("Date")
    plt.ylabel("Close ($)")
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()