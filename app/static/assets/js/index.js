if (isAuthenticated) {
    fetchBasketItems();
}

if(window.location.pathname == "/basket/" || window.location.pathname == "/en/basket/" || window.location.pathname == "/ru/basket/"){
    document.getElementById('selectAllCheckbox').addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function addToBasket(product_id, quantity) {
    fetch(`/add-to-basket/${product_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
        },
        body: JSON.stringify({ quantity: quantity  }),
    })
    .then(data => {
        if (data) {
            // Kullanıcıya bildirim göster
            fetchBasketItems();
            // Sepet ikonunu güncelle
            $('#basket-item-count').text(data.basket_item_count);
            showNotification("Məshul səbətə əlavə edildi")
        } else {
           console.log('Bir hata oluştu.');
        }
    })
    .catch(error => console.error('Error:', error));
}
function removeFromBasket(basketItemId) {
    fetch(`/remove-from-basket/${basketItemId}/`,)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fetchBasketItems();
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
}
function incrementQuantity(product_id) {
    fetch(`/update_basket_item_count/${product_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
        },
        body: JSON.stringify({ quantity_change: 1  }),
    })
    .then(data => {
        fetchBasketItems();
    })
    .catch(error => console.error('Error:', error));
}
function decrementQuantity(product_id) {
    fetch(`/update_basket_item_count/${product_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
        },
        body: JSON.stringify({ quantity_change: -1  }),
    })
    .then(data => {
        fetchBasketItems();
    })
    .catch(error => console.error('Error:', error));
}
function updateURLParameter(key, value) {
    // Get the current URL
    var url = new URL(window.location.href);

    // Set or update the parameter in the URL
    url.searchParams.set(key, value);

    // Replace the current URL with the updated one
    history.replaceState(null, null, url.href);

}
var coupon_is_applied = false;
if (window.location.pathname == '/basket/' || window.location.pathname == "/en/basket/" || window.location.pathname == "/ru/basket/") {
    localStorage.removeItem('coupon_code');
}
function applyCoupon() {
    var form = document.getElementById('couponForm');
    var input = form.querySelector('input[name="coupon_code"]');
    var couponValue = input.value;

    // Update URL with coupon code
    updateURLParameter('coupon_code', couponValue);

    // Call the fetchBasketItems function with the coupon code
    fetchBasketItems(couponValue);
    if (couponValue !== '') {
        coupon_is_applied = true
    }
    localStorage.setItem('coupon_code', couponValue);
}
function notApplyCoupon() {
    localStorage.removeItem('discount');
    fetchBasketItems();
    coupon_is_applied = false
    localStorage.removeItem('coupon_code');
    updateURLParameter('coupon_code', '');
}

function check_stock_status() {
    return new Promise((resolve, reject) => {
        fetch(`/check-stock-status/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resolve(data); // Veriyi döndür
            })
            .catch(error => {
                reject(error); // Hata durumunda hata nesnesini döndür
            });
    });
}


function fetchBasketItems(coupon_code) {
    fetch(`/get-basket-items/${coupon_code?`?coupon_code=${coupon_code}`:''}`)
        .then(response => response.json())
        .then(data => {
            updateNavbarBasket(data);
            if(window.location.pathname == "/basket/" || window.location.pathname == "/en/basket/" || window.location.pathname == "/ru/basket/"){
            updateBasketTable(data);
            }
        })
        .catch(error => console.error('Error:', error));
}

