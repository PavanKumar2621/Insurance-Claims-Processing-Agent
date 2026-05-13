def determine_route(data, missing_fields):

    description = (
        (data.get("description") or "")
        .lower()
    )

    claim_type = (
        (data.get("claim_type") or "")
        .lower()
    )

    estimated_damage = data.get("estimated_damage")

    if estimated_damage is not None:

        estimated_damage = int(
            str(estimated_damage).replace(",", "")
        )

    # RULE 1
    if missing_fields:

        return (
            "Manual Review",
            "Mandatory fields are missing."
        )

    # RULE 2
    fraud_keywords = [
        "fraud",
        "staged",
        "inconsistent"
    ]

    for word in fraud_keywords:

        if word in description:

            return (
                "Investigation Flag",
                f"Description contains suspicious keyword: {word}"
            )

    # RULE 3
    if claim_type == "injury":

        return (
            "Specialist Queue",
            "Claim type is injury."
        )

    # RULE 4
    if estimated_damage < 25000:

        return (
            "Fast-track",
            "Estimated damage below 25000."
        )

    # DEFAULT
    return (
        "Standard Review",
        "Requires normal processing."
    )