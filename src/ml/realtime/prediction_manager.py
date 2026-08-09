class PredictionManager:

    def __init__(self):

        self.predictions = []

    def add(self, prediction):

        self.predictions.insert(0, prediction)

        if len(self.predictions) > 100:

            self.predictions.pop()

    def get_predictions(self):

        return self.predictions.copy()

    def clear(self):

        self.predictions.clear()