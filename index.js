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
        const cardWidth = productCards[0].offsetWidth + 16; // Include margin/padding
        const maxScroll = (productCards.length - 1) * cardWidth;
        
        // Calculate the new scroll position
        carouselIndex += n;
        if (carouselIndex < 0) carouselIndex = 0;
        if (carouselIndex * cardWidth > maxScroll) carouselIndex = Math.floor(maxScroll / cardWidth);

        productContainer.style.transform = `translateX(-${carouselIndex * cardWidth}px)`; // Move the container
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

    /* Slideshow Navigation */
    document.querySelector('.prev').addEventListener('click', () => moveSlides(-1));
    document.querySelector('.next').addEventListener('click', () => moveSlides(1));

    // Bind carousel navigation
    document.querySelector('.carousel-btn.prev-btn').addEventListener('click', () => moveCarousel(-1));
    document.querySelector('.carousel-btn.next-btn').addEventListener('click', () => moveCarousel(1));

    /* Add-to-Cart Functionality for Home Page */
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function () {
            // Retrieve product details from data attributes
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');
            const productPrice = this.getAttribute('data-product-price');
            const productImage = this.getAttribute('data-product-image'); // Correctly getting the image URL from data attribute
            
            // Default quantity for home page is 1
            const quantity = 1;

            // Ensure the price is a valid number (remove currency symbols if present)
            const price = parseFloat(productPrice.replace("EGP", "").replace(",", "").trim());

            // Create a product object
            const product = {
                id: productId,
                name: productName,
                price: price,
                image: productImage,  // Store image URL correctly
                quantity: quantity
            };

            // Retrieve the existing cart from localStorage
            let cart = JSON.parse(localStorage.getItem('cart')) || [];

            // Check if the product already exists in the cart
            const existingProduct = cart.find(item => item.id === productId);
            if (existingProduct) {
                // Increment quantity if the product is already in the cart
                existingProduct.quantity += quantity;
            } else {
                // Add the new product to the cart
                cart.push(product);
            }

            // Save the updated cart to localStorage
            localStorage.setItem('cart', JSON.stringify(cart));

            // Notify the user
            alert(`${product.name} added to cart!`);
        });
    });
});
