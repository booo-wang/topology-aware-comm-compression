from __future__ import annotations

import argparse
import html
from pathlib import Path

from tacc.reporting.findings import build_findings
from tacc.reporting.markdown import load_latest_benchmark_result


PALETTE = {
    "chain": "#1f6feb",
    "ring": "#2da44e",
    "star": "#bc4c00",
    "fully_connected": "#8250df",
}


def _group_topologies(experiments: list[dict[str, object]]) -> list[dict[str, object]]:
    buckets: dict[str, list[dict[str, object]]] = {}
    for item in experiments:
        topology = item["communication"]["topology"]
        buckets.setdefault(topology, []).append(item)

    summary = []
    for topology, items in buckets.items():
        avg_recall = sum(entry["summary"]["avg_mean_recall"] for entry in items) / len(items)
        avg_efficiency = sum(entry["summary"]["avg_efficiency"] for entry in items) / len(items)
        summary.append(
            {
                "topology": topology,
                "count": len(items),
                "avg_recall": avg_recall,
                "avg_efficiency": avg_efficiency,
                "color": PALETTE.get(topology, "#57606a"),
            }
        )
    return sorted(summary, key=lambda item: item["avg_recall"], reverse=True)


def _build_topology_cards(experiments: list[dict[str, object]]) -> str:
    cards: list[str] = []
    for item in _group_topologies(experiments):
        cards.append(
            f"""
            <div class="mini-card" style="border-top-color: {item['color']}">
              <div class="mini-label">{html.escape(item['topology'])}</div>
              <div class="mini-metric">{item['avg_recall']:.3f}</div>
              <div class="mini-sub">avg recall across {item['count']} runs</div>
              <div class="mini-sub">efficiency {item['avg_efficiency']:.5f}</div>
            </div>
            """.strip()
        )
    return "\n".join(cards)


def _build_rows(experiments: list[dict[str, object]], limit: int = 12) -> str:
    rows: list[str] = []
    for item in experiments[:limit]:
        comm = item["communication"]
        env = item["environment"]
        summary = item["summary"]
        topology = comm["topology"]
        color = PALETTE.get(topology, "#57606a")
        rows.append(
            f"""
            <tr>
              <td><span class="pill" style="background:{color}"></span>{html.escape(item['name'])}</td>
              <td>{html.escape(topology)}</td>
              <td>{html.escape(comm['compressor'])}</td>
              <td>{comm['message_budget']}</td>
              <td>{env['visibility_prob']}</td>
              <td>{comm['message_dropout_prob']}</td>
              <td>{summary['avg_mean_recall']:.4f}</td>
              <td>{summary['avg_efficiency']:.6f}</td>
              <td>{' / '.join(f'{hop:.3f}' for hop in summary['avg_hop_mean_recalls'])}</td>
            </tr>
            """.strip()
        )
    return "\n".join(rows)


def _build_hop_bars(hops: list[float]) -> str:
    bars: list[str] = []
    for idx, hop in enumerate(hops, start=1):
        width = max(4, int(hop * 100))
        bars.append(
            f"""
            <div class="hop-row">
              <div class="hop-label">Hop {idx}</div>
              <div class="hop-track"><div class="hop-fill" style="width:{width}%"></div></div>
              <div class="hop-value">{hop:.3f}</div>
            </div>
            """.strip()
        )
    return "\n".join(bars)


def _build_findings(findings: list[str]) -> str:
    cards: list[str] = []
    for finding in findings:
        cards.append(
            f"""
            <div class="finding-card">
              <div class="finding-title">Current finding</div>
              <div class="finding-body">{html.escape(finding)}</div>
            </div>
            """.strip()
        )
    return "\n".join(cards)


