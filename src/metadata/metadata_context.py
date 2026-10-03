from src.metadata.metadata_loader import (
    get_tables,
    get_columns,
    get_relationships,
    get_metrics
)


def build_metadata_context():
    tables = get_tables()
    columns = get_columns()
    relationships = get_relationships()
    metrics = get_metrics()

    context = {
        "tables": [],
        "columns": [],
        "relationships": [],
        "metrics": []
    }

    for table in tables:
        context["tables"].append({
            "table_name": table[0],
            "table_type": table[1],
            "description": table[2]
        })

    for column in columns:
        context["columns"].append({
            "table_name": column[0],
            "column_name": column[1],
            "data_type": column[2],
            "semantic_type": column[3],
            "column_role": column[4],
            "description": column[5],
            "is_nullable": column[6]
        })

    for relationship in relationships:
        context["relationships"].append({
            "source_table": relationship[0],
            "source_column": relationship[1],
            "target_table": relationship[2],
            "target_column": relationship[3],
            "relationship_type": relationship[4],
            "description": relationship[5]
        })

    for metric in metrics:
        context["metrics"].append({
            "metric_name": metric[0],
            "definition": metric[1],
            "sql_expression": metric[2],
            "metric_type": metric[3]
        })

    return context