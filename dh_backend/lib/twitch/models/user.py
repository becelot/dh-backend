

class TwitchUser(object):

    def __init__(self, data: dict = None):
        # Meta
        self.data: dict = data

        # Response fields
        self.broadcaster_type: str = None
        self.description: str = None
        self.display_name: str = None
        self.email: str = None
        self.id: str = None
        self.login: str = None
        self.offline_image_url: str = None
        self.profile_image_url: str = None
        self.type: str = None
        self.view_count: int = None

        # Fill response fields
        for key, value in data.items():
            self.__dict__[key] = value
