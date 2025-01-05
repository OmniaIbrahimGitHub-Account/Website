document.addEventListener('DOMContentLoaded', function() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartList = document.getElementById('cart-list');
    const totalPriceElement = document.getElementById('total-price');
    
    // Update the cart display and total price
    function updateCartDisplay() {
        cartList.innerHTML = ''; // Clear the cart display
        let total = 0;

        if (cart.length === 0) { 
            cartList.innerHTML = "<p>Your cart is empty.</p>"; 
            totalPriceElement.textContent = "Total: EGP 0.00"; 
            return; 
        }

        // Loop through each item in the cart
        cart.forEach(item => {
            const price = parseFloat(item.price); // Ensure price is a number
            const quantity = parseInt(item.quantity, 10); // Ensure quantity is an integer

            const cartItem = document.createElement('li');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `  
                <img src="${item.image}" alt="${item.name}"> <!-- Correct image path -->
                <div class="details">
                    <h2>${item.name}</h2>
                    <p>Price: EGP ${price.toFixed(2)}</p> <!-- Display price in EGP -->
                    <div class="quantity-controls">
                        <button class="quantity-button decrease" data-product-id="${item.id}">-</button>
                        <span>${item.quantity}</span>
                        <button class="quantity-button increase" data-product-id="${item.id}">+</button>
                        <button class="remove-from-cart" data-product-id="${item.id}">Remove</button>
                    </div>
                </div>
            `;
            cartList.appendChild(cartItem);

            // Calculate total price
            total += price * quantity; 
        });

        // Display total price
        totalPriceElement.textContent = `Total: EGP ${total.toFixed(2)}`;
    }

    updateCartDisplay(); // Initial render of cart

    // Handle button clicks for quantity changes and item removal
    cartList.addEventListener('click', function(e) {
        const productId = e.target.getAttribute('data-product-id');
        const productIndex = cart.findIndex(item => item.id === productId);

        // Increase quantity
        if (e.target.classList.contains('increase')) {
            cart[productIndex].quantity++;
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartDisplay();
        }

        // Decrease quantity
        if (e.target.classList.contains('decrease')) {
            if (cart[productIndex].quantity > 1) {
                cart[productIndex].quantity--;
                localStorage.setItem('cart', JSON.stringify(cart));
                updateCartDisplay();
            }
        }

        // Remove item from cart
        if (e.target.classList.contains('remove-from-cart')) {
            cart.splice(productIndex, 1); // Remove the item from cart
            localStorage.setItem('cart', JSON.stringify(cart)); // Update localStorage
            updateCartDisplay(); // Re-render the cart
        }
    });

    // Checkout button functionality
    document.getElementById('checkout').addEventListener('click', function() {
        window.location.href = "/checkout";
    });
});