from collections import deque


class AlertManager:

    def __init__(self):

        self.alerts = deque(maxlen=100)

    def add_alert(self, threat):

        self.alerts.append(threat)

    def get_alerts(self):

        return list(self.alerts)

    def clear_alerts(self):

        self.alerts.clear()

    def total_alerts(self):

        return len(self.alerts)

    def critical_alerts(self):

        return sum(
            1
            for alert in self.alerts
            if alert.severity == "Critical"
        )

    def high_alerts(self):

        return sum(
            1
            for alert in self.alerts
            if alert.severity == "High"
        )

    def medium_alerts(self):

        return sum(
            1
            for alert in self.alerts
            if alert.severity == "Medium"
        )

    def low_alerts(self):

        return sum(
            1
            for alert in self.alerts
            if alert.severity == "Low"
        )

    def reset(self):

        self.alerts.clear()