from src.metadata.metadata_context import build_metadata_context


context = build_metadata_context()

print("Tables:", len(context["tables"]))
print("Columns:", len(context["columns"]))
print("Relationships:", len(context["relationships"]))
print("Metrics:", len(context["metrics"]))

print("\nFirst table:")
print(context["tables"][0])

print("\nFirst metric:")
print(context["metrics"][0])