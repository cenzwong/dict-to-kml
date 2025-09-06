# make_kml.py
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

# 拍攝點（可自行增刪或改名次序）
WAYPOINTS = [
    {"code": "A", "name": "Shakespeare & Company 書店",
     "addr": "37 Rue de la Bûcherie, 75005 Paris", "lat": 48.852524, "lon": 2.347130},
    {"code": "B", "name": "Rue Saint-Julien-le-Pauvre（小街）",
     "addr": "Rue Saint-Julien-le-Pauvre, 75005 Paris", "lat": 48.852500, "lon": 2.347222},
    {"code": "C", "name": "Rue Galande（拉丁區小街）",
     "addr": "57 Rue Galande, 75005 Paris", "lat": 48.851634, "lon": 2.346867},
    {"code": "D1", "name": "Rue des Jardins-Saint-Paul（聖保羅花園街）",
     "addr": "Rue des Jardins-Saint-Paul, 75004 Paris", "lat": 48.853480, "lon": 2.360670},
    {"code": "D2", "name": "Rue Charlemagne（查理曼街）",
     "addr": "16 Rue Charlemagne, 75004 Paris", "lat": 48.854404, "lon": 2.360027},
    {"code": "D3", "name": "Rue Éginhard（艾金納爾街）",
     "addr": "Rue Éginhard, 75004 Paris", "lat": 48.854000, "lon": 2.361810},
    {"code": "E", "name": "Le Pure Café（《Before Sunset》咖啡場景）",
     "addr": "14 Rue Jean-Macé, 75011 Paris", "lat": 48.853056, "lon": 2.383333},
    {"code": "F", "name": "Coulée Verte René-Dumont 高架花園（Daumesnil 入口）",
     "addr": "Viaduc des Arts / Av. Daumesnil, 75012 Paris（近Rue de Lyon口）",
     "lat": 48.849414, "lon": 2.371423},
    {"code": "G", "name": "Quai de la Tournelle（塞納河畔上船位）",
     "addr": "21 Quai de la Tournelle, 75005 Paris", "lat": 48.850005, "lon": 2.354430},
    {"code": "H", "name": "Quai Henri IV（下船位／或步行到此）",
     "addr": "10 Quai Henri IV, 75004 Paris", "lat": 48.847818, "lon": 2.364474},
    {"code": "I", "name": "Cour de l’Étoile-d’Or（Céline 的庭院，門口遠望）",
     "addr": "75 Rue du Faubourg Saint-Antoine, 75011 Paris", "lat": 48.852080, "lon": 2.374560},
]

def build_kml(waypoints, title="Before Sunset – Paris Walk"):
    # KML 根節點
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(kml, "Document")
    ET.SubElement(doc, "name").text = title

    # 簡單樣式（可選）
    style_line = ET.SubElement(doc, "Style", id="routeLine")
    ls = ET.SubElement(style_line, "LineStyle")
    ET.SubElement(ls, "color").text = "ff0000ff"  # aabbggrr（紅色線，反向透明度）
    ET.SubElement(ls, "width").text = "3"

    # 每個地標（Placemark）
    for w in waypoints:
        pm = ET.SubElement(doc, "Placemark")
        ET.SubElement(pm, "name").text = f"{w['code']} – {w['name']}"
        ET.SubElement(pm, "description").text = w["addr"]
        pt = ET.SubElement(pm, "Point")
        ET.SubElement(pt, "coordinates").text = f"{w['lon']},{w['lat']},0"

    # 連線路徑（LineString）— 依照清單順序連起來
    line_pm = ET.SubElement(doc, "Placemark")
    ET.SubElement(line_pm, "name").text = "Walking Route (straight-line)"
    ET.SubElement(line_pm, "styleUrl").text = "#routeLine"
    line = ET.SubElement(line_pm, "LineString")
    ET.SubElement(line, "tessellate").text = "1"
    coords = " ".join(f"{w['lon']},{w['lat']},0" for w in waypoints)
    ET.SubElement(line, "coordinates").text = coords

    return ET.ElementTree(kml)

if __name__ == "__main__":
    out_file = "before_sunset_route.kml"
    tree = build_kml(WAYPOINTS, title="Before Sunset – Paris Walk")
    tree.write(out_file, encoding="utf-8", xml_declaration=True)
    print(f"KML written to: {out_file}")
