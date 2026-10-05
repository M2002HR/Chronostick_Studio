#!/usr/bin/env python3
"""Create deterministic ChronoStick map and clock anchors for Episode 006."""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episodes/006-shortest-war-ever"
OUT = ROOT / "assets/episodes/006-shortest-war-ever/references"
GEO = EP / "source/map-geometry-natural-earth-10m.geojson"
W, H = 1600, 900
INK = (35, 40, 38)
PAPER = (238, 225, 193)
LAND = (211, 190, 151)
SEA = (106, 153, 160)
ACCENT = (177, 85, 59)


def canvas():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, H), fill=SEA)
    for y in range(45, H, 65):
        for x in range(30 + (y % 3) * 11, W, 90):
            d.arc((x, y, x + 28, y + 10), 195, 340, fill=(146, 181, 179), width=2)
    return im, d


def coords(extent, lon, lat):
    lo, hi, bottom, top = extent
    return ((lon - lo) / (hi - lo) * W, (top - lat) / (top - bottom) * H)


def coast(d, extent):
    data = json.loads(GEO.read_text())
    for feature in data["features"]:
        g = feature["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring = poly[0]
            if len(ring) < 3:
                continue
            if not any(extent[0] - 2 < p[0] < extent[1] + 2 and extent[2] - 2 < p[1] < extent[3] + 2 for p in ring):
                continue
            pts = [coords(extent, a, b) for a, b in ring]
            d.polygon(pts, fill=LAND)
            d.line(pts + [pts[0]], fill=INK, width=5, joint="curve")


def border(d):
    d.rectangle((14, 14, W - 15, H - 15), outline=INK, width=8)
    d.rectangle((25, 25, W - 26, H - 26), outline=(235, 218, 183), width=3)
    d.ellipse((W - 114, 52, W - 58, 108), outline=INK, width=4)
    d.line((W - 86, 61, W - 86, 96), fill=INK, width=4)
    d.polygon([(W - 86, 47), (W - 93, 64), (W - 79, 64)], fill=INK)


def dot(d, pos, color=ACCENT, radius=18):
    x, y = pos
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color, outline=INK, width=5)


def stick(d, x, y, robe=(110, 71, 65), turban=True, scale=1):
    s = scale
    d.ellipse((x - 15*s, y - 50*s, x + 15*s, y - 20*s), fill=(245, 232, 205), outline=INK, width=max(2, int(3*s)))
    if turban:
        d.arc((x - 18*s, y - 56*s, x + 18*s, y - 28*s), 190, 350, fill=INK, width=max(3, int(5*s)))
    d.line((x, y - 20*s, x, y + 22*s), fill=INK, width=max(4, int(7*s)))
    d.polygon([(x - 12*s, y - 18*s), (x + 12*s, y - 18*s), (x + 15*s, y + 20*s), (x - 15*s, y + 20*s)], fill=robe, outline=INK)
    d.line((x - 10*s, y - 7*s, x - 24*s, y + 12*s), fill=INK, width=max(3, int(4*s)))
    d.line((x + 10*s, y - 7*s, x + 24*s, y + 12*s), fill=INK, width=max(3, int(4*s)))
    d.line((x - 5*s, y + 20*s, x - 12*s, y + 38*s), fill=INK, width=max(3, int(4*s)))
    d.line((x + 5*s, y + 20*s, x + 12*s, y + 38*s), fill=INK, width=max(3, int(4*s)))


def ship(d, x, y, size=1, sunk=False):
    s = size
    hull = [(x - 45*s, y), (x + 45*s, y), (x + 30*s, y + 15*s), (x - 30*s, y + 15*s)]
    d.polygon(hull, fill=INK if not sunk else (77, 89, 85), outline=PAPER)
    d.rectangle((x - 16*s, y - 15*s, x + 12*s, y), fill=(228, 214, 186), outline=INK, width=2)
    d.line((x - 30*s, y - 5*s, x - 50*s, y - 5*s), fill=INK, width=4)


def arrow(d, a, b, fill=ACCENT, width=7):
    d.line((a, b), fill=fill, width=width)
    theta = math.atan2(b[1] - a[1], b[0] - a[0])
    p = [(b[0], b[1]), (b[0] - 24*math.cos(theta-.42), b[1] - 24*math.sin(theta-.42)), (b[0] - 24*math.cos(theta+.42), b[1] - 24*math.sin(theta+.42))]
    d.polygon(p, fill=fill)


def save(im, name):
    revision=1
    path = OUT / f"{name}-r{revision:03d}.png"
    while path.exists():
        revision+=1
        path=OUT / f"{name}-r{revision:03d}.png"
    im.save(path)
    print(path.relative_to(ROOT))


