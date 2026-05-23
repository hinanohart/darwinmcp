"""Render a LineageGraph to a minimal standalone SVG (no graphviz dep).

The intent is debuggability, not aesthetics: a vertical chain of labelled
boxes, one per variant, with the fitness next to the variant ID.
"""

from __future__ import annotations

from .graph import LineageGraph


def render_svg(lineage: LineageGraph) -> str:
    nodes = list(lineage.graph.nodes(data=True))
    if not nodes:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="40"><text x="10" y="25">(empty lineage)</text></svg>'
    row_h = 36
    width = 380
    height = row_h * len(nodes) + 20
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'font-family="monospace" font-size="12">'
    ]
    for i, (vid, data) in enumerate(nodes):
        y = 20 + i * row_h
        fit = data.get("fitness")
        label = f"{vid}  fitness={fit}"
        parts.append(
            f'<rect x="10" y="{y - 14}" width="{width - 20}" height="22" '
            f'fill="white" stroke="black"/>'
        )
        parts.append(f'<text x="20" y="{y}">{label}</text>')
    parts.append("</svg>")
    return "".join(parts)
