import ast
from typing import Dict, Any, Tuple

class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.max_depth = 0
        self.node_count = 0

    def parse_code(self, source_code: str) -> Tuple[Dict[str, Any], int, int]:
        tree = ast.parse(source_code)
        raw_tree = self._visit_node(tree, depth=0)
        return raw_tree, self.node_count, self.max_depth

    def _visit_node(self, node: ast.AST, depth: int) -> Dict[str, Any]:
        self.node_count += 1
        if depth > self.max_depth:
            self.max_depth = depth

        kind = node.__class__.__name__
        name = getattr(node, 'name', str(kind))
        line = getattr(node, 'lineno', 1)

        children = []
        for child in ast.iter_child_nodes(node):
            # Focus on structural statement nodes to keep tree clean
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                                 ast.If, ast.For, ast.While, ast.Import, ast.ImportFrom,
                                 ast.Assign, ast.Return, ast.Call)):
                children.append(self._visit_node(child, depth + 1))

        return {
            "id": f"{kind}_{line}_{self.node_count}",
            "name": name,
            "kind": kind,
            "line": line,
            "depth": depth,
            "children": children
        }