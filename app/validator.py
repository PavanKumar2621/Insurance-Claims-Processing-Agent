def validate_fields(data):

    mandatory_fields = [
        "policy_number",
        "policyholder_name",
        "effective_dates",
        "date_of_loss",
        "time_of_loss",
        "location",
        "claimant",
        "third_parties",
        "contact_details",
        "asset_type",
        "asset_id",
        "estimated_damage",
        "claim_type",
        "attachments",
        "initial_estimate",
        "description"
    ]

    missing_fields = []

    for field in mandatory_fields:

        value = data.get(field)

        if value is None or value == "":
            missing_fields.append(field)

    return missing_fields