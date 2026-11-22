// Create the map inside <div id="map">, centered at [0° lat, 0° lon] with zoom level 2
const map = L.map("map", {
  worldCopyJump: true, // Smoothly wraps markers when panning across the antimeridian
}).setView([15, 0], 2);

// Add dark-mode map tiles from CartoDB (free for prototyping, no API key required)
L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
  attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
  subdomains: "abcd",
  maxZoom: 18,
}).addTo(map);