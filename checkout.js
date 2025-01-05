document.addEventListener('DOMContentLoaded', function() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartDetailsElement = document.getElementById('cartDetails');

    function renderCartDetails(cart, containerId) {
      const container = document.getElementById(containerId);
      if (cart.length === 0) {
        container.innerHTML = "<p>Your cart is empty.</p>";
        return;
      }

      container.innerHTML = cart.map(item => ` 
        <div class="cart-item">
          <strong>${item.name}</strong><br>
          Quantity: ${item.quantity}<br>
          Price: EGP ${item.price.toFixed(2)}<br><br>
        </div>
      `).join('') + `<strong>Total Price:</strong> EGP ${cart.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2)}`;
    }

    renderCartDetails(cart, 'cartDetails');

    document.getElementById('checkoutForm').addEventListener('submit', async function (e) {
      e.preventDefault();

      const formData = new FormData(this);

      try {
        const response = await fetch('/submit', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const error = await response.json();
          alert(error.error);
          return;
        }

        const user = await response.json();

        const card = document.getElementById('userCard');
        const cardContent = document.getElementById('cardContent');
        const orderDetailsElement = document.getElementById('orderDetails');

        cardContent.innerHTML = `
          <strong>First Name:</strong> ${user.first_name}<br>
          <strong>Last Name:</strong> ${user.last_name}<br>
          <strong>Address:</strong> ${user.address}<br>
          <strong>City:</strong> ${user.city}<br>
          <strong>Phone Number:</strong> ${user.phone}<br><br>
          <strong>Thank you for trusting us with your order! We look forward to serving you again.</strong><br>
          <strong>If you have any problem, Contact us via this email:<a> WeJustGirles@gmail.com.</a> Thank you!</strong><br><br>
          <strong>Hint:</strong> Your order will arrive from 2 to 5 days.<br><br>
        `;

        renderCartDetails(cart, 'orderDetails');

        card.style.display = 'block';
        document.getElementById('checkoutForm').style.display = 'none';
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
      }
    });
  });