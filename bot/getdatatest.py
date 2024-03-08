import requests
import pandas as pd
from io import StringIO

response = requests.get("https://free-proxy-list.net/")
html_content = StringIO(response.text)
proxy_list = pd.read_html(html_content)[0]
# Fix the typo in the column name
proxy_list["url"] = "https://" + proxy_list["IP Address"] + ":" + proxy_list["Port"].astype(str)
proxy_list.head()
https_proxies = proxy_list[proxy_list["Https"] == "yes"]
https_proxies.count()