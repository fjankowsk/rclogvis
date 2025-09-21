#
#   2025 Fabian Jankowski
#   GPS related functions.
#

import gpxpy.gpx


def create_gpx_file(df):
    gpx = gpxpy.gpx.GPX()
    gpx.name = ""
    gpx.description = ""

    # track
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # segment
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # track points
    for i in range(len(df.index)):
        gpx_segment.points.append(
            gpxpy.gpx.GPXTrackPoint(
                df["latitude"].iloc[i],
                df["longitude"].iloc[i],
                elevation=df["Alt(m)"].iloc[i],
                time=df["datetime"].iloc[i],
            )
        )

    with open("export.gpx", "w") as fd:
        fd.write(gpx.to_xml())
