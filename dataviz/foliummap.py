import folium
import os
from folium.plugins import MarkerCluster

def create_map(groups):
    # create map (t_list = ["Stamen Terrain", "Stamen Toner", "Mapbox Bright"])
    map = folium.Map(location=[50, 5],
                           zoom_start=3,
                           tiles='Stamen Terrain')
    folium.TileLayer('cartodbpositron').add_to(map)
    folium.TileLayer('openstreetmap').add_to(map)
    folium.TileLayer('Stamen Terrain').add_to(map)

    marker_cluster = MarkerCluster().add_to(map)

    group_sub_group = {}
    for group in groups :
        subgroup = folium.plugins.FeatureGroupSubGroup(marker_cluster, group)
        map.add_child(subgroup)
        group_sub_group[group] = subgroup

    folium.LayerControl(collapsed=True).add_to(map)

    return map, group_sub_group

def plot_markers(group, location, popup):
    folium.Marker(location, popup=popup).add_to(group)

def save_map (map,outputfile, filename):
    if not os.path.exists(outputfile):
        os.makedirs(outputfile)
    map.save(outputfile+"/"+filename)




