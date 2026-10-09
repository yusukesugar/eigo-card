"""ホーム画面の世界地図を SVG にする。

- 元データは map/countries-110m.json（world-atlas 2.0、Natural Earth 1:110m）。ネットに取りに行かない
- 投影は Equal Earth（面積が正しい）。「この国はこのぐらいの広さ」を見せるため、メルカトルは使わない
- 日本の地図帳と同じく 太平洋を真ん中にする（中心 経度150°）。切れ目が大西洋に来るので、
  グリーンランドのように切れ目をまたぐ国は 左右に2回描き、地球の輪郭で切り抜く
"""
import json
import math
import pathlib

HERE = pathlib.Path(__file__).parent
CENTER_LON = 150
SCALE = 180  # 単位球の座標 → viewBox。横幅はおよそ 2*2.7*SCALE

A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
M = math.sqrt(3) / 2


def project(lon: float, lat: float) -> tuple[float, float]:
    lam, phi = math.radians(lon), math.radians(max(-89.9, min(89.9, lat)))
    t = math.asin(M * math.sin(phi))
    t2, t6 = t * t, t ** 6
    x = 2 * math.sqrt(3) * lam * math.cos(t) / (3 * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = t * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return x * SCALE, -y * SCALE


X_EDGE = project(180, 0)[0]
Y_EDGE = -project(0, 90)[1]
WIDTH, HEIGHT = 2 * X_EDGE, 2 * Y_EDGE


def decode_arcs(topo: dict) -> list[list[tuple[float, float]]]:
    (sx, sy), (tx, ty) = topo["transform"]["scale"], topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    return arcs


def ring_points(ring: list[int], arcs) -> list[tuple[float, float]]:
    pts = []
    for i in ring:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return pts


def unwrap(pts):
    """中心経度からの差にして、点どうしが 180° 以上飛ばないようにつなぐ。"""
    out = []
    for lon, lat in pts:
        d = (lon - CENTER_LON + 180) % 360 - 180
        if out:
            while d - out[-1][0] > 180:
                d -= 360
            while out[-1][0] - d > 180:
                d += 360
        out.append((d, lat))
    return out


def ring_path(pts, shift: float) -> str:
    xy = [project(lon + shift, lat) for lon, lat in pts]
    return "M" + "L".join(f"{x + X_EDGE:.1f},{y + Y_EDGE:.1f}" for x, y in xy) + "Z"


def polygon_paths(polys) -> str:
    parts = []
    for poly in polys:
        rings = [unwrap(r) for r in poly]
        lons = [p[0] for p in rings[0]]
        for shift in (0, 360, -360):
            if min(lons) + shift < 180 and max(lons) + shift > -180:
                parts.extend(ring_path(r, shift) for r in rings)
    return "".join(parts)


def outline_path(n: int = 90) -> str:
    right = [project(180, -90 + 180 * i / n) for i in range(n + 1)]
    left = [(-x, y) for x, y in reversed(right)]
    return "M" + "L".join(f"{x + X_EDGE:.1f},{y + Y_EDGE:.1f}" for x, y in right + left) + "Z"


def world_svg(groups: dict[str, dict], box: tuple | None = None, uid: str = "w", label: str = "世界地図") -> str:
    """box: (西の経度, 東の経度, 南の緯度, 北の緯度) で切り出す。無ければ 世界全体。
    groups: ISO 3166 数字コード → {"cls": CSS クラス, "href": 押したときの行き先, "label": 読み上げ用}"""
    topo = json.loads((HERE / "map" / "countries-110m.json").read_text())
    arcs = decode_arcs(topo)
    plain, marked = [], []
    for g in topo["objects"]["countries"]["geometries"]:
        if g.get("id") == "010" or g["type"] not in ("Polygon", "MultiPolygon"):
            continue  # 南極は描かない
        polys = [g["arcs"]] if g["type"] == "Polygon" else g["arcs"]
        polys = [[ring_points(r, arcs) for r in p] for p in polys]
        d = polygon_paths(polys)
        info = groups.get(g.get("id"))
        if info is None:
            plain.append(d)
        elif info.get("href"):
            marked.append(f'<a href="{info["href"]}" aria-label="{info["label"]}">'
                          f'<path class="{info["cls"]}" d="{d}"/></a>')
        else:
            marked.append(f'<path class="{info["cls"]}" d="{d}"><title>{info["label"]}</title></path>')
    outline = outline_path()
    if box is None:
        left, right = 0, WIDTH
        top, bottom = project(0, 84)[1] + Y_EDGE, project(0, -57)[1] + Y_EDGE  # 南極の分の余白を切る
    else:
        w, e, south, north = box
        corners = [project(lon - CENTER_LON, lat) for lon in (w, e) for lat in (south, north)]
        left, right = min(x for x, _ in corners) + X_EDGE, max(x for x, _ in corners) + X_EDGE
        top, bottom = project(0, north)[1] + Y_EDGE, project(0, south)[1] + Y_EDGE
    return (
        f'<svg class="world" viewBox="{left:.0f} {top:.0f} {right - left:.0f} {bottom - top:.0f}" '
        f'role="img" aria-label="{label}">'
        f'<defs><clipPath id="globe-{uid}"><path d="{outline}"/></clipPath></defs>'
        f'<path class="sea" d="{outline}"/>'
        f'<g clip-path="url(#globe-{uid})"><path class="land" d="{"".join(plain)}"/>{"".join(marked)}</g>'
        f'</svg>'
    )
