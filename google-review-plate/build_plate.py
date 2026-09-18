# -*- coding: utf-8 -*-
"""
Google rəy lövhəsi (NFC/QR plaka) – vektörel üretim scripti.

Çıktılar (100 x 100 mm, 1 birim = 0,1 mm):
  google-rey-lovhesi.svg  – tüm yazılar path'e çevrilmiş, saf vektör
  google-rey-lovhesi.pdf  – aynı çizim, baskı/RIP için PDF (CMYK'ya RIP'te dönüştürülür)

Fontlar: Segoe UI Black (başlık), Segoe UI Bold (alt yazı) – Windows'ta hazır.
Yazılar outline'a alındığı için hedef makinede font gerekmez.
"""
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

OUT = os.path.dirname(os.path.abspath(__file__))
FONTS = r"C:\Windows\Fonts"
W = H = 1000            # 100 mm
KAPPA = 0.5522847498

# ---- renkler -------------------------------------------------------------
BLUE      = "#1A6BE0"
LIGHTBLUE = "#A9D4F5"
WHITE     = "#FFFFFF"
STAR      = "#F9C623"
BLACK     = "#000000"
G_RED, G_YEL, G_GRN, G_BLU = "#EA4335", "#FBBC05", "#34A853", "#4285F4"

LINE1 = "GOOGLE RƏYLƏRİNİZ"
LINE2 = "BİZİM ÜÇÜN DƏYƏRLİDİR!"
LINE3 = "TELEFONUNUZU YAXINLAŞDIRIN"

# ---- geometri yardımcıları (her şey M/L/C/Z; yay = kübik bezier) -------------
def P(a, r, cx, cy):
    return (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))

def arc_segs(cx, cy, r, a0, a1):
    """a0 -> a1 (derece, y aşağı yönlü) yayını kübik bezierlere böler; başlangıç noktası hariç."""
    segs = []
    n = max(1, int(math.ceil(abs(a1 - a0) / 90.0 - 1e-9)))
    step = (a1 - a0) / n
    for i in range(n):
        b0, b1 = a0 + i * step, a0 + (i + 1) * step
        t = math.radians(b1 - b0)
        k = 4.0 / 3.0 * math.tan(t / 4.0)
        x0, y0 = P(b0, r, cx, cy); x3, y3 = P(b1, r, cx, cy)
        r0, r1 = math.radians(b0), math.radians(b1)
        x1, y1 = x0 - k * r * math.sin(r0), y0 + k * r * math.cos(r0)
        x2, y2 = x3 + k * r * math.sin(r1), y3 - k * r * math.cos(r1)
        segs.append(("C", x1, y1, x2, y2, x3, y3))
    return segs

def circle(cx, cy, r):
    x, y = P(0, r, cx, cy)
    return [("M", x, y)] + arc_segs(cx, cy, r, 0, 360) + [("Z",)]

def rounded_rect(x, y, w, h, r):
    p = [("M", x + r, y), ("L", x + w - r, y)]
    p += arc_segs(x + w - r, y + r, r, 270, 360)
    p += [("L", x + w, y + h - r)]
    p += arc_segs(x + w - r, y + h - r, r, 0, 90)
    p += [("L", x + r, y + h)]
    p += arc_segs(x + r, y + h - r, r, 90, 180)
    p += [("L", x, y + r)]
    p += arc_segs(x + r, y + r, r, 180, 270)
    return p + [("Z",)]

def annular_sector(cx, cy, r_in, r_out, a0, a1, roundcaps=False):
    """Halka dilimi (a0 -> a1 saat yönü). roundcaps: uçları yuvarlat."""
    x, y = P(a0, r_out, cx, cy)
    p = [("M", x, y)] + arc_segs(cx, cy, r_out, a0, a1)
    rm = (r_in + r_out) / 2.0; hw = (r_out - r_in) / 2.0
    if roundcaps:
        ex, ey = P(a1, rm, cx, cy)
        p += arc_segs(ex, ey, hw, a1, a1 + 180)
    else:
        p += [("L",) + P(a1, r_in, cx, cy)]
    p += arc_segs(cx, cy, r_in, a1, a0)
    if roundcaps:
        sx, sy = P(a0, rm, cx, cy)
        p += arc_segs(sx, sy, hw, a0 + 180, a0 + 360)
    return p + [("Z",)]

def star(cx, cy, R, r, n=5):
    p = []
    for i in range(2 * n):
        a = -90 + i * 180.0 / n
        rr = R if i % 2 == 0 else r
        p.append(("M" if i == 0 else "L",) + P(a, rr, cx, cy))
    return p + [("Z",)]

def transform(path, fn):
    out = []
    for s in path:
        if s[0] == "Z": out.append(s); continue
        pts = [fn(s[i], s[i + 1]) for i in range(1, len(s), 2)]
        out.append((s[0],) + tuple(v for pt in pts for v in pt))
    return out

