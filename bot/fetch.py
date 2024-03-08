import time
import discord
import requests
from concurrent.futures import ThreadPoolExecutor
from discord import Embed
from datetime import datetime

# Discord Webhook URL
discord_webhook_urls = [
    "https://discord.com/api/webhooks/1215234554525261854/Pi3DDjHSIdVNKZkbDUOPd1KljpUv48QD1ie7KlKN0HfMr2j14S2I8kjKOWGAd8v6LfeQ",
    "https://discord.com/api/webhooks/1215258899796467763/5MvBK0fX1XV2Rbgo3I6VQkTDGxrb0IDgav-82T-etw1P8eIOKvMSlcKH0gK47BS1CRTv"
]


def get_vinted_item_data():
    try:
        vinted_response = requests.get(vinted_item_url, params=params, headers=headers)
        vinted_item_data = vinted_response.json() if vinted_response.status_code == 200 else None
        return vinted_item_data
    except requests.RequestException as e:
        print(f"Vinted API request failed: {e}")


def get_vinted_seller_data():
    try:
        vinted_response = requests.get(vinted_seller_url, headers=headers)
        vinted_seller_data = vinted_response.json() if vinted_response.status_code == 200 else None
        return vinted_seller_data
    except requests.RequestException as e:
        print(f"Vinted API request failed: {e}")


def send_to_discord(item):
    try:
        user_info = {
            "seller_id": item.get("user", {}).get("id"),
            "item_name": item.get("title"),
            "item_price": item.get("price"),
            "item_size": item.get("size_title"),
            "item_status": item.get("status"),
            "total_price": item.get("total_item_price", {}).get("amount"),
            "seller_name": item.get("user", {}).get("login"),
            "favourite_count": item.get("favorite_count"),
            "item_url": item.get("url"),
            "item_thumbnail": item.get("photo", {}).get("url"),
        }

        # Create a Discord Embed
        embed = discord.Embed(
            title="Item_name",
            colour=0x00b0f4,
            timestamp=datetime.now()
        )
        embed.set_author(name="VINSTANT", url="https://example.com")

        embed.add_field(name="💰PRICE💰", value=user_info["total_price"], inline=True)
        embed.add_field(name="🥇AVIS🥇", value="seller_rating", inline=True)
        embed.add_field(name="🔨ETAT🔨", value=user_info["item_status"], inline=True)
        embed.set_image(url=user_info["item_thumbnail"])

        # Send data to Discord webhook
        discord_payload = {
            "content": "",
            "embeds": [embed.to_dict()]
        }

        for webhook_url in discord_webhook_urls:
            discord_response = requests.post(webhook_url, json=discord_payload)
            # Add your existing logic for checking the response status code and printing messages

        if discord_response.status_code == 204:
            print(f"Data for user {user_info['username']} sent to Discord successfully.")
        else:
            print(
                f"Failed to send data for user {user_info['username']} to Discord. Status code: {discord_response.status_code}")
    except Exception as e:
        print(f"Error sending to Discord: {e}")


# Vinted API URL
vinted_item_url = "https://www.vinted.fr/api/v2/catalog/items"
vinted_seller_url = "https://www.vinted.fr/member/{seller_id}-{seller_name}"
params = {
    "page": 1,
    "per_page": 200,
    "search_text": "sport",
    "catalog_ids": 1904,
    "order": "newest_first",
    "size_ids": "",
    "brand_ids": "53",
    "status_ids": "6",
    "color_ids": "",
    "material_ids": "",
    "price_to": 10,
    "price_from": 0,
}

