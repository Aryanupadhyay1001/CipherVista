import time


class IncidentManager:

    def __init__(self):
        self.incidents = {}

    def process(self, threat):

        key = (
            threat.source_ip,
            threat.destination_ip,
            threat.protocol,
            threat.threat_type
        )

        now = time.time()

        if key in self.incidents:

            incident = self.incidents[key]

            incident["count"] += 1
            incident["last_seen"] = now

            return None

        self.incidents[key] = {
            "count": 1,
            "first_seen": now,
            "last_seen": now
        }

        return threat

    def get_active_incidents(self):
        return self.incidents