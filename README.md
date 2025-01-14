# Aggregation Tree Viewer

A Python-based application to visualize and compute group-by statistics from hierarchical JSON data. The app uses an **aggregation tree** to represent and process the data efficiently. It provides a Streamlit frontend for easy interaction, allowing users to input a local JSON file path, compute statistics, and visualize the aggregation tree.

---

## Features

- **Compute Group-By Statistics**: Aggregate the `pr` values based on columns such as `fname`, `bnum`, or `os`.
- **Tree Visualization**: Generate and display an image of the aggregation tree.
- **Interactive Frontend**: Streamlit-based user interface to input file paths and view results.
- **Error Handling**: Provides user-friendly error messages for invalid file paths or JSON formats.

---

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

1. **Python (>= 3.7)**
2. **pip** (Python package manager)
3. **Graphviz** (for tree visualization)

---

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo-name/aggregation-tree-viewer.git
   cd aggregation-tree-viewer

2. **Install Graphviz**:
   2.1 for ubuntu/debain:
        sudo apt install graphviz
   2.2 for macos:
        brew install graphviz

3. **Run the application:**
   streamlit run app.py

4. Input json format:
[
    {"fname": "sam", "bnum": "batch-1", "os": "iOS", "pr": 23},
    {"fname": "john", "bnum": "batch-2", "os": "iOS", "pr": 14},
    {"fname": "sam", "bnum": "batch-2", "os": "win", "pr": 15},
    {"fname": "sam", "bnum": "batch-1", "os": "linux", "pr": 22}
]
    
