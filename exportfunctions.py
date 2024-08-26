import csv
import gpxpy
import gpxpy.gpx


############################################################################################################

                                          # Export The Route In Different Formats #
############################################################################################################


def create_csv_for_mymaps(nodes, filename='route.csv'):
    # Define the header for the CSV file
    header = ['ID', 'Data', 'Latitude', 'Longitude']

    # Open the file in write mode
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(header)

        # Write the data rows
        for node in nodes:
            writer.writerow([node.id, node.data, node.latitude, node.longitude])

    print(f"CSV file '{filename}' created successfully.")


def create_gpx_from_nodes(nodes, filename='route.gpx'):
    # Create GPX object
    gpx = gpxpy.gpx.GPX()

    # Create a GPX track
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create a GPX track segment
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Add nodes to the GPX track segment as GPX points
    for node in nodes:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(node.latitude, node.longitude))

    # Write the GPX file
    with open(filename, 'w') as f:
        f.write(gpx.to_xml())

    print(f"GPX file '{filename}' created successfully.")


def export_route_format(formats, path):

    if formats is None:
        print("You haven't specified formats to export")
        return

    for format in formats:
        if format == "csv":
            create_csv_for_mymaps(path)

        elif format == "gpx":
            create_gpx_from_nodes(path)

        else:
            print(f"Unknown format '{format}'")


############################################################################################################


############################################################################################################