def build_dashboard_html(result: dict[str, object], source_path: Path) -> str:
    experiments = result["experiments"]
    top_result = result["top_result"]
    summary = top_result["summary"]
    comm = top_result["communication"]
    env = top_result["environment"]
    findings = build_findings(result)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TACC Dashboard</title>
  <style>
    :root {{
      --bg: #f6f1e8;
      --panel: rgba(255,255,255,0.78);
      --ink: #1d232a;
      --muted: #59636e;
      --accent: #bc4c00;
      --line: rgba(29,35,42,0.08);
      --shadow: 0 18px 45px rgba(44, 31, 10, 0.12);
      --radius: 22px;
      font-family: Georgia, 'Times New Roman', serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(188,76,0,0.14), transparent 28%),
        radial-gradient(circle at top right, rgba(31,111,235,0.10), transparent 24%),
        linear-gradient(180deg, #fbf6ef 0%, var(--bg) 100%);
    }}
    .page {{ max-width: 1180px; margin: 0 auto; padding: 36px 20px 64px; }}
    .hero {{ display: grid; grid-template-columns: 1.4fr 1fr; gap: 18px; margin-bottom: 18px; }}
    .panel {{ background: var(--panel); backdrop-filter: blur(12px); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); }}
    .hero-main {{ padding: 28px; }}
    .eyebrow {{ font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); margin-bottom: 10px; }}
    h1 {{ margin: 0 0 10px; font-size: clamp(32px, 5vw, 54px); line-height: 0.95; }}
    .sub {{ color: var(--muted); font-size: 17px; line-height: 1.55; max-width: 58ch; }}
    .meta {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }}
    .tag {{ border: 1px solid var(--line); border-radius: 999px; padding: 8px 12px; font-size: 13px; background: rgba(255,255,255,0.5); }}
    .hero-side {{ padding: 22px; display: grid; gap: 12px; }}
    .stat {{ padding: 14px 16px; border-radius: 16px; background: rgba(255,255,255,0.72); border: 1px solid var(--line); }}
    .stat-label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }}
    .stat-value {{ font-size: 28px; margin-top: 6px; font-weight: 700; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; margin-bottom: 18px; }}
    .card {{ padding: 22px; }}
    .card h2 {{ margin: 0 0 14px; font-size: 20px; }}
    .best-lines {{ display: grid; gap: 8px; color: var(--muted); }}
    .best-lines strong {{ color: var(--ink); }}
    .hop-stack {{ display: grid; gap: 10px; }}
    .hop-row {{ display: grid; grid-template-columns: 70px 1fr 52px; gap: 10px; align-items: center; }}
    .hop-label, .hop-value {{ font-size: 13px; color: var(--muted); }}
    .hop-track {{ height: 12px; background: rgba(29,35,42,0.08); border-radius: 999px; overflow: hidden; }}
    .hop-fill {{ height: 100%; background: linear-gradient(90deg, var(--accent), #e58d2d); border-radius: 999px; }}
    .mini-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 14px; }}
    .mini-card, .finding-card {{ padding: 16px; border-radius: 18px; background: rgba(255,255,255,0.76); border: 1px solid var(--line); border-top: 4px solid var(--accent); }}
    .mini-label, .finding-title {{ font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }}
    .mini-metric {{ font-size: 28px; margin: 8px 0 2px; }}
    .mini-sub, .finding-body {{ font-size: 13px; color: var(--muted); line-height: 1.5; }}
    .table-panel {{ padding: 16px; overflow: hidden; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
    th, td {{ padding: 12px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }}
    .pill {{ display: inline-block; width: 10px; height: 10px; border-radius: 999px; margin-right: 8px; vertical-align: middle; }}
    .footer {{ margin-top: 16px; color: var(--muted); font-size: 13px; }}
    @media (max-width: 980px) {{
      .hero, .grid {{ grid-template-columns: 1fr; }}
      .mini-grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
    }}
    @media (max-width: 640px) {{
      .page {{ padding: 20px 14px 44px; }}
      .mini-grid {{ grid-template-columns: 1fr; }}
      table {{ display: block; overflow-x: auto; white-space: nowrap; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <div class="panel hero-main">
        <div class="eyebrow">TACC Findings Dashboard</div>
        <h1>Communication Strategy Explorer</h1>
        <div class="sub">A static results dashboard for comparing how topology, compression, and message budgets shape information recovery in a multi-agent sensor-fusion sandbox.</div>
        <div class="meta">
          <div class="tag">source {html.escape(source_path.name)}</div>
          <div class="tag">{result['num_experiments']} scenarios</div>
          <div class="tag">best topology {html.escape(comm['topology'])}</div>
          <div class="tag">best compressor {html.escape(comm['compressor'])}</div>
        </div>
      </div>
      <div class="panel hero-side">
        <div class="stat"><div class="stat-label">Benchmark</div><div class="stat-value">{html.escape(result['benchmark'])}</div></div>
        <div class="stat"><div class="stat-label">Best Recall</div><div class="stat-value">{summary['avg_mean_recall']:.3f}</div></div>
        <div class="stat"><div class="stat-label">Efficiency</div><div class="stat-value">{summary['avg_efficiency']:.5f}</div></div>
      </div>
    </section>

    <section class="grid">
      <article class="panel card">
        <h2>Best Configuration</h2>
        <div class="best-lines">
          <div><strong>Scenario</strong>: {html.escape(top_result['name'])}</div>
          <div><strong>Topology</strong>: {html.escape(comm['topology'])}</div>
          <div><strong>Compressor</strong>: {html.escape(comm['compressor'])}</div>
          <div><strong>Budget</strong>: {comm['message_budget']}</div>
          <div><strong>Dropout</strong>: {comm['message_dropout_prob']}</div>
          <div><strong>Visibility</strong>: {env['visibility_prob']}</div>
        </div>
      </article>
      <article class="panel card">
        <h2>Hop Trajectory</h2>
        <div class="hop-stack">{_build_hop_bars(summary['avg_hop_mean_recalls'])}</div>
      </article>
      <article class="panel card">
        <h2>Interpretation</h2>
        <div class="best-lines">
          <div><strong>Question</strong>: how topology and compression shape recovery under bandwidth limits.</div>
          <div><strong>Signal</strong>: compare raw recall, efficiency, and hop-wise information flow together.</div>
          <div><strong>Use</strong>: early-stage comparative evidence before a more method-centered project.</div>
        </div>
      </article>
    </section>

    <section class="panel card" style="margin-bottom:18px;">
      <h2>Current Findings</h2>
      <div class="mini-grid">{_build_findings(findings)}</div>
    </section>

    <section class="panel card" style="margin-bottom:18px;">
      <h2>Topology Snapshot</h2>
      <div class="mini-grid">{_build_topology_cards(experiments)}</div>
    </section>

    <section class="panel table-panel">
      <table>
        <thead>
          <tr>
            <th>Scenario</th>
            <th>Topology</th>
            <th>Compressor</th>
            <th>Budget</th>
            <th>Visibility</th>
            <th>Dropout</th>
            <th>Recall</th>
            <th>Efficiency</th>
            <th>Hop Path</th>
          </tr>
        </thead>
        <tbody>
          {_build_rows(experiments)}
        </tbody>
      </table>
      <div class="footer">Showing the top 12 scenarios ranked by recall, then efficiency.</div>
    </section>
  </div>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a static HTML dashboard from the latest benchmark result.")
    parser.add_argument("--results-dir", required=True, help="Directory containing saved result JSON files.")
    parser.add_argument("--write", action="store_true", help="Write the generated dashboard to dashboard.html in the results directory.")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    source_path, result = load_latest_benchmark_result(args.results_dir)
    dashboard = build_dashboard_html(result, source_path)
    if args.write:
        output_path = Path(args.results_dir) / "dashboard.html"
        output_path.write_text(dashboard, encoding="utf-8")
    print(dashboard)


if __name__ == "__main__":
    main()
