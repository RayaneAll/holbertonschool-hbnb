// --- Utilitaires globaux ---
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function checkAuthentication(redirectIfUnauthenticated = false) {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    if (redirectIfUnauthenticated) {
      window.location.href = 'index.html';
    }
    if (loginLink) loginLink.style.display = 'block';
  } else {
    if (loginLink) loginLink.style.display = 'none';
  }

  return token;
}

document.addEventListener('DOMContentLoaded', () => {
  const pagePath = window.location.pathname;

  // === Tâche 1 - login.html ===
  const loginForm = document.querySelector('.login-form');
  if (loginForm) {
    const errorMessage = document.createElement('p');
    errorMessage.id = 'login-error';
    errorMessage.style.color = 'red';
    loginForm.appendChild(errorMessage);

    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          const errorText = await response.text();
          errorMessage.textContent = 'Login failed: ' + errorText;
        }
      } catch (error) {
        errorMessage.textContent = 'Network error: ' + error.message;
      }
    });
  }

  // === Tâche 2 - index.html ===
  const placesList = document.getElementById('places-list');
  if (placesList) {
    const token = getCookie('token');
    checkAuthentication(); // affiche ou masque "Login"

    if (token) {
      fetchPlaces(token);
    }

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
      priceFilter.addEventListener('change', () => {
        filterPlacesByPrice();
      });
    }
  }

  // === Tâche 3 - place.html ===
  const placeDetailsSection = document.getElementById('place-details');
  if (placeDetailsSection) {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    checkAuthentication(); // pour gérer login-link

    if (token) {
      if (addReviewSection) addReviewSection.style.display = 'block';
    } else {
      if (addReviewSection) addReviewSection.style.display = 'none';
    }

    fetchPlaceDetails(token, placeId);
  }

  // === Tâche 4 - add_review.html ===
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    const messageBox = document.getElementById('message');
    const token = checkAuthentication(true); // redirige si pas connecté
    const placeId = getPlaceIdFromURL();

    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const username = document.getElementById('username').value;
      const rating = parseInt(document.getElementById('rating').value, 10);
      const comment = document.getElementById('comment').value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            user: username,
            rating: rating,
            comment: comment,
            place_id: placeId
          })
        });

        if (response.ok) {
          messageBox.textContent = 'Review submitted successfully!';
          messageBox.style.color = 'green';
          reviewForm.reset();
        } else {
          const errorText = await response.text();
          messageBox.textContent = 'Failed to submit review: ' + errorText;
          messageBox.style.color = 'red';
        }
      } catch (error) {
        messageBox.textContent = 'Network error: ' + error.message;
        messageBox.style.color = 'red';
      }
    });
  }
});

// === Fonctions spécifiques à l’index ===
let allPlaces = [];

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` }
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

  placesList.innerHTML = '';

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

function filterPlacesByPrice() {
  const selected = document.getElementById('price-filter').value;
  const maxPrice = selected === 'all' ? Infinity : parseInt(selected, 10);

  document.querySelectorAll('.place-card').forEach(card => {
    const price = parseFloat(card.getAttribute('data-price'));
    card.style.display = price <= maxPrice ? 'block' : 'none';
  });
}

// === place.html - détails d’un lieu ===
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });

    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    } else {
      console.error('Failed to fetch place details:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

function displayPlaceDetails(place) {
  const detailsSection = document.getElementById('place-details');
  const reviewsSection = document.getElementById('reviews');

  if (!detailsSection) return;

  detailsSection.innerHTML = `
    <h1>${place.name}</h1>
    <div class="place-info">
      <p><strong>Host:</strong> ${place.host || 'N/A'}</p>
      <p><strong>Price:</strong> $${place.price_per_night} per night</p>
      <p><strong>Description:</strong> ${place.description || 'No description'}</p>
      <p><strong>Amenities:</strong> ${place.amenities?.join(', ') || 'None'}</p>
    </div>
  `;

  if (reviewsSection && place.reviews) {
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    place.reviews.forEach(review => {
      const card = document.createElement('div');
      card.className = 'review-card';
      card.innerHTML = `
        <p><strong>${review.user}:</strong> ${review.comment}</p>
        <p>Rating: ${'⭐'.repeat(review.rating)}</p>
      `;
      reviewsSection.appendChild(card);
    });
  }
}
