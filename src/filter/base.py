from abc import ABC


class Filter(ABC):
    # Basic filters just need a path of where to find the data
    _path = []
    # Filter behaves as OR or AND when more than one value is selected, only relevant if filtering on array
    _or_mode = False
    # if strict, remove even if we don't know the value
    _strict = True
    # set if scalar or list, we could get this on runtime, but let's be more strict
    _is_list = False
    # In case we are filtering on a list of dictionaries
    _list_path =[]
    _aggregations = {}
    _selected = []

    @ABC.abstractmethod
    def filter_name:
        return

    # Override to provide name mapping for filters
    def _agg_name_map(self):
        return {}

    def __init__(self):
        self._path = ''

    def set_selected(self, selected: list) -> int:
        current_selected = len(self._selected)
        new_selected = len(selected)
        self._selected = selected
        return new_selected - current_selected

    def _get_value(self, element, path):
        if len(path) == 0:
            return element
        current = element
        for move in path:
            if move not in current:
                return None
            current = current[move]
        return current

    def _is_selected(self, value):
        return value in self._selected

    def is_match(self, element: dict):
        if len(self._selected) == 0:
            return True
        data = self._get_value(element, self._path)
        # This case (list) can become suboptimal very easily.
        # It would be better to implement a class specific for this.
        # For now let us use this, while the other class is written
        if self._is_list:
            selected_count = 0
            for dt in data:
                value = self._get_value(dt,self._list_path)
                selected_count = selected_count + self._is_selected(value=value)
                # In or mode if any filter matches, return true
                if self._or_mode and selected_count:
                    return True
                elif selected_count == len(self._selected):
                    return True
            # We finished the loop and didn't return true
            return False
        else:
            value = data
            return self._is_selected(value=value)

    def aggregate(self, element: dict):
        data = self._get_value(element, self._path)
        if self._is_list:
            for dt in data:
                value = self._get_value(dt, self._list_path)
                if value in self._aggregations:
                    self._aggregations[value] = self._aggregations[value] + 1
                else:
                    self._aggregations[value] = 1
        else:
            value = data
            if value in self._aggregations:
                self._aggregations[value] = self._aggregations[value] + 1
            else:
                self._aggregations[value] = 1

    def _build_filters_output(self):
        filters = {}
        name_map = self._agg_name_map()
        for agg, val in self._aggregations.items():
            filters[agg] = {
                "count": val,
                "selected": agg in self._selected,
                "text" : name_map[agg] if agg in name_map else agg
            }
        return filters

    def output(self) -> dict:
        filter = {
            "name": self.filter_name,
            "filters": self._build_filters_output()
        }
