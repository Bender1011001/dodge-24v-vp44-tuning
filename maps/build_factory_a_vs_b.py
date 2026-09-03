#!/usr/bin/env python3
"""Build the shop presentation of factory CM551 cal A vs B.

Reads maps/tune_A_vs_B.json plus A/B identity JSON. Writes:

  maps/factory-a-vs-b.html   interactive deck (Plotly CDN, file:// ok)
  maps/factory-a-vs-b.pdf    matplotlib printout (if matplotlib is installed)

Does not invent cells. No VIN / ESN. Not a flash or write recipe.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def by_name(maps, name):
    for m in maps:
        if m.get("name") == name:
            return m
    raise KeyError(name)


def r3(v):
    if v is None:
        return None
    return round(float(v), 3)


def fmt(v):
    if v is None:
        return "—"
    v = float(v)
    if math.isnan(v):
        return "—"
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s


def axis_i(axis, value, tol=0.051):
    for i, x in enumerate(axis):
        if abs(float(x) - float(value)) <= tol:
            return i
    return None


def shared_axis(a_axis, b_axis, tol=0.051):
    out = []
    used = set()
    for va in a_axis:
        for j, vb in enumerate(b_axis):
            if j in used:
                continue
            if abs(float(va) - float(vb)) <= tol:
                out.append(float(va))
                used.add(j)
                break
    return out


def cell(grid, y_axis, x_axis, yv, xv):
    yi = axis_i(y_axis, yv)
    xi = axis_i(x_axis, xv)
    if yi is None or xi is None:
        return None
    row = grid[yi]
    if xi >= len(row):
        return None
    v = row[xi]
    return None if v is None else float(v)


def delta_grid(a, b):
    out = []
    for ra, rb in zip(a, b):
        row = []
        for va, vb in zip(ra, rb):
            if va is None or vb is None:
                row.append(None)
            else:
                row.append(r3(va - vb))
        out.append(row)
    return out


def wot_row(m):
    y = m["y"]
    yi = axis_i(y, 100.0)
    if yi is None:
        yi = len(y) - 1
    return m["x"], m["a"][yi], m["b"][yi]


def count_present(grid):
    n = 0
    for row in grid or []:
        for v in row:
            if v is not None:
                n += 1
    return n


def nearest_y(axis, target):
    return min(axis, key=lambda y: abs(float(y) - target))


def build_payload(tune, ident_a, ident_b):
    maps = tune["maps"]
    m00 = by_name(maps, "5DFL00ZA")
    m01 = by_name(maps, "5DFL01ZA")
    t00 = by_name(maps, "4DTA00ZA")
    t01 = by_name(maps, "4DTA01ZA")
    fl = by_name(maps, "FLFLTBZA")
    afc = by_name(maps, "AFFLLMZA")

    x00, a_wot00, b_wot00 = wot_row(m00)
    x01, a_wot01, b_wot01 = wot_row(m01)
    d00 = [r3(a - b) for a, b in zip(a_wot00, b_wot00)]
    d01 = [r3(a - b) for a, b in zip(a_wot01, b_wot01)]

    def gap_at(xs, da, db, rpm):
        i = axis_i(xs, rpm)
        return {
            "rpm": rpm,
            "a": r3(da[i]),
            "b": r3(db[i]),
            "delta": r3(da[i] - db[i]),
        }

    g00_3000 = gap_at(x00, a_wot00, b_wot00, 3000)
    g01_3000 = gap_at(x01, a_wot01, b_wot01, 3000)
    g00_2800 = gap_at(x00, a_wot00, b_wot00, 2800)
    g01_2800 = gap_at(x01, a_wot01, b_wot01, 2800)

    # Timing slices: light Y=0 (shared), mid Y≈65 (shared), peak = each table's top Y.
    t_x = t00["x"]
    y_light = 0.0
    y_mid = nearest_y(t00["y"], 65.014)
    y_peak_tr = t00["y"][-1]
    y_peak_ss = t01["y"][-1]
    yi_light_00 = axis_i(t00["y"], y_light)
    yi_mid_00 = axis_i(t00["y"], y_mid)
    yi_peak_00 = len(t00["y"]) - 1
    yi_light_01 = axis_i(t01["y"], y_light)
    yi_mid_01 = axis_i(t01["y"], y_mid)
    yi_peak_01 = len(t01["y"]) - 1

    # Deepest transient retard (most negative) in 4DTA00.
    deepest = None
    for yi, yv in enumerate(t00["y"]):
        for xi, xv in enumerate(t00["x"]):
            z = t00["a"][yi][xi]
            if z is None:
                continue
            if deepest is None or z < deepest["z"]:
                deepest = {"y": r3(yv), "rpm": r3(xv), "z": r3(z)}

    # Transient minus steady where Y is shared.
    shared_ty = shared_axis(t00["y"], t01["y"])
    hole = []
    hole_y = []
    for yv in shared_ty:
        hole_y.append(r3(yv))
        row = []
        for xv in t_x:
            a = cell(t00["a"], t00["y"], t00["x"], yv, xv)
            b = cell(t01["a"], t01["y"], t01["x"], yv, xv)
            row.append(None if a is None or b is None else r3(a - b))
        hole.append(row)

    # FLFL: peak (max across Y) vs RPM, skip the all-zero Y=0 row for peak.
    fl_peak = []
    for xi in range(len(fl["x"])):
        vals = [row[xi] for row in fl["a"] if row[xi] is not None]
        fl_peak.append(r3(max(vals) if vals else 0))

    # AFC: compare by physical breakpoint, never by column index.
    xa, xb = afc["x_a"], afc["x_b"]
    ya, yb = afc["y_a"], afc["y_b"]
    rpm_shared = shared_axis(xa, xb)
    boost_shared = shared_axis(ya, yb)
    y0 = nearest_y(boost_shared, 0.0)
    y20 = nearest_y(boost_shared, 19.99)

    def afc_slice(yv):
        aa, bb, dd = [], [], []
        for rpm in rpm_shared:
            va = cell(afc["a"], ya, xa, yv, rpm)
            vb = cell(afc["b"], yb, xb, yv, rpm)
            aa.append(r3(va) if va is not None else None)
            bb.append(r3(vb) if vb is not None else None)
            if va is None or vb is None:
                dd.append(None)
            else:
                dd.append(r3(va - vb))
        return {"y": r3(yv), "a": aa, "b": bb, "delta": dd}

    afc_0 = afc_slice(y0)
    afc_20 = afc_slice(y20)

    n_a = count_present(afc["a"])
    n_b = count_present(afc["b"])
    n_declared = int(afc["dims"][0]) * int(afc["dims"][1])

    same, differ, nak = [], [], []
    for m in maps:
        rec = {
            "name": m["name"],
            "itn": m.get("itn"),
            "units": m.get("units"),
            "dims": m.get("dims"),
            "equal": m.get("equal"),
            "note": m.get("note") or "",
        }
        if m.get("a") is None:
            nak.append(rec)
        elif not m.get("equal"):
            differ.append(rec)
        else:
            same.append(rec)

    scalars = tune.get("scalars") or []
    n_scalar_diff = sum(1 for s in scalars if s.get("diff"))

    return {
        "identity": {
            "a": ident_a,
            "b": ident_b,
            "map_count": tune.get("map_count"),
            "scalar_count": tune.get("scalar_count"),
            "scalar_diff": n_scalar_diff,
            "itns_ok": ident_a.get("itns_ok"),
            "itns_miss": ident_a.get("itns_miss"),
            "protocol": ident_a.get("protocol"),
            "catalog": ident_a.get("catalog"),
        },
        "catalog": {
            "same": same,
            "differ": differ,
            "nak": nak,
        },
        "scales": {
            "rpm": 0.125,
            "fuel": 0.0679348,
            "fuel_5dfl_add": -800,
            "timing": 0.1171875,
            "timing_add": -60,
            "axis_prefix": "first u16 BE = byte length of points; Z = Y rows × X cols",
        },
        "fuel": {
            "x": [r3(v) for v in x00],
            "y": [r3(v) for v in m00["y"]],
            "a00": m00["a"],
            "b00": m00["b"],
            "a01": m01["a"],
            "b01": m01["b"],
            "delta00": delta_grid(m00["a"], m00["b"]),
            "delta01": delta_grid(m01["a"], m01["b"]),
            "wot00_a": [r3(v) for v in a_wot00],
            "wot00_b": [r3(v) for v in b_wot00],
            "wot01_a": [r3(v) for v in a_wot01],
            "wot01_b": [r3(v) for v in b_wot01],
            "wot00_delta": d00,
            "wot01_delta": d01,
            "gap": {
                "dfl00_3000": g00_3000,
                "dfl01_3000": g01_3000,
                "dfl00_2800": g00_2800,
                "dfl01_2800": g01_2800,
            },
            "equal00": m00["equal"],
            "equal01": m01["equal"],
        },
        "timing": {
            "x": [r3(v) for v in t_x],
            "y00": [r3(v) for v in t00["y"]],
            "y01": [r3(v) for v in t01["y"]],
            "z00": t00["a"],
            "z01": t01["a"],
            "equal00": t00["equal"],
            "equal01": t01["equal"],
            "light_y": r3(y_light),
            "mid_y": r3(y_mid),
            "peak_tr_y": r3(y_peak_tr),
            "peak_ss_y": r3(y_peak_ss),
            "tr_light": [r3(v) for v in t00["a"][yi_light_00]],
            "tr_mid": [r3(v) for v in t00["a"][yi_mid_00]],
            "tr_peak": [r3(v) for v in t00["a"][yi_peak_00]],
            "ss_light": [r3(v) for v in t01["a"][yi_light_01]],
            "ss_mid": [r3(v) for v in t01["a"][yi_mid_01]],
            "ss_peak": [r3(v) for v in t01["a"][yi_peak_01]],
            "deepest": deepest,
            "hole_y": hole_y,
            "hole": hole,
        },
        "flfl": {
            "x": [r3(v) for v in fl["x"]],
            "y": [r3(v) for v in fl["y"]],
            "z": fl["a"],
            "equal": fl["equal"],
            "peak": fl_peak,
        },
        "afc": {
            "note": afc.get("note") or "",
            "dims": afc["dims"],
            "equal": afc["equal"],
            "cells_present_a": n_a,
            "cells_present_b": n_b,
            "cells_declared": n_declared,
            "x_a": [r3(v) for v in xa],
            "x_b": [r3(v) for v in xb],
            "y_a": [r3(v) for v in ya],
            "y_b": [r3(v) for v in yb],
            "rpm_a_only": [r3(v) for v in xa if axis_i(xb, v) is None],
            "rpm_b_only": [r3(v) for v in xb if axis_i(xa, v) is None],
            "boost_a_only": [r3(v) for v in ya if axis_i(yb, v) is None],
            "boost_b_only": [r3(v) for v in yb if axis_i(ya, v) is None],
            "rpm_shared": [r3(v) for v in rpm_shared],
            "boost_shared": [r3(v) for v in boost_shared],
            "slice0": afc_0,
            "slice20": afc_20,
        },
    }


def html_escape(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def num_td(v, diff=False):
    cls = "diff" if diff else "same"
    return f'<td class="{cls}">{html_escape(fmt(v))}</td>'


def header_rpm(xs):
    cells = "".join(f"<th>{html_escape(fmt(x))}</th>" for x in xs)
    return f'<tr><th class="corner">Y \\ X</th>{cells}</tr>'


def grid_html(x, y, a, b=None, caption=""):
    rows = [header_rpm(x)]
    for i, yv in enumerate(y):
        tds = [f'<th class="y">{html_escape(fmt(yv))}</th>']
        for j, _xv in enumerate(x):
            va = a[i][j]
            if b is None:
                tds.append(num_td(va, False))
            else:
                vb = b[i][j]
                differ = va is not None and vb is not None and r3(va) != r3(vb)
                if differ:
                    tds.append(
                        f'<td class="diff">{html_escape(fmt(va))}'
                        f'<span class="bval">B {html_escape(fmt(vb))}</span></td>'
                    )
                else:
                    tds.append(num_td(va, False))
        rows.append("<tr>" + "".join(tds) + "</tr>")
    cap = f"<p class='tblcap'>{html_escape(caption)}</p>" if caption else ""
    return cap + "<div class='scroll'><table class='grid'>" + "".join(rows) + "</table></div>"


def wot_table_html(x, a, b, title):
    head = (
        "<tr><th>RPM</th><th>A</th><th>B</th><th>A − B</th></tr>"
    )
    body = []
    for xv, va, vb in zip(x, a, b):
        d = r3(va - vb)
        hi = abs(d or 0) >= 10
        cls = "diff" if d else "same"
        if hi:
            cls += " hi"
        body.append(
            f'<tr class="{cls}"><td>{html_escape(fmt(xv))}</td>'
            f"<td>{html_escape(fmt(va))}</td>"
            f"<td>{html_escape(fmt(vb))}</td>"
            f"<td>{html_escape(fmt(d))}</td></tr>"
        )
    return (
        f"<p class='tblcap'>{html_escape(title)}</p>"
        f"<div class='scroll'><table class='grid wot'>{head}{''.join(body)}</table></div>"
    )


def afc_table_html(rpm, a, b, title):
    head = "<tr><th>RPM</th><th>A</th><th>B</th><th>A − B</th></tr>"
    body = []
    for xv, va, vb in zip(rpm, a, b):
        d = None if va is None or vb is None else r3(va - vb)
        body.append(
            f'<tr class="diff"><td>{html_escape(fmt(xv))}</td>'
            f"<td>{html_escape(fmt(va))}</td>"
            f"<td>{html_escape(fmt(vb))}</td>"
            f"<td>{html_escape(fmt(d))}</td></tr>"
        )
    return (
        f"<p class='tblcap'>{html_escape(title)}</p>"
        f"<div class='scroll'><table class='grid wot'>{head}{''.join(body)}</table></div>"
    )


def chip_list(items, kind):
    bits = []
    for m in items:
        dims = m.get("dims") or []
        shape = "×".join(str(d) for d in dims) if dims else "—"
        bits.append(
            f'<span class="chip {kind}" title="ITN {html_escape(m.get("itn") or "")}">'
            f'{html_escape(m["name"])} <small>{html_escape(shape)}</small></span>'
        )
    return "".join(bits)


def render_html(p):
    fuel = p["fuel"]
    ident = p["identity"]
    ia, ib = ident["a"], ident["b"]
    g = fuel["gap"]
    afc = p["afc"]
    cat = p["catalog"]

    tbl00 = grid_html(
        fuel["x"], fuel["y"], fuel["a00"], fuel["b00"],
        "5DFL00ZA transient · 4 × 18 · ITN 1059 · amber = A ≠ B",
    )
    tbl01 = grid_html(
        fuel["x"], fuel["y"], fuel["a01"], fuel["b01"],
        "5DFL01ZA steady-state · 4 × 18 · ITN 1056 · amber = A ≠ B",
    )
    wot00 = wot_table_html(
        fuel["x"], fuel["wot00_a"], fuel["wot00_b"],
        "5DFL00ZA 100% row (MM3S)",
    )
    wot01 = wot_table_html(
        fuel["x"], fuel["wot01_a"], fuel["wot01_b"],
        "5DFL01ZA 100% row (MM3S)",
    )
    afc0 = afc_table_html(
        afc["rpm_shared"], afc["slice0"]["a"], afc["slice0"]["b"],
        f"AFFLLMZA at {fmt(afc['slice0']['y'])} inHg (zero boost), shared RPM only",
    )
    afc20 = afc_table_html(
        afc["rpm_shared"], afc["slice20"]["a"], afc["slice20"]["b"],
        f"AFFLLMZA at {fmt(afc['slice20']['y'])} inHg (~10 psi), shared RPM only",
    )

    payload = json.dumps(p, separators=(",", ":"))

    return HTML_TEMPLATE.replace("%%PAYLOAD%%", payload).replace("%%TBL00%%", tbl00).replace("%%TBL01%%", tbl01).replace(
        "%%WOT00%%", wot00
    ).replace("%%WOT01%%", wot01).replace("%%AFC0%%", afc0).replace(
        "%%AFC20%%", afc20
    ).replace("%%G00_3000_A%%", fmt(g["dfl00_3000"]["a"])).replace(
        "%%G00_3000_B%%", fmt(g["dfl00_3000"]["b"])
    ).replace("%%G00_3000_D%%", fmt(g["dfl00_3000"]["delta"])).replace(
        "%%G01_3000_A%%", fmt(g["dfl01_3000"]["a"])
    ).replace("%%G01_3000_B%%", fmt(g["dfl01_3000"]["b"])).replace(
        "%%G01_3000_D%%", fmt(g["dfl01_3000"]["delta"])
    ).replace("%%G00_2800_D%%", fmt(g["dfl00_2800"]["delta"])).replace(
        "%%G01_2800_D%%", fmt(g["dfl01_2800"]["delta"])
    ).replace("%%CODE_A%%", html_escape(ia["ecm_code"])).replace(
        "%%CODE_B%%", html_escape(ib["ecm_code"])
    ).replace("%%PN%%", html_escape(ia["ecm_pn"])).replace(
        "%%ROM%%", html_escape(ia["rom_date"])
    ).replace("%%CAL_A%%", html_escape(ia["cal_date"])).replace(
        "%%CAL_B%%", html_escape(ib["cal_date"])
    ).replace("%%PLATE_A%%", html_escape(ia["dataplate"]["engine"])).replace(
        "%%PLATE_B%%", html_escape(ib["dataplate"]["engine"])
    ).replace("%%PUMP_A%%", html_escape(ia["dataplate"]["fuel_pump"])).replace(
        "%%PUMP_B%%", html_escape(ib["dataplate"]["fuel_pump"])
    ).replace("%%APP_A%%", html_escape(ia["dataplate"]["application"])).replace(
        "%%APP_B%%", html_escape(ib["dataplate"]["application"])
    ).replace("%%HRS_A%%", html_escape(ia["engine_hours"])).replace(
        "%%HRS_B%%", html_escape(ib["engine_hours"])
    ).replace("%%KEY_A%%", html_escape(ia["key_on"])).replace(
        "%%KEY_B%%", html_escape(ib["key_on"])
    ).replace("%%MI_A%%", html_escape(str(ia["ecm_vss_miles"]))).replace(
        "%%MI_B%%", html_escape(str(ib["ecm_vss_miles"]))
    ).replace("%%ITN_OK%%", html_escape(str(ident["itns_ok"]))).replace(
        "%%ITN_MISS%%", html_escape(str(ident["itns_miss"]))
    ).replace("%%N_SAME%%", str(len(cat["same"]))).replace(
        "%%N_DIFF%%", str(len(cat["differ"]))
    ).replace("%%N_NAK%%", str(len(cat["nak"]))).replace(
        "%%N_SCALAR%%", str(ident["scalar_count"])
    ).replace("%%N_SCALAR_DIFF%%", str(ident["scalar_diff"])).replace(
        "%%CHIPS_DIFF%%", chip_list(cat["differ"], "diff")
    ).replace("%%CHIPS_SAME%%", chip_list(cat["same"], "same")).replace(
        "%%CHIPS_NAK%%", chip_list(cat["nak"], "nak")
    ).replace("%%AFC_NOTE%%", html_escape(afc["note"])).replace(
        "%%AFC_HAVE%%", str(afc["cells_present_a"])
    ).replace("%%AFC_DECL%%", str(afc["cells_declared"])).replace(
        "%%AFC_RPM_A%%", html_escape(", ".join(fmt(v) for v in afc["x_a"]))
    ).replace("%%AFC_RPM_B%%", html_escape(", ".join(fmt(v) for v in afc["x_b"]))
    ).replace("%%AFC_Y_A%%", html_escape(", ".join(fmt(v) for v in afc["y_a"]))
    ).replace("%%AFC_Y_B%%", html_escape(", ".join(fmt(v) for v in afc["y_b"]))
    ).replace(
        "%%AFC_RPM_A_ONLY%%", html_escape(", ".join(fmt(v) for v in afc["rpm_a_only"]) or "—")
    ).replace(
        "%%AFC_RPM_B_ONLY%%", html_escape(", ".join(fmt(v) for v in afc["rpm_b_only"]) or "—")
    ).replace(
        "%%AFC_Y_A_ONLY%%", html_escape(", ".join(fmt(v) for v in afc["boost_a_only"]) or "—")
    ).replace(
        "%%AFC_Y_B_ONLY%%", html_escape(", ".join(fmt(v) for v in afc["boost_b_only"]) or "—")
    ).replace("%%DEEP_Y%%", fmt(p["timing"]["deepest"]["y"])).replace(
        "%%DEEP_RPM%%", fmt(p["timing"]["deepest"]["rpm"])
    ).replace("%%DEEP_Z%%", fmt(p["timing"]["deepest"]["z"])).replace(
        "%%MID_Y%%", fmt(p["timing"]["mid_y"])
    ).replace("%%PEAK_TR%%", fmt(p["timing"]["peak_tr_y"])).replace(
        "%%PEAK_SS%%", fmt(p["timing"]["peak_ss_y"])
    ).replace("%%PROTO%%", html_escape(ident["protocol"] or "")).replace(
        "%%CATALOG%%", html_escape(ident["catalog"] or "")
    )


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Factory CM551 A vs B — J90269.06 / J90268.04</title>
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.3/plotly.min.js"></script>
<style>
:root {
  --bg:#0c0e14; --fg:#e8eaed; --muted:#8b93a7; --card:#161a24;
  --border:#2c3344; --accent:#8ec0ff; --a:#5eb0ef; --b:#e8a04a;
  --diff-bg:#4a3210; --diff-fg:#ffd48a; --ok:#3ecf8e; --warn:#ff8a80;
  --navh:56px;
}
* { box-sizing:border-box; }
html, body { margin:0; background:var(--bg); color:var(--fg);
  font:15px/1.45 "Segoe UI", system-ui, sans-serif; }
html { scroll-snap-type: y proximity; }
a { color:var(--accent); }
.nav {
  position:sticky; top:0; z-index:20; height:var(--navh);
  display:flex; align-items:center; gap:10px; flex-wrap:wrap;
  padding:0 18px; background:rgba(12,14,20,.94);
  border-bottom:1px solid var(--border); backdrop-filter:blur(8px);
}
.nav strong { color:#fff; letter-spacing:.02em; }
.nav a { color:var(--muted); text-decoration:none; font-size:13px; padding:4px 8px; border-radius:6px; }
.nav a:hover, .nav a.on { color:#fff; background:#1e2433; }
.nav .print { margin-left:auto; background:#1e2433; border:1px solid var(--border);
  color:var(--fg); border-radius:6px; padding:5px 10px; cursor:pointer; font:inherit; }
.slide {
  min-height:calc(100vh - var(--navh)); scroll-snap-align:start;
  padding:28px 32px 40px; max-width:1400px; margin:0 auto;
}
.slide h1, .slide h2 { color:#fff; font-weight:650; margin:0 0 10px; }
.slide h1 { font-size:clamp(1.6rem, 3vw, 2.4rem); letter-spacing:-.02em; }
.slide h2 { font-size:1.35rem; }
.kicker { color:var(--accent); font-size:12px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; }
.lead { color:var(--muted); max-width:72ch; margin:0 0 18px; }
.hero-codes { display:flex; gap:16px; flex-wrap:wrap; margin:22px 0 18px; }
.hero-codes div {
  flex:1; min-width:240px; background:var(--card); border:1px solid var(--border);
  border-radius:14px; padding:18px 20px;
}
.hero-codes .who { font-size:12px; color:var(--muted); font-weight:700; letter-spacing:.08em; }
.hero-codes .code { font-size:2rem; font-weight:700; color:#fff; letter-spacing:-.03em; }
.hero-codes .a .code { color:var(--a); }
.hero-codes .b .code { color:var(--b); }
.pills { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 0; }
.pill { border:1px solid var(--border); background:#121622; border-radius:999px;
  padding:4px 10px; font-size:12px; color:var(--muted); }
.pill em { color:var(--fg); font-style:normal; }
.cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; }
.card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:16px 18px; }
.card h3 { margin:0 0 8px; font-size:13px; color:var(--accent); letter-spacing:.06em; text-transform:uppercase; }
.kv { display:grid; grid-template-columns:140px 1fr; gap:4px 10px; font-size:14px; }
.kv span { color:var(--muted); }
.big { font-size:clamp(2.2rem, 5vw, 3.6rem); font-weight:700; letter-spacing:-.04em; color:var(--diff-fg); line-height:1; }
.big small { display:block; font-size:13px; color:var(--muted); font-weight:500; letter-spacing:0; margin-top:8px; }
.split { display:grid; grid-template-columns:1.3fr .9fr; gap:18px; align-items:start; }
.split3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px; }
.chart { width:100%; height:46vh; min-height:340px; }
.chart.short { height:38vh; min-height:280px; }
.chart.tall { height:52vh; min-height:400px; }
.scroll { overflow-x:auto; border:1px solid var(--border); border-radius:8px; }
table.grid { border-collapse:collapse; font-size:11px; min-width:100%; }
table.grid th, table.grid td { border:1px solid #2c313c; padding:3px 5px; text-align:right; white-space:nowrap; }
table.grid th { background:#1e2433; }
table.grid th.y, table.grid th.corner { position:sticky; left:0; background:#1e2433; z-index:1; }
td.same { color:#c5c9d1; }
td.diff, tr.diff td { background:var(--diff-bg); color:var(--diff-fg); }
tr.hi td { outline:1px solid #c9a227; }
.bval { display:block; color:#ffcc80; font-size:10px; font-weight:500; }
.tblcap { color:var(--muted); font-size:12px; margin:8px 0 6px; }
.chip { display:inline-block; margin:3px 4px 0 0; padding:3px 8px; border-radius:6px;
  border:1px solid var(--border); font-size:12px; background:#121622; }
.chip.diff { border-color:#b8862b; color:var(--diff-fg); background:var(--diff-bg); }
.chip.same { color:#a8b0c2; }
.chip.nak { opacity:.55; }
.chip small { color:var(--muted); }
.call { display:flex; gap:14px; flex-wrap:wrap; margin:12px 0 16px; }
.call .card { min-width:200px; }
.note { border-left:3px solid var(--b); padding:8px 12px; color:var(--muted); background:#16120c; border-radius:0 8px 8px 0; }
.warnbox { border:1px solid #5a3030; background:#1a1010; color:#ffb4ae; border-radius:8px; padding:10px 14px; margin:10px 0; }
.okbox { border:1px solid #1f4d3a; background:#0f1c16; color:#9fe7c3; border-radius:8px; padding:10px 14px; margin:10px 0; }
.two { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.mono { font-family:ui-monospace, Consolas, monospace; font-size:13px; }
footer.slide { color:var(--muted); font-size:13px; }
@media (max-width:980px) {
  .split, .two, .split3 { grid-template-columns:1fr; }
  .slide { padding:20px 16px 32px; }
  .chart, .chart.short, .chart.tall { height:300px; min-height:260px; }
  html { scroll-snap-type: none; }
}
@page { size: landscape; margin: 8mm; }
@media print {
  .nav, .print { display:none !important; }
  html { scroll-snap-type:none; }
  .slide { min-height:auto; page-break-after:always; padding:12px 16px; max-width:none; }
  .chart, .chart.short, .chart.tall { height:320px; min-height:320px; break-inside:avoid; }
  body { background:#0c0e14; }
}
</style>
</head>
<body>
<nav class="nav">
  <strong>CM551 A vs B</strong>
  <a href="#title">Title</a>
  <a href="#identity">Identity</a>
  <a href="#same">Same</a>
  <a href="#fuel-wot">Fuel WOT</a>
  <a href="#fuel-delta">Fuel Δ</a>
  <a href="#fuel-grids">Grids</a>
  <a href="#timing">Timing</a>
  <a href="#flfl">FLFL</a>
  <a href="#afc">AFC</a>
  <a href="#tune">If you tune</a>
  <a href="tune_A_vs_B.html">29-map viewer</a>
  <button class="print" type="button" onclick="window.print()">Print / PDF</button>
</nav>

<section class="slide" id="title">
  <p class="kicker">Live KennPar dumps · read-only</p>
  <h1>Two factory Cummins CM551 / Dodge 24v VP44 calibrations</h1>
  <p class="lead">Same ECM part number and ROM date. Different silk-screen codes, different cal dates, different WOT fuel. Timing tables match. This is a decoded compare of two boxes the owner already had — not a flash image and not a write recipe.</p>
  <div class="hero-codes">
    <div class="a"><div class="who">ECM A</div><div class="code">%%CODE_A%%</div>
      <div class="mono">cal %%CAL_A%% · 6BTA 5.9 Li</div></div>
    <div class="b"><div class="who">ECM B</div><div class="code">%%CODE_B%%</div>
      <div class="mono">cal %%CAL_B%% · ISB 235</div></div>
  </div>
  <div class="pills">
    <span class="pill">P/N <em>%%PN%%</em></span>
    <span class="pill">ROM <em>%%ROM%%</em></span>
    <span class="pill">ReadByNTN <em>0x48</em></span>
    <span class="pill">ITNs <em>%%ITN_OK%% / %%ITN_MISS%%</em></span>
    <span class="pill">Z-maps decoded <em>29</em></span>
    <span class="pill">%%CATALOG%%</span>
  </div>
  <p class="lead" style="margin-top:18px">%%PROTO%%. Packed ITN dump, not ROM. VIN and engine serial are not published.</p>
</section>

<section class="slide" id="identity">
  <p class="kicker">The two boxes</p>
  <h2>Identity, hours, miles — no VIN / ESN</h2>
  <div class="cards">
    <div class="card">
      <h3>ECM A · %%CODE_A%%</h3>
      <div class="kv">
        <span>Plate</span><div>%%PLATE_A%%, %%PUMP_A%%, %%APP_A%%</div>
        <span>P/N / ROM</span><div>%%PN%% / %%ROM%%</div>
        <span>Cal date</span><div>%%CAL_A%%</div>
        <span>Engine hours</span><div>%%HRS_A%%</div>
        <span>Key-on</span><div>%%KEY_A%%</div>
        <span>ECM VSS miles</span><div>%%MI_A%%</div>
      </div>
    </div>
    <div class="card">
      <h3>ECM B · %%CODE_B%%</h3>
      <div class="kv">
        <span>Plate</span><div>%%PLATE_B%%, %%PUMP_B%%, %%APP_B%%</div>
        <span>P/N / ROM</span><div>%%PN%% / %%ROM%%</div>
        <span>Cal date</span><div>%%CAL_B%%</div>
        <span>Engine hours</span><div>%%HRS_B%%</div>
        <span>Key-on</span><div>%%KEY_B%%</div>
        <span>ECM VSS miles</span><div>%%MI_B%%</div>
      </div>
    </div>
  </div>
  <p class="note" style="margin-top:16px">Hours, key-on, and VSS are <em style="color:var(--fg)">runtime</em> counters — they differ because the boxes lived different lives. A’s ~81 ECM VSS miles with 13k hours is consistent with a module that ran a long time without a speed input the ECM trusted, or that did not spend its whole life in the truck that holds it now. Those numbers are not the calibration delta.</p>
  <p class="lead">Decode: <span class="mono">physical = raw × scale + add</span>. RPM × 0.125. Fuel Z on 5DFL × 0.0679348, add −800. Timing Z × 0.1171875, add −60. Axis prefix: first u16 BE is byte length of points. Z is Y rows × X columns. Catalog comments that say 17×4 / 17×9 are wrong on these boxes — live prefixes are 4×18 fuel and 11×18 timing.</p>
</section>

<section class="slide" id="same">
  <p class="kicker">29 Z-maps</p>
  <h2>What is the same — and the three that are not</h2>
  <div class="split3">
    <div class="card">
      <h3>Differ · %%N_DIFF%%</h3>
      <div>%%CHIPS_DIFF%%</div>
      <p class="tblcap">Complete fuel request (5DFL) plus truncated AFC. Timing grids match.</p>
    </div>
    <div class="card">
      <h3>Decoded same · %%N_SAME%%</h3>
      <div>%%CHIPS_SAME%%</div>
    </div>
    <div class="card">
      <h3>NAK / empty · %%N_NAK%%</h3>
      <div>%%CHIPS_NAK%%</div>
      <p class="tblcap">Chr0000 listed them; this Dodge cal NAKed ReadByNTN.</p>
    </div>
  </div>
  <div class="okbox">Timing <span class="mono">4DTA00ZA</span> / <span class="mono">4DTA01ZA</span> (11×18) are <strong>the same</strong> A vs B. Conversion <span class="mono">FLFLTBZA</span> (15×15) is <strong>the same</strong>. Altitude derate <span class="mono">ATFLLMZA</span> is the same (flat 400). The silk-screen codes are not “the same tune with a sticker change.”</div>
  <p class="lead">Scalars: %%N_SCALAR%% decoded, %%N_SCALAR_DIFF%% differ — many are runtime (hours, key-on, VSS, faults). <span class="mono">4DTA00ZA</span> raw blob first differs at byte 480 of 512, past the 11×18 table. <span class="mono">5DFL*</span> first differs at byte 114, inside the table.</p>
</section>

<section class="slide" id="fuel-wot">
  <p class="kicker">The actual difference · 5DFL 100% row</p>
  <h2>WOT fuel vs RPM — A is richer mid/high</h2>
  <div class="call">
    <div class="card">
      <div class="big">+%%G01_3000_D%%<small>mm³/s at 3000 RPM · 5DFL01 100% (steady) · A %%G01_3000_A%% vs B %%G01_3000_B%%</small></div>
    </div>
    <div class="card">
      <div class="big" style="color:var(--a)">+%%G00_3000_D%%<small>mm³/s at 3000 RPM · 5DFL00 100% (transient) · A %%G00_3000_A%% vs B %%G00_3000_B%%</small></div>
    </div>
    <div class="card">
      <p class="tblcap" style="margin-top:0">2800 RPM gaps</p>
      <p>Transient +%%G00_2800_D%% · steady +%%G01_2800_D%% mm³/s. Part-load rows (0 / 25 / 50%) match. 3800 column is 0 on both (unused breakpoint).</p>
    </div>
  </div>
  <div id="chart-wot" class="chart"></div>
  <p class="tblcap">Verified from <span class="mono">tune_A_vs_B.json</span>. Earlier shop note of ~+20–23 mm³/s at 3000 RPM 100% is the pair above (19.973 transient / 22.691 steady), not a third table.</p>
</section>

<section class="slide" id="fuel-delta">
  <p class="kicker">5DFL00ZA / 5DFL01ZA</p>
  <h2>A − B heatmap and the 100% tables</h2>
  <div class="two">
    <div>
      <div id="chart-delta" class="chart short"></div>
      <div id="chart-bars" class="chart short"></div>
    </div>
    <div>
      %%WOT00%%
      %%WOT01%%
    </div>
  </div>
</section>

<section class="slide" id="fuel-grids">
  <p class="kicker">Full 4 × 18 grids</p>
  <h2>Low-load rows match; only the 100% row moves</h2>
  %%TBL00%%
  %%TBL01%%
</section>

<section class="slide" id="timing">
  <p class="kicker">4DTA00ZA / 4DTA01ZA · A = B</p>
  <h2>Timing vs RPM — peak-load vs light, and the transient hole</h2>
  <p class="lead">Decoded 11×18 grids match A vs B. The contrast that matters is <strong>transient (00) vs steady (01)</strong>, not box vs box. Y is commanded fuel (mm³/s), not throttle percent. Peak Y is not shared: transient top %%PEAK_TR%% vs steady top %%PEAK_SS%%.</p>
  <div class="two">
    <div id="chart-timing" class="chart tall"></div>
    <div>
      <div id="chart-hole" class="chart short"></div>
      <div class="warnbox">Deepest transient retard: <strong>%%DEEP_Z%%°</strong> at %%DEEP_RPM%% RPM, Y=%%DEEP_Y%% mm³/s on 4DTA00. From 1280 through ~2800 RPM the transient table goes negative at mid/high fuel (~−2 to −6.3°). Steady-state stays positive in that band (~+4 to +8°). At 3000+ both come back positive. 3800 repeats 3250 on most rows.</div>
    </div>
  </div>
</section>

<section class="slide" id="flfl">
  <p class="kicker">FLFLTBZA · A = B · 15 × 15 · ITN 8014</p>
  <h2>Fuel units → mg/stroke — conversion, not the request</h2>
  <p class="lead">This is the density-style conversion table. Changing it without changing 5DFL is a different edit than raising the 100% fuel row. Below ~160 mm³/s the table still varies with RPM (dip 1200–2700, bump at 3000). From Y ≈ 160 up, rows are flat across RPM.</p>
  <div class="two">
    <div id="chart-flfl" class="chart tall"></div>
    <div id="chart-flfl-peak" class="chart tall"></div>
  </div>
</section>

<section class="slide" id="afc">
  <p class="kicker">AFFLLMZA · truncated · axes differ</p>
  <h2>AFC limiter — compare by breakpoint, not column index</h2>
  <div class="warnbox"><strong>%%AFC_NOTE%%</strong> — %%AFC_HAVE%% of %%AFC_DECL%% cells present. Last complete row is Y index 11; Y index 12 has four cells; Y index 13 is empty. Do not treat the declared 14×21 as fully known. The 29-map HTML viewer is index-aligned and will mislead on this map.</div>
  <div class="two" style="margin-top:12px">
    <div class="card">
      <h3>RPM X AFFLLMXA</h3>
      <p class="mono">A: %%AFC_RPM_A%%</p>
      <p class="mono">B: %%AFC_RPM_B%%</p>
      <p class="tblcap">A only: %%AFC_RPM_A_ONLY%% · B only: %%AFC_RPM_B_ONLY%%</p>
    </div>
    <div class="card">
      <h3>Boost Y AFFLLMYA (inHg)</h3>
      <p class="mono">A: %%AFC_Y_A%%</p>
      <p class="mono">B: %%AFC_Y_B%%</p>
      <p class="tblcap">A only: %%AFC_Y_A_ONLY%% · B only: %%AFC_Y_B_ONLY%% (100/110 inHg is above stock Dodge boost — leftover tail).</p>
    </div>
  </div>
  <div id="chart-afc" class="chart"></div>
  <div class="two">
    <div>%%AFC0%%</div>
    <div>%%AFC20%%</div>
  </div>
  <p class="note">At zero boost, B falls to a 44.973 mm³/s ceiling from 1280 RPM up; A holds 73.573 (then 72.147 at 3250+). At ~20 inHg A sits near 164 mm³/s across most RPM — above any 5DFL 100% cell — while B is lower and RPM-shaped. On the sampled complete rows, A’s AFC ceiling is well above 5DFL; B’s AFC is much tighter at low boost. This is a third decoded-table difference, incomplete.</p>
</section>

<section class="slide" id="tune">
  <p class="kicker">Shop takeaway</p>
  <h2>What this means if you tune</h2>
  <div class="split">
    <div>
      <div class="okbox"><strong>A is the richer WOT fuel cal.</strong> Timing is identical on these two boxes, so <em>fueling</em> is the lever between them — not a hidden timing advance on J90269.06.</div>
      <ul>
        <li>Part-throttle 5DFL (0 / 25 / 50) matches. Cruise / light load is not the delta.</li>
        <li>The 100% row is the complete, trustworthy cal delta: A holds ~107–110 mm³/s at 2800–3000; B drops into the high-80s / 90s.</li>
        <li>Steady-state 5DFL01 is slightly leaner than transient 5DFL00 on both boxes, and the A-vs-B gap is <em>larger</em> there (+22.691 vs +19.973 at 3000).</li>
        <li><span class="mono">FLFLTBZA</span> matches — you are not looking at a conversion-table difference.</li>
        <li>AFC also differs (A richer limiter at shared low-boost breakpoints) but the dump is truncated. Do not index-align it.</li>
        <li>A piggyback that already adds fuel stacked on A’s richer 5DFL is more fuel than either change alone. This page does not tell you how to program an ECM.</li>
      </ul>
    </div>
    <div class="card">
      <h3>This is not</h3>
      <p>Not a flash / ROM image. Not a download-to-ECM file. Not a pump-frame recipe. Not overlay AID curves. Decoded values are engineering units after scale/add from a live upload.</p>
      <p class="tblcap">Full grids: <a href="tune_A_vs_B.html">tune_A_vs_B.html</a> · <a href="../docs/factory-fuel.md">factory-fuel.md</a> · <a href="../docs/factory-timing.md">factory-timing.md</a></p>
    </div>
  </div>
</section>

<section class="slide" id="notes">
  <p class="kicker">Sources</p>
  <h2>Where the numbers came from</h2>
  <p class="lead">Chart data is generated from <span class="mono">maps/tune_A_vs_B.json</span> (re-run <span class="mono">maps/build_factory_a_vs_b.py</span>). Identity from <span class="mono">A_identity.json</span> / <span class="mono">B_identity.json</span>. Cells are not invented.</p>
  <p class="note">Smarty handheld SW capture on a spare is <strong>future work</strong> (owner will flash level 6 then level 4 on that box). It is not in this dump and not the point of this deck.</p>
  <p class="tblcap">Read-only documentation. Open as a file in a browser; charts load Plotly from a CDN (tables still work offline).</p>
</section>

<script>
const DATA = %%PAYLOAD%%;
const PLOT = {
  paper_bgcolor: "rgba(0,0,0,0)",
  plot_bgcolor: "#121622",
  font: { color: "#c5c9d1", size: 12, family: "Segoe UI, system-ui, sans-serif" },
  margin: { t: 36, r: 24, b: 48, l: 56 },
  legend: { orientation: "h", y: 1.12, font: { size: 11 } },
  xaxis: { gridcolor: "#2c3344", zerolinecolor: "#2c3344", automargin: true },
  yaxis: { gridcolor: "#2c3344", zerolinecolor: "#2c3344", automargin: true },
};
const COL = { a: "#5eb0ef", b: "#e8a04a", tr: "#9b8cff", ss: "#3ecf8e", hole: "#ff8a80" };

function ready() {
  const F = DATA.fuel, T = DATA.timing, L = DATA.flfl, A = DATA.afc;
  const rpm = F.x;
  Plotly.newPlot("chart-wot", [
    { x: rpm, y: F.wot00_a, name: "A 5DFL00 100%", mode: "lines+markers", line: { color: COL.a, width: 3 }, marker: { size: 6 } },
    { x: rpm, y: F.wot00_b, name: "B 5DFL00 100%", mode: "lines+markers", line: { color: COL.b, width: 3, dash: "dash" }, marker: { size: 6 } },
    { x: rpm, y: F.wot01_a, name: "A 5DFL01 100%", mode: "lines+markers", line: { color: COL.a, width: 1.5 }, marker: { size: 4 }, opacity: 0.75 },
    { x: rpm, y: F.wot01_b, name: "B 5DFL01 100%", mode: "lines+markers", line: { color: COL.b, width: 1.5, dash: "dot" }, marker: { size: 4 }, opacity: 0.75 },
  ], Object.assign({}, PLOT, {
    title: { text: "WOT (100% throttle) fuel vs RPM", font: { size: 14, color: "#fff" } },
    xaxis: Object.assign({}, PLOT.xaxis, { title: "RPM" }),
    yaxis: Object.assign({}, PLOT.yaxis, { title: "mm³/s" }),
    annotations: [{
      x: 3000, y: F.gap.dfl01_3000.a, text: "3000 · SS Δ " + F.gap.dfl01_3000.delta,
      showarrow: true, arrowcolor: "#ffd48a", font: { color: "#ffd48a", size: 11 }, ax: 40, ay: -30
    }],
  }), {responsive: true, displaylogo: false});

  Plotly.newPlot("chart-delta", [{
    z: F.delta00, x: rpm, y: F.y.map(function(v){ return String(v) + "%"; }),
    type: "heatmap", colorscale: [[0,"#1b2838"],[0.35,"#3d4a22"],[0.7,"#b8862b"],[1,"#ffe08a"]],
    colorbar: { title: "A−B", thickness: 12 }, hoverongaps: false,
  }], Object.assign({}, PLOT, {
    title: { text: "5DFL00 A − B (mm³/s)", font: { size: 14, color: "#fff" } },
    xaxis: Object.assign({}, PLOT.xaxis, { title: "RPM" }),
    yaxis: Object.assign({}, PLOT.yaxis, { title: "throttle %", type: "category" }),
    margin: { t: 36, r: 48, b: 48, l: 64 },
  }), {responsive: true, displaylogo: false});

  Plotly.newPlot("chart-bars", [
    { x: rpm, y: F.wot00_delta, name: "5DFL00 Δ", type: "bar", marker: { color: COL.a } },
    { x: rpm, y: F.wot01_delta, name: "5DFL01 Δ", type: "bar", marker: { color: COL.b } },
  ], Object.assign({}, PLOT, {
    barmode: "group",
    title: { text: "100% row A − B vs RPM", font: { size: 14, color: "#fff" } },
    xaxis: Object.assign({}, PLOT.xaxis, { title: "RPM" }),
    yaxis: Object.assign({}, PLOT.yaxis, { title: "mm³/s" }),
  }), {responsive: true, displaylogo: false});

  Plotly.newPlot("chart-timing", [
    { x: T.x, y: T.tr_light, name: "00 transient · Y=" + T.light_y + " (light)", mode: "lines+markers", line: { color: COL.a, width: 2, dash: "dot" } },
    { x: T.x, y: T.ss_light, name: "01 steady · Y=" + T.light_y + " (light)", mode: "lines+markers", line: { color: COL.ss, width: 2, dash: "dot" } },
    { x: T.x, y: T.tr_mid, name: "00 transient · Y=" + T.mid_y + " (mid)", mode: "lines+markers", line: { color: COL.hole, width: 3 } },
    { x: T.x, y: T.ss_mid, name: "01 steady · Y=" + T.mid_y + " (mid)", mode: "lines+markers", line: { color: COL.ss, width: 3 } },
    { x: T.x, y: T.tr_peak, name: "00 transient · Y=" + T.peak_tr_y + " (peak)", mode: "lines+markers", line: { color: COL.a, width: 2 } },
    { x: T.x, y: T.ss_peak, name: "01 steady · Y=" + T.peak_ss_y + " (peak)", mode: "lines+markers", line: { color: COL.b, width: 2 } },
  ], Object.assign({}, PLOT, {
    title: { text: "Injection timing (deg) vs RPM — A = B", font: { size: 14, color: "#fff" } },
    xaxis: Object.assign({}, PLOT.xaxis, { title: "RPM" }),
    yaxis: Object.assign({}, PLOT.yaxis, { title: "deg", zeroline: true, zerolinecolor: "#ff8a80" }),
    shapes: [{ type: "line", x0: T.x[0], x1: T.x[T.x.length-1], y0: 0, y1: 0, line: { color: "#445", width: 1 } }],
  }), {responsive: true, displaylogo: false});

  Plotly.newPlot("chart-hole", [{
    z: T.hole, x: T.x, y: T.hole_y.map(String),
    type: "heatmap", colorscale: "RdBu", zmid: 0,
    colorbar: { title: "00−01", thickness: 12 },
  }], Object.assign({}, PLOT, {
    title: { text: "Transient − steady (deg), shared Y", font: { size: 14, color: "#fff" } },
    xaxis: Object.assign({}, PLOT.xaxis, { title: "RPM" }),
    yaxis: Object.assign({}, PLOT.yaxis, { title: "fuel Y mm³/s", type: "category" }),
    margin: { t: 36, r: 48, b: 48, l: 72 },
  }), {responsive: true, displaylogo: false});

  Plotly.newPlot("chart-flfl", [{
    z: L.z, x: L.x, y: L.y.map(String),
    type: "heatmap", colorscale: "Viridis",
    colorbar: { title: "mg/str", thickness: 12 },
  }], Object.assign({}, PLOT, {
    title: { text: "FLFLTBZA mg/stroke (A = B)", font: { size: 14, color: "#fff" } },
    xaxis: Object.assign({}, PLOT.xaxis, { title: "RPM" }),
    yaxis: Object.assign({}, PLOT.yaxis, { title: "Y mm³/s", type: "category" }),
    margin: { t: 36, r: 48, b: 48, l: 72 },
  }), {responsive: true, displaylogo: false});

  Plotly.newPlot("chart-flfl-peak", [
    { x: L.x, y: L.peak, name: "max across Y", mode: "lines+markers", line: { color: COL.a, width: 3 } },
    { x: L.x, y: L.z[5], name: "Y=" + L.y[5], mode: "lines+markers", line: { color: COL.b, width: 2 } },
  ], Object.assign({}, PLOT, {
    title: { text: "Conversion vs RPM (peak row + Y≈150)", font: { size: 14, color: "#fff" } },
    xaxis: Object.assign({}, PLOT.xaxis, { title: "RPM" }),
    yaxis: Object.assign({}, PLOT.yaxis, { title: "mg/stroke" }),
  }), {responsive: true, displaylogo: false});

  Plotly.newPlot("chart-afc", [
    { x: A.rpm_shared, y: A.slice0.a, name: "A @ 0 inHg", mode: "lines+markers", line: { color: COL.a, width: 3 } },
    { x: A.rpm_shared, y: A.slice0.b, name: "B @ 0 inHg", mode: "lines+markers", line: { color: COL.b, width: 3, dash: "dash" } },
    { x: A.rpm_shared, y: A.slice20.a, name: "A @ ~20 inHg", mode: "lines+markers", line: { color: COL.a, width: 2 }, opacity: 0.8 },
    { x: A.rpm_shared, y: A.slice20.b, name: "B @ ~20 inHg", mode: "lines+markers", line: { color: COL.b, width: 2, dash: "dot" }, opacity: 0.8 },
  ], Object.assign({}, PLOT, {
    title: { text: "AFC limit vs RPM — aligned by shared RPM, not column index", font: { size: 14, color: "#fff" } },
    xaxis: Object.assign({}, PLOT.xaxis, { title: "RPM" }),
    yaxis: Object.assign({}, PLOT.yaxis, { title: "mm³/s limit" }),
  }), {responsive: true, displaylogo: false});
}

function bindNav() {
  const links = [...document.querySelectorAll(".nav a[href^='#']")];
  const slides = links.map(a => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  const io = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      links.forEach(a => a.classList.toggle("on", a.getAttribute("href") === "#" + en.target.id));
    });
  }, { rootMargin: "-40% 0px -50% 0px" });
  slides.forEach(s => io.observe(s));
  document.addEventListener("keydown", (e) => {
    if (e.key !== "ArrowDown" && e.key !== "ArrowUp" && e.key !== "PageDown" && e.key !== "PageUp") return;
    const ids = slides.map(s => s.id);
    const on = document.querySelector(".nav a.on");
    let i = on ? ids.indexOf(on.getAttribute("href").slice(1)) : 0;
    if (e.key === "ArrowDown" || e.key === "PageDown") i = Math.min(ids.length - 1, i + 1);
    else i = Math.max(0, i - 1);
    e.preventDefault();
    slides[i].scrollIntoView({ behavior: "smooth" });
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", function(){ ready(); bindNav(); });
} else { ready(); bindNav(); }
</script>
</body>
</html>
"""


