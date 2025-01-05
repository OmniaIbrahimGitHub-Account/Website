document.addEventListener('DOMContentLoaded', function () {
    /* Slideshow Functionality */
    let slideIndex = 0;

    const showSlides = () => {
        const slides = document.querySelectorAll('.slide');
        slides.forEach((slide) => (slide.style.display = 'none'));
        slideIndex++;
        if (slideIndex > slides.length) slideIndex = 1;
        slides[slideIndex - 1].style.display = 'block';
        setTimeout(showSlides, 4000); // Change slide every 4 seconds
    };

    const moveSlides = (n) => {
        const slides = document.querySelectorAll('.slide');
        slides[slideIndex - 1].style.display = 'none';
        slideIndex += n;
        if (slideIndex > slides.length) slideIndex = 1;
        if (slideIndex < 1) slideIndex = slides.length;
        slides[slideIndex - 1].style.display = 'block';
    };

    showSlides();

    /* Carousel Functionality */
    let carouselIndex = 0;

    const moveCarousel = (n) => {
        const productContainer = document.querySelector('.product-carousel .product-container');
        const productCards = document.querySelectorAll('.product-carousel .product-card');
        const cardWidth = productCards[0].offsetWidth + 16; // Include margin
        const maxScroll = (productCards.length - 1) * cardWidth;
        carouselIndex += n;

        if (carouselIndex < 0) carouselIndex = 0;
        if (carouselIndex * cardWidth >= maxScroll) carouselIndex -= n;

        productContainer.scrollTo({
            left: carouselIndex * cardWidth,
            behavior: 'smooth',
        });
    };

    /* Recently Viewed Products */
    const trackViewedProduct = (product) => {
        let viewedProducts = JSON.parse(localStorage.getItem('viewedProducts')) || [];

        // Check if the product already exists in the recently viewed list
        const productExists = viewedProducts.some((item) => item.id === product.id);

        if (!productExists) {
            viewedProducts.push(product); // Add product if not already in the list
            localStorage.setItem('viewedProducts', JSON.stringify(viewedProducts));
        }
    };

    document.querySelectorAll('.product-card').forEach((card) => {
        card.addEventListener('click', function () {
            const productId = this.getAttribute('href').split('/product/')[1];
            const productName = this.querySelector('h3').innerText;
            const productImage = this.querySelector('.product-image').getAttribute('src');
            const productDescription = this.querySelector('p:not(.price)').innerText; // Fetch description
            const productPrice = this.querySelector('.price').innerText;

            const product = {
                id: productId,
                name: productName,
                image: productImage,
                description: productDescription,
                price: productPrice,
            };

            trackViewedProduct(product);
        });
    });

    const renderRecentlyViewedProducts = () => {
        const viewedProductsContainer = document.querySelector('.recently-viewed-container .product-container');
        const viewedProducts = JSON.parse(localStorage.getItem('viewedProducts')) || [];

        // Clear existing content
        viewedProductsContainer.innerHTML = '';

        if (viewedProducts.length === 0) {
            viewedProductsContainer.innerHTML = `
                <div class="message-text">
                    <p>You haven't explored any products yet. Start discovering our amazing range of items and check back here to see your recently viewed products!</p>
                    <a href="/product" class="shop-now-link">Shop Now</a>
                </div>`;
            return;
        }

        // Render each recently viewed product
        viewedProducts.forEach((product) => {
            viewedProductsContainer.innerHTML += `
                <a href="/product/${product.id}" class="product-card">
                    <img src="${product.image}" alt="${product.name}" class="product-image">
                    <h3>${product.name}</h3>
                    <p>${product.description}</p>
                    <p class="price">${product.price}</p>
                    <div class="product-actions">
                        <button class="add-to-cart-btn" 
                            data-product-id="${product.id}"
                            data-product-name="${product.name}"
                            data-product-price="${product.price}"
                            data-product-image="${product.image}">
                            Add to Cart
                        </button>
                    </div>
                </a>`;
        });
    };

    renderRecentlyViewedProducts(); // Initialize the rendering

    /* Go to Products on Click */
    window.goToProducts = () => {
        window.location.href = '/product';
    };
});


