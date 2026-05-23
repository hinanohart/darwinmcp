"""Concrete FitnessTask implementations bundled with darwinmcp.

v0.1 ships ONE task — `HelloWorldTask` — sufficient to exercise the smoke
loop end-to-end. SWE-bench Verified adapters land in v0.2.
"""

from __future__ import annotations

from .fitness_base import FitnessTask


class HelloWorldTask(FitnessTask):
    """The simplest possible probe: parse-check the variant code.

    The probe imports the variant module body via `compile()`. The variant
    passes iff it is syntactically valid Python. This is intentionally weak:
    it lets DummyLLM-driven evolve runs progress, while making it obvious in
    the README and CHANGELOG that v0.1 does NOT claim a substantive fitness.
    """

    name = "hello_world"

    def probe(self, variant_code: str) -> str:
        # We embed the variant as a triple-quoted string so the sandbox is one
        # short self-contained Python program. The sandbox runs this string.
        escaped = variant_code.replace('"""', '\\"\\"\\"')
        return (
            "code = '''" + escaped.replace("'", "\\'") + "'''\n"
            "try:\n"
            "    compile(code, '<variant>', 'exec')\n"
            "    print('PASS')\n"
            "except SyntaxError as e:\n"
            "    print(f'FAIL: {e!s}')\n"
        )
