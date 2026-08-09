class SeverityCalculator:

    def calculate(
        self,
        rule_threats,
        ml_prediction,
        flow
    ):

        score = 0

        # -------------------------
        # Rule Engine
        # -------------------------

        if rule_threats:
            score += 40

        # -------------------------
        # Random Forest Confidence
        # -------------------------

        confidence = ml_prediction["confidence"]

        if confidence >= 95:
            score += 35

        elif confidence >= 80:
            score += 25

        elif confidence >= 60:
            score += 15

        # -------------------------
        # Isolation Forest
        # -------------------------

        if ml_prediction["is_anomaly"]:
            score += 20

        # -------------------------
        # Traffic Volume
        # -------------------------

        if flow.total_packets > 100:
            score += 15

        if flow.total_bytes > 500000:
            score += 10

        # -------------------------
        # Final Severity
        # -------------------------

        if score >= 80:
            severity = "Critical"

        elif score >= 60:
            severity = "High"

        elif score >= 35:
            severity = "Medium"

        else:
            severity = "Low"

        return {
            "score": score,
            "severity": severity
        }