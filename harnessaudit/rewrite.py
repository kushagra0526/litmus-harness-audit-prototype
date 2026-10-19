"""Semantics-preserving rewrites of the reference: correct solutions that just look different.
A test that fails on one of these is testing the reference's internals, not the spec."""
import ast


class _RenamePrivate(ast.NodeTransformer):
    def _new(self, name):
        return "_r" + name if name.startswith("_") and not name.startswith("__") else name

    def visit_Attribute(self, n):
        self.generic_visit(n)
        n.attr = self._new(n.attr)
        return n

    def visit_FunctionDef(self, n):
        self.generic_visit(n)
        n.name = self._new(n.name)
        return n

    def visit_Name(self, n):
        n.id = self._new(n.id)
        return n


class _Reword(ast.NodeTransformer):
    def visit_Raise(self, n):
        if isinstance(n.exc, ast.Call) and n.exc.args:
            a = n.exc.args[0]
            if isinstance(a, ast.Constant) and isinstance(a.value, str):
                a.value = "invalid input (" + a.value.upper() + ")"
            elif isinstance(a, ast.BinOp) and isinstance(a.left, ast.Constant) and isinstance(a.left.value, str):
                a.left.value = "invalid input: "
        return n


class _ReverseUnordered(ast.NodeTransformer):
    def __init__(self, names):
        self.names, self.inside = set(names), False

    def visit_FunctionDef(self, n):
        prev, self.inside = self.inside, n.name in self.names
        self.generic_visit(n)
        self.inside = prev
        return n

    def visit_Return(self, n):
        if self.inside and n.value is not None:
            n.value = ast.Call(ast.Name("list", ast.Load()), [ast.Call(ast.Name("reversed", ast.Load()),
                               [ast.Call(ast.Name("list", ast.Load()), [n.value], [])], [])], [])
        return n


def rewrites(src, unordered=()):
    """{name: (reason, source)} for each rewrite that changes the code."""
    out = {}
    base = ast.unparse(ast.parse(src))
    for name, reason, tr in [
        ("rename_private", "uses a private name (attribute or helper starting with _) that a correct solution may not have", _RenamePrivate()),
        ("reword_errors", "asserts the exact text of an error message; the spec only fixes the exception type", _Reword()),
        ("reorder_unordered", "asserts an order the spec leaves open", _ReverseUnordered(unordered)),
    ]:
        t = tr.visit(ast.parse(src))
        ast.fix_missing_locations(t)
        s = ast.unparse(t)
        if s != base:
            out[name] = (reason, s)
    return out
