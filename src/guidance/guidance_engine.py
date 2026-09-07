"""
Bilingual Guidance Engine for UPI-Shield.
Provides actionable, natural English and Hindi safety recommendations calibrated to risk levels.
"""

from pydantic import BaseModel
from src.config import (
    RISK_LEVEL_LOW,
    RISK_LEVEL_MEDIUM,
    RISK_LEVEL_HIGH,
    RISK_LEVEL_CRITICAL,
)


class GuidanceResult(BaseModel):
    risk_level: str
    recommendation_en: str
    recommendation_hi: str
    action_bullet_points_en: list[str] = []
    action_bullet_points_hi: list[str] = []


class GuidanceEngine:
    """Generates natural bilingual safety guidance."""

    def generate_guidance(self, risk_level: str) -> GuidanceResult:
        if risk_level == RISK_LEVEL_LOW:
            en = "Stay alert. Always double-check payees and details before authorizing any transaction."
            hi = "सतर्क रहें। किसी भी लेन-देन को अधिकृत करने से पहले हमेशा प्राप्तकर्ता और विवरण की दोबारा जांच करें।"
            bullets_en = [
                "Verify the recipient's name before sending money.",
                "Ensure payment requests originate from people or services you know.",
            ]
            bullets_hi = [
                "पैसा भेजने से पहले प्राप्तकर्ता के नाम की पुष्टि करें।",
                "सुनिश्चित करें कि भुगतान अनुरोध आपके परिचित लोगों या सेवाओं से ही आए हैं।",
            ]

        elif risk_level == RISK_LEVEL_MEDIUM:
            en = "Pause before paying. Verify the sender's claim independently using official contacts or trusted channels."
            hi = "भुगतान करने से पहले रुकें। आधिकारिक संपर्कों या विश्वसनीय चैनलों का उपयोग करके स्वतंत्र रूप से दावे की पुष्टि करें।"
            bullets_en = [
                "Do not click unverified links embedded in messages.",
                "Cross-check account or bill details on official websites/apps.",
                "Avoid urgent payment decisions made under pressure.",
            ]
            bullets_hi = [
                "संदेशों में दिए गए असत्यापित लिंक पर क्लिक न करें।",
                "आधिकारिक वेबसाइट/ऐप पर खाता या बिल विवरण की जांच करें।",
                "दबाव में आकर जल्दबाजी में भुगतान का निर्णय न लें।",
            ]

        elif risk_level == RISK_LEVEL_HIGH:
            en = (
                "HIGH RISK DETECTED! Do not make the requested payment immediately. "
                "Never share your OTP, UPI PIN, password, or CVV. Verify directly with official authorities."
            )
            hi = (
                "उच्च जोखिम पहचाना गया! तुरंत मांगा गया भुगतान न करें। "
                "अपना ओटीपी, यूपीआई पिन, पासवर्ड या कार्ड विवरण कभी भी साझा न करें। आधिकारिक अधिकारियों से सीधे पुष्टि करें।"
            )
            bullets_en = [
                "Do NOT enter your UPI PIN to receive money (UPI PIN is ONLY required to SEND money).",
                "Do NOT install screen-sharing apps like AnyDesk or TeamViewer.",
                "Contact customer care directly using numbers from official utility bills or bank websites.",
            ]
            bullets_hi = [
                "पैसा प्राप्त करने के लिए अपना यूपीआई पिन न डालें (यूपीआई पिन केवल पैसा भेजने के लिए होता है)।",
                "एनीडेस्क (AnyDesk) या टीमव्यूअर जैसे स्क्रीन-शेयरिंग ऐप इंस्टॉल न करें।",
                "बिल या बैंक वेबसाइट से प्राप्त आधिकारिक नंबरों का उपयोग करके संपर्क करें।",
            ]

        else:  # CRITICAL
            en = (
                "CRITICAL WARNING: STOP THE TRANSACTION IMMEDIATELY! "
                "This message displays severe coercion and scam indicators. "
                "Never share credentials. Report suspected fraud to Helpline 1930 or your bank."
            )
            hi = (
                "गंभीर चेतावनी: लेन-देन तुरंत रोकें! "
                "इस संदेश में गंभीर धोखाधड़ी और दबाव के लक्षण हैं। "
                "अपनी गोपनीय जानकारी कभी साझा न करें। हेल्पलाइन 1930 या बैंक को धोखाधड़ी की सूचना दें।"
            )
            bullets_en = [
                "STOP! Do not send money or scan any QR code.",
                "Block and report the sender's phone number.",
                "If money was lost, report immediately to Cyber Crime Helpline 1930 or cybercrime.gov.in.",
            ]
            bullets_hi = [
                "रुकें! पैसा न भेजें और न ही कोई क्यूआर कोड स्कैन करें।",
                "भेजने वाले का नंबर ब्लॉक और रिपोर्ट करें।",
                "यदि पैसा कट गया है, तो तुरंत साइबर अपराध हेल्पलाइन 1930 या cybercrime.gov.in पर रिपोर्ट करें।",
            ]

        return GuidanceResult(
            risk_level=risk_level,
            recommendation_en=en,
            recommendation_hi=hi,
            action_bullet_points_en=bullets_en,
            action_bullet_points_hi=bullets_hi,
        )
