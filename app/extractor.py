# import re
# import pdfplumber


# def extract_text_from_pdf(file_path):

#     text = ""

#     with pdfplumber.open(file_path) as pdf:

#         for page in pdf.pages:

#             extracted = page.extract_text()

#             if extracted:
#                 text += extracted + "\n"

#     return text


# def extract_fields(text):

#     extracted_data = {}

#     # POLICY NUMBER
#     policy_match = re.search(
#         r'POLICY NUMBER\s+([A-Z0-9\-]{5,})',
#         text,
#         re.IGNORECASE
#     )

#     # DATE OF LOSS
#     date_match = re.search(
#         r'DATE OF LOSS.*?(\d{2}/\d{2}/\d{4})',
#         text,
#         re.IGNORECASE
#     )

#     # ESTIMATE AMOUNT
#     estimate_match = re.search(
#         r'ESTIMATE AMOUNT[:\s]+\$?([\d,]+)',
#         text,
#         re.IGNORECASE
#     )

#     # DESCRIPTION OF ACCIDENT
#     description_match = re.search(
#         r'DESCRIPTION OF ACCIDENT(.*?)(LOSS|OWNER)',
#         text,
#         re.IGNORECASE | re.DOTALL
#     )

#     extracted_data["policy_number"] = clean_text(
#         policy_match.group(1)
#         if policy_match else None
#     )

#     extracted_data["date_of_loss"] = (
#         date_match.group(1)
#         if date_match else None
#     )

#     extracted_data["estimated_damage"] = (
#         estimate_match.group(1)
#         if estimate_match else None
#     )

#     extracted_data["description"] = (
#         description_match.group(1).strip()
#         if description_match else None
#     )

#     return extracted_data


# def clean_text(value):

#     if not value:
#         return None

#     value = value.strip()

#     junk_words = [
#         "CONTACT",
#         "LOSS",
#         "OWNER",
#         "INSURED"
#     ]

#     if value.upper() in junk_words:
#         return None

#     return value

import re
import pdfplumber


def extract_text_from_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    return text
def extract_fields(text):

    extracted_data = {
        "policy_number": None,
        "policyholder_name": None,
        "effective_dates": None,
        "date_of_loss": None,
        "time_of_loss": None,
        "location": None,
        "claimant": None,
        "third_parties": None,
        "contact_details": None,
        "asset_type": None,
        "asset_id": None,
        "estimated_damage": None,
        "claim_type": None,
        "attachments": None,
        "initial_estimate": None,
        "description": None
    }

    lines = text.splitlines()

    description_started = False
    description_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # POLICY NUMBER
        if line.startswith("Policy Number:"):
            value = line.replace("Policy Number:", "").strip()
            extracted_data["policy_number"] = value or None

        # POLICYHOLDER NAME
        elif line.startswith("Policyholder Name:"):
            value = line.replace("Policyholder Name:", "").strip()
            extracted_data["policyholder_name"] = value or None

        # EFFECTIVE DATES
        elif line.startswith("Effective Dates:"):
            value = line.replace("Effective Dates:", "").strip()
            extracted_data["effective_dates"] = value or None

        # DATE OF LOSS
        elif line.startswith("Date of Loss:"):
            value = line.replace("Date of Loss:", "").strip()
            extracted_data["date_of_loss"] = value or None

        # TIME OF LOSS
        elif line.startswith("Time of Loss:"):
            value = line.replace("Time of Loss:", "").strip()
            extracted_data["time_of_loss"] = value or None

        # LOCATION
        elif line.startswith("Location:"):
            value = line.replace("Location:", "").strip()
            extracted_data["location"] = value or None

        # CLAIMANT
        elif line.startswith("Claimant:"):
            value = line.replace("Claimant:", "").strip()
            extracted_data["claimant"] = value or None

        # THIRD PARTIES
        elif line.startswith("Third Parties:"):
            value = line.replace("Third Parties:", "").strip()
            extracted_data["third_parties"] = value or None

        # CONTACT DETAILS
        elif line.startswith("Contact Details:"):
            value = line.replace("Contact Details:", "").strip()
            extracted_data["contact_details"] = value or None

        # ASSET TYPE
        elif line.startswith("Asset Type:"):
            value = line.replace("Asset Type:", "").strip()
            extracted_data["asset_type"] = value or None

        # ASSET ID
        elif line.startswith("Asset ID:"):
            value = line.replace("Asset ID:", "").strip()
            extracted_data["asset_id"] = value or None

        # ESTIMATED DAMAGE
        elif line.startswith("Estimated Damage:"):
            value = line.replace("Estimated Damage:", "").strip()
            extracted_data["estimated_damage"] = value or None

        # CLAIM TYPE
        elif line.startswith("Claim Type:"):
            value = line.replace("Claim Type:", "").strip()
            extracted_data["claim_type"] = value or None

        # ATTACHMENTS
        elif line.startswith("Attachments:"):
            value = line.replace("Attachments:", "").strip()
            extracted_data["attachments"] = value or None

        # INITIAL ESTIMATE
        elif line.startswith("Initial Estimate:"):
            value = line.replace("Initial Estimate:", "").strip()
            extracted_data["initial_estimate"] = value or None

        # DESCRIPTION START
        elif line.startswith("Description:"):

            description_started = True

            value = line.replace("Description:", "").strip()

            if value:
                description_lines.append(value)

        # DESCRIPTION CONTENT
        elif description_started:
            description_lines.append(line)

    # FINAL DESCRIPTION
    if description_lines:
        extracted_data["description"] = " ".join(description_lines)

    return extracted_data