def write_pdf(p, dest: Path):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        import numpy as np
    except ImportError:
        return False, "matplotlib not installed"

    fuel = p["fuel"]
    T = p["timing"]
    L = p["flfl"]
    A = p["afc"]
    g = fuel["gap"]
    ia, ib = p["identity"]["a"], p["identity"]["b"]
    rpm = fuel["x"]
    bg, fg, gridc = "#0c0e14", "#e8eaed", "#2c3344"
    cola, colb = "#5eb0ef", "#e8a04a"

    def style(ax, xlabel, ylabel, title):
        ax.set_facecolor("#121622")
        ax.set_title(title, color="#fff", loc="left", fontsize=11)
        ax.set_xlabel(xlabel, color=fg)
        ax.set_ylabel(ylabel, color=fg)
        ax.tick_params(colors=fg)
        ax.grid(True, color=gridc, linewidth=0.6)
        for sp in ax.spines.values():
            sp.set_color(gridc)
        ax.legend(facecolor="#161a24", edgecolor=gridc, labelcolor=fg, fontsize=8)

    with PdfPages(dest) as pdf:
        fig = plt.figure(figsize=(11, 8.5), facecolor=bg)
        fig.text(0.07, 0.88, "Two factory CM551 / Dodge 24v VP44 cals", color="#fff", fontsize=18, weight="bold")
        fig.text(0.07, 0.82, f"A  {ia['ecm_code']}   vs   B  {ib['ecm_code']}", color=cola, fontsize=14)
        fig.text(
            0.07, 0.72,
            "ReadByNTN 0x48 · 667/667 ITNs · same P/N 03942336 / ROM 091197 · different cal dates.\n"
            "Decoded KennPar dump, not a flash image. VIN/ESN omitted.\n"
            f"Biggest complete fuel gap: 5DFL01 100% @ 3000 RPM  A−B = +{g['dfl01_3000']['delta']} mm³/s "
            f"({g['dfl01_3000']['a']} vs {g['dfl01_3000']['b']}).\n"
            f"Transient 5DFL00 at the same cell: +{g['dfl00_3000']['delta']} mm³/s "
            f"({g['dfl00_3000']['a']} vs {g['dfl00_3000']['b']}).",
            color=fg, fontsize=11, va="top",
        )
        fig.text(0.07, 0.12, "Generated from maps/tune_A_vs_B.json. Timing A=B. Fuel 100% row differs.", color="#8b93a7", fontsize=9)
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(11, 8.5), facecolor=bg)
        ax.plot(rpm, fuel["wot00_a"], "o-", color=cola, lw=2.4, label="A 5DFL00 100%")
        ax.plot(rpm, fuel["wot00_b"], "s--", color=colb, lw=2.4, label="B 5DFL00 100%")
        ax.plot(rpm, fuel["wot01_a"], "o-", color=cola, lw=1.2, alpha=0.7, label="A 5DFL01 100%")
        ax.plot(rpm, fuel["wot01_b"], "s:", color=colb, lw=1.2, alpha=0.7, label="B 5DFL01 100%")
        ax.annotate(
            f"3000 SS Δ {g['dfl01_3000']['delta']}",
            xy=(3000, g["dfl01_3000"]["a"]),
            xytext=(3100, g["dfl01_3000"]["a"] + 8),
            color="#ffd48a", fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#ffd48a"),
        )
        style(ax, "RPM", "mm³/s", "WOT (100% throttle) fuel vs RPM")
        fig.patch.set_facecolor(bg)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        fig, axes = plt.subplots(2, 1, figsize=(11, 8.5), facecolor=bg)
        z = np.array(fuel["delta00"], dtype=float)
        im = axes[0].imshow(z, aspect="auto", cmap="YlOrBr", origin="lower")
        axes[0].set_xticks(range(len(rpm)))
        axes[0].set_xticklabels([str(int(v)) if float(v).is_integer() else str(v) for v in rpm], rotation=45, ha="right", color=fg, fontsize=7)
        axes[0].set_yticks(range(len(fuel["y"])))
        axes[0].set_yticklabels([f"{v}%" for v in fuel["y"]], color=fg)
        axes[0].set_title("5DFL00 A − B heatmap (mm³/s)", color="#fff", loc="left")
        axes[0].set_facecolor("#121622")
        fig.colorbar(im, ax=axes[0], fraction=0.03)
        w = 0.38
        xs = np.arange(len(rpm))
        axes[1].bar(xs - w / 2, fuel["wot00_delta"], w, color=cola, label="5DFL00 Δ")
        axes[1].bar(xs + w / 2, fuel["wot01_delta"], w, color=colb, label="5DFL01 Δ")
        axes[1].set_xticks(xs)
        axes[1].set_xticklabels([str(int(v)) if float(v).is_integer() else str(v) for v in rpm], rotation=45, ha="right", fontsize=7)
        style(axes[1], "RPM", "mm³/s", "100% row A − B")
        fig.patch.set_facecolor(bg)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        fig, axes = plt.subplots(2, 1, figsize=(11, 8.5), facecolor=bg)
        axes[0].plot(T["x"], T["tr_light"], ":", color=cola, label=f"00 light Y={T['light_y']}")
        axes[0].plot(T["x"], T["ss_light"], ":", color="#3ecf8e", label=f"01 light Y={T['light_y']}")
        axes[0].plot(T["x"], T["tr_mid"], "-", color="#ff8a80", lw=2.2, label=f"00 mid Y={T['mid_y']}")
        axes[0].plot(T["x"], T["ss_mid"], "-", color="#3ecf8e", lw=2.2, label=f"01 mid Y={T['mid_y']}")
        axes[0].plot(T["x"], T["tr_peak"], "-", color=cola, label=f"00 peak Y={T['peak_tr_y']}")
        axes[0].plot(T["x"], T["ss_peak"], "-", color=colb, label=f"01 peak Y={T['peak_ss_y']}")
        axes[0].axhline(0, color="#445", lw=0.8)
        style(axes[0], "RPM", "deg", "Timing vs RPM (A = B). Mid-fuel transient is the retard hole.")
        hole = np.array(T["hole"], dtype=float)
        im2 = axes[1].imshow(hole, aspect="auto", cmap="RdBu_r", origin="lower")
        axes[1].set_xticks(range(len(T["x"])))
        axes[1].set_xticklabels([str(int(v)) for v in T["x"]], rotation=45, ha="right", color=fg, fontsize=7)
        axes[1].set_yticks(range(len(T["hole_y"])))
        axes[1].set_yticklabels([str(v) for v in T["hole_y"]], color=fg, fontsize=7)
        axes[1].set_title("Transient − steady (deg), shared Y", color="#fff", loc="left")
        axes[1].set_facecolor("#121622")
        fig.colorbar(im2, ax=axes[1], fraction=0.03)
        fig.patch.set_facecolor(bg)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        fig, axes = plt.subplots(1, 2, figsize=(11, 8.5), facecolor=bg)
        im3 = axes[0].imshow(np.array(L["z"], dtype=float), aspect="auto", cmap="viridis", origin="lower")
        axes[0].set_title("FLFLTBZA mg/stroke (A = B)", color="#fff", loc="left")
        axes[0].set_xlabel("RPM index", color=fg)
        axes[0].set_ylabel("Y mm³/s index", color=fg)
        axes[0].tick_params(colors=fg)
        axes[0].set_facecolor("#121622")
        fig.colorbar(im3, ax=axes[0], fraction=0.04)
        axes[1].plot(L["x"], L["peak"], "o-", color=cola, label="max across Y")
        axes[1].plot(L["x"], L["z"][5], "s-", color=colb, label=f"Y={L['y'][5]}")
        style(axes[1], "RPM", "mg/stroke", "Conversion vs RPM")
        fig.patch.set_facecolor(bg)
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(11, 8.5), facecolor=bg)
        ax.plot(A["rpm_shared"], A["slice0"]["a"], "o-", color=cola, lw=2.2, label="A @ 0 inHg")
        ax.plot(A["rpm_shared"], A["slice0"]["b"], "s--", color=colb, lw=2.2, label="B @ 0 inHg")
        ax.plot(A["rpm_shared"], A["slice20"]["a"], "o-", color=cola, lw=1.4, alpha=0.8, label="A @ ~20 inHg")
        ax.plot(A["rpm_shared"], A["slice20"]["b"], "s:", color=colb, lw=1.4, alpha=0.8, label="B @ ~20 inHg")
        style(ax, "RPM (shared breakpoints)", "mm³/s limit", "AFFLLMZA — aligned by RPM, not column index (truncated dump)")
        fig.text(
            0.07, 0.04,
            f"{A['note']}  A-only RPM {A['rpm_a_only']}  B-only RPM {A['rpm_b_only']}  "
            f"A-only boost {A['boost_a_only']}  B-only boost {A['boost_b_only']}",
            color="#8b93a7", fontsize=8,
        )
        fig.patch.set_facecolor(bg)
        fig.tight_layout(rect=(0, 0.08, 1, 1))
        pdf.savefig(fig)
        plt.close(fig)

        fig = plt.figure(figsize=(11, 8.5), facecolor=bg)
        fig.text(0.07, 0.88, "If you tune", color="#fff", fontsize=18, weight="bold")
        fig.text(
            0.07, 0.78,
            "A is the richer WOT fuel cal. Timing is identical, so fueling is the lever\n"
            "between these two boxes.\n\n"
            "Part-load 5DFL matches. FLFL conversion matches. AFC differs but is truncated.\n"
            "This PDF is not a flash file and does not describe how to program an ECM.\n\n"
            "Smarty SW capture on a spare (level 6 then 4) is future work — not this dump.",
            color=fg, fontsize=12, va="top",
        )
        pdf.savefig(fig)
        plt.close(fig)

    return True, str(dest)


