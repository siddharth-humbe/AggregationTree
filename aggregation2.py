import graphviz

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.children = {}
        self.sum_pr = 0

    def add_child(self, key):
        if key not in self.children:
            self.children[key] = TreeNode(key)
        return self.children[key]

    def generate_graphviz(self, graph=None):
        """
        Recursively generates a Graphviz DOT representation of the tree.
        """
        if graph is None:
            graph = graphviz.Digraph(format="png")
            graph.node(str(id(self)), f"{self.key} ({self.sum_pr})")

        for child in self.children.values():
            graph.node(str(id(child)), f"{child.key} ({child.sum_pr})")
            graph.edge(str(id(self)), str(id(child)))
            child.generate_graphviz(graph)

        return graph

class AggregationTree:
    def __init__(self, data):
        self.data = data
        self.root = TreeNode("root")
        self.build_tree()

    def build_tree(self):
        for record in self.data:
            fname, bnum, os, pr = record["fname"], record["bnum"], record["os"], record["pr"]

            # Build the tree based on the hierarchy: fname -> bnum -> os
            current = self.root
            for key in [fname, bnum, os]:
                current = current.add_child(key)
                current.sum_pr += pr

    def compute_groupby(self, group_by_column):
        # Determine the target level based on the column
        levels = {"fname": 1, "bnum": 2, "os": 3}
        if group_by_column not in levels:
            raise ValueError(f"Invalid column name: {group_by_column}")
        target_level = levels[group_by_column]

        # Collect results from the target level
        result = {}
        self._compute_groupby_helper(self.root, result, target_level, current_level=0)
        return result

    def _compute_groupby_helper(self, node, result, target_level, current_level):
        if current_level == target_level:
            # Aggregate sum_pr for each group
            if node.key != "root":  # Skip the root node
                if node.key not in result:
                    result[node.key] = 0
                result[node.key] += node.sum_pr
            return

        # Traverse children
        for child in node.children.values():
            self._compute_groupby_helper(child, result, target_level, current_level + 1)