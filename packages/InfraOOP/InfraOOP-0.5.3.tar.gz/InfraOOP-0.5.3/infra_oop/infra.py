class Machine:
    def __init__(self, search_threads=6):
        self._search_threads = search_threads

    @property
    def cpu_budget(self):
        return self._search_threads * 1000


class Cluster:
    def __init__(self, search_threads=6):
        self._machines = [Machine(search_threads) for m in range(0, 3)]

    @property
    def cpu_budget(self):
        return sum([m.cpu_budget for m in self._machines])

    def get_used_search_capacity(self, queries, query_proc_time):
        demanded_budget = queries * query_proc_time
        return round(demanded_budget / self.cpu_budget, 3)

