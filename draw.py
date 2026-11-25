#!/usr/bin/env python3
"""Draw the news-image-20261125 front page (1024x1024 PNG).

Fresh build for Wednesday 25 November 2026. Deterministic: no clock, no
randomness, fixed fonts. Run: python3 draw.py -> entry.png in this dir.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

CREAM = (247, 241, 227)
PAPER = (232, 223, 200)
INK = (27, 27, 47)
NAVY = (31, 56, 100)
NAVY_D = (22, 41, 77)
RED = (169, 44, 38)
RED_D = (140, 32, 28)
GOLD = (201, 162, 39)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
SKY = (38, 68, 110)
DUSK = (232, 150, 80)
SAND = (226, 205, 160)
MAPDOT = (185, 160, 106)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = fnt.size + 2
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def tag_chip(draw, x, y, label, bg):
    f = SANS_B(10)
    w = int(draw.textlength(label, font=f)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=bg)
    draw.text((x + 6, y + 2), label, font=f, fill=WHITE)
    return w


# ---------------------------------------------------------------- data
BIG = [
    ("16", "TRADING PARTNERS FACE\nNEW US TARIFFS"),
    ("\u22128.2%", "TAIWAN TAIEX,\nWORST IN ASIA"),
    ("74,746", "GAZA DEATH TOLL,\nSAYS WAFA"),
    ("266m", "FACE ACUTE HUNGER\nWORLDWIDE, WFP"),
    ("4", "POLITBURO MEMBERS\nPROBED SINCE 2025"),
    ("\u00bd\u2013\u00bd", "CHESS: GUKESH \u2013\nSINDAROV, GENEVA"),
]

REGIONS = [
    ("EUROPE", 8, (31, 78, 121)),
    ("ASIA-PACIFIC", 8, (201, 162, 39)),
    ("SOUTH ASIA", 10, (46, 125, 50)),
    ("MIDDLE EAST", 5, (176, 58, 46)),
    ("AMERICAS", 7, (108, 52, 131)),
    ("OCEANIA", 1, (20, 143, 119)),
    ("WORLD", 1, (93, 109, 126)),
]

LEADS = [
    dict(n=1, place="WASHINGTON, US", tag="REPORTED", tagbg=NAVY,
         src="BBC \u00b7 REUTERS \u00b7 AP", art="tariffs",
         head="US to unveil new tariffs on 16 partners",
         body="Duties stack on existing tariffs: 15% cap for EU, Japan, Korea; 20% for China. They replace levies the Supreme Court struck down in February."),
    dict(n=2, place="TOKYO / SEOUL / TAIPEI", tag="REPORTED", tagbg=NAVY,
         src="WSJ \u00b7 REUTERS", art="markets",
         head="Asia's chip stocks plunge",
         body="Taiex \u22128.2% (TSMC \u22128.3%), Kospi \u22124.7%, Nikkei \u22123.15% as the AI rally fades. MSCI Asia ex-Japan \u22122.3%; Hong Kong +1.0% alone rises."),
    dict(n=3, place="SHANGHAI, CHINA", tag="REPORTED", tagbg=NAVY,
         src="REUTERS", art="shanghai",
         head="Shanghai pledges loyalty after Chen falls",
         body="City leaders vow loyalty a day after Chen Jining was put under a graft probe \u2014 the fourth Politburo member since 2025, and the first Shanghai chief since 2006."),
    dict(n=4, place="WARSAW, POLAND", tag="REPORTED", tagbg=NAVY,
         src="REPORTS WED", art="nato",
         head="NATO jets to watch Poland's skies",
         body="NATO will send early-warning aircraft over Poland after missiles landed there Monday. Rutte: the alliance will defend \u2018every inch\u2019 \u2014 including in space."),
    dict(n=5, place="GAZA", tag="REPORTED", tagbg=NAVY,
         src="WAFA \u00b7 WFP", art="gaza",
         head="Toll 74,746 as hunger spreads",
         body="Gaza's death toll reaches 74,746, WAFA says. The WFP warns 266 million people face acute food insecurity worldwide, with wars adding $727m to its costs."),
    dict(n=6, place="GENEVA, SWITZERLAND", tag="SCHEDULED", tagbg=(20, 143, 119),
         src="FIDE \u00b7 WORLDCHESS.COM", art="chess",
         head="Game 2 today: Gukesh has White",
         body="The championship resumes 15:00 CET in Geneva at \u00bd\u2013\u00bd. Game 1 was drawn in 38 moves \u2014 Gukesh held Sindarov in a Berlin Defence after a 36-minute think."),
]

SMALL = [
    (7, "MOSCOW", "Russia calls ship strikes \u2018terrorism\u2019",
     "Moscow warns of \u2018severe consequences\u2019 after Ukraine's Baltic and Libya strikes. (BD Global Times)"),
    (8, "TEHRAN", "Iran: close Hormuz \u2018day by day\u2019",
     "Army chief orders the strait shut further each day until the US meets Tehran's terms. (Euronews)"),
    (9, "KUALA LUMPUR", "Malaysia to return 6,800 to Myanmar",
     "PM says returns go ahead despite the ICJ genocide ruling. (Reports)"),
    (10, "BAGHDAD", "Iraq takes over Kurdish oil posts",
     "PM orders federal control of Kurdish checkpoints and oil output areas. (Reports)"),
    (11, "TEHRAN", "Khamenei: more babies \u2018vital\u2019",
     "Population growth is \u2018vital to Iran's national security\u2019, the leader says. (BD Global Times)"),
    (12, "MOSCOW", "Russia plans $609bn for defence",
     "Moscow earmarks over $609bn of defence spending for 2027\u201329. (Reports)"),
    (13, "KYIV", "Zelenskyy mocks Lukashenko offer",
     "\u2018Invite Putin to Kyiv,\u2019 he says of the proposal to fly together to Moscow. (Reports)"),
    (14, "NEW DELHI", "India hosts EU maritime talks",
     "First India\u2013EU Maritime Roundtable opens in Delhi, with IORA. (Reports)"),
    (15, "NEW DELHI", "Delhi denies defence data breach",
     "Centre orders a cyber audit of messaging groups after breach claims. (Reports)"),
]

BRIEFS = [
    (16, "VARANASI", "Dev Deepawali lights the ghats", "Reports"),
    (17, "CUTTACK", "President Murmu at Bali Jatra", "Reports"),
    (18, "SRINAGAR", "Police stop Mehbooba Mufti", "Reports"),
    (19, "LUCKNOW", "SP names UP 2027 candidates", "Reports"),
    (20, "CANBERRA", "Shares dip; inflation above target", "Reuters"),
    (21, "IOWA", "Controlled blast; 5 days' warning", "BBC"),
    (22, "ALASKA", "M4.2 quake near Point MacKenzie", "USGS"),
    (23, "WASHINGTON", "AG dodges Nvidia probe questions", "BBC"),
    (24, "CHISINAU", "Moldova aligns with EU sanctions", "Reports"),
    (25, "BERLIN", "Lufthansa mediation fails, union says", "Reports"),
    (26, "GENEVA", "UN condemns Ahmadi flogging", "Reports"),
    (27, "TOKYO", "Services prices +4.2%, fastest since 1990", "RTTNews"),
    (28, "NEW YORK", "S&P futures \u22120.3%; Nasdaq \u22122% Tue", "Reuters"),
    (29, "LUCKNOW", "CM: India safe \u2018while it reveres Sikh Gurus\u2019", "Hindu"),
    (30, "MUMBAI", "India women v China, Champions Trophy", "Sched."),
    (31, "WASHINGTON", "Thanksgiving eve travel begins", "Reports"),
    (32, "ROME", "WFP: wars add $727m to costs", "WFP"),
    (33, "NEW DELHI", "Coal accreditation extended 5 years", "Reports"),
    (34, "KOZHIKODE", "16,000 unsafe eggs seized", "Hindu"),
    (35, "SINGAPORE", "Straits Times \u22120.1%; Sydney \u22120.4%", "Edge"),
    (36, "HONG KONG", "Hang Seng +1.0%, Asia's only gainer", "WSJ"),
    (37, "TOKYO", "SoftBank \u221213%, Advantest \u221213%", "WSJ"),
    (38, "WASHINGTON", "Tariff probe: 16 economies named", "Reuters"),
    (39, "GAZA CITY", "Medics: strikes kill at least 6", "Reports"),
    (40, "BEIJING", "Politburo down to 21 of 24", "WSJ"),
]

DATECHECK = [
    "Riyadh tower hit, 11 hurt \u2014 TUE \u00b7 Huawei guilty 10/12 \u2014 TUE \u00b7 Chen probe announced \u2014 TUE \u00b7 Hamas chief Abu Nahel killed \u2014 TUE \u00b7 Suryavanshi 204 \u2014 TUE \u00b7 England win 2nd T20I \u2014 TUE",
    "Nepal quake 5.3 \u2014 TUE \u00b7 COP31 collapse \u2014 TUE \u00b7 Trump turkeys + Giuliani medal \u2014 TUE \u00b7 Iran: no talks, 7 conditions \u2014 TUE \u00b7 Hormuz claims \u2014 MON \u00b7 Ahmadi flogged \u2014 MON \u00b7 DR Congo Cessna \u2014 SUN",
]

# lon/lat polygons for the dotted world map (map box 336x144)
POLYS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 70), (-85, 66), (-75, 60), (-60, 55), (-55, 47), (-65, 45), (-70, 42), (-75, 35), (-80, 25), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 48), (-135, 58), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-20, 70), (-25, 76), (-45, 78), (-58, 74)],
    [(-80, 10), (-75, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -45), (-70, -52), (-73, -40), (-73, -25), (-77, -15), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (28, 70), (20, 70), (15, 68), (12, 62), (5, 58), (0, 50), (-5, 48), (-10, 43)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15), (43, 11), (48, 10), (51, 12), (44, 0), (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(30, 36), (35, 36), (40, 38), (45, 40), (48, 38), (50, 30), (55, 26), (58, 25), (62, 25), (66, 25), (70, 20), (72, 20), (75, 15), (78, 8), (80, 10), (85, 18), (88, 22), (92, 22), (95, 16), (98, 10), (100, 8), (103, 2), (105, 9), (108, 12), (110, 20), (115, 23), (120, 25), (122, 30), (125, 35), (127, 40), (130, 42), (135, 44), (140, 45), (142, 50), (140, 55), (135, 60), (130, 62), (125, 68), (120, 72), (115, 73), (110, 73), (105, 75), (100, 76), (95, 75), (90, 75), (85, 74), (80, 73), (75, 72), (70, 72), (65, 70), (60, 69), (55, 68), (50, 68), (45, 67), (40, 66), (35, 66), (30, 65)],
    [(95, 5), (100, 0), (105, -2), (110, -5), (115, -8), (120, -10), (125, -8), (130, -3), (135, 0), (140, -2)],
    [(113, -22), (114, -30), (115, -35), (120, -35), (125, -32), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -18), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (170, -42), (174, -38), (177, -38), (175, -41), (170, -43)],
]

PINS = [  # (story number, lon, lat, dx, dy) offsets keep crowded Europe readable
    (1, -77, 39, 0, 0), (2, 140, 36, 0, 0), (3, 121, 31, 0, 0),
    (4, 21, 52, -2, -3), (5, 34, 31, -9, 11), (6, 6, 46, -3, 5),
    (7, 38, 56, 7, -9), (8, 51, 36, 12, 2), (9, 102, 3, 0, 0),
    (10, 44, 33, 2, 8), (11, 51, 36, 20, 14), (12, 38, 56, 19, -1),
    (13, 31, 50, 1, 9), (14, 77, 29, 7, 3), (15, 77, 29, -13, 17),
]


def inside_poly(lon, lat, poly):
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def lonlat_to_xy(lon, lat, mw, mh):
    return (lon + 180.0) / 360.0 * mw, (90.0 - lat) / 180.0 * mh


# ---------------------------------------------------------------- art
def art_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # capitol dome
    cx = x + w // 2
    d.pieslice([cx - 26, y + 12, cx + 26, y + 52], 180, 360, fill=WHITE)
    d.rectangle([cx - 30, y + 34, cx + 30, y + h - 14], fill=WHITE)
    for i in range(5):
        px = cx - 22 + i * 11
        d.rectangle([px, y + 40, px + 5, y + h - 14], fill=NAVY)
    d.rectangle([cx - 2, y + 4, cx + 2, y + 14], fill=WHITE)
    d.ellipse([cx - 4, y + 1, cx + 4, y + 7], fill=GOLD)
    # flag stripes bottom
    for i in range(4):
        d.rectangle([x, y + h - 12 + i * 3, x + w, y + h - 10 + i * 3], fill=RED if i % 2 == 0 else WHITE)
    d.text((x + 8, y + 6), "%", font=SERIF_B(20), fill=GOLD)
    d.text((x + w - 26, y + 6), "$", font=SERIF_B(20), fill=GOLD)


def art_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 244, 230))
    d.line([x + 8, y + h - 12, x + w - 8, y + 12], fill=RED, width=2)
    candles = [(0.55, 0.75), (0.42, 0.68), (0.45, 0.62), (0.30, 0.55), (0.18, 0.38), (0.15, 0.28)]
    cw = w // 7
    for i, (lo, hi) in enumerate(candles):
        cx0 = x + 14 + i * cw
        top = y + int(h * lo)
        bot = y + int(h * hi)
        col = (46, 125, 50) if i == 3 else RED
        d.line([cx0 + 8, y + 6, cx0 + 8, y + h - 8], fill=col, width=1)
        d.rectangle([cx0 + 2, top, cx0 + 14, bot], fill=col)
    d.text((x + w - 62, y + 4), "\u22128.2%", font=SANS_B(13), fill=RED)


def art_shanghai(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DUSK)
    d.ellipse([x + w - 58, y + 8, x + w - 22, y + 44], fill=(250, 210, 120))
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 34, 30), (36, 26, 44), (64, 30, 26), (96, 24, 38), (122, 30, 22), (154, 26, 34), (182, 30, 26), (210, 26, 40), (238, 30, 24), (270, 26, 32)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(90, 60, 70))
    # oriental pearl tower
    tx = x + 150
    d.rectangle([tx - 2, y + 16, tx + 2, base], fill=(120, 40, 50))
    d.ellipse([tx - 12, y + 12, tx + 12, y + 34], fill=(120, 40, 50))
    d.ellipse([tx - 8, y + 38, tx + 8, y + 52], fill=(120, 40, 50))
    d.polygon([(tx - 14, y + 12), (tx, y + 2), (tx + 14, y + 12)], fill=(120, 40, 50))


def art_nato(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY_D)
    for r in (14, 26, 38):
        d.ellipse([x + 52 - r, y + h // 2 - r, x + 52 + r, y + h // 2 + r], outline=(120, 180, 120), width=1)
    d.ellipse([x + 48, y + h // 2 - 4, x + 56, y + h // 2 + 4], fill=(120, 220, 120))
    # plane silhouette
    px, py = x + w - 120, y + 18
    d.polygon([(px, py + 8), (px + 70, py + 8), (px + 92, py + 12), (px + 70, py + 16), (px, py + 16)], fill=WHITE)
    d.polygon([(px + 28, py + 8), (px + 44, py - 6), (px + 52, py + 8)], fill=WHITE)
    d.polygon([(px + 28, py + 16), (px + 44, py + 28), (px + 52, py + 16)], fill=WHITE)
    for sx, sy in [(200, 8), (240, 16), (280, 6), (300, 22), (170, 12)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)


def art_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    base = y + h
    for bx, bw, bh in [(0, 40, 26), (44, 34, 40), (82, 30, 22), (116, 36, 34), (156, 30, 20), (190, 34, 30), (228, 30, 18), (262, 34, 28)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(120, 95, 70))
    # smoke columns
    for sx in (60, 140, 230):
        for i in range(3):
            d.ellipse([x + sx - 6 + i * 2, y + 8 + i * 8, x + sx + 8 - i * 2, y + 20 + i * 8], fill=(140, 140, 140))
    # aid boxes
    for bx in (20, 250):
        d.rectangle([x + bx, base - 14, x + bx + 18, base - 2], fill=WHITE)
        d.rectangle([x + bx + 8, base - 12, x + bx + 10, base - 4], fill=RED)
        d.rectangle([x + bx + 3, base - 9, x + bx + 15, base - 7], fill=RED)


def art_chess(d, x, y, w, h):
    sq = h // 8
    ox = x + (w - sq * 8) // 2
    for r in range(8):
        for c in range(8):
            col = CREAM if (r + c) % 2 == 0 else INK
            d.rectangle([ox + c * sq, y + r * sq, ox + (c + 1) * sq, y + (r + 1) * sq], fill=col)
    # two kings
    d.ellipse([ox + 2 * sq + 1, y + 1 * sq + 1, ox + 3 * sq - 1, y + 2 * sq - 1], fill=WHITE, outline=INK)
    d.ellipse([ox + 5 * sq + 1, y + 6 * sq + 1, ox + 6 * sq - 1, y + 7 * sq - 1], fill=INK, outline=WHITE)
    d.text((ox + 2 * sq + 2, y + 1 * sq + 1), "K", font=SERIF_B(sq - 2), fill=INK)
    d.text((ox + 5 * sq + 2, y + 6 * sq + 1), "K", font=SERIF_B(sq - 2), fill=WHITE)


ART = {"tariffs": art_tariffs, "markets": art_markets, "shanghai": art_shanghai,
       "nato": art_nato, "gaza": art_gaza, "chess": art_chess}


# ---------------------------------------------------------------- draw
def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=PAPER, width=2)

    # top navy band
    d.rectangle([0, 0, W, 30], fill=NAVY)
    d.text((12, 7), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=WHITE)
    rt = "A ONE-PAGE BRIEF OF ONE DAY'S NEWS"
    d.text((W - 12 - d.textlength(rt, font=SANS_B(13)), 7), rt, font=SANS_B(13), fill=WHITE)

    # masthead
    title = "Wednesday 25 November 2026"
    tf = SERIF_B(56)
    d.text(((W - d.textlength(title, font=tf)) / 2, 34), title, font=tf, fill=INK)
    sub = "40 DATED STORIES  \u00b7  7 REGIONS  \u00b7  EVERY STORY DATED WEDNESDAY 25 NOVEMBER 2026 AT ITS SOURCE"
    sf = SANS(13)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 96), sub, font=sf, fill=INK)

    # ticker
    d.line([12, 112, W - 12, 112], fill=RED, width=2)
    tick = "US tariffs due today  \u00b7  Asia's chip stocks plunge  \u00b7  Shanghai pledges loyalty after Chen probe"
    tif = SERIF(16)
    d.text(((W - d.textlength(tick, font=tif)) / 2, 118), tick, font=tif, fill=RED_D)
    d.line([12, 140, W - 12, 140], fill=INK, width=1)

    # big numbers strip
    cw = (W - 24) // 6
    for i, (val, lab) in enumerate(BIG):
        x0 = 12 + i * cw
        if i:
            d.line([x0, 148, x0, 184], fill=PAPER, width=1)
        vf = SERIF_B(30)
        d.text((x0 + (cw - d.textlength(val, font=vf)) / 2, 146), val, font=vf, fill=RED if i % 2 == 0 else NAVY)
        lf = SANS_B(9)
        for j, ll in enumerate(lab.split("\n")):
            d.text((x0 + (cw - d.textlength(ll, font=lf)) / 2, 180 + j * 11), ll, font=lf, fill=GREY)
    d.line([12, 204, W - 12, 204], fill=INK, width=1)

    # region bar
    total = sum(c for _, c, _ in REGIONS)
    bx, bw_total = 12, W - 24
    x = bx
    for name, cnt, col in REGIONS:
        wseg = bw_total * cnt // total
        d.rectangle([x, 208, x + wseg, 220], fill=col)
        x += wseg
    rlab = "WHERE THE DAY HAPPENED   " + "   ".join("%s %d" % (n, c) for n, c, _ in REGIONS)
    d.text((12, 224), rlab, font=SANS_B(11), fill=INK)

    # UTC strip
    d.rectangle([0, 242, W, 260], fill=NAVY)
    utc = "THE DAY IN UTC   00:38  BBC reports US tariff plan   \u00b7   02:43  Asia wrap: Taiex \u22127.6%   \u00b7   03:06  NATO Poland plan   \u00b7   15:00 CET  Chess Game 2, Geneva"
    d.text((12, 246), utc, font=SANS_B(11), fill=WHITE)

    # lead cards (2 rows x 3)
    card_w, card_h, gap = 328, 184, 4
    for idx, L in enumerate(LEADS):
        row, col = divmod(idx, 3)
        x0 = 12 + col * (card_w + gap)
        y0 = 264 + row * (card_h + gap)
        d.rectangle([x0, y0, x0 + card_w, y0 + card_h], fill=WHITE, outline=PAPER, width=1)
        ART[L["art"]](d, x0 + 1, y0 + 1, card_w - 2, 62)
        d.rectangle([x0, y0 + 63, x0 + card_w, y0 + 66], fill=RED)
        ly = y0 + 71
        nf = SANS_B(11)
        d.text((x0 + 8, ly), "%d \u00b7 %s" % (L["n"], L["place"]), font=nf, fill=INK)
        tag_chip(d, x0 + card_w - 92, ly - 1, L["tag"], L["tagbg"])
        hy = ly + 17
        hl = wrap(d, L["head"], SERIF_B(19), card_w - 16)
        text_block(d, x0 + 8, hy, hl[:2], SERIF_B(19), INK, leading=21)
        by = hy + len(hl[:2]) * 21 + 3
        bl = wrap(d, L["body"], SANS(11), card_w - 16)
        text_block(d, x0 + 8, by, bl[:3], SANS(11), (40, 40, 40), leading=12)
        src = L["src"]
        d.text((x0 + card_w - 8 - d.textlength(src, font=SANS_B(9)), y0 + card_h - 12),
               src, font=SANS_B(9), fill=GREY)

    # small cards (3 rows x 3)
    sc_w, sc_h = 328, 54
    sy0 = 640
    for idx, (n, place, head, body) in enumerate(SMALL):
        row, col = divmod(idx, 3)
        x0 = 12 + col * (sc_w + gap)
        y0 = sy0 + row * (sc_h + 4)
        d.rectangle([x0, y0, x0 + sc_w, y0 + sc_h], fill=WHITE, outline=PAPER, width=1)
        d.rectangle([x0, y0, x0 + 5, y0 + sc_h], fill=NAVY)
        d.text((x0 + 10, y0 + 4), "%d \u00b7 %s" % (n, place), font=SANS_B(10), fill=RED_D)
        hl = wrap(d, head, SANS_B(13), sc_w - 16)
        text_block(d, x0 + 10, y0 + 18, hl[:1], SANS_B(13), INK, leading=15)
        bl = wrap(d, body, SANS(11), sc_w - 16)
        text_block(d, x0 + 10, y0 + 33, bl[:2], SANS(11), (40, 40, 40), leading=11)

    # rest of the day header
    d.text((12, 812), "THE REST OF THE DAY  \u2014  25 briefs, numbered 16\u201340, each with its source",
           font=SANS_B(12), fill=INK)
    d.line([12, 826, W - 12, 826], fill=INK, width=1)

    # briefs (2 columns) + map
    bx0, bx1 = 12, 352
    bw = 330
    for i, (n, place, head, src) in enumerate(BRIEFS):
        col = 0 if i < 13 else 1
        row = i if i < 13 else i - 13
        x0 = bx0 if col == 0 else bx1
        y0 = int(830 + row * 10.5)
        line = "%d %s \u2014 %s (%s)" % (n, place, head, src)
        f = SANS(10)
        if d.textlength(line, font=f) > bw:
            f = SANS(9)
        d.text((x0, y0), line, font=f, fill=INK)

    # map
    mx0, my0, mw, mh = 700, 830, 312, 136
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(250, 246, 236), outline=PAPER, width=1)
    d.text((mx0 + 6, my0 + 3), "WHERE IT HAPPENED \u2014 PINS MATCH STORY NUMBERS",
           font=SANS_B(9), fill=INK)
    map_top = my0 + 16
    map_h = mh - 16
    step = 5
    gx, gy = mx0, map_top
    yy = 0
    while yy < map_h:
        xx = 0
        while xx < mw:
            lon = (xx / mw) * 360.0 - 180.0
            lat = 90.0 - (yy / map_h) * 180.0
            if any(inside_poly(lon, lat, p) for p in POLYS):
                d.ellipse([gx + xx - 1, gy + yy - 1, gx + xx + 1, gy + yy + 1], fill=MAPDOT)
            xx += step
        yy += step
    for n, lon, lat, dx, dy in PINS:
        px, py = lonlat_to_xy(lon, lat, mw, map_h)
        px += mx0 + dx
        py += map_top + dy
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=WHITE, outline=RED, width=2)
        t = str(n)
        tf2 = SANS_B(8)
        d.text((px - d.textlength(t, font=tf2) / 2, py - 5), t, font=tf2, fill=RED)

    # date check
    d.rectangle([12, 970, W - 12, 1006], fill=RED)
    d.text((20, 973), "DATE CHECK \u2014 NOT WEDNESDAY, LEFT OUT ON PURPOSE:",
           font=SANS_B(11), fill=WHITE)
    df = SANS(9)
    d.text((20, 986), DATECHECK[0], font=df, fill=WHITE)
    d.text((20, 997), DATECHECK[1], font=df, fill=WHITE)

    # footer
    foot = "Sources are named on the page  \u00b7  Compiled Wednesday 25 November 2026  \u00b7  REPORTED = carried by the day's wires  \u00b7  CLAIM = one side's claim, printed beside the denial  \u00b7  SCHEDULED = set for Wednesday"
    ff = SANS(9)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1010), foot, font=ff, fill=GREY)

    img.save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
