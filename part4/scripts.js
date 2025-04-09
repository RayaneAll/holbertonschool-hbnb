document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();

  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', () => {
      filterPlacesByPrice();
    });
  }
});

// --- Auth ---
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
  } else {
    if (loginLink) loginLink.style.display = 'none';
    fetchPlaces(token);  // ✅ Appel uniquement si connecté
  }
}

// --- Fetch + display places ---
let allPlaces = [];

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      allPlaces = data;
      displayPlaces(data);
    } else {
      console.error('Failed to fetch places:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;

  placesList.innerHTML = ''; // Clear existing content

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price_per_night);

    card.innerHTML = `
      <h2>${place.name}</h2>
      <p>Price per night: $${place.price_per_night}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(card);
  });
}

// --- Filter ---
function filterPlacesByPrice() {
  const selected = document.getElementById('price-filter').value;
  const maxPrice = selected === 'all' ? Infinity : parseInt(selected, 10);

  document.querySelectorAll('.place-card').forEach(card => {
    const price = parseFloat(card.getAttribute('data-price'));
    card.style.display = price <= maxPrice ? 'block' : 'none';
  });
}
