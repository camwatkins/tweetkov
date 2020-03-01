class User:
    def __init__(self, data):
        self.id = data.id
        self.verified = data.verified
        self.followers_count = data.followers_count
        self.location = data.location
        self.id_str = data.id_str
        self.utc_offset = data.utc_offset
        self.profile_image_url = data.profile_image_url
        self.screen_name = data.screen_name
        self.lang = data.lang
        self.name = data.name
        self.url = data.url
        self.created_at = data.created_at

    def as_dict(self):
        return {
            "id": self.id,
            "verified": self.verified,
            "followers_count": self.followers_count,
            "location": self.location,
            "id_str": self.id_str,
            "utc_offset": self.utc_offset,
            "profile_image_url": self.profile_image_url,
            "screen_name": self.screen_name,
            "lang": self.lang,
            "name": self.name,
            "url": self.url,
            "created_at": self.created_at
        }
