    /* Add-to-Cart Functionality for product Page */
    document.addEventListener('DOMContentLoaded', function () {
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