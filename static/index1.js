async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const myLatlng = { lat: 41.308750, lng: -72.931877 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 16,
    center: myLatlng,
  });

  // Create the initial InfoWindow.
  let infoWindow = new google.maps.InfoWindow({
    content: "Click location of blockage",
    position: myLatlng,
  });

  infoWindow.open(map);

  // Configure the click listener.
  map.addListener("click", (mapsMouseEvent) => {
    var rep_lat = document.getElementById("rLatitude");
    var rep_long = document.getElementById("rLongitude");
    // Close the current InfoWindow.
    infoWindow.close();
    // Create a new InfoWindow.
    infoWindow = new google.maps.InfoWindow({
      position: mapsMouseEvent.latLng,
    });
    infoWindow.setContent("Blockage located here.");
    infoWindow.open(map);

    // Set the reported lat and long equal to most recent click
    rep_lat.value = mapsMouseEvent.latLng.lat();
    rep_long.value = mapsMouseEvent.latLng.lng();
  });
}

function GeoClick() {
  var startTime = performance.now(); // Start timestamp
  var Lat = document.getElementById("latitude");
  var Long = document.getElementById("longitude");
  var submit = document.getElementById("submitButton")
  var label = document.getElementById("locationDisplay");

  label.innerHTML = "Retrieving Location...";

  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(processPosition, processError);
    } else {
      label.innerHTML = "Geolocation is not supported by this browser.";
    }
  }

  function processPosition(position) {
    var endTime = performance.now(); // End timestamp
    console.log('Time taken:', endTime - startTime, 'milliseconds');
    label.innerHTML = "";
    showCheckmark();
    submit.classList.remove('disabled');
    Lat.value = position.coords.latitude;
    Long.value = position.coords.longitude;
  }

  function processError(error) {
    switch(error.code) {
      case error.PERMISSION_DENIED:
        label.innerHTML = "Error: User denied the request for Geolocation."
        break;
      case error.POSITION_UNAVAILABLE:
        label.innerHTML = "Error: Location information is unavailable."
        break;
      case error.TIMEOUT:
        label.innerHTML = "Error: The request to get user location timed out."
        break;
      case error.UNKNOWN_ERROR:
        label.innerHTML = "Error: An unknown error occurred."
        break;
    }
  }
  getLocation();
}

function showCheckmark() {
  var checkmark = document.getElementById("checkmark");
  checkmark.style.display = "inline";
}

// Load everything
initMap();

// Listen for user submitting button
document.addEventListener("DOMContentLoaded", () => {
  var GeoButton = document.getElementById("GeoButton");
  GeoButton.addEventListener("click", GeoClick);
})
