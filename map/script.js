let map, marker, tempChart;

function initMap() {
  const bangladeshBounds = {
    north: 26.631,
    south: 20.59,
    west: 88.01,
    east: 92.67,
  };

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 23.685, lng: 90.3563 },
    zoom: 7,
    restriction: {
      latLngBounds: bangladeshBounds,
      strictBounds: true,
    },
  });

  const input = document.getElementById("search-box");
  const searchBox = new google.maps.places.SearchBox(input, {
    componentRestrictions: { country: "bd" },
  });

  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });

  map.addListener("click", (e) => {
    const lat = e.latLng.lat();
    const lon = e.latLng.lng();
    setMarker(e.latLng);
    fetchWeather(lat, lon);
  });

  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();
    if (!places.length) return;

    const place = places[0];
    if (!place.geometry || !place.geometry.location) return;

    const latLng = place.geometry.location;
    map.panTo(latLng);
    map.setZoom(10);
    setMarker(latLng, true);
    fetchWeather(latLng.lat(), latLng.lng());
  });
}

function setMarker(position, isSearch = false) {
  if (marker) marker.setMap(null);
  marker = new google.maps.Marker({
    position,
    map,
    icon: isSearch
      ? "https://maps.google.com/mapfiles/ms/icons/green-dot.png"
      : undefined,
  });
}

function fetchWeather(lat, lon) {
  const apiKey = "8dfc22e08ceb9d73ca772504247edf9b";
  const currentURL = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`;
  const forecastURL = `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`;

  fetch(currentURL)
    .then(res => res.json())
    .then(current => {
      document.getElementById("city-name").textContent = current.name || "Unknown";
      document.getElementById("temperature").textContent = `${Math.round(current.main.temp)}°C`;
      document.getElementById("description").textContent = current.weather[0].description;
      document.getElementById("humidity").textContent = `${current.main.humidity}%`;
      document.getElementById("wind").textContent = `${(current.wind.speed * 3.6).toFixed(1)} km/h`;
      document.getElementById("weather-icon").src = `https://openweathermap.org/img/wn/${current.weather[0].icon}@2x.png`;
      document.getElementById("date-time").textContent = new Date().toLocaleString();
    });

  fetch(forecastURL)
    .then(res => res.json())
    .then(data => {
      const forecastBox = document.getElementById("forecast");
      forecastBox.innerHTML = "";
      const daily = {};
      data.list.forEach(item => {
        const date = item.dt_txt.split(" ")[0];
        if (!daily[date] && item.dt_txt.includes("12:00:00")) {
          daily[date] = item;
        }
      });

      const labels = [], temps = [];
      let count = 0;
      for (let date in daily) {
        if (count >= 5) break;
        const item = daily[date];
        const day = new Date(date).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
        forecastBox.innerHTML += `
          <div class="forecast-day">
            <div>${day}</div>
            <img src="https://openweathermap.org/img/wn/${item.weather[0].icon}@2x.png" />
            <div>${Math.round(item.main.temp)}°C</div>
            <div>💧${item.main.humidity}%</div>
          </div>
        `;
        labels.push(day);
        temps.push(item.main.temp);
        count++;
      }

      if (tempChart) tempChart.destroy();
      const ctx = document.getElementById("tempChart").getContext("2d");
      tempChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [{
            label: "Temperature (°C)",
            data: temps,
            borderColor: "blue",
            backgroundColor: "rgba(0, 123, 255, 0.1)",
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: false }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    });
}
/*function signUp() {
  const username = document.getElementById("username").value;
  const defaultLocation = document.getElementById("default-location").value;

  // Use Places API to convert text to lat/lng
  const geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: defaultLocation }, (results, status) => {
    if (status === "OK") {
      const location = results[0].geometry.location;
      const lat = location.lat();
      const lng = location.lng();

      // Simulated user save (replace with backend save)
      localStorage.setItem("user", JSON.stringify({ username, lat, lng }));

      alert("User signed up! Reloading map...");
      location.reload();
    } else {
      alert("Could not find location. Please enter a valid place.");
    }
  });
}

window.addEventListener("load", () => {
  const user = JSON.parse(localStorage.getItem("user"));
  if (user) {
    highlightDefaultLocation(user.lat, user.lng);
  }
});

function highlightDefaultLocation(lat, lng) {
  const position = { lat, lng };
  map.setCenter(position);
  map.setZoom(10);
  if (marker) marker.setMap(null);
  marker = new google.maps.Marker({
    position,
    map,
    icon: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
  });
  fetchWeather(lat, lng);
}*/
