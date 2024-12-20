class GetFrames:
    _instance = None

    @staticmethod
    def get_instance():
        if GetFrames._instance is None:
            GetFrames._instance = GetFrames()
        return GetFrames._instance

    def __init__(self):
        self.frames = {}

    def get_frames(self):
        return self.frames

class GetUserInfo:
    _instance = None

    @staticmethod
    def get_instance():
        if GetUserInfo._instance is None:
            GetUserInfo._instance = GetUserInfo()
        return GetUserInfo._instance

    def __init__(self):
        self.usertype = None
        self.username = None

    def get_usertype(self):
        return self.usertype

    def get_username(self):
        return self.username

