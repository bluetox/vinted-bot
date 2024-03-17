from datetime import datetime, timezone
from pyVinted.requester import requester


class Item: #creates an Item class
    def __init__(self, data): #creates a new object to initiate this class takes a data argument which is an item extracted from the response
        self.raw_data = data #sets the raw data variable as the item object itself  as .raw_data
        self.id = data["id"] #sets the id as .id
        self.title = data["title"] #sets the title as .title
        self.brand_title = data["brand_title"] #sets the brand as .brand_title
        self.size_title = data["size_title"] #sets the data size as .size_title
        self.photo = data["photo"]["url"] #sets the photo URL as .photo
        self.url = data["url"] #sets the article URL as .url
        self.user_id = data["user"]["id"] #sets the seller id as .user_id
        self.created_at_ts = datetime.fromtimestamp(data["photo"]["high_resolution"]["timestamp"], tz=timezone.utc) #stores data in .created_as_ts to compare article and system time
        self.raw_timestamp = data["photo"]["high_resolution"]["timestamp"] #sets timestamp in a raw format at .raw_timestamp variable
        self.condition = data["status"]
        try:
            user_response = requester.get(f"https://www.vinted.fr/api/v2/users/{self.user_id}?localize=false")
            user_items = user_response.json()
            self.feedbacks = user_items["user"]["feedback_count"]
            self.rating_raw = user_items["user"]["feedback_reputation"]
            self.rating = self.rating_raw * 5
        except Exception as e:
            print(f"Error fetching user data: {e}")
            self.feedbacks = None
            self.rating_raw = None
            self.rating = None


    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(('id', self.id))

    def isNewItem(self, minutes=3):
        delta = datetime.now(timezone.utc) - self.created_at_ts
        return delta.total_seconds() < minutes * 60

