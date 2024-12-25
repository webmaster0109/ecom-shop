document.addEventListener('DOMContentLoaded', () => {
    fetch('/products/')
        .then(response => response.json())
        .then(data => {
            console.log(Array.isArray(data.products));
            if (typeof data.products === 'string') {
                // If it's a string, parse it into an array
                data.products = JSON.parse(data.products);
            }
            if (Array.isArray(data.products)) {
                const productContainer = document.getElementById('product-container');
                data.products.forEach(product => {
                    const productFields = product.fields;
                    const productElement = document.createElement('div');
                    productElement.className = 'product';
                    productElement.innerHTML = `
                        <h2>${productFields.name}</h2>
                        <img src="/media/${productFields.image}" alt="${productFields.name}" style="width: 150px; height: auto;">
                        <p>${productFields.description}</p>
                        <p>Price: $${productFields.price}</p>
                        <a class="btn btn-danger" href="/product/${productFields.slug}/" target="_self">View Details</a>
                    `;
                    productContainer.appendChild(productElement);
                });
            } else {
                console.error('Failed to fetch products:', data.message);
                createToast(data.message, 'Error');
            }
        })
        .catch((error) => {
            console.error('Error fetching products:', error);
            createToast(error, 'Error');
        });
});
