class Node:
    def __init__(self, id, data, latitude, longitude):
        self.id = id
        self.data = data
        self.latitude = latitude
        self.longitude = longitude

    def __lt__(self, other):
        return self.id < other.id

