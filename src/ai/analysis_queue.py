class AnalysisQueue:

    def __init__(self):

        self.queue = []

    def add(self, threat):

        self.queue.append(threat)

    def get_all(self):

        return self.queue.copy()

    def clear(self):

        self.queue.clear()

    def size(self):

        return len(self.queue)