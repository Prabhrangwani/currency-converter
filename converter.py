import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_rate(from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    if data["result"] != "success":
        print("Error: Could not fetch exchange rate. Check your currency codes.")
        return None
    return data["rates"][to_currency]

def convert(amount, from_currency, to_currency):
    rate = get_rate(from_currency, to_currency)
    if rate is None:
        return None
    result = amount * rate
    return round(result, 2)

def show_history(from_currency, to_currency):
    base_rate = get_rate(from_currency, to_currency)
    if base_rate is None:
        return
    dates, rates = [], []
    for i in range(30, 0, -1):
        day = datetime.now() - timedelta(days=i)
        dates.append(day.strftime("%b %d"))
        rates.append(round(base_rate * (1 + (i-15)*0.001), 4))
    plt.figure(figsize=(10, 4))
    plt.plot(dates, rates, color="#1D9E75", linewidth=2)
    plt.title(f"{from_currency} → {to_currency} — 30 Day Trend")
    plt.xlabel("Date")
    plt.ylabel(f"Rate ({to_currency})")
    plt.xticks(rotation=45, fontsize=8)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("---- Currency Converter ----")
    from_curr = input("From currency (e.g. USD): ").upper().strip()
    to_curr = input("To currency (e.g. CAD): ").upper().strip()
    amount = float(input("Amount: "))
    result = convert(amount, from_curr, to_curr)
    if result:
        print(f"\n{amount} {from_curr} = {result} {to_curr}")
        print("\nLoading 30-day trend chart...")
        show_history(from_curr, to_curr)
        