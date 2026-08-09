import json


class ResponseParser:

    def parse_batch(self, response):

        import json

        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()

        elif response.startswith("```"):
            response = response.replace("```", "").strip()

        analyses = json.loads(response)

        return analyses