
class Components(object):

    def __init__(self):
        self.components = None

    def delete(self):
        if self.components:
            self.components.empty()


class StockInfo(Components):
    pass
