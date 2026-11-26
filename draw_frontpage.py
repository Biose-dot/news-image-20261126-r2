#!/usr/bin/env python3
"""Draw the front page for THE WORLD TODAY, Thursday 26 November 2026.

A single 1024x1024 PNG broadsheet summarising the day's world news.
Deterministic: fixed palette, fixed fonts, no clock, no randomness,
no network. Run:  python3 draw_frontpage.py  -> writes entry.png
next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (18, 18, 18)
NAVY = (22, 50, 79)
RED = (163, 22, 33)
GREY = (90, 86, 76)
RULE = (60, 58, 52)
LIGHT = (232, 226, 210)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one(draw, text, fnt, width):
    """Shrink text to a single line with an ellipsis if it overflows."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "...", font=fnt) > width:
        text = text[:-1]
    return text + "..."


# ---------------------------------------------------------------- content
LEAD_HEAD = "PEACE TALKS AT A CROSSROADS"
LEAD_LINES = [
    "Trump wants the war ended \u201ceven today\u201d, but sets no deadline for a deal.",
    "Washington pauses business incentives to Moscow as envoys Kushner and Witkoff press on.",
    "The EU is to join the next round; Kyiv awaits a date for four-way talks.",
]

SECTIONS = [
    ("AMERICAS", [
        ("Confidence at a near two-year high",
         "US consumer confidence jumps to 103.3 in November after the midterms."),
        ("US economy grew 4.3% in Q3",
         "Fastest pace in three years, powered by spending and AI investment."),
        ("New tariffs on 14 partners",
         "Trump targets excess factory capacity; China, Japan and the EU in line."),
        ("Markets shut for Thanksgiving",
         "Storms threaten holiday travel as Americans head home for the feast."),
        ("Six missing after plane crash",
         "Small aircraft goes down off the Mississippi coast; search goes on."),
        ("Abrego Garcia lands in Spain",
         "Migrant at the centre of the deportation fight leaves the US in a deal."),
    ]),
    ("EUROPE", [
        ("Chess title match tied 1\u20131",
         "Gukesh and Sindarov draw Game 2; Game 3 is played today in Geneva."),
        ("Russia raises defence spending",
         "Moscow lifts military allocations as the war grinds into winter."),
        ("Poland alarmed by airspace violations",
         "Warsaw warns over incursions as NATO watches its eastern flank."),
        ("France chases mineral independence",
         "Paris moves to cut reliance on foreign supplies of critical minerals."),
        ("Britain probes nuclear-test legacy",
         "London opens an inquiry into veterans of Cold War atomic trials."),
        ("Ukraine and Hungary renew ties",
         "Kyiv and Budapest agree new economic links despite the war."),
    ]),
    ("MIDDLE EAST & AFRICA", [
        ("Houthi drone hits Riyadh tower",
         "Eleven people are hurt as a drone strikes a skyscraper in the capital."),
        ("Houthis claim Ras Tanura strike",
         "Saudi jets answer with raids on Sanaa and the port of Hodeidah."),
        ("UK sanctions Houthi leaders",
         "London acts as Gulf states condemn the attack on Riyadh."),
        ("Hamas security chief killed in Gaza",
         "Israeli strike kills Mohammad Abuelouf, his wife and two children."),
        ("Sudan drone strikes kill 19",
         "RSF drones hit homes in Damazin; six of the dead are women."),
        ("Libya vows retaliation",
         "Two naval officers die in a Ukrainian drone hit on a Russian warship."),
    ]),
    ("ASIA-PACIFIC", [
        ("First Pakistani in orbit",
         "Shenzhou-24 docks at Tiangong with Muhammad Zeeshan Ali aboard."),
        ("BepiColombo reaches Mercury",
         "European-Japanese craft enters orbit after an eight-year voyage."),
        ("Record 1,220 for IPL auction",
         "Players register for the 2027 auction in Goa on 16 December."),
        ("India marks Constitution Day",
         "The nation honours the adoption of its constitution in 1949."),
        ("Magnitude 5.6 quake in Nepal",
         "Tremor shakes the hills; no major damage is reported at first."),
        ("Bangladesh raises garment wage",
         "Pay for garment workers rises 36% after months of unrest."),
    ]),
    ("SCIENCE, TECH & MARKETS", [
        ("Nvidia soars 32% on Huang return",
         "Board reinstates its chief; shares post their best day since 2003."),
        ("S&P puts Nvidia on watch",
         "Ratings agency cites board turmoil after the CEO's brief exit."),
        ("Nine measles deaths in the US",
         "CDC counts nine measles-related deaths in 2026 so far."),
        ("Mosquito trial cuts infections 68%",
         "Wolbachia mosquitoes slash viral illness in Brazilian cities."),
        ("Sensex drops 1,484 points",
         "Indian shares slide as the AI sell-off spreads across Asia."),
        ("Flipkart chief steps down",
         "India's e-commerce giant names a successor as growth slows."),
    ]),
    ("SPORT & CULTURE", [
        ("New Zealand hold India to a draw",
         "Tourists bat out the final day to save the Test in India."),
        ("Sooryavanshi smashes 204 off 53",
         "Teenager's double hundred lights up the domestic one-day cup."),
        ("Hockey series marks 100 years",
         "India and New Zealand celebrate a century of sporting ties."),
        ("World Boxing Cup finals open",
         "The finals run from today until 4 December."),
        ("Syed Modi badminton under way",
         "India's Super 300 event opens in Lucknow."),
    ]),
]

