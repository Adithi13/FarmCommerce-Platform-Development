let categories = [];
let cart = [];
let i = 0;
//kdsjhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh


// function addToCart(pid) {
//     const selectedProduct = { id: pid };
//     cart.push(selectedProduct);
//     updateCart();
// }

// function delElement(index) {
//     cart.splice(index, 1);
//     updateCart();
// }

// function updateCart() {
//     // Your logic to update the cart display
//     console.log(cart);
// }

// mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmnnnnnnnnnnnnnnnnnnnnnnnnnnn
// document.addEventListener('DOMContentLoaded', () => {
//     // Fetch products from the server when the page loads
//     fetch('/getproducts')
//         .then(response => response.json())
//         .then(data => {
//             categories = data;
//             updateProductList();
//         })
//         .catch(error => console.error('Error fetching products:', error));
// });

// function updateProductList() {
//     document.getElementById('root').innerHTML = categories.map(item => {
//         const { image, title, price } = item;
//         return `
//             <div class='box'>
//                 <div class='img-box'>
//                     <img class='images' src=${image}></img>
//                 </div>
//                 <div class ='bottom'>
//                     <p>${title}</p>
//                     <h2>$ ${price}.00</h2>
//                     <button onclick='addtocart(${i++})'>Add to cart</button>
//                 </div>
//             </div>`;
//     }).join('');
// }
// document.addEventListener('DOMContentLoaded', () => {
//     // Fetch product details when the page loads (you can adjust the endpoint)
//     fetch('/getproductdetails?pid=2')  // Make sure to provide the correct product ID
//         .then(response => response.json())
//         .then(productDetails => {
//             // Process the single product details as needed
//             categories = [productDetails];
//             updateProductList();
//         })
//         .catch(error => console.error('Error fetching product details:', error));
// });

// function updateProductList() {
//     document.getElementById('root').innerHTML = categories.map(item => {
//         const { image, title, price } = item;
//         return `
//             <div class='box'>
//                 <div class='img-box'>
//                     <img class='images' src=${image}></img>
//                 </div>
//                 <div class ='bottom'>
//                     <p>${title}</p>
//                     <h2>$ ${price}.00</h2>
//                     <button onclick='addtocart(${i++})'>Add to cart</button>
//                 </div>
//             </div>`;
//     }).join('');
// }


// Rest of your existing code...

// function addtocart(index) {
//     const selectedProduct = { ...categories[index] };
//     cart.push(selectedProduct);
//     displayCart();
// Add this function to fetch the product details when the page loads
function fetchProductDetails(pid) {
    fetch(`/addtocart?pid=${pid}`)
        .then(response => response.text())  // Use text() to get HTML content
        .then(data => {
            categories = data;
            updateProductList();
        })
        .then(htmlContent => {
            // Append the HTML content to the desired location on your page
            document.getElementById('productDetailsContainer').innerHTML = htmlContent;
        })
        .catch(error => console.error('Error fetching product details:', error));
}

// document.addEventListener('DOMContentLoaded', () => {
//     // Fetch product details when the page loads
//     const pid = 2;  // Replace with the actual product ID
//     fetchProductDetails(pid);

//     // ... rest of your code ...
// });

// Modify the addtocart function to fetch and display product details
// function addtocart(index) {
//     const selectedProduct = {
//         id: categories[index].id,
//         title: categories[index].title,
//         image: categories[index].image,
//         price: categories[index].price
//     };
//     cart.push(selectedProduct);
//     displayCart();

//     // Fetch and display product details when adding to the cart
//     fetchProductDetails(selectedProduct.id);
// }

// }
document.addEventListener('DOMContentLoaded', () => {
    // Fetch product details when the page loads (you can adjust the endpoint)
    fetch(`/getproductdetails?pid=${pid}`)  // Make sure to provide the correct product ID
        .then(response => response.json())
        .then(productDetails => {
            // Process the single product details as needed
            categories = [productDetails];
            updateProductList();
        })
        .catch(error => console.error('Error fetching product details:', error));
});

function updateProductList() {
    document.getElementById('root').innerHTML = categories.map(item => {
        const { image, productname, price, productdesc } = item;
        return `
            <div class='box'>
                <div class='img-box'>
                    <img class='images' src=${image}></img>
                </div>
                <div class ='bottom'>
                    <p>${productname}</p>
                    <p>${productdesc}</p>
                    <h2>$ ${price}.00</h2>
                    <button onclick='addtocart(${i++})'>Add to cart</button>
                </div>
            </div>`;
    }).join('');
}

function addtocart(index) {
    const selectedProduct = {
        id: categories[index].id,
        title: categories[index].productname,
        description: categories[index].productdesc,
        price: categories[index].price
    };
    cart.push(selectedProduct);
    displayCart();
    fetchProductDetails(selectedProduct.id);
}
function fetchProductDetails(pid) {
    fetch(`/getproductdetails?pid=${pid}`)
        .then(response => response.json())
        .then(productDetails => {
            categories = [productDetails];
            updateProductList();
        })
        .catch(error => console.error('Error fetching product details:', error));
}
function displayCart() {
    let total = 0;
    document.getElementById('count').innerHTML = cart.length;
    document.getElementById('count').innerHTML = `$ ${total}.00`;
    const cartItemElement = document.getElementById('cartItem');
    if (cart.length === 0) {
        cartItemElement.innerHTML = "Your cart is empty";
    } else {
        cartItemElement.innerHTML = cart.map((item, index) => {
            const {  title,description, price } = item;
            total += price;
            document.getElementById('total').innerHTML = `$ ${total}.00`;
            return `
                <div class='cart-item'>
                    <div class='row-img'>
                        <img class='rowimg' src=${description}>
                    </div>
                    <p style='font-size:12px;'>${title}</p>
                    <h2 style='font-size: 15px;'>$ ${price}.00</h2>
                    <i class='fa-solid fa-trash' onclick='delElement(${index})'></i>
                </div>`;
        }).join('');
    }
}

// function addtocart(index) {
//     const selectedProduct = {
//         id: categories[index].id,
//         title: categories[index].title,
//         image: categories[index].image,
//         price: categories[index].price
//     };
//     cart.push(selectedProduct);
//     displayCart();
// }

function delElement(index) {
    cart.splice(index, 1);
    displayCart();
}

function displayCart() {
    let total = 0;
    document.getElementById('count').innerHTML = cart.length;
    document.getElementById('count').innerHTML = `$ ${total}.00`;

    const cartItemElement = document.getElementById('cartItem');
    if (cart.length === 0) {
        cartItemElement.innerHTML = "Your cart is empty";
    } else {
        cartItemElement.innerHTML = cart.map((item, index) => {
            const { image, title, price } = item;
            total += price;
            document.getElementById('total').innerHTML = `$ ${total}.00`;
            return `
                <div class='cart-item'>
                    <div class='row-img'>
                        <img class='rowimg' src=${image}>
                    </div>
                    <p style='font-size:12px;'>${title}</p>
                    <h2 style='font-size: 15px;'>$ ${price}.00</h2>
                    <i class='fa-solid fa-trash' onclick='delElement(${index})'></i>
                </div>`;
        }).join('');
    }
}
