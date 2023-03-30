// Initialize the Google Maps API and get the map element
let map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 9.0152, lng: 38.7636},
        zoom: 12
    });
    
    // Add a click event listener to the map
    map.addListener('click', function(event) {
        // Get the latitude and longitude of the clicked location
        const lat = event.latLng.lat();
        const lng = event.latLng.lng();
        
        // Use reverse geocoding to get the address of the clicked location
        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({
            'location': {lat: lat, lng: lng}
        }, function(results, status) {
            if (status === 'OK') {
                // Update the value of the input fields in the HTML form
                const address = results[0].formatted_address;
                document.querySelector("#pickup-location").value = address;
                document.querySelector("#dropoff-location").value = address;
                
                // Calculate the fare and distance
                calculateFareAndDistance();
            } else {
                alert('Geocoder failed due to: ' + status);
            }
        });
    });
}

// Wait for the document to be ready
$(document).ready(function() {
    // Initialize the Google Maps API
    initMap();

    // Get the ride booking form and attach an event listener to it
    const form = document.getElementById('ride-booking-form');
    form.addEventListener('submit', function(event) {
        // Prevent the form from submitting normally
        event.preventDefault();

        // Get the form data and create a FormData object
        const formData = new FormData(form);

        // Send an AJAX request to the server with the ride booking details
        $.ajax({
            type: 'POST',
            url: '/book_ride',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Handle the response from the server
                // ...
            }
        });
    });
});

function calculateFareAndDistance() {
  const directionsService = new google.maps.DirectionsService();
  const pickup = document.querySelector("#pickup-location").value;
  const dropoff = document.querySelector("#dropoff-location").value;
  const rideType = document.querySelector("#ride-type").value;

  directionsService.route(
    {
      origin: pickup,
      destination: dropoff,
      travelMode: google.maps.TravelMode.DRIVING,
    },
    (result, status) => {
      if (status == "OK") {
        const distance = result.routes[0].legs[0].distance.value / 1000;
        const fare = calculateFare(distance, rideType);
        document.querySelector("#distance").value = distance.toFixed(2);
        document.querySelector("#fare").value = fare.toFixed(2);
      } else {
        alert("Directions request failed due to " + status);
      }
    }
  );
}

function calculateFare(distance, rideType) {
  const BASE_FARE = 2.5;
  const FARE_PER_KM = {
    regular: 0.5,
    premium: 1,
    luxury: 2,
  };
  const farePerKm = FARE_PER_KM[rideType] || 0;
  const fare = BASE_FARE + farePerKm * distance;
  return fare;
}
document.querySelector("#pickup-location").onchange = calculateFareAndDistance;
document.querySelector("#dropoff-location").onchange = calculateFareAndDistance;
document.querySelector("#ride-type").onchange = calculateFareAndDistance;

$(document).ready(function () {
    $("#book-btn").click(function () {
        const pickupLocation = $("#pickup-location").val();
        const dropoffLocation = $("#dropoff-location").val();
        const rideType = $("#ride-type").val();
        const distance = $("#distance").val();
        const fare = $("#fare").val();

        // Display a confirmation message with the details of the ride
        const message = `You have booked a ${rideType} ride from ${pickupLocation} to ${dropoffLocation}. The distance is ${distance} km and the estimated fare is ${fare} ETB. Thank you for choosing RideShare!`;
        alert(message);
    });
});

