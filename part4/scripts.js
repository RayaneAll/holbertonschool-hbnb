document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
    if (addReviewSection) addReviewSection.style.display = 'none';
  } else {
    if (loginLink) loginLink.style.display = 'none';
    if (addReviewSection) addReviewSection.style.display = 'block';
  }

  fetchPlaceDetails(token, placeId);
});

// --- Obtenir le token depuis les cookies ---
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// --- Extraire l’ID du lieu depuis l’URL ---
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// --- Récupérer les détails du lieu ---
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });

    if (response.ok) {
      const data = await response.json();
      displayPlaceDetails(data);
    } else {
      console.error('Failed to fetch place details:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

// --- Affichage dynamique des détails du lieu ---
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

  // Reviews
  if (reviewsSection && place.reviews) {
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    place.reviews.forEach(review => {
      const reviewCard = document.createElement('div');
      reviewCard.className = 'review-card';
      reviewCard.innerHTML = `
        <p><strong>${review.user}:</strong> ${review.comment}</p>
        <p>Rating: ${'⭐'.repeat(review.rating)}</p>
      `;
      reviewsSection.appendChild(reviewCard);
    });
  }
}
