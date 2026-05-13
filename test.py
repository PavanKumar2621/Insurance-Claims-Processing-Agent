# from app.extractor import (
#     extract_text_from_pdf,
#     extract_fields
# )

# # text = extract_text_from_pdf(
# #     # "docs/ACORD-Automobile-Loss-Notice-12.05.16.pdf"
# #     "docs/sample.pdf"
# # )
# with open("docs/sample_claim.txt", "r") as file:
#     text = file.read()

# # data = extract_fields(text)

# # print(data)
# data = extract_fields(text)

# print(data)

from app.extractor import extract_fields
from app.validator import validate_fields
from app.router import determine_route


with open("docs/sample_claim.txt", "r") as file:
    text = file.read()


data = extract_fields(text)

missing_fields = validate_fields(data)

route, reason = determine_route(
    data,
    missing_fields
)


final_output = {
    "extractedFields": data,
    "missingFields": missing_fields,
    "recommendedRoute": route,
    "reasoning": reason
}


print(final_output)