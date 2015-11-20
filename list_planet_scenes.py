import requests
import argparse


def list_scenes(key, input_geojson=None, all=False, count=False):
    params = {}
    if input_geojson:
        with open(input_geojson) as f:
            geojson_data = f.read()
        params["intersects"] = geojson_data

    url = "https://api.planet.com/v0/scenes/ortho/"

    if count:
        # Just show the count and quit
        data = requests.get(url, params=params, auth=(key, '')).json()
        print data['count']
        return
    if all:
        for i in range(10000):
            print url
            data = requests.get(url, params=params, auth=(key, '')).json()
            for image in data['features']:
                image_url = \
                    image['properties']['data']['products']['visual']['full']
                print image_url
            url = data['links']['next']
            params = {}
    else:
        data = requests.get(url, params=params, auth=(key, '')).json()
        for image in data['features']:
            image_url = \
                image['properties']['data']['products']['visual']['full']
            print image_url


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser("Lists planet scenes")
    arg_parser.add_argument(
        '--geojson',
        default=None,
        help='Geojson description of a polygon that limits our search')
    arg_parser.add_argument(
        '--key',
        required=True,
        help='API key to use with the Planet API')
    arg_parser.add_argument(
        '--all', '-a',
        help='list all scenes instead of just the first 50',
        action="store_true")
    arg_parser.add_argument(
        '--count', '-c',
        help='Just show the count instead of listing the scenes',
        action="store_true")
    args = arg_parser.parse_args()
    list_scenes(
        args.key, input_geojson=args.geojson, all=args.all, count=args.count)
