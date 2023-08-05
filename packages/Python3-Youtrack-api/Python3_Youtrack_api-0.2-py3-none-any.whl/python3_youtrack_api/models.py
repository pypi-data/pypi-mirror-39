class BaseModel:
    data = None

    def __init__(self, data):
        self.data = data
        for k, v in self.data.items():
            setattr(self, k, v)