/*Sign Up*/
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('signup-form').addEventListener('submit', function (e) {
      e.preventDefault();
  
      // Clear errors
      document.getElementById('username-error').textContent = '';
      document.getElementById('email-error').textContent = '';
      document.getElementById('password-error').textContent = '';
      document.getElementById('confirm-password-error').textContent = '';
  
      // Get user input
      const username = document.getElementById('username').value.trim();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirm-password').value;
  
      let isValid = true;
  
      // Validate username
      if (!/^[a-zA-Z]+$/.test(username)) {
        document.getElementById('username-error').textContent = 'Username must contain letters only.';
        isValid = false;
      }
  
      // Validate email
      if (!email.includes('@')) {
        document.getElementById('email-error').textContent = 'Email must contain "@" symbol.';
        isValid = false;
      }
  
      // Validate password
      const passwordRegex = /^(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
      if (!passwordRegex.test(password)) {
        document.getElementById('password-error').textContent =
          'Password must be at least 8 characters long, contain at least one uppercase letter, and include both letters and numbers.';
        isValid = false;
      }
  
      // Confirm password
      if (password !== confirmPassword) {
        document.getElementById('confirm-password-error').textContent = 'Passwords do not match.';
        isValid = false;
      }
  
      // If valid, send data to backend
      if (isValid) {
        fetch('/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username,
            email,
            password,
            confirm_password: confirmPassword,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              alert(data.message);
              window.location.href = '/'; // Redirect on success
            } else {
              alert(data.message); // Show server error
            }
          })
          .catch((error) => {
            alert('An error occurred. Please try again.');
            console.error('Error:', error);
          });
      }
    });
  });
  
/*login*/
const form = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const rememberMeCheckbox = document.getElementById('rememberMe');
const forgetPasswordLink = document.getElementById('forgetPasswordLink');
const forgetPasswordPopup = document.getElementById('forgetPasswordPopup');
const resetButton = document.getElementById('resetButton');
const closePopup = document.getElementById('closePopup');
const resetEmail = document.getElementById('resetEmail');
const emailError = document.getElementById('emailError');

window.onload = () => {
    const savedUsername = localStorage.getItem('username');
    const savedPassword = localStorage.getItem('password');
    const rememberMe = localStorage.getItem('rememberMe') === 'true';

    if (rememberMe) {
        usernameInput.value = savedUsername;
        passwordInput.value = savedPassword;
        rememberMeCheckbox.checked = true;
    }
};

form.addEventListener('submit', (e) => {
    let isValid = true;
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    usernameInput.style.borderColor = '';
    passwordInput.style.borderColor = '';
    
    if (username === '' || username.length < 3) {
        alert('❌ Username must be at least 3 characters long!');
        usernameInput.style.borderColor = 'red';
        isValid = false;
    }

    if (password === '' || password.length < 6) {
        alert('❌ Password must be at least 6 characters long!');
        passwordInput.style.borderColor = 'red';
        isValid = false;
    }

    if (!isValid) {
        e.preventDefault();
    } else {
        if (rememberMeCheckbox.checked) {
            localStorage.setItem('username', username);
            localStorage.setItem('password', password);
            localStorage.setItem('rememberMe', true);
        } else {
            localStorage.removeItem('username');
            localStorage.removeItem('password');
            localStorage.setItem('rememberMe', false);
        }
        alert('✅ Login successful!');
    }
});

forgetPasswordLink.addEventListener('click', (e) => {
    e.preventDefault();
    forgetPasswordPopup.style.display = 'block';
});

closePopup.addEventListener('click', () => {
    forgetPasswordPopup.style.display = 'none';
});

resetButton.addEventListener('click', () => {
    const email = resetEmail.value.trim();
    
    // Validate if the email contains "@"
    if (email === '' || !email.includes('@')) {
        emailError.style.display = 'block'; // Show error message
    } else {
        emailError.style.display = 'none'; // Hide error message
        alert(`✅ Reset link has been sent to ${email}`);
        forgetPasswordPopup.style.display = 'none';
    }
});

// Product Page JavaScript
const stars = document.querySelectorAll('.star');
let ratings = JSON.parse(localStorage.getItem('ratings')) || {};  // استرجاع التقييمات من localStorage إذا كانت موجودة

// تحديث النجوم بناءً على التقييم المخزن
function updateStars(productId, rating) {
    const productDiv = document.querySelector(`[data-product-id="${productId}"]`);
    const allStars = productDiv.querySelectorAll('.star');
    allStars.forEach((s, index) => {
        s.classList.toggle('selected', index < rating);
    });
    productDiv.querySelector('.rating-value').textContent = rating;
}

// إذا كان هناك تقييم موجود في localStorage، عرض النجوم على هذا الأساس
for (const productId in ratings) {
    updateStars(productId, ratings[productId]);
}

stars.forEach(star => {
    star.addEventListener('click', function() {
        const productDiv = this.parentElement;
        const productId = productDiv.getAttribute('data-product-id');
        const selectedRating = Array.from(productDiv.querySelectorAll('.star')).indexOf(this) + 1;

        // تحديث تقييمات النجوم
        const allStars = productDiv.querySelectorAll('.star');
        allStars.forEach((s, index) => {
            s.classList.toggle('selected', index < selectedRating);
        });

        // تخزين التقييم في localStorage
        ratings[productId] = selectedRating;
        localStorage.setItem('ratings', JSON.stringify(ratings));  // حفظ التقييم في localStorage
        updateStars(productId, selectedRating);
    });
});

//Search results page
