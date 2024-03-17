import time
import json
import concurrent.futures
from requester import requester
from items.item import Item
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

list_of_items = []

def extract_channel_data(channel_data):
    channel_name = channel_data.get("ChannelName", "")
    webhook_url = channel_data.get("Webhook")
    brand = channel_data.get("Brand", "")
    max_price = channel_data.get("Maxprice", "")
    keyword = channel_data.get("Keyword", "")

    return {
        "channel_name": channel_name,
        "webhook_url": webhook_url,
        "brand": brand,
        "max_price": max_price,
        "keyword": keyword
    }

def convert_brand(brand):
    brand_mapping = {
        "nike": "53",
        "cp_company": "73952",
        "adidas": "14",
        "ralph_lauren": "88",
        "stussy": "441",
        "stone_island": "73306"
    }
    return brand_mapping.get(brand, brand)

def send_embed_to_discord(webhook_url, embed):
    webhook = DiscordWebhook(url=webhook_url)
    webhook.add_embed(embed)
    response = webhook.execute()
    if response and response.status_code == 200:
        print("Embed sent successfully to Discord")
    else:
        print(f"Failed to send embed to Discord. Status code: {response.status_code if response else 'Unknown'}")

def process(webhook_url, brand, max_price, keyword, list_of_items):
    try:
        response = requester.get(f"https://www.vinted.fr/api/v2/catalog/items?page=1&per_page=50&search_text={keyword}&price_to=40&order=newest_first&size_ids=&brand_ids={brand}&status_ids=&color_ids=&material_ids=")
        response.raise_for_status()

        items = response.json().get("items", [])
        for item in items:
            data = Item(item)
            if data.id in list_of_items:
                print("already sent")

            else:
                embed = DiscordEmbed(title=data.title, color=0x00FFFF)
                embed.add_embed_field(name="📏Taille:", value=data.size_title, inline=True)
                embed.add_embed_field(name="💵Prix:", value=20, inline=True)
                embed.add_embed_field(name="🏅Avis:", value=f"{data.rating} ({data.feedbacks})", inline=True)
                embed.add_embed_field(name="🔧Condition:", value=data.condition, inline=True)
                embed.set_image(url=data.photo)

                # Send the embed to Discord
                send_embed_to_discord(webhook_url, embed)

                list_of_items.append(data.id)
                time.sleep(0.1)

    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    with open('channels_data.json', 'r') as file:
        json_data = json.load(file)

    # Define a ThreadPoolExecutor with desired number of threads
    with ThreadPoolExecutor() as executor:
        # Submit tasks for each channel to the executor
        futures = []
        for channel_key, channel_data in json_data.items():
            settings = extract_channel_data(channel_data)
            brand = convert_brand(settings["brand"])
            future = executor.submit(process, settings["webhook_url"], brand, settings["max_price"], settings["keyword"], list_of_items)
            futures.append(future)

        # Wait for all tasks to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred while processing a channel: {e}")

if __name__ == "__main__":
    main()