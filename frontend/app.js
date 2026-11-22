// 1. Initialize the map
const map = L.map("map", {
  worldCopyJump: true,
}).setView([15, 0], 2);

L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}",
  {
    attribution: "Tiles &copy; Esri",
    maxZoom: 16,
  }
).addTo(map);

// 2. Configuration & state
const API_URL = "http://127.0.0.1:8000/api/satellites?limit=200";
const satelliteMarkers = {}; // Stores existing markers by norad_id so we can move them

// 3. Fetch latest coordinates and create/move dots
async function updateSatellites() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    data.satellites.forEach((sat) => {
      const coords = [sat.latitude, sat.longitude];
      const popupText = `
        <strong>${sat.name}</strong><br>
        NORAD ID: ${sat.norad_id}<br>
        Altitude: ${sat.altitude_km} km
      `;

      if (satelliteMarkers[sat.norad_id]) {
        // Satellite already exists on the map -> smoothly move it to its new position
        satelliteMarkers[sat.norad_id].setLatLng(coords);
        satelliteMarkers[sat.norad_id].setPopupContent(popupText);
      } else {
        // First time seeing this satellite -> create a lightweight glowing dot
        const marker = L.circleMarker(coords, {
          radius: 4,
          color: "#38bdf8",
          fillColor: "#38bdf8",
          fillOpacity: 0.85,
          weight: 1,
        })
          .bindPopup(popupText)
          .addTo(map);

        satelliteMarkers[sat.norad_id] = marker;
      }
    });
  } catch (error) {
    console.error("Failed to fetch satellite positions:", error);
  }
}

// 4. Run immediately on page load, then refresh every 2 seconds (2000 ms)
updateSatellites();
setInterval(updateSatellites, 2000);