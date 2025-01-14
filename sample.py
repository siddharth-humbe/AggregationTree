import json

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.children = {}
        self.sum_pr = 0

    def add_child(self, key):
        if key not in self.children:
            self.children[key] = TreeNode(key)
        return self.children[key]

    def __repr__(self):
        return f"TreeNode(key={self.key}, sum_pr={self.sum_pr})"


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


# fetching when online URI
# def fetch_data(uri):
#     """
#     Fetch JSON data from a given URI.
#     """
#     response = requests.get(uri)
#     response.raise_for_status()  # Raise an error for unsuccessful requests
#     return response.json()

# # Example usage
# uri = '/Users/siddharth/Desktop_Folder/Siglens_AggregationTrees/MOCK_DATA.json'
# # Replace with the actual URI
# data = fetch_data(uri)
# data = [
#     {"fname": "sam", "bnum": "batch-1", "os": "iOS",   "pr": 23},
#     {"fname": "john", "bnum": "batch-2", "os": "iOS",   "pr": 14},
#     {"fname": "sam", "bnum": "batch-2", "os": "win",   "pr": 15},
#     {"fname": "sam", "bnum": "batch-1", "os": "linux", "pr": 22},
# ]
def fetch_data(file_path):
    """
    Load JSON data from a local file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

# Example usage
file_path = "/Users/siddharth/Desktop_Folder/Siglens_AggregationTrees/MOCK_DATA2.json"
data = fetch_data(file_path)

aggregation_tree = AggregationTree(data)

# Compute statistics grouped by fname
print("Group by fname:")
group_by_fname = aggregation_tree.compute_groupby("fname")
for key, pr_sum in group_by_fname.items():
    print(f"{key}, {pr_sum}")

# Compute statistics grouped by bnum
print("\nGroup by bnum:")
group_by_bnum = aggregation_tree.compute_groupby("bnum")
for key, pr_sum in group_by_bnum.items():
    print(f"{key}, {pr_sum}")

# Compute statistics grouped by os
print("\nGroup by os:")
group_by_os = aggregation_tree.compute_groupby("os")
for key, pr_sum in group_by_os.items():
    print(f"{key}, {pr_sum}")