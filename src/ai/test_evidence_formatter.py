from src.ai.investigator import investigate
from src.ai.evidence_formatter import (
    format_investigation_evidence
)


question = "Why did revenue decrease between 2017 and 2018?"

result = investigate(question)

if result["status"] != "success":

    print("Investigation failed:")
    print(result["message"])

else:

    evidence = format_investigation_evidence(
        result["investigation"]
    )

    print("FORMATTED ANALYTICAL EVIDENCE")
    print("=" * 100)
    print(evidence)