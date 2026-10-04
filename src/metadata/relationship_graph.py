from collections import defaultdict, deque

from src.metadata.metadata_loader import get_relationships


class RelationshipGraph:
    """
    Metadata-driven graph of relationships between analytical tables.

    The graph is built from metadata.relationships and can be used
    to discover join paths between fact, dimension, and analytical
    tables.
    """

    def __init__(self):
        self.relationships = self._load_relationships()
        self.graph = self._build_graph()

    def _load_relationships(self):
        """
        Load relationship metadata from PostgreSQL.
        """

        relationships = []

        for row in get_relationships():
            relationships.append({
                "source_table": row[0],
                "source_column": row[1],
                "target_table": row[2],
                "target_column": row[3],
                "relationship_type": row[4],
                "description": row[5]
            })

        return relationships

    def _build_graph(self):
        """
        Build a bidirectional graph.

        Each edge retains the columns required to construct
        the corresponding JOIN.
        """

        graph = defaultdict(list)

        for relationship in self.relationships:

            source_table = relationship["source_table"]
            target_table = relationship["target_table"]

            graph[source_table].append({
                "table": target_table,
                "from_column": relationship["source_column"],
                "to_column": relationship["target_column"],
                "direction": "forward",
                "relationship": relationship
            })

            graph[target_table].append({
                "table": source_table,
                "from_column": relationship["target_column"],
                "to_column": relationship["source_column"],
                "direction": "reverse",
                "relationship": relationship
            })

        return graph

    def get_neighbors(self, table_name):
        """
        Return tables directly connected to the given table.
        """

        return self.graph.get(
            table_name,
            []
        )

    def find_path(self, source_table, target_table):
        """
        Find the shortest metadata-defined relationship path
        between two tables.

        Returns a list of relationship edges.

        Returns an empty list when source and target are the same.
        Returns None when no path exists.
        """

        if source_table == target_table:
            return []

        queue = deque([
            (
                source_table,
                []
            )
        ])

        visited = {
            source_table
        }

        while queue:

            current_table, path = queue.popleft()

            for edge in self.graph.get(
                current_table,
                []
            ):

                next_table = edge["table"]

                if next_table in visited:
                    continue

                new_path = path + [edge]

                if next_table == target_table:
                    return new_path

                visited.add(next_table)

                queue.append(
                    (
                        next_table,
                        new_path
                    )
                )

        return None

    def get_join_path(
        self,
        source_table,
        target_table
    ):
        """
        Return a simplified join path containing the table
        and column information required for SQL generation.
        """

        path = self.find_path(
            source_table=source_table,
            target_table=target_table
        )

        if path is None:
            return None

        current_table = source_table
        joins = []

        for edge in path:

            joins.append({
                "left_table": current_table,
                "left_column": edge["from_column"],
                "right_table": edge["table"],
                "right_column": edge["to_column"]
            })

            current_table = edge["table"]

        return joins


def get_relationship_graph():
    """
    Create a relationship graph from the current dataset metadata.
    """

    return RelationshipGraph()