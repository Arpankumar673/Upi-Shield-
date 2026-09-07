"""
UPI-Shield Streamlit Application
Contextual Digital Payment Scam & Coercion Detector
Hackathon Demo Shell (Phase 5 Hardened & Polished)
"""

import streamlit as st
from data.sample_messages import SAMPLE_MESSAGES
from src.preprocessing import TextProcessor
from src.detection import SignalDetector
from src.scoring import RiskEngine
from src.explanations import Explainer
from src.guidance import GuidanceEngine
from src.ocr import OCREngine
from src.upi import UPIParser

# Page Configuration
st.set_page_config(
    page_title="UPI-Shield | Scam & Coercion Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def render_analysis_dashboard(input_text: str, processor, detector, risk_engine, explainer, guidance_engine):
    """Renders the primary Threat Assessment Dashboard for analyzed message text."""
    if not input_text or not input_text.strip():
        st.warning("⚠️ Please provide text to analyze.")
        return

    with st.spinner("Analyzing message semantics and deception indicators..."):
        # 1. Preprocess Input & Extract Entities
        processed = processor.process(input_text)

        # 2. Detect Deceptive Signals
        detection_res = detector.analyze(processed)

        # 3. Calculate Risk Score & Level
        risk_res = risk_engine.calculate_risk(detection_res)

        # 4. Generate Explanations & Evidence Breakdown
        explanation_res = explainer.explain(detection_res, risk_res)

        # 5. Generate Bilingual Safety Guidance
        guidance_res = guidance_engine.generate_guidance(risk_res.risk_level)

    st.markdown("## 📊 Threat Assessment Dashboard")

    # Top Metrics Layout: Threat Score & Risk Badge
    col_score, col_explain = st.columns([2, 3])

    with col_score:
        st.metric(label="THREAT METER SCORE", value=f"{risk_res.score} / 100")
        st.progress(float(risk_res.score / 100.0))

        # Risk Level Badge
        if risk_res.risk_level == "LOW":
            st.success(f"🟢 **RISK LEVEL: LOW** ({risk_res.score}/100)")
        elif risk_res.risk_level == "MEDIUM":
            st.warning(f"🟡 **RISK LEVEL: MEDIUM** ({risk_res.score}/100)")
        elif risk_res.risk_level == "HIGH":
            st.error(f"🟧 **RISK LEVEL: HIGH** ({risk_res.score}/100)")
        else:
            st.error(f"🚨 **RISK LEVEL: CRITICAL** ({risk_res.score}/100)")

        # Extracted Entity Context Badges
        if processed.has_urls or processed.has_upi_ids or processed.has_phones or processed.has_amounts:
            st.markdown("### 🔍 Extracted Payment Context Entities")
            if processed.has_urls:
                st.markdown(f"🔗 **URLs:** `{', '.join(processed.extracted_urls)}`")
            if processed.has_upi_ids:
                st.markdown(f"💳 **UPI VPAs:** `{', '.join(processed.extracted_upi_ids)}`")
            if processed.has_phones:
                st.markdown(f"📞 **Phone Numbers:** `{', '.join(processed.extracted_phones)}`")
            if processed.has_amounts:
                st.markdown(f"💰 **Amounts Mentioned:** `{', '.join(processed.extracted_amounts)}`")

    with col_explain:
        st.markdown("### 💡 Why was this flagged?")
        st.write(explanation_res.summary)
        
        for reason in explanation_res.reasons:
            st.markdown(f"{reason}")

        if explanation_res.evidence_breakdown:
            st.markdown("#### 📌 Matched Evidence Snippets")
            for ev in explanation_res.evidence_breakdown:
                st.markdown(f"- {ev}")

    # Detected Indicators Section
    detected_signals = [s for s in detection_res.signals if s.detected]
    if detected_signals:
        st.markdown("---")
        st.markdown("### 🚨 Detected Deception Indicators")
        sig_cols = st.columns(len(detected_signals))
        for idx, signal in enumerate(detected_signals):
            contrib_val = risk_res.signal_contributions.get(signal.name, 0.0)
            with sig_cols[idx]:
                st.markdown(f"✓ **{signal.display_name}**")
                st.progress(float(signal.score))
                st.caption(f"Confidence: {int(signal.score * 100)}% | Risk Impact: +{contrib_val:.1f} pts")

    st.markdown("---")

    # Bilingual Safety Guidance Cards
    st.markdown("## 🛡️ Bilingual Safety Guidance / सुरक्षा मार्गदर्शन")
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        st.markdown("### 🇬🇧 English Safety Guidance")
        st.info(f"**{guidance_res.recommendation_en}**")
        if guidance_res.action_bullet_points_en:
            st.markdown("**Recommended Actions:**")
            for bp in guidance_res.action_bullet_points_en:
                st.markdown(f"- {bp}")

    with g_col2:
        st.markdown("### 🇮🇳 हिंदी सुरक्षा मार्गदर्शन")
        st.warning(f"**{guidance_res.recommendation_hi}**")
        if guidance_res.action_bullet_points_hi:
            st.markdown("**सुझाई गई कार्रवाइयां:**")
            for bp in guidance_res.action_bullet_points_hi:
                st.markdown(f"- {bp}")


def main():
    # Header Section
    st.title("🛡️ UPI-Shield")
    st.markdown("#### **Contextual Digital Payment Scam & Coercion Detector**")
    st.markdown("*Analyze suspicious payment messages and identify contextual scam indicators before you act.*")

    st.info(
        "ℹ️ **Safety Disclaimer:** UPI-Shield evaluates message semantics for psychological coercion, urgency, "
        "and scam indicators. It never requests or processes real UPI PINs, passwords, or bank credentials, and does not execute payment transactions."
    )
    st.caption("🔒 **Privacy Protection:** Uploaded screenshots and text are processed in-memory and are not permanently stored.")

    st.markdown("---")

    # Initialize Controller Components
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    explainer = Explainer()
    guidance_engine = GuidanceEngine()
    ocr_engine = OCREngine()
    upi_parser = UPIParser()

    # Sidebar Scenario Selector
    st.sidebar.header("📋 Demo Scenarios")
    st.sidebar.markdown("Select a scenario to load pre-configured test text:")
    selected_sample = st.sidebar.selectbox(
        "Scenarios:",
        ["-- Select Demo Scenario --"] + list(SAMPLE_MESSAGES.keys())
    )

    default_text = ""
    if selected_sample != "-- Select Demo Scenario --":
        default_text = SAMPLE_MESSAGES[selected_sample]

    # Input Mode Tabs
    tab1, tab2, tab3 = st.tabs([
        "💬 Text Analysis",
        "🖼️ Screenshot Analysis",
        "💳 UPI Intent Analysis"
    ])

    # TAB 1: TEXT ANALYSIS
    with tab1:
        st.subheader("📥 Analyze Message Text")
        st.markdown("Paste SMS, WhatsApp message, or payment note below:")

        input_text = st.text_area(
            label="Message Text Input",
            value=default_text,
            height=130,
            key="text_input_area",
            label_visibility="collapsed",
            placeholder="e.g. URGENT! Your electricity connection will be disconnected today..."
        )

        btn_col1, btn_col2 = st.columns([1, 5])
        with btn_col1:
            analyze_clicked = st.button("🔍 Analyze Message", type="primary", key="btn_analyze_text")
        with btn_col2:
            if st.button("🗑️ Clear Input", key="btn_clear_text"):
                st.rerun()

        if analyze_clicked:
            if not input_text.strip():
                st.warning("⚠️ Please paste a message to analyze.")
            else:
                render_analysis_dashboard(input_text, processor, detector, risk_engine, explainer, guidance_engine)

    # TAB 2: SCREENSHOT OCR ANALYSIS
    with tab2:
        st.subheader("🖼️ Screenshot OCR Analysis")
        st.markdown("Upload a screenshot of a suspicious SMS or WhatsApp message (PNG, JPG, WEBP):")

        uploaded_file = st.file_uploader(
            "Choose a screenshot file",
            type=["png", "jpg", "jpeg", "webp"],
            key="ocr_uploader",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            col_img, col_txt = st.columns([1, 1])

            with col_img:
                st.image(uploaded_file, caption="Uploaded Screenshot Preview", use_container_width=True)

            image_bytes = uploaded_file.getvalue()
            ocr_res = ocr_engine.extract_text_from_bytes(image_bytes, mime_type=uploaded_file.type)

            with col_txt:
                if ocr_res.success:
                    st.success("✅ Text Extracted Successfully via OCR")
                    extracted_text = st.text_area("Extracted Text Preview:", value=ocr_res.extracted_text, height=130)
                    if st.button("🔍 Analyze Extracted Text", type="primary", key="btn_ocr_analyze"):
                        render_analysis_dashboard(extracted_text, processor, detector, risk_engine, explainer, guidance_engine)
                else:
                    st.warning(f"⚠️ OCR Notice: {ocr_res.error}")
                    st.info("💡 You can manually copy the text from your image and paste it into the **Text Analysis** tab.")

    # TAB 3: UPI INTENT URI ANALYSIS
    with tab3:
        st.subheader("💳 UPI Intent URI Analysis")
        st.markdown("Paste a `upi://pay` payment intent link to parse payment parameters and analyze transaction context:")

        sample_uri = "upi://pay?pa=merchant@upi&pn=Merchant&am=2999&cu=INR&tn=refund%20verification"
        pasted_uri = st.text_input(
            "Paste UPI URI:",
            value="",
            placeholder=sample_uri,
            key="upi_uri_input",
            label_visibility="collapsed"
        )

        u_btn1, u_btn2 = st.columns([1, 4])
        with u_btn1:
            parse_clicked = st.button("🔍 Parse & Analyze URI", type="primary", key="btn_upi_analyze")
        with u_btn2:
            if st.button("📋 Load Sample UPI URI", key="btn_load_sample_upi"):
                st.session_state["upi_uri_input"] = sample_uri
                st.rerun()

        target_uri = pasted_uri or (sample_uri if parse_clicked and not pasted_uri else "")
        if parse_clicked and target_uri:
            intent_data = upi_parser.parse_uri(target_uri)

            if intent_data.is_valid:
                st.success("✅ Valid UPI Payment Intent Format")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Payee Name", intent_data.payee_name or "N/A")
                c2.metric("Payee VPA", intent_data.payee_vpa or "N/A")
                c3.metric("Amount", f"{intent_data.currency or 'INR'} {intent_data.amount or 'N/A'}")
                c4.metric("Transaction Note", intent_data.transaction_note or "None")

                context_msg = intent_data.get_message_context()
                st.markdown(f"**Extracted Context for Analysis:** *\"{context_msg}\"*")
                st.markdown("---")
                render_analysis_dashboard(context_msg, processor, detector, risk_engine, explainer, guidance_engine)
            else:
                st.error("⚠️ Invalid UPI Intent URI")
                for err in intent_data.errors:
                    st.write(f"- {err}")


if __name__ == "__main__":
    main()
