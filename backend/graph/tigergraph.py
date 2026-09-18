class TigerGraphClient:
    def __init__(self, host="", username="", password="", graphname=""):
        self.host = host
        self.username = username
        self.password = password
        self.graphname = graphname

    def query(self, gsql: str):
        # Add pyTigerGraph connection/query execution here.
        return []