def main():
    tune = load_json(HERE / "tune_A_vs_B.json")
    ident_a = load_json(HERE / "A_identity.json")
    ident_b = load_json(HERE / "B_identity.json")
    payload = build_payload(tune, ident_a, ident_b)

    g = payload["fuel"]["gap"]
    print("Verified 5DFL 100% @ 3000 RPM from JSON:")
    print(f"  5DFL00 A={g['dfl00_3000']['a']} B={g['dfl00_3000']['b']} d={g['dfl00_3000']['delta']}")
    print(f"  5DFL01 A={g['dfl01_3000']['a']} B={g['dfl01_3000']['b']} d={g['dfl01_3000']['delta']}")
    print(f"  5DFL00 @2800 d={g['dfl00_2800']['delta']}  5DFL01 @2800 d={g['dfl01_2800']['delta']}")
    print(f"  AFFLLMZA cells {payload['afc']['cells_present_a']}/{payload['afc']['cells_declared']}")
    print(f"  AFC A-only RPM {payload['afc']['rpm_a_only']}  B-only RPM {payload['afc']['rpm_b_only']}")

    html_path = HERE / "factory-a-vs-b.html"
    html_path.write_text(render_html(payload), encoding="utf-8")
    print(f"Wrote {html_path}")

    pdf_path = HERE / "factory-a-vs-b.pdf"
    ok, msg = write_pdf(payload, pdf_path)
    if ok:
        print(f"Wrote {msg}")
    else:
        print(f"PDF skipped: {msg}")

    # Guard: generated files must not contain published VIN/ESN tokens from the lab notes.
    text = html_path.read_text(encoding="utf-8").upper()
    for needle in ("3B7KF236", "3B6MC366", "56512048", "VIN", "ESN"):
        if needle in ("VIN", "ESN"):
            continue  # words "VIN"/"ESN" appear in the redaction note on purpose
        if needle in text:
            raise SystemExit(f"refusing to write identity leak: {needle}")


if __name__ == "__main__":
    main()
