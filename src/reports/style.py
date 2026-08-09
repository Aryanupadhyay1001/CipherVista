from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

styles = getSampleStyleSheet()

TITLE_STYLE = styles["Heading1"]
TITLE_STYLE.fontName = "Helvetica-Bold"
TITLE_STYLE.fontSize = 28
TITLE_STYLE.leading = 34
TITLE_STYLE.alignment = TA_CENTER
TITLE_STYLE.textColor = colors.HexColor("#1D4ED8")

HEADING_STYLE = styles["Heading2"]
HEADING_STYLE.fontName = "Helvetica-Bold"
HEADING_STYLE.fontSize = 18
HEADING_STYLE.leading = 22
HEADING_STYLE.textColor = colors.HexColor("#2563EB")

SUB_STYLE = styles["Heading3"]
SUB_STYLE.fontName = "Helvetica-Bold"
SUB_STYLE.fontSize = 13
SUB_STYLE.leading = 18
SUB_STYLE.textColor = colors.HexColor("#0F172A")

BODY_STYLE = styles["BodyText"]
BODY_STYLE.fontName = "Helvetica"
BODY_STYLE.fontSize = 10.5
BODY_STYLE.leading = 18
BODY_STYLE.spaceAfter = 10

SMALL_STYLE = styles["BodyText"]
SMALL_STYLE.fontName = "Helvetica"
SMALL_STYLE.fontSize = 9
SMALL_STYLE.leading = 13

RISK_STYLE = styles["Heading2"]
RISK_STYLE.fontName = "Helvetica-Bold"
RISK_STYLE.fontSize = 20
RISK_STYLE.alignment = TA_CENTER
RISK_STYLE.textColor = colors.white