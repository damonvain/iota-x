from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from data_fetcher import load_starlink_satellites, get_live_positions

app = FastAPI(title="Starlink Live Tacker API")

# Allow the frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

satellites = load_starlink_satellites()


@app.get("/api/satellites")
def read_satellites(limit: int = Query(default=100, ge=1, le=2000)):
    """Return live latitude, longitude, and altitude for active Starlink satellites."""
    positions = get_live_positions(satellites, limit=limit)
    return {"count": len(positions), "satellites": positions}
