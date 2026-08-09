class AnalysisManager:

    def __init__(self):

        self.analyses = []

    def add(self, analysis):

        self.analyses.insert(0, analysis)

        if len(self.analyses) > 100:

            self.analyses.pop()

    def get_analyses(self):

        return self.analyses.copy()

    def clear(self):

        self.analyses.clear()