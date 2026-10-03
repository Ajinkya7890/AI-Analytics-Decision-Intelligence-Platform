from src.ai.root_cause_engine import analyze_root_cause
from src.ai.investigation_result import (
    build_investigation_result,
    print_investigation_result
)


root_cause_result = analyze_root_cause(
    current_year=2018,
    previous_year=2017
)


investigation_result = build_investigation_result(
    root_cause_result
)


print_investigation_result(
    investigation_result
)