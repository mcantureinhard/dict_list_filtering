

class OfferFilters:
    _filters = []
    _buckets = []
    _strict_filter = True
    def __init__(self, input: list[dict]):
        self._buckets.append(input)
        print("Init Filters")
    def register_filter(self, filter):
        self._filters.append(filter)