import os
import json
from src.storage_handler import create_directory, directory_exists

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")


def iterate_over_dirs():
    count = 0
    for subdir, dirs, files in os.walk(DATA_DIR):
        if not subdir.endswith('data') and not subdir.endswith('geojsons') and not directory_exists(subdir, 'geojsons'):
            create_directory(subdir, 'geojsons')

        print('dir: %s\n' % subdir)

        for file in files:
            if not file.endswith('_.json') and file.endswith('.json'):
                with open(os.path.join(subdir, file)) as json_file:
                    json_data = json.load(json_file)

                    print('loaded json: %s' % file)

                    if 'geometry' in json_data:
                        geojson = json_data['geometry']
                        file_extension_index = file.index('.json')
                        geojson_file_name = file[:file_extension_index] + '_geo' + file[file_extension_index:]
                        geojsons_dir = os.path.join(subdir, 'geojsons')

                        print('geometry extracted: %s\n' % geojson_file_name)
                        count = count + 1

                        with open(os.path.join(geojsons_dir, geojson_file_name), 'w') as out_geojson:
                            json.dump(geojson, out_geojson)

    print('how many geojsons: %i' % count)

