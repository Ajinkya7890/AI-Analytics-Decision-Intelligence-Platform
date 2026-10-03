from src.ai.root_cause import compare_years


result = compare_years(
    current_year=2018,
    previous_year=2017
)


print("ROOT-CAUSE BASELINE")
print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")