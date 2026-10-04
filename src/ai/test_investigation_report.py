from src.ai.root_cause_engine import analyze_root_cause
from src.ai.investigation_report import (
    build_investigation_report,
    print_investigation_report
)


previous_year = 2017
current_year = 2018


root_cause_result = analyze_root_cause(
    current_year=current_year,
    previous_year=previous_year
)


report = build_investigation_report(
    root_cause_result
)


print_investigation_report(report)