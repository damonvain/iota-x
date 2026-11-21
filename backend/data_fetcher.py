from pathlib import Path

from skyfield.api import Loader, wgs84

# celestrak gp endpoint URL for Starlink TLE data
Starlink_TLE_URL = (
    "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
)

# Store downloaded data so we dont spam celestrak on every run
DATA_DIR = Path(__file__).parent / "data"
loader = Loader(str(DATA_DIR))


def load_starlink_satellites(max_age_days: float = 1.0):
    """Download (or load cached) Starlink TLE data and return EarthSatellite objects"""
    tle_filename = "starlink_tle.txt"

    # Re-dolwnload TLE data only if the local file doesnt exist or is older than max_age_days
    should_reload = (
        not loader.exists(tle_filename) or loader.days_old(tle_filename) >= max_age_days
    )

    satellites = loader.tle_file(
        Starlink_TLE_URL, filename=tle_filename, reload=should_reload
    )
    return satellites


def get_live_positions(satellites, limit: int = 5):
    """Calculate current latitude, longitude, and altitude (km) for satellites."""
    # Skyfield requires its ownm astronomical timescale object to track utc/leap seconds
    ts = loader.timescale()
    now = ts.now()

    results = []
    for sat in satellites[:limit]:
        # propagate the satellite's position to the current instant
        geocentric = sat.at(now)
        subpoint = wgs84.subpoint(geocentric)
        results.append(
            {
                "name": sat.name,
                "norad_id": sat.model.satnum,
                "latitude": round(subpoint.latitude.degrees, 4),
                "longitude": round(subpoint.longitude.degrees, 4),
                "altitude_km": round(subpoint.elevation.km, 2),
            }
        )
    return results


if __name__ == "__main__":
    sats = load_starlink_satellites()
    print(f"loaded {len(sats)} Starlink satellites.\n")

    for pos in get_live_positions(sats, limit=5):
        print(
            f"{pos['name']} (NORAD ID: {pos['norad_id']}) "
            f"Lat: {pos['latitude']}, Lon: {pos['longitude']}, Alt: {pos['altitude_km']} km"
        )
