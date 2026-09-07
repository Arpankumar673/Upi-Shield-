"""
UPI Intent URI Parser for UPI-Shield.
Parses, decodes, and validates upi://pay URI strings and extracts transaction context parameters.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from urllib.parse import urlparse, parse_qs, unquote


class UPIIntentData(BaseModel):
    is_valid: bool = False
    payee_vpa: Optional[str] = None
    payee_name: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    transaction_note: Optional[str] = None
    raw_uri: str = ""
    errors: List[str] = Field(default_factory=list)

    def get_message_context(self) -> str:
        """Combines parsed parameters into a natural message context for the detection pipeline."""
        parts = []
        if self.transaction_note:
            parts.append(f"Transaction note: {self.transaction_note}")
        if self.payee_name:
            parts.append(f"Payee Name: {self.payee_name}")
        if self.payee_vpa:
            parts.append(f"Payee VPA: {self.payee_vpa}")
        if self.amount:
            curr = self.currency or "INR"
            parts.append(f"Payment Amount requested: {curr} {self.amount}")

        if not parts:
            return f"UPI payment intent to VPA: {self.payee_vpa or 'Unknown'}"

        return ". ".join(parts) + "."


class UPIParser:
    """Parses and validates upi://pay URI parameters."""

    def parse_uri(self, uri: Optional[str]) -> UPIIntentData:
        if not uri or not isinstance(uri, str):
            return UPIIntentData(
                is_valid=False,
                raw_uri=str(uri or ""),
                errors=["Empty or invalid URI input."]
            )

        raw = uri.strip()
        errors = []

        # Validate URI Scheme
        if not raw.lower().startswith("upi://pay"):
            return UPIIntentData(
                is_valid=False,
                raw_uri=raw,
                errors=["Invalid UPI scheme. Expected URI starting with 'upi://pay'."]
            )

        try:
            parsed = urlparse(raw)
            qs_dict = parse_qs(parsed.query, keep_blank_values=True)

            # Extract fields
            pa_raw = qs_dict.get("pa", [None])[0]
            pn_raw = qs_dict.get("pn", [None])[0]
            am_raw = qs_dict.get("am", [None])[0]
            cu_raw = qs_dict.get("cu", ["INR"])[0]
            tn_raw = qs_dict.get("tn", [None])[0]

            payee_vpa = unquote(pa_raw).strip() if pa_raw else None
            payee_name = unquote(pn_raw).strip() if pn_raw else None
            currency = unquote(cu_raw).strip().upper() if cu_raw else "INR"
            transaction_note = unquote(tn_raw).strip() if tn_raw else None

            # Validate VPA presence
            if not payee_vpa:
                errors.append("Missing required payee VPA ('pa') parameter.")

            # Validate Amount if present
            amount = None
            if am_raw:
                am_clean = unquote(am_raw).strip()
                try:
                    amt_val = float(am_clean)
                    if amt_val <= 0:
                        errors.append(f"Non-positive amount specified: '{am_clean}'.")
                    amount = f"{amt_val:.2f}"
                except ValueError:
                    errors.append(f"Invalid numeric amount format: '{am_clean}'.")
                    amount = am_clean

            is_valid = len(errors) == 0 and payee_vpa is not None

            return UPIIntentData(
                is_valid=is_valid,
                payee_vpa=payee_vpa,
                payee_name=payee_name,
                amount=amount,
                currency=currency,
                transaction_note=transaction_note,
                raw_uri=raw,
                errors=errors
            )

        except Exception as e:
            return UPIIntentData(
                is_valid=False,
                raw_uri=raw,
                errors=[f"URI parsing error: {str(e)}"]
            )