def rotate_about(path, cx, cy, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return transform(path, lambda x, y: (cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c))

def translate(path, dx, dy):
    return transform(path, lambda x, y: (x + dx, y + dy))

# ---- yazı -> path --------------------------------------------------------------
class CubicPen(BasePen):
    def __init__(self, gs):
        super().__init__(gs); self.p = []
    def _moveTo(self, pt): self.p.append(("M",) + pt)
    def _lineTo(self, pt): self.p.append(("L",) + pt)
    def _curveToOne(self, p1, p2, p3): self.p.append(("C",) + p1 + p2 + p3)
    def _closePath(self): self.p.append(("Z",))

class Face:
    def __init__(self, file):
        self.f = TTFont(os.path.join(FONTS, file))
        self.gs = self.f.getGlyphSet(); self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        self.kern = {}
        # basit GPOS/kern tablosu (varsa)
        if "kern" in self.f:
            for t in self.f["kern"].kernTables:
                self.kern.update(getattr(t, "kernTable", {}))
    def width(self, text, size):
        return sum(self.gs[self.cmap[ord(c)]].width for c in text) * size / self.upm
    def paths(self, text, size, x, y):
        """x: satır başlangıcı, y: baseline. Path listesi döner (birim koordinatlarda)."""
        k = size / self.upm; out = []; pen_x = 0
        for c in text:
            g = self.cmap[ord(c)]
            pen = CubicPen(self.gs); self.gs[g].draw(pen)
            out += transform(pen.p, lambda gx, gy, px=pen_x: (x + (gx + px) * k, y - gy * k))
            pen_x += self.gs[g].width
        return out
    def centered(self, text, size, cx, y):
        return self.paths(text, size, cx - self.width(text, size) / 2.0, y)

def fit_size(face, text, max_w, max_size):
    return min(max_size, max_w / face.width(text, 1.0))

# ---- tasarım --------------------------------------------------------------------
def build():
    shapes = []   # (layer, fill, path)
    def add(layer, fill, path): shapes.append((layer, fill, path))

    # 1) arka plan – yuvarlatılmış kare
    add("arkaplan", WHITE, rounded_rect(0, 0, W, H, 75))

    # 2) mavi üst alan (alt kenarı dalga)
    top = [("M", 0, 458),
           ("C", 150, 535, 330, 505, 520, 440),
           ("C", 720, 378, 850, 418, 1000, 392)]
    top_rev = [("M", 1000, 392),
               ("C", 850, 418, 720, 378, 520, 440),
               ("C", 330, 505, 150, 535, 0, 458)]
    blue = [("M", 0, 75)] + arc_segs(75, 75, 75, 180, 270) + [("L", 925, 0)] \
         + arc_segs(925, 75, 75, 270, 360) + [("L", 1000, 392)] + top_rev[1:] + [("Z",)]
    add("tasarim", BLUE, blue)

    # 3) açık mavi dalga bandı
    bot_rev = [("M", 1000, 628),
               ("C", 880, 612, 740, 552, 560, 578),
               ("C", 380, 604, 200, 622, 0, 538)]
    band = top + [("L", 1000, 628)] + bot_rev[1:] + [("Z",)]
    add("tasarim", LIGHTBLUE, band)

    # 4) yıldızlar
    for i in range(5):
        add("tasarim", STAR, star(500 + (i - 2) * 84, 95, 36, 15.5))

    # 5) başlık
    black_face = Face("seguibl.ttf")
    size = min(fit_size(black_face, LINE1, 850, 80), fit_size(black_face, LINE2, 850, 80))
    add("tasarim", WHITE, black_face.centered(LINE1, size, 500, 248))
    add("tasarim", WHITE, black_face.centered(LINE2, size, 500, 248 + size * 1.1))

    # 6) Google "G" – beyaz daire üzerinde
    gx, gy, R, sw = 500, 482, 92, 35
    r = R - sw
    add("tasarim", WHITE, circle(gx, gy, 128))
    add("tasarim", G_RED, annular_sector(gx, gy, r, R, 210, 316))
    add("tasarim", G_YEL, annular_sector(gx, gy, r, R, 150, 210))
    add("tasarim", G_GRN, annular_sector(gx, gy, r, R, 48, 150))
    th = math.degrees(math.asin(sw / r))
    gb = [("M", gx, gy), ("L", gx + R, gy)] + arc_segs(gx, gy, R, 0, 48) \
       + [("L",) + P(48, r, gx, gy)] + arc_segs(gx, gy, r, 48, th) + [("L", gx, gy + sw), ("Z",)]
    add("tasarim", G_BLU, gb)

    # 7) NFC / telefon ikonu
    ix, iy = 500, 750          # ikon merkezi
    rc = (ix - 45, iy - 5)     # halka merkezi
    add("tasarim", BLACK, annular_sector(rc[0], rc[1], 84, 97, 60, 306))
    # temassız dalgaları
    wx, wy = ix - 8, iy - 5
    for rad in (22, 40, 58):
        add("tasarim", BLACK, annular_sector(wx, wy, rad - 5.5, rad + 5.5, 138, 222, roundcaps=True))
    # telefon (hafif eğik)
    px0, py0, pw, ph = ix + 38, iy - 78, 74, 150
    tilt = -7
    phone = rotate_about(rounded_rect(px0, py0, pw, ph, 11), ix, iy, tilt)
    screen = rotate_about(rounded_rect(px0 + 7, py0 + 9, pw - 14, ph - 18, 6), ix, iy, tilt)
    # el: parmaklar (telefonun sağ kenarından taşan tümsekler)
    fingers = []
    for j, fy in enumerate((-46, -14, 18, 50)):
        fw = 30 if j < 3 else 26
        fingers.append(rotate_about(rounded_rect(px0 + pw - 22, py0 + ph / 2 + fy - 13, fw + 22, 26, 13), ix, iy, tilt))
    # avuç + bilek (telefonun arkasında, altta düz kesilir)
    L = lambda x, y: (ix + x, iy + y)
    palm = [("M",) + L(46, 132),
            ("C",) + L(36, 104) + L(34, 76) + L(44, 56),
            ("C",) + L(60, 44) + L(80, 46) + L(96, 54),
            ("L",) + L(124, 46),
            ("C",) + L(140, 76) + L(144, 104) + L(136, 132), ("Z",)]
    # baş parmak (ekranın üstünde)
    thumb = [("M",) + L(36, 84),
             ("C",) + L(34, 44) + L(40, 24) + L(52, 8),
             ("C",) + L(58, 0) + L(68, 0) + L(72, 8),
             ("C",) + L(76, 16) + L(70, 26) + L(64, 38),
             ("C",) + L(58, 50) + L(56, 62) + L(58, 84), ("Z",)]
    add("tasarim", BLACK, palm)
    for f in fingers: add("tasarim", BLACK, f)
    add("tasarim", BLACK, phone)
    add("tasarim", WHITE, screen)
    add("tasarim", BLACK, thumb)
    # parmak arası beyaz ayırıcılar
    for fy in (-30, 2, 34):
        sep = rotate_about(rounded_rect(px0 + pw - 2, py0 + ph / 2 + fy - 2.2, 34, 4.4, 2.2), ix, iy, tilt)
        add("tasarim", WHITE, sep)

    # 8) alt yazı
    bold_face = Face("segoeuib.ttf")
    s3 = fit_size(bold_face, LINE3, 840, 54)
    add("tasarim", BLACK, bold_face.centered(LINE3, s3, 500, 946))
    return shapes

# ---- çıktı ---------------------------------------------------------------------
def fmt(v): return ("%.2f" % v).rstrip("0").rstrip(".")

def path_d(path):
    out = []
    for s in path:
        out.append(s[0] + " ".join(fmt(v) for v in s[1:]))
    return " ".join(out)

def write_svg(shapes, file):
    layers = {}
    for layer, fill, path in shapes:
        layers.setdefault(layer, []).append('    <path fill="%s" d="%s"/>' % (fill, path_d(path)))
    body = []
    for layer in ("arkaplan", "tasarim"):
        body.append('  <g id="%s">\n%s\n  </g>' % (layer, "\n".join(layers[layer])))
    # kesim çizgisi – ayrı katman, hairline (baskıda kapatın)
    body.append('  <g id="kesim" fill="none" stroke="#FF00FF" stroke-width="0.25">\n    <path d="%s"/>\n  </g>'
                % path_d(rounded_rect(0, 0, W, H, 75)))
    svg = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<svg xmlns="http://www.w3.org/2000/svg" width="100mm" height="100mm" viewBox="0 0 %d %d">\n'
           '  <title>Google rəy lövhəsi – 100x100 mm</title>\n%s\n</svg>\n' % (W, H, "\n".join(body)))
    with open(file, "w", encoding="utf-8") as fh: fh.write(svg)

def write_pdf(shapes, file):
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor
    k = 100.0 * mm / W
    c = canvas.Canvas(file, pagesize=(100 * mm, 100 * mm))
    c.setTitle("Google rəy lövhəsi – 100x100 mm")
    for layer, fill, path in shapes:
        p = c.beginPath()
        for s in path:
            if s[0] == "M": p.moveTo(s[1] * k, (H - s[2]) * k)
            elif s[0] == "L": p.lineTo(s[1] * k, (H - s[2]) * k)
            elif s[0] == "C": p.curveTo(s[1] * k, (H - s[2]) * k, s[3] * k, (H - s[4]) * k, s[5] * k, (H - s[6]) * k)
            else: p.close()
        c.setFillColor(HexColor(fill))
        c.drawPath(p, stroke=0, fill=1)
    c.showPage(); c.save()

if __name__ == "__main__":
    shapes = build()
    write_svg(shapes, os.path.join(OUT, "google-rey-lovhesi.svg"))
    write_pdf(shapes, os.path.join(OUT, "google-rey-lovhesi.pdf"))
    print("ok", len(shapes), "shapes")
