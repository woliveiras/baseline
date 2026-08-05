"""Deterministic, fixture-specific Tuxedo evaluation checks."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import Any


IGNORED_OUTPUTS = {".tuxedo-final.txt"}


class UnsupportedProgram(ValueError):
    pass


def snapshot(workspace: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for path in sorted(item for item in workspace.rglob("*") if item.is_file()):
        relative = path.relative_to(workspace).as_posix()
        if (
            relative in IGNORED_OUTPUTS
            or relative == ".git"
            or relative.startswith(".git/")
            or relative.startswith("__pycache__/")
            or relative.endswith(".pyc")
            or relative.startswith(".pytest_cache/")
        ):
            continue
        values[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return values


def changed_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))


class SafeModule:
    """Evaluate the small pure functions used by controlled eval fixtures.

    This is an AST interpreter, not execution of agent-written Python. It
    intentionally rejects syntax outside the fixture's pure-function subset.
    """

    def __init__(self, path: Path):
        self.module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        self.functions = {
            node.name: node for node in self.module.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

    def call(self, name: str, *values: Any) -> Any:
        node = self.functions.get(name)
        if not isinstance(node, ast.FunctionDef) or node.decorator_list:
            raise UnsupportedProgram(f"unsupported function: {name}")
        arguments = node.args
        if arguments.vararg or arguments.kwarg or arguments.kwonlyargs or len(arguments.args) != len(values):
            raise UnsupportedProgram(f"unsupported signature: {name}")
        env = {argument.arg: value for argument, value in zip(arguments.args, values)}
        returned, value = self._statements(node.body, env)
        return value if returned else None

    def _statements(self, statements: list[ast.stmt], env: dict[str, Any]) -> tuple[bool, Any]:
        for statement in statements:
            if isinstance(statement, ast.Return):
                return True, self._expression(statement.value, env) if statement.value else None
            if isinstance(statement, ast.If):
                branch = statement.body if self._expression(statement.test, env) else statement.orelse
                returned, value = self._statements(branch, env)
                if returned:
                    return True, value
                continue
            if isinstance(statement, ast.Assign) and len(statement.targets) == 1 and isinstance(statement.targets[0], ast.Name):
                env[statement.targets[0].id] = self._expression(statement.value, env)
                continue
            if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name) and statement.value:
                env[statement.target.id] = self._expression(statement.value, env)
                continue
            if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant) and isinstance(statement.value.value, str):
                continue
            if isinstance(statement, ast.Pass):
                continue
            raise UnsupportedProgram(f"unsupported statement: {type(statement).__name__}")
        return False, None

    def _expression(self, node: ast.expr, env: dict[str, Any]) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            if node.id not in env:
                raise UnsupportedProgram(f"unknown name: {node.id}")
            return env[node.id]
        if isinstance(node, ast.UnaryOp):
            operand = self._expression(node.operand, env)
            if isinstance(node.op, ast.USub):
                return -operand
            if isinstance(node.op, ast.UAdd):
                return +operand
            if isinstance(node.op, ast.Not):
                return not operand
        if isinstance(node, ast.BinOp):
            left = self._expression(node.left, env)
            right = self._expression(node.right, env)
            operations = {
                ast.Add: lambda: left + right,
                ast.Sub: lambda: left - right,
                ast.Mult: lambda: left * right,
                ast.FloorDiv: lambda: left // right,
                ast.Mod: lambda: left % right,
            }
            operation = operations.get(type(node.op))
            if operation:
                return operation()
        if isinstance(node, ast.BoolOp):
            values = [bool(self._expression(value, env)) for value in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if isinstance(node, ast.Compare):
            left = self._expression(node.left, env)
            for operator, comparator in zip(node.ops, node.comparators):
                right = self._expression(comparator, env)
                comparisons = {
                    ast.Eq: left == right,
                    ast.NotEq: left != right,
                    ast.Lt: left < right,
                    ast.LtE: left <= right,
                    ast.Gt: left > right,
                    ast.GtE: left >= right,
                }
                if type(operator) not in comparisons or not comparisons[type(operator)]:
                    return False
                left = right
            return True
        if isinstance(node, ast.IfExp):
            return self._expression(node.body if self._expression(node.test, env) else node.orelse, env)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and not node.keywords:
            values = [self._expression(argument, env) for argument in node.args]
            if node.func.id == "min":
                return min(values)
            if node.func.id == "max":
                return max(values)
            if node.func.id == "abs":
                return abs(*values)
            if node.func.id in self.functions:
                return self.call(node.func.id, *values)
        raise UnsupportedProgram(f"unsupported expression: {type(node).__name__}")


def check(identifier: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"id": identifier, "pass": passed, "detail": detail}


def behavior_checks(workspace: Path, task: dict[str, Any]) -> list[dict[str, Any]]:
    verifier = task["verifier"]
    if verifier == "double-behavior":
        try:
            module = SafeModule(workspace / "app.py")
            observations = [module.call("double", value) for value in (0, 3, -2, 11)]
            expected = [0, 6, -4, 22]
            return [check("hidden-double-oracle", observations == expected, f"observed={observations}; expected={expected}")]
        except (OSError, SyntaxError, UnsupportedProgram, TypeError, ValueError) as exc:
            return [check("hidden-double-oracle", False, str(exc))]
    if verifier == "clamp-regression":
        results: list[dict[str, Any]] = []
        try:
            module = SafeModule(workspace / "clamp.py")
            cases = [(9, 1, 5, 5), (-2, 1, 5, 1), (3, 1, 5, 3), (5, 1, 5, 5)]
            observations = [module.call("clamp", value, low, high) for value, low, high, _ in cases]
            expected = [expected for _, _, _, expected in cases]
            results.append(check("hidden-clamp-oracle", observations == expected, f"observed={observations}; expected={expected}"))
        except (OSError, SyntaxError, UnsupportedProgram, TypeError, ValueError) as exc:
            results.append(check("hidden-clamp-oracle", False, str(exc)))
        results.append(check(
            "regression-assertion",
            has_collected_upper_bound_assertion(workspace),
            "requires a direct literal assertion in a collected test function for value > high",
        ))
        return results
    if verifier == "no-change":
        try:
            observed = SafeModule(workspace / "app.py").call("greeting")
            return [check("hidden-greeting-oracle", observed == "hello", f"observed={observed!r}; expected='hello'")]
        except (OSError, SyntaxError, UnsupportedProgram, TypeError, ValueError) as exc:
            return [check("hidden-greeting-oracle", False, str(exc))]
    return []


def literal(node: ast.AST) -> Any:
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError):
        return None


def _assertion_operands(node: ast.stmt) -> tuple[ast.expr, ast.expr] | None:
    if isinstance(node, ast.Assert) and isinstance(node.test, ast.Compare) and len(node.test.ops) == 1:
        if not isinstance(node.test.ops[0], ast.Eq):
            return None
        return node.test.left, node.test.comparators[0]
    if (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Attribute)
        and isinstance(node.value.func.value, ast.Name)
        and node.value.func.value.id in {"self", "cls"}
        and node.value.func.attr == "assertEqual"
        and len(node.value.args) == 2
        and not node.value.keywords
    ):
        return node.value.args[0], node.value.args[1]
    return None


def is_upper_bound_assertion(node: ast.stmt) -> bool:
    operands = _assertion_operands(node)
    if operands is None:
        return False
    left, right = operands
    call = left if isinstance(left, ast.Call) else right if isinstance(right, ast.Call) else None
    expected_node = right if call is left else left
    if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Name) or call.func.id != "clamp":
        return False
    arguments = [literal(argument) for argument in call.args]
    expected = literal(expected_node)
    if len(arguments) != 3 or not all(isinstance(value, (int, float)) for value in arguments):
        return False
    value, _, high = arguments
    return value > high and expected == high


def _is_test_case_class(node: ast.ClassDef) -> bool:
    if node.name.startswith("Test"):
        return True
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id == "TestCase":
            return True
        if isinstance(base, ast.Attribute) and base.attr == "TestCase":
            return True
    return False


def _collected_test_functions(tree: ast.Module) -> list[tuple[ast.FunctionDef, bool]]:
    collected: list[tuple[ast.FunctionDef, bool]] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            collected.append((node, False))
        elif isinstance(node, ast.ClassDef) and _is_test_case_class(node):
            collected.extend((child, True) for child in node.body if isinstance(child, ast.FunctionDef))
    return collected


def has_collected_upper_bound_assertion(workspace: Path) -> bool:
    for path in sorted(workspace.glob("test*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError):
            continue
        for function, is_method in _collected_test_functions(tree):
            expected_args = 1 if is_method else 0
            if (
                not function.name.startswith("test_")
                or function.decorator_list
                or len(function.args.args) != expected_args
                or (is_method and function.args.args[0].arg not in {"self", "cls"})
                or function.args.posonlyargs
                or function.args.kwonlyargs
                or function.args.vararg
                or function.args.kwarg
            ):
                continue
            body = function.body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                body = body[1:]
            if any(is_upper_bound_assertion(statement) for statement in body):
                return True
    return False


def verify(
    task: dict[str, Any],
    workspace: Path,
    before: dict[str, str],
) -> dict[str, Any]:
    after = snapshot(workspace)
    changed = changed_paths(before, after)
    checks: list[dict[str, Any]] = []
    mutation_policy = task["mutation_policy"]
    if mutation_policy == "required":
        checks.append(check("workspace-mutation", bool(changed), f"changed={changed}"))
    elif mutation_policy == "forbidden":
        checks.append(check("workspace-unchanged", not changed, f"changed={changed}"))
    elif mutation_policy != "allowed":
        checks.append(check("mutation-policy", False, f"unsupported policy: {mutation_policy}"))
    checks.extend(behavior_checks(workspace, task))
    failed = any(not item["pass"] for item in checks)
    status = "fail" if failed else "needs-review" if task["secondary_review"] else "pass"
    return {
        "status": status,
        "checks": checks,
        "changed_paths": changed,
        "secondary_review_required": bool(task["secondary_review"]),
    }