headers = {
    "authority": "www.vinted.fr",
    "method": "GET",
    "path": "/api/v2/catalog/items?page=1&per_page=96&search_text=&catalog_ids=1904&order=newest_first&size_ids=&brand_ids=&status_ids=&color_ids=&material_ids=",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "fr",
    "cookie": "v_sid=e4c7cf9b72eedf2717614d63355765ae; v_udt=Nkc1bU1aQVBibENnRFhreG1UTk1oUkcxbkQ0Ui0tSmpwcTdKbEJjRGgyQm5XUy0tU3JraUx3NC82UDVucnNzRlFEVjdNUT09; anon_id=052c3f7a-2719-4c89-bc25-0140ffa8a774; anonymous-locale=fr; ab.optOut=This-cookie-will-expire-in-2025; eupubconsent-v2=CP6_zhgP6_zhgAcABBENAqEgAAAAAAAAAChQAAAAAAFBIHoACAAFwAUABUADgAHgAQAAwgBkAGoAPAAiABMACqAG8APQAfgBCQCGAIkARwAlgBNADDgGUAZYA2QB3wD2APiAfYB-gEAAIpARcBGACNAFBAKgAVcAuYBigDRAG0ANwAcQBIgCdgFDgKPAUiAtgBcgC7wF5gMGAYaAyQBk4DOYGsAayA28BuoDggHJgOXAeOBCEIAdAAcACQAc4BBwCfgI9ASKAlYBNoCnwFhALyAYgAxaBkIGRgNGAamA2gBtwDdIHkgeUA-QB-4EBAIGQQRBBMCDAEKwIXDgGQACIAHAAeABcAEgAPwA0ADnAHcAQCAg4CEAERAJ-AVAAvQBxwDpAI9ASKAlYBMQCZQE2gKQAUmAqoBXYC1AF0AMQAYsAyEBkwDRgGmgNTAa8A2gBtgDbgHHwOdA5-B5IHlAPiAfbA_YD9wIHgQRAgwBBsCFY6CYAAuACgAKgAcABAAC6AGAAagA8ACIAEwAKsAXABdADEAGYAN4AegA_QCGAIkASwAmgBRgDDAGUANEAbIA7wB7QD7AP0Af8BFAEYAKCAVcAsQBcwC8gGKANoAbgA4gB1AEXgJEATIAnYBQ4CjwFNAKsAWLAtgC2QFwALkAXaAu8BeYC-gGDAMNAY8AyQBk4DKgGWAM5AaIA1UBrADbwG6gOLAcmA5cB44D6wH_AQBAhaQAJgAIADQAOcAsQCPQE2gKTAXkA1MBtgDbgHPwPJA8oB8QD9gIHgQYAg2BCshAhAAWABQAFwAMQAmABVAC4AGIAN4AegBHADvAH-ARQAlIBQQCrgFzAMUAbQA6gCmgFigLRAXAAuQBk4DOQGiANVAeOBCgCFpKA-AAgABYAFAAOQAwADEAHgARAAmABVAC4AGKAQwBEgCOAFGANkAd4A_ACrgGKAOoAi8BIgCjwFigLYAXmAycBnIDWAG3gQPJADgALgDuAIAAVABHoCRQErAJtAUmAxYB5QD9wIIgQYKQNQAFwAUABUADgAIIAYABqADwAIgATAApABVADEAGYAP0AhgCJAFGAMoAaIA2QB3wD8AP0AiwBGACggFXALmAXkAxQBtADcAIvASIAnYBQ4CxQFsALgAXIAu0BeYC-gGGgMkAZOAywBnMDWANZAbeA3UBwQDkwHjgQhAhaUARgAXABIAI4Ac4A7gCAAEiALEAXUA14B2wD_gI9ASKAmIBNoCkAFPgK7AXQAvIBiwDJgGiANTAa8A8oB8UD9gP3AgYBA8CCYEGAINgQrAA.YAAAAAAAAAAA; OTAdditionalConsentString=1~; OptanonAlertBoxClosed=2024-03-05T14:59:53.875Z; domain_selected=true; cf_clearance=3CUHKYKotu_Z.JxnGhzfpQQsi_5vGH2ffRicrQgQENs-1709842535-1.0.1.1-y2jD7WFHYYdFW.2MAPHJ.6ZW1KKs66ASirvzm9NGuKpbY1s.HBlO6qsw0KglQPEY_mXFPVG3Hs4t0rUE0M.how; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Mar+07+2024+21%3A15%3A36+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=052c3f7a-2719-4c89-bc25-0140ffa8a774&interactionCount=80&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CV2STACK42%3A0%2CC0015%3A0&geolocation=%3B&AwaitingReconsent=false; datadome=9osKr3HLmAnincgYYLUr1uTtLq16eOr7ZyEFpwzAVk6m~1W_1hMc_~F7z1SpzmfJp_UO6TkLCGndEnvDA9JU4G1gxN~CbpgWdmjRJZkiHW~x71HaAg_nJLbWlCJH3eQ8; __cf_bm=.Nw289YnmfuQpLiHLXSOPj_fAxolD1rPyBCcSEyBpt8-1709843390-1.0.1.1-2eiEKY_CS20zPZlVqNSEObpXqkSIiV.5fNoMWYTiLDChF7Lny_vszECErmHzFenY7ubbsuaRlM.BnZtKHk.xlTRHN.Xv4W8Hc.IhMiIXk6w; _vinted_fr_session=cVlacHlvNmpyYzNJdllwV3ZLWDVYbWhZTkl6WkZxQnZRcHJuN3ZMOHExTlhLelNVYlVBY0E0L3lpbmVINkJzZnd2MWZOSG1oQXg4Qi9kVmF3SFd2TFZGd3hUdWp6aENESVFZUy9ZbEpBWmZ0MitpSWVHaWplWHJzNjEvTUdQclhHY09najQzRW5KYzVNR1VjVHpqcDZkcXR4NDVMTllhZjQ1WW8vR3IxTklhZXFNdmVXaklhN0lINXllRTN6WlgxVWZucEhMSlJydzMvcHd3SlRnd1lZaXVNbi9XSlN0WnlrVGJSK2pGYjY5dVNIMjBPSFN5TGdHemNlamliU1Z1QmtpamdIdFZna0kvZjhKdmZHUE5NWDQvbmN0cnFnb1MvcnRLaXp6b1R4UmFmRXFQcmZ5K0ZlVWYrcytaQkNwRWtySlhZZkpKTW1rdm1yYmNUTzd4ZWhHaXpPWldzUlFaRXZQWDUvK2hkTmhoNVUvT0MrZk83N3gxMjQ2VDJLRHk4eTVmT1RXYktWNWJpdEhwTmRhcE9nbVFVSzJYdld5ejdZdkJSRmZCWURVM2QyakNzRHpXNU5LNHhGQ2wzeUpNc1lJZ2h6dDVuUG1ueFRDd2tXWlBwZlVzWXBrOG16NytWVTcyTEcvWEo5UlhsalBxdC9oSjNuQUVjeHBlQzZDR0pDWWUzRXBuUDBEd1ZoaGY2YTdrQ0RiM2tudWhwZFdPYjN6Y0YxN2VYRlJiREJodzZ0eFF3WTgzaWdOODdrMnVWSm11Mm5ia2srYjBnNWJMYnUvOHIzdnV3UFZ5YnE1RHBTM1NMY1dSeUx1UUxJcHBOZXpnaVpSYlgwd0lGa3JNOEVsWTQ0VGYrRDRtS3ZUS1E1UDlsaWRRNG94MDB3Zmh1RkZBSEltemNvVjJkOWRlNXBiRFpHSnVyak01SkhWZEZFbDFFRWRYMW9wVm1BQmVFRlpzS3VUaVpkOGVVL1ZjS2I0M2VEMy9ONncvNkRVdGNReHVsbkltcnpmZTRCb24rWG9sNzJvOWRjTm54Q3BpM2NuOFUwekpBK0tCcFMxdGM4eVV3Y1YrMHJVdjJqQ3hWT2VpVEZvTGhyNUhwaHNFeW92cGxuRnVzSmJEU3hra1Rmaml1UDk0TSsvUUtjSE95aHVRZE55OUVGa1FrYjk1RVJNckRnem5aV1FFbkJhSlIwZVUxV2FXanRpVXdBaDd6OW1ma1BWdTE1VDFFZ0puVzM4TTlLUWp4dnd0UGdTZWFiVVJKUWNsL3U3MGNMd0FWODRURGYvb1huZ21ITnU3c1RIUmFQME5ZS3VHc2RGU1dMeXNqeG93NHhPNE5icC82TFZPR044TnhuRjRFU3pJRmVLMENnOFlzZG51Wm5zZWgwaVFBUEJiSjhuVk4vczdHalRlTDJYbUdSdHoxNy8rSU1zbXU1OVp0dkVoQjI1ek91NHhpQ1hwT2ZNQVBNWElCU1lIc21pSFdLeEdlako2MmR6Uk8xS20rT0ZhRituTWIvOENtNkJ2T21maVdwbjVYcnRKRU15RjJNOGNEeXFWakVoWUlDQkdtY3I4K1kwWG91aFlLVXBTWnpScFNBamUxeURHQTFVMFNmclhCeExBc3pnWjExd05ubkJFejVQU1FKTlFrcHp4YytZQzJGUTBOSzdkNGQ0aWc4cERUcUp2b0dPL0FJeFRscHJ1aW5hdHdzeFBpc1UyTENxd0dDNXVubGwvK0ZkN1RUMlM4NGFkVnZkZ2hGTXI2ZnBjZlpkdm5obTJ6Q1FOMkxzMC9uMzNFOGJlQ2lQRHVTalp4eElFK1p0cENOZnlXaHBiVm0rYVByOFJlU24rTGxQcmpjeUJNTTRjMlljT01xVVRET2Fad2dUc0NUaGF0THIrSFpQaXpPQ3l2ZkVZdlJob0hISVhKSjVjN2RVYWNGMWhiWGlZMjVuWmhMVjZ6RzRJcGRKZjF3VG50TUZoN1IyV3hTZkFoOUpsQytKT2NPd3VFSHpsMngvUGFzTDZhVllPREhDVm9xMENuK3R0ZEkrL3N2YUp6eWJFVXdmbTMza1dTdTJEbG0xQUxib2JWQS8rQk9UUFprTlZUNHgvWVN3bVlreEI3OUk1ZGJ0QU5wTmhLYTVXUnl6QTl1SlFPelA0dWFCSFdHdWxLQituQ1hEREdQcEM3MzIyWXN1TVI5ZWdCaW9IMmsxdVB1K2svSFRZckFQVS8zZU9WcTdMZFdRYU9reGZNQlNNQzlWNitNekpoOW1mRG5xa2NNNGYyT2dWUDQ4cnZvb1NXWXc3Mi90b3BDRVZLeTQ5OGdBaHVRTXR6MUdsOVVDSFEreWlweGs1a29RU0RENUJxSVpHYmVlVVNsT2U3ZmFEcjVsZTdrckdTdUZuS3dGdFEzRkpkUEdjZGRSWFRscmt2d0tnR0Q2RmMwVDM5OUhtSS9uKzdhQ3FxMm1sREVvNXZhNW1PREdPRms0TjEtLVZMZW9neWdmcEdnTWw1UlhXNWJpQlE9PQ%3D%3D--c64cd1ee568d0725de30002b7457b3c00974b5ab; _dd_s=rum=0&expire=1709844300144; viewport_size=241",
    "if-none-match": 'W/"3a421aa6e75406b0c5953c98330f5352"',
    "referer": "https://www.vinted.fr/catalog?catalog[]=1904&order=newest_first",
    "sec-ch-ua": '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "x-anon-id": "052c3f7a-2719-4c89-bc25-0140ffa8a774",
    "x-csrf-token": "75f6c9fa-dc8e-4e52-a000-e09dd4084b3e",
    "x-money-object": "true"
}

try:
    # Get data from Vinted API
    vinted_item_data = get_vinted_item_data()
    vinted_seller_data = get_vinted_seller_data()

    if vinted_item_data:
        # Create a ThreadPoolExecutor for concurrent processing
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Iterate over items in the Vinted API response and submit tasks to the thread pool
            for item in vinted_item_data.get("items", []):
                try:
                    executor.submit(send_to_discord, item)
                except Exception as e:
                    print(f"Error submitting task to thread pool: {e}")
                time.sleep(0.5)

except Exception as e:
    print(f"An error occurred: {e}")