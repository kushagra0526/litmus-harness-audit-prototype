"""AST mutants of a reference solution: small, plausible bugs a candidate's code could contain."""
import ast
import copy

CMP = {ast.Lt: [ast.LtE], ast.LtE: [ast.Lt], ast.Gt: [ast.GtE], ast.GtE: [ast.Gt], ast.Eq: [ast.NotEq],
       ast.NotEq: [ast.Eq], ast.In: [ast.NotIn], ast.NotIn: [ast.In]}
BIN = {ast.Add: [ast.Sub], ast.Sub: [ast.Add], ast.Mult: [ast.Add], ast.FloorDiv: [ast.Div], ast.Mod: [ast.FloorDiv]}
STMTS = (ast.Assign, ast.AugAssign, ast.Expr, ast.If, ast.Delete, ast.Raise)


def _ops(node):
    """(description, function(node_copy) -> replacement node) for one AST node."""
    out = []
    if isinstance(node, ast.Compare) and len(node.ops) == 1:
        for new in CMP.get(type(node.ops[0]), []):
            out.append((f"{type(node.ops[0]).__name__} -> {new.__name__}", lambda n, new=new: _set(n, "ops", [new()])))
    if isinstance(node, ast.BinOp):
        for new in BIN.get(type(node.op), []):
            out.append((f"{type(node.op).__name__} -> {new.__name__}", lambda n, new=new: _set(n, "op", new())))
    if isinstance(node, ast.Constant) and type(node.value) is int:
        for d in (1, -1):
            out.append((f"{node.value} -> {node.value + d}", lambda n, d=d: ast.Constant(n.value + d)))
    if isinstance(node, ast.BoolOp):
        new = ast.Or if isinstance(node.op, ast.And) else ast.And
        out.append((f"{type(node.op).__name__} -> {new.__name__}", lambda n, new=new: _set(n, "op", new())))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.Not, ast.USub)):
        out.append((f"drop {type(node.op).__name__}", lambda n: n.operand))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and not node.args and not node.keywords:
        out.append((f"drop .{node.func.attr}()", lambda n: n.func.value))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("max", "min") and len(node.args) == 2:
        for i in (0, 1):
            out.append((f"{node.func.id}(a, b) -> arg {i}", lambda n, i=i: n.args[i]))
    if isinstance(node, ast.Return) and node.value is not None:
        out.append(("return None", lambda n: _set(n, "value", None)))
    return out


def _set(n, field, value):
    setattr(n, field, value)
    return n


class _Replace(ast.NodeTransformer):
    def __init__(self, target, fn):
        self.target, self.fn, self.i = target, fn, -1

    def generic_visit(self, node):
        return super().generic_visit(node)

    def visit(self, node):
        self.i += 1
        if self.i == self.target:
            return self.fn(node)
        return self.generic_visit(node)


def _preorder(tree):
    out = []

    class V(ast.NodeVisitor):
        def visit(self, node):
            out.append(node)
            self.generic_visit(node)
    V().visit(tree)
    return out


def mutants(src):
    """Yield dicts {line, op, source} for every single-site mutant (deduplicated, syntax-valid)."""
    tree = ast.parse(src)
    base = ast.unparse(tree)
    seen = {base}
    nodes = _preorder(tree)
    for idx, node in enumerate(nodes):
        cands = list(_ops(node))
        for desc, fn in cands:
            t = copy.deepcopy(tree)
            t = _Replace(idx, fn).visit(t)
            ast.fix_missing_locations(t)
            yield from _emit(t, node, desc, seen)
        # statement deletion inside any body
        for field in ("body", "orelse"):
            body = getattr(node, field, None)
            if isinstance(body, list):
                for j, st in enumerate(body):
                    if isinstance(st, STMTS) and not (isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant)):
                        t = copy.deepcopy(tree)
                        tgt = _preorder(t)[idx]
                        getattr(tgt, field)[j] = ast.Pass()
                        ast.fix_missing_locations(t)
                        yield from _emit(t, st, "delete statement", seen)


def _emit(t, node, desc, seen):
    try:
        s = ast.unparse(t)
        compile(s, "<mutant>", "exec")
    except (SyntaxError, ValueError, TypeError):
        return
    if s in seen:
        return
    seen.add(s)
    yield {"line": getattr(node, "lineno", 0), "op": desc, "source": s}
