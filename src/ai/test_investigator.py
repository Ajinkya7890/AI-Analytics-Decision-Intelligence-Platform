from src.ai.investigator import investigate


question = "Why did revenue decrease between 2017 and 2018?"

result = investigate(question)

print("INVESTIGATION STATUS")
print("=" * 80)

print(result["status"])

print("\nQUESTION")
print(result["question"])

print("\nANALYSIS")
print(result["analysis"])

if result["status"] == "success":

    print("\nINVESTIGATION")
    print(result["investigation"])

else:

    print("\nMESSAGE")
    print(result["message"])