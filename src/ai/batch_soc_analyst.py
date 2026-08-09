from src.ai.prompt_builder import PromptBuilder
from src.ai.gemini_client import GeminiClient
from src.ai.response_parser import ResponseParser
from src.ai.analysis_manager import AnalysisManager


class BatchSOCAnalyst:

    def __init__(self):

        self.prompt_builder = PromptBuilder()

        self.gemini = GeminiClient()

        self.parser = ResponseParser()

        self.analysis_manager = AnalysisManager()

    def analyze(self, threats):

        if not threats:
            return

        prompt = self.prompt_builder.build_batch(threats)

        response = self.gemini.generate(prompt)

        if response is None:

            for threat in threats:

                self.analysis_manager.add({

                    "time": threat.time,
                    "threat": threat.threat_type,
                    "severity": threat.severity,
                    "source": threat.source_ip,
                    "destination": threat.destination_ip,
                    "confidence": threat.confidence,
                    "mitre": threat.mitre,

                    "summary": threat.description,

                    "impact": "Potential impact on network availability.",

                    "risk": threat.severity,

                    "recommendations":[
                        "Investigate the source host",
                        "Review firewall logs",
                        "Block the source if malicious"
                    ]

                })

            return

        analyses = self.parser.parse_batch(response)

        for analysis, threat in zip(analyses, threats):

            analysis["time"] = threat.time
            analysis["threat"] = threat.threat_type
            analysis["severity"] = threat.severity
            analysis["source"] = threat.source_ip
            analysis["destination"] = threat.destination_ip
            analysis["confidence"] = threat.confidence
            analysis["mitre"] = threat.mitre

            self.analysis_manager.add(analysis)

    def get_analyses(self):

        return self.analysis_manager.get_analyses()

    def clear(self):

        self.analysis_manager.clear()