ALSO = [
    "Thanksgiving Day in the USA \u2014 Trump pardons turkeys Freedom and Feathers.",
    "Hong Kong marks one year since the Tai Po fire.",
    "Cyberattack hits US intelligence agencies; key systems stay safe.",
    "UAE road crash kills 11 people.",
]


# ---------------------------------------------------------------- drawing
def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 228, 238))
    for k in range(-2, 3):
        x = cx + k * r // 3
        d.arc([x - r // 3, cy - r, x + r // 3, cy + r], 90, 270,
              fill=NAVY, width=1)
        d.arc([x - r // 3, cy - r, x + r // 3, cy + r], 270, 90,
              fill=NAVY, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=NAVY, width=1)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 22  # margin

    f_title = font(SERIF, 58)
    f_date = font(SANS_B, 15)
    f_lead = font(SERIF, 27)
    f_body = font(SANS, 13)
    f_sec = font(SANS_B, 14)
    f_head = font(SANS_B, 13)
    f_sum = font(SANS, 11)
    f_small = font(SANS, 11)
    f_foot = font(SANS, 10)

    # ---- masthead
    d.text((W // 2, 30), "THE WORLD TODAY", font=f_title, fill=INK,
           anchor="ma")
    d.rectangle([mx, 96, W - mx, 99], fill=INK)
    d.rectangle([mx, 102, W - mx, 105], fill=RED)
    d.text((W // 2, 112), "THURSDAY 26 NOVEMBER 2026  \u00b7  ONE DAY'S WORLD NEWS",
           font=f_date, fill=INK, anchor="ma")

    # ---- lead story
    ly0, ly1 = 140, 252
    d.rectangle([mx, ly0, W - mx, ly1], outline=RULE, width=2)
    d.rectangle([mx, ly0, W - mx, ly0 + 4], fill=RED)
    draw_globe(d, mx + 46, ly0 + 56, 30)
    d.text((mx + 92, ly0 + 12), LEAD_HEAD, font=f_lead, fill=INK)
    y = ly0 + 52
    for line in LEAD_LINES:
        d.text((mx + 92, y), "\u2022  " + line, font=f_body, fill=INK)
        y += 19
    d.text((W - mx - 8, ly1 - 18), "UKRAINE \u00b7 WASHINGTON \u00b7 KYIV",
           font=f_small, fill=GREY, anchor="ra")

    # ---- six sections in a 2 x 3 grid
    gx0, gy0 = mx, 264
    col_w = (W - 2 * mx - 12) // 2
    row_h = 216
    for i, (name, stories) in enumerate(SECTIONS):
        x0 = gx0 + (i % 2) * (col_w + 12)
        y0 = gy0 + (i // 2) * (row_h + 10)
        d.rectangle([x0, y0, x0 + col_w, y0 + row_h], outline=RULE, width=1)
        d.rectangle([x0, y0, x0 + col_w, y0 + 26], fill=NAVY)
        d.text((x0 + 10, y0 + 5), name, font=f_sec, fill=(255, 255, 255))
        sy = y0 + 34
        for head, summ in stories:
            d.text((x0 + 10, sy), fit_one(d, head, f_head, col_w - 20),
                   font=f_head, fill=INK)
            sy += 15
            for ln in wrap(d, summ, f_sum, col_w - 20)[:1]:
                d.text((x0 + 10, sy), ln, font=f_sum, fill=(52, 50, 46))
                sy += 13
            sy += 1

    # ---- also today strip
    ay0 = 264 + 3 * row_h + 2 * 10 + 12
    d.rectangle([mx, ay0, W - mx, ay0 + 2], fill=INK)
    d.text((mx, ay0 + 8), "ALSO TODAY", font=f_sec, fill=RED)
    y = ay0 + 28
    half = (len(ALSO) + 1) // 2
    for col, items in enumerate((ALSO[:half], ALSO[half:])):
        x = mx if col == 0 else W // 2 + 6
        yy = y
        for it in items:
            d.text((x, yy), fit_one(d, "\u2022  " + it, f_small, W // 2 - 30),
                   font=f_small, fill=INK)
            yy += 14
    fy = ay0 + 28 + 2 * 14 + 6
    d.rectangle([mx, fy, W - mx, fy + 1], fill=RULE)
    d.text((mx, fy + 5),
           "Wires: Reuters \u00b7 AP \u00b7 Xinhua \u00b7 Conference Board \u00b7 ESA \u00b7 FIDE. "
           "All artwork drawn in code; no photographs.",
           font=f_foot, fill=GREY)
    d.text((W - mx, fy + 7), "make.fun \u00b7 news-image-20261126",
           font=f_foot, fill=GREY, anchor="ra")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