def regional(name, extent, focus=None, routes=False, people=False):
    im, d = canvas()
    coast(d, extent)
    if routes:
        p = coords(extent, 39.2, -6.15)
        for end in [(51, -2), (58, 11), (33, -13)]:
            q = coords(extent, *end)
            arrow(d, q, p, fill=(239, 219, 174), width=6)
    if focus:
        p = coords(extent, 39.2, -6.15)
        dot(d, p, radius=21)
        d.arc((p[0]-48,p[1]-48,p[0]+48,p[1]+48), 20, 340, fill=ACCENT, width=7)
        if people:
            stick(d, p[0]+75, p[1]-10, scale=1.3)
    border(d)
    save(im, name)


def harbour(name, mode):
    im, d = canvas()
    # Single invariant schematic: waterfront at right, British fleet west/left, Glasgow centre.
    d.polygon([(1160, 45), (W, 45), (W, H-45), (1165, H-45), (1120, 710), (1180, 510), (1110, 300)], fill=LAND, outline=INK)
    d.rectangle((1215, 315, 1490, 585), fill=(236, 218, 179), outline=INK, width=9)
    for x in range(1240, 1490, 50):
        d.rectangle((x, 365, x+22, 410), fill=(110, 92, 75), outline=INK, width=3)
    for x,y in [(170,190),(370,285),(240,490),(500,645),(690,180)]:
        ship(d,x,y,1.35)
    ship(d,820,500,1.1,sunk=mode=="glasgow-sunk")
    if mode in {"first-fire", "glasgow-sunk"}:
        arrow(d,(530,635),(1190,520))
    if mode=="glasgow-sunk":
        d.arc((748,478,890,610),0,180,fill=INK,width=8)
        for xx in [740,790,850]: d.arc((xx,570,xx+100,610),180,350,fill=(231,226,193),width=5)
    if mode=="refuge":
        stick(d,1300,620,scale=1.3)
        arrow(d,(1370,650),(1510,180),fill=(79,103,77))
    if mode=="surrender":
        d.line((1340,275,1340,160),fill=INK,width=8)
        d.polygon([(1340,160),(1430,180),(1340,205)],fill=(246,245,226),outline=INK)
    border(d)
    save(im,name)


def clock(name,text,hour,minute):
    im=Image.new("RGB",(W,H),PAPER)
    d=ImageDraw.Draw(im)
    for i in range(25, W, 80): d.line((i,0,i,H),fill=(227,211,177),width=2)
    for i in range(25,H,80): d.line((0,i,W,i),fill=(227,211,177),width=2)
    cx,cy,r=520,450,305
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(244,231,203),outline=INK,width=18)
    for n in range(12):
        th=(n/12)*2*math.pi-math.pi/2
        a=(cx+260*math.cos(th),cy+260*math.sin(th));b=(cx+283*math.cos(th),cy+283*math.sin(th))
        d.line((a,b),fill=INK,width=10)
    ht=((hour%12)+minute/60)/12*2*math.pi-math.pi/2
    mt=minute/60*2*math.pi-math.pi/2
    d.line((cx,cy,cx+165*math.cos(ht),cy+165*math.sin(ht)),fill=INK,width=16)
    d.line((cx,cy,cx+235*math.cos(mt),cy+235*math.sin(mt)),fill=ACCENT,width=10)
    d.ellipse((cx-18,cy-18,cx+18,cy+18),fill=INK)
    if text:
        font_size=116
        while True:
            font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",font_size)
            test=d.textbbox((0,0),text,font=font)
            if test[2]-test[0] <= 530 or font_size <= 35:
                break
            font_size-=4
        d.rounded_rectangle((925,295,1515,600),radius=35,fill=(246,235,212),outline=INK,width=10)
        box=d.textbbox((0,0),text,font=font)
        d.text((1220-(box[2]-box[0])/2,450-(box[3]-box[1])/2-box[1]),text,font=font,fill=INK)
    border(d)
    save(im,name)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    regional("map-east-africa",(25,65,-24,18),True,False,False)
    regional("map-trade-routes",(25,65,-24,18),True,True,False)
    regional("map-zanzibar-coast",(36,42,-8,-3.5),True,False,True)
    regional("map-zanzibar-island",(38.5,40.5,-7.5,-5.5),True,False,False)
    for name,mode in [("map-harbour-prebattle","prebattle"),("map-harbour-first-fire","first-fire"),("map-harbour-glasgow-sunk","glasgow-sunk"),("map-harbour-refuge","refuge"),("map-harbour-surrender","surrender")]:
        harbour(name,mode)
    for name,text,h,m in [("clock-0800","08:00",8,0),("clock-0859","08:59",8,59),("clock-0900","09:00",9,0),("clock-0905","09:05",9,5),("clock-0938","09:38",9,38),("clock-38-minutos","38 MINUTOS",9,38)]:
        clock(name,text,h,m)


if __name__=="__main__": main()
