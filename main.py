import requests
import time
from rich.console import Console
from rich.table import Table

console = Console()


def get_item_info(item_name):
    api_url = f"https://steamcommunity.com/market/priceoverview/?appid=2923300&country=US&currency=1&market_hash_name={item_name}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()

        if data.get('success'):
            current_price = data.get('lowest_price', 'N/A')
            median_price = data.get('median_price', 'N/A')
            total_listings = data.get('volume', 'N/A')

            return current_price, median_price, total_listings
        else:
            console.print(f"Failed to retrieve data for {item_name}. Reason: {data.get('message', 'Unknown error')}",
                          style="bold red")
            return 'N/A', 'N/A', 'N/A'

    except requests.RequestException as e:
        console.print(f"Error fetching data for {item_name}: {e}", style="bold red")
        return 'N/A', 'N/A', 'N/A'


def main():
    with open('items.txt', 'r') as file:
        item_names = [line.strip() for line in file.readlines()]

    while True:
        table = Table(title="Steam Market Items")

        table.add_column("Item", justify="left", style="cyan", no_wrap=True)
        table.add_column("Current Price", style="magenta")
        table.add_column("Median Price", style="green")
        table.add_column("Total Listings", style="blue")

        for item_name in item_names:
            current_price, median_price, total_listings = get_item_info(item_name)
            table.add_row(item_name, current_price, median_price, total_listings)
            time.sleep(1)

        console.clear()
        console.print(table)

        time.sleep(10)


if __name__ == "__main__":
    main()
