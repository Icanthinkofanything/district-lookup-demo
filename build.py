"""Fetch public Census TIGERweb boundaries for Vanderburgh County, IN and write one GeoJSON per layer."""
import json, requests, geopandas as gpd
B = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb"
def q(svc, layer, where="1=1", geom=None):
    p = {"where": where, "outFields": "*", "outSR": 4326, "f": "geojson", "returnGeometry": "true"}
    if geom is not None:
        p.update(geometry=json.dumps(geom), geometryType="esriGeometryEnvelope", inSR=4326, spatialRel="esriSpatialRelIntersects")
    r = requests.get(f"{B}/{svc}/MapServer/{layer}/query", params=p, timeout=120); r.raise_for_status()
    return gpd.GeoDataFrame.from_features(r.json()["features"], crs=4326)
county = q("State_County", 1, "STATE='18' AND COUNTY='163'")
print("county", len(county), county.columns.tolist()[:12])
minx, miny, maxx, maxy = county.total_bounds
env = {"xmin": minx, "ymin": miny, "xmax": maxx, "ymax": maxy}
cpoly = county.geometry.iloc[0]
layers = {
    "congressional": q("Legislative", 4, "STATE='18'", env),
    "state_senate": q("Legislative", 1, "STATE='18'", env),
    "state_house": q("Legislative", 2, "STATE='18'", env),
    "township": q("Places_CouSub_ConCity_SubMCD", 1, "STATE='18' AND COUNTY='163'"),
    "precinct": q("Legislative", 15, "STATE='18' AND COUNTY='163'"),
}
for k, g in layers.items():
    g = g[g.intersects(cpoly.buffer(-0.001))].copy()
    g["geometry"] = g.geometry.intersection(cpoly).simplify(0.0002)
    print(k, len(g), [c for c in g.columns if c not in ("geometry",)][:15])
    g.to_file(f"{k}.geojson", driver="GeoJSON")
county.assign(geometry=county.geometry.simplify(0.0002)).to_file("county.geojson", driver="GeoJSON")
