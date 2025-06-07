import re
import folium


def dms_to_decimal(deg, min_, sec, direction):
    d = float(deg)
    m = float(min_)
    s = float(sec)
    decimal = d + m / 60 + s / 3600
    return -decimal if direction in ['S', 'W'] else decimal


def extract_coordinates_from_text(text):
    lines = text.split('\n')
    lat_pattern = re.compile(r"GPS Latitude.*?:\s*(\d+)\s*deg\s*(\d+)'\s*(\d+(?:\.\d+)?)\"?\s*([NS])", re.IGNORECASE)
    lon_pattern = re.compile(r"GPS Longitude.*?:\s*(\d+)\s*deg\s*(\d+)'\s*(\d+(?:\.\d+)?)\"?\s*([EW])", re.IGNORECASE)

    coords = []
    lat = None

    for i in range(len(lines)):
        lat_match = lat_pattern.search(lines[i])
        if lat_match:
            lat = dms_to_decimal(*lat_match.groups())

        lon_match = lon_pattern.search(lines[i])
        if lon_match and lat is not None:
            lon = dms_to_decimal(*lon_match.groups())
            coords.append((lat, lon))
            lat = None

    print(f"Matched {len(coords)} coordinate pairs.")
    return coords


def create_map_with_path(coords, output_file='gps_path_map.html'):
    if not coords:
        raise ValueError("No coordinates to plot.")

    start_location = coords[0]
    m = folium.Map(location=start_location, zoom_start=16)
    folium.PolyLine(coords, color='blue', weight=3).add_to(m)
    folium.Marker(start_location, tooltip="Start").add_to(m)
    folium.Marker(coords[-1], tooltip="End").add_to(m)
    m.save(output_file)


if __name__ == '__main__':
    with open('gps_data.txt', 'r') as f:
        gps_text = f.read()

    coordinates = extract_coordinates_from_text(gps_text)
    create_map_with_path(coordinates)
    print(f"Map generated with {len(coordinates)} points. Open 'gps_path_map.html' to view it.")