function updateNavbarBasket(data){
    document.getElementById('header-basket-count').innerText = `${data.basketItemCount}`;
    if (data.basketItems.length > 0){
        const basketItemsBody = document.getElementById('navbar-basket-items');
        document.getElementById('navbar-basket-total').innerText = `${data.totalPrice} AZN`;
        basketItemsBody.innerHTML = '';
        data.basketItems.forEach((item, count)=>{
            if (count<3) {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="shopping-cart-img">
                        <a href="/products/${item.product.slug}/"><img alt="Nest" src="${item.product.image_url}"></a>
                    </div>
                    <div class="shopping-cart-title">
                        <h4><a href="/products/${item.product.slug}/">${item.product.title.length > 18 ? `${item.product.title.slice(0, 18)} ...` : item.product.title}</a></h4>
                        <h4><span>${item.quantity} × </span>₼ ${item.product.price}</h4>
                    </div>
                    <div class="shopping-cart-delete">
                        <a onclick="removeFromBasket(${item.id})"><i class="fi-rs-cross-small"></i></a>
                    </div>
             `;
            basketItemsBody.appendChild(li);
            }
        })
        if (data.totalPrice == 0 || !data.stock_status) {
            document.getElementById("navbar-basket-checkout").disabled = true;
        }else{
            document.getElementById("navbar-basket-checkout").disabled = false;
        }
        document.getElementById('navbar-basket').classList.remove("d-none");
    }else{
        document.getElementById('navbar-basket').classList.add("d-none");
    }

    
}

function updateBasketTable(data) {
    // Sepet tablosunu güncelleme kodları buraya eklenebilir
    // Örneğin, data içindeki bilgileri kullanarak HTML içeriğini dinamik olarak oluşturabilirsiniz.
    var urlParams = new URLSearchParams(window.location.search);
    var couponCode = urlParams.get('coupon_code');
    document.getElementById('basket-item-count').innerText = data.basketItemCount;
    document.getElementById('basket-checkout-form').innerHTML = `
            <div class="border p-md-4 cart-totals">
                
                ${!data.stock_status ? `<p class="text-danger">* Stokda olmayan məhsullar var</p>`: ''}
                <div class="table-responsive">
                    <table class="table no-border">
                        <tbody id="basket-item-checkout">
                            <tr id="basket-item-total">
                                <td class="cart_total_label">
                                    <h6 class="text-muted">Ümumi qiymət</h6>
                                </td>
                                <td class="cart_total_amount">
                                    <h4 class="text-brand text-end">₼ ${data.totalPrice}</h4>
                                </td>
                            </tr>
                            <tr>
                                <td scope="col" colspan="2">
                                    <div class="divider-2 mt-10 mb-10"></div>
                                </td>
                            </tr>
                            <tr>
                                <td class="cart_total_label">
                                    <h6 class="text-muted">Endirim</h6>
                                </td>
                                <td class="cart_total_amount">
                                    <h5 class="text-heading text-end">₼ ${data.discount ? data.discount : 0}</h5></td> </tr> <tr>
                                <td scope="col" colspan="2">
                                    <div class="divider-2 mt-10 mb-10"></div>
                                </td>
                            </tr>
                            <tr>
                                <td class="cart_total_label">
                                    <h6 class="text-muted">Yekun qiymət</h6>
                                </td>
                                <td class="cart_total_amount">
                                    <h4 class="text-brand text-end">₼ ${data.discount ? data.discountPrice : data.totalPrice}</h4>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="border mt-3 p-md-4 cart-totals">
                <div class="table-responsive">
                    <button data-bs-toggle="modal" data-bs-target="#checkoutBasket" class="payment-option text-center w-100 ${data.totalPrice == 0 || !data.stock_status ? 'bg-success' : ''}" ${data.totalPrice == 0 || !data.stock_status ? `disabled style="cursor: not-allowed;"`: ''} data-value="cash_on_delivery">
                        Səbəti tamamla
                    </button>
                </div>
            </div>
            <div class="border p-md-4 cart-totals mt-3">
                ${!data.stock_status ? `<p class="text-danger">* Stokda olmayan məhsullar var</p>`: ''}
                <h4 class="mb-10">Kupon tətbiq et</h4>
                <form  id="couponForm" class="mb-3">
                    <div class="d-flex justify-content-between">
                        <input class="font-medium mr-15 coupon" ${couponCode ? `value="${couponCode}"`: ''} name="coupon_code" placeholder="Kupon">
                        ${coupon_is_applied ? `
                        <button ${data.totalPrice == 0 || !data.stock_status ? 'disabled' : ''} onclick="notApplyCoupon()" type="button" style="width:265px;padding:0;" class="btn btn-danger"><i class="fi-rs-label mr-10"></i>Ləğv et</button>
                        `:`
                        <button ${data.totalPrice == 0 || !data.stock_status ? 'disabled' : ''} onclick="applyCoupon()" type="button" style="width:265px;padding:0;" class="btn btn-success"><i class="fi-rs-label mr-10"></i>Tətbiq et</button>
                        `}
                    </div>
                    <div id="coupon_error" class="mt-3 text-danger"></div>
                </form>
            </div>
            
    `;
    saveDataToLocalStorage(data);

    const coupon_error = document.getElementById('coupon_error')

    if (data.error) {
        coupon_error.innerText = `* ${data.error}`;
        localStorage.removeItem('coupon_code')
    }else{
        coupon_error.innerText = '';
    }
    const basketItemsBody = document.getElementById('basket-items-body');
    basketItemsBody.innerHTML = ''; // Önce mevcut içeriği temizle

    

    data.basketItems.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
        <td class="custome-checkbox pl-30">
            <input checked class="form-check-input" type="checkbox" name="selected_items[]" id="selected_item${item.id}" value="${item.id}">
            <label class="form-check-label" for="selected_item${item.id}"></label>
        </td>
        <td class="image product-thumbnail"><img src="${item.product.image_url}" alt="#"></td>
        <td class="product-des product-name">
            <h6 class="mb-5"><a class='product-name mb-10 text-heading' data-bs-toggle="modal" data-bs-target="#quickViewModal${item.product.id}">${item.product.title}</a></h6>
            ${item.product.stock > 0 && item.product.stock < item.quantity ? '<span class="text-danger border-solid border-1 border-danger rounded p-1">Stokda kifayət qədər yoxdur</span>' :''}
            ${item.product.stock == 0 ? '<span class="text-danger border-solid border-1 border-danger rounded p-1">Stokda yoxdur</span>' :''}
        </td>
        <td class="price" data-title="Qiymət">
            <h4 class="text-body">₼ ${item.product.price}</h4>
        </td>
        ${item.product.stock > 0 ? `
        <td class="text-center detail-info" data-title="Say">
            <div class="detail-extralink mr-15">
                <div class="detail-qty border radius">
                    <a onclick="decrementQuantity(${ item.product.id })" class="qty-down"><i class="fi-rs-angle-small-down"></i></a>
                    <span class="qty-val">${item.quantity}</span>
                    ${item.product.stock > item.quantity ? `
                    <a onclick="incrementQuantity(${ item.product.id })" class="qty-up"><i class="fi-rs-angle-small-up"></i></a>
                    `: ''}
                </div>
            </div>
        </td>
        <td class="price" data-title="Ümumi qiymət">
            <h4 class="text-brand">₼ ${item.total_price}</h4>
        </td>
        ` : '<td></td><td></td>'}
        <td class="action text-center" data-title="Remove">
            <a href="#" class="text-body" onclick="removeFromBasket(${item.id})"><i class="fi-rs-trash"></i></a>
        </td>
    `;
        basketItemsBody.appendChild(tr);
        document.getElementById(`selected_item${item.id}`).addEventListener('change', function () {
            const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
            const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);
            document.getElementById('selectAllCheckbox').checked = allChecked;
        });
    });
}

function saveDataToLocalStorage(data) {
    localStorage.setItem('discount', data.discount);
    localStorage.setItem('totalPrice', data.totalPrice);
    localStorage.setItem('discountPrice', data.discountPrice);
}


// Sayfa yüklendiğinde sepeti getir
function deleteSelectedBasketItems() {
    const selectedItems = document.querySelectorAll('input[name="selected_items[]"]:checked');
    const selectedIds = Array.from(selectedItems).map(item => Number(item.value));
    if (selectedIds.length === 0) {
        alert('Please select at least one item to delete.');
        return;
    }

    fetch('/delete_selected_basket_items/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
        },
        body: JSON.stringify({ selected_items: selectedIds }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)

        if (data.success) {
            // Optionally handle success feedback
            console.log(data.message);
            fetchBasketItems();  // Optionally refresh the basket items display
        } else {
            console.log('An error occurred while deleting selected basket items.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function toggleFavorite(productId) {
    fetch(`/favorite_toggle/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        credentials: 'same-origin',
        // body: JSON.stringify({}),  // Eğer gerekirse bir içerik göndermek isterseniz bu satırı kullanabilirsiniz
    })
    .then(response => response.json())
    .then(data => {
        // Favori durumuna göre UI güncelleme işlemleri
        const productCart = document.getElementById(`product_action_${productId}`)
        const mobileproductCart = document.getElementById(`mobile_product_action_${productId}`)
        const favorite_count =  document.getElementById("favorite_count")
        if (data.action == 'added') {
            productCart.innerHTML = `<img style="width:14px;" src="${window.location.origin}/static/assets/imgs/heart.png" alt="">
            `;
            mobileproductCart.innerHTML = `<img style="width:14px;" src="${window.location.origin}/static/assets/imgs/heart.png" alt="">
            `;
            favorite_count.innerText = `${Number(favorite_count.innerText)+1}`
        } else {
            productCart.innerHTML = '<i class="fi-rs-heart"></i>';
            mobileproductCart.innerHTML = '<i class="fi-rs-heart"></i>';
            favorite_count.innerText = `${Number(favorite_count.innerText)-1}`
        }
    })
    .catch(error => console.error('Error:', error));
}

function toggleBasketInfo(){
    var detailInfo = document.querySelector("#payment-info-detail")
    detailInfo.classList.toggle("d-none")
}
window.addEventListener('click', function(e){   
  if ( !document.getElementById('payment-info').contains(e.target) && !document.getElementById('payment-info-detail').contains(e.target)){
    var detailInfo = document.querySelector("#payment-info-detail")
    detailInfo.classList.add("d-none")
  } 
});