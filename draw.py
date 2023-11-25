import folium
from xyzservices import TileProvider

tileprovider = TileProvider(
    name="Esri Worldimagery",
    url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attribution="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, "
                "IGP, UPR-EGP, and the GIS User Community", )


def draw(shapelist, schnittflaeche):
    my_map = folium.Map(location=shapelist[0].shape[0], zoom_start=10, tiles=None)
    folium.TileLayer("OpenStreetMap").add_to(my_map)
    folium.TileLayer(tileprovider, show=False, name="Esri Worldimagery").add_to(my_map)
    folium.LayerControl().add_to(my_map)
    for y in shapelist:
        locations = y.shape
        folium.Polygon(
            locations=locations,
            fill_opacity=0.15,
            fill=True,
        ).add_to(my_map)
    folium.Polygon(
        locations=schnittflaeche,
        color="#ff0000",
        fill_opacity=0.15,
        fill=True,
    ).add_to(my_map)
    my_map.show_in_browser()
    save = input("Do you want to save your Result? (y)es/(n)o: ")
    if "y" in save.lower():
        my_map.save("result.html")
