from src.ai.prompt_builder import PromptBuilder
from src.ai.gemini_client import GeminiClient
from src.ai.response_parser import ResponseParser
from src.ai.analysis_manager import AnalysisManager

class SOCAnalyst:

    def __init__(self):
        self.prompt_builder = PromptBuilder()
        self.gemini = GeminiClient()
        self.parser = ResponseParser()
        self.analysis_manager = AnalysisManager()

    def analyze(self, threat):

        prompt = self.prompt_builder.build(threat)

        response = self.gemini.generate(prompt)

        if response is None:

            analysis = {
                "summary": threat.description,
                "impact": "Potential disruption of network services.",
                "recommendations": [
                    "Block source IP",
                    "Review firewall logs",
                    "Investigate affected host"
                ],
                "risk": threat.severity,
                "mitre_description": "Network Denial of Service"
            }

        else:

            analysis = self.parser.parse(response)

        analysis["time"] = threat.time
        analysis["threat"] = threat.threat_type
        analysis["severity"] = threat.severity
        analysis["source"] = threat.source_ip
        analysis["destination"] = threat.destination_ip
        analysis["confidence"] = threat.confidence
        analysis["mitre"] = threat.mitre

        self.analysis_manager.add(analysis)

        return analysis

    def get_analyses(self):
        return self.analysis_manager.get_analyses()

    def clear(self):
        self.analysis_manager.clear()