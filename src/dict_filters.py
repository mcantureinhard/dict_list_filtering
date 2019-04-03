

class DictFilters:
    _filters = {}
    _buckets = []

    # strict will run in O(n) (filtering) + O(n') x O(f) x O(k) (Aggregating)
    # n  = number of elements
    # n' = number of elements that match filters
    # f  = number of filters
    # k  = average number of filter options (1 for non list filters)
    _strict = True

    def __init__(self, input: list[dict]):
        self._buckets.append(input)
        print("Init Filters")
    def register_filter(self, filter):
        self._filters[filter.filter_name] = filter
    def update_filters(self, selected_filters: dict):
        if self._strict:
            #TODO