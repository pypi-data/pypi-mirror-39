import vaex.serialize
import json
import numpy as np
# @vaex.serialize.register
# class Function(FunctionSerializable):

def add_geo_json(ds, json_or_file, column_name, longitude_expression, latitude_expresion, label=None, persist=True, overwrite=False, inplace=False, mapping=None):
    ds = ds if inplace else ds.copy()
    if not isinstance(json_or_file, (list, tuple)):
        with open(json_or_file) as f:
            geo_json = json.load(f)
    else:
        geo_json = json_or_file
    def default_label(properties):
        return " - ".join(properties.values())
    label = label or default_label
    features = geo_json['features']
    list_of_polygons = []
    labels = []
    if mapping:
        mapping_dict = {}
    for i, feature in enumerate(features[:]):
        geo = feature['geometry']
        properties = feature['properties']
        if mapping:
            mapping_dict[properties[mapping]] = i
    #     print(properties)
        # label = f"{properties['borough']} - {properties['zone']}'"
        labels.append(label(properties))#roperties[label_key])
        list_of_polygons.append([np.array(polygon_set[0]).T for polygon_set in geo['coordinates']])
        M = np.sum([polygon_set.shape[1] for polygon_set in list_of_polygons[-1]])
        # print(M)
        # N += M
    ds[column_name] = ds.func.inside_which_polygons(longitude_expression, latitude_expresion, list_of_polygons)
    if persist:
        ds.persist(column_name, overwrite=overwrite)
    ds.categorize(column_name, labels=labels, check=False)
    if mapping:
        return ds, mapping_dict
    else:
        return ds
