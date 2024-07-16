BASE_ORDERS_URL = `${location.origin}/custom-admin/api/orders`

document.addEventListener('DOMContentLoaded', function () {
    const modals = document.querySelectorAll('[id^="exampleScrollableModal-"]');

    async function fetchOrders(orderId) {
        try {
            const response = await fetch(`${BASE_ORDERS_URL}/?id=${orderId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch orders');
            }
            const responseData = await response.json();

            if (Array.isArray(responseData)) {
                return responseData.length > 0 ? responseData[0] : null;
            } else {
                return responseData;
            }
        } catch (error) {
            console.error('Error fetching orders:', error);
            return null;
        }
    }

    async function UpdateOrderToPackaged(orderId) {
        const url = `${BASE_ORDERS_URL}/${orderId}/`;
        let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const updatedOrderData = {
            order_type: 'Paketlənən'
        };

        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(updatedOrderData)
            });

            if (!response.ok) {
                throw new Error(`Failed to update order (status ${response.status})`);
            }

            const updatedOrder = await response.json();
            return updatedOrder;
        } catch (error) {
            console.error('Error updating order:', error);
            return null;
        }
    }

    async function UpdateOrderToReadyForDelivery(orderId) {
        const url = `${BASE_ORDERS_URL}/${orderId}/`;
        let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const updatedOrderData = {
            order_type: 'Təhvilə hazır'
        };

        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(updatedOrderData)
            });

            if (!response.ok) {
                throw new Error(`Failed to update order (status ${response.status})`);
            }

            const updatedOrder = await response.json();
            return updatedOrder;
        } catch (error) {
            console.error('Error updating order:', error);
            return null;
        }
    }

    async function UpdateOrderToCompleted(orderId) {
        const url = `${BASE_ORDERS_URL}/${orderId}/`;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const updatedOrderData = {
            order_type: "Tamamlanmış"
        };

        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(updatedOrderData)
            });
    
            if (!response.ok) {
                throw new Error(`Failed to update order (status ${response.status})`);
            }
    
            const updatedOrder = await response.json();
            return updatedOrder;
        } catch (error) {
            console.error('Error updating order:', error.message);
            return null;
        }
    }

    async function UpdateOrderToCancel(orderId) {
        const url = `${BASE_ORDERS_URL}/${orderId}/`;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const updatedOrderData = {
            order_type: "Ləğv edilib"
        };

        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(updatedOrderData)
            });
    
            if (!response.ok) {
                throw new Error(`Failed to update order (status ${response.status})`);
            }
    
            const updatedOrder = await response.json();
            return updatedOrder;
        } catch (error) {
            console.error('Error updating order:', error.message);
            return null;
        }
    }
    

    modals.forEach(async function (modal) {
        const orderId = modal.id.split('-')[1];
        const orderModalBody = document.getElementById(`order-body-${orderId}`);
        const orderTitle = document.getElementById(`order-title-${orderId}`)
        const orderFooter = document.getElementById(`order-footer-${orderId}`)

        const order = await fetchOrders(orderId);

        orderModalBody.innerHTML = '';
        orderTitle.innerHTML = ''
        orderFooter.innerHTML = ''

        if (order) {
            orderTitle.innerHTML += `
            Sifariş No: ${order.id}
            `
            order.order_items.forEach(item => {
                orderModalBody.innerHTML += `
                <div class="card mb-3">
                    <div class="row g-0">
                        <div class="col-md-4">
                            <img src="${item.product.image}" class="img-fluid rounded-start" style="max-height: 200px;" alt="Product Image">
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title">
                                    ${item.product.title}
                                </h5>
                                <div class="mb-3">
                                    <span class="d-inline-block me-3 mt-1"><i class="bi bi-clipboard-check text-primary me-1"></i> Quantity: ${item.quantity}</span>
                                    <span class="d-inline-block me-3 mt-1"><i class="bi bi-upc text-info me-1"></i> Barcode: ${item.product.barcode_code}</span>
                                    <span class="d-inline-block mt-1"><i class="bi bi-upc-scan text-warning me-1"></i> Product Code: ${item.product.product_code}</span>
                                </div>
                                ${order.is_wolt == false ?
                        `
                                        <div class="d-flex align-items-center mb-3">
                                            <i class="bi bi-person-fill me-2 text-success" style="font-size: 1.2rem;"></i>
                                            <div>
                                                <span style="font-size: 1.1rem;">${order.user.full_name}</span><br>
                                                <span style="font-size: 1rem; color: #6c757d;">${order.user.email}</span>
                                            </div>
                                        </div>
                                        <div class="d-flex align-items-center">
                                            <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                                            <div>
                                                <span style="font-size: 1rem;">Ofisdən götürülmə</span><br>
                                            </div>
                                        </div>
                                    `
                        : `
                                        <div class="d-flex align-items-center mb-3">
                                            <i class="bi bi-person-fill me-2 text-success" style="font-size: 1.2rem;"></i>
                                            <div>
                                                <span style="font-size: 1.1rem;">${order.user.full_name}</span><br>
                                                <span style="font-size: 1rem; color: #6c757d;">${order.user.email}</span>
                                                <span style="font-size: 1rem; color: #6c757d;">${order.transaction.recipient_phone}</span>
                                            </div>
                                        </div>
                                        <div class="d-flex align-items-center">
                                            <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                                            <div>
                                                <span style="font-size: 1.1rem;">${order.transaction.dropoff_comment}</span><br>
                                            </div>
                                        </div>
                                        `
                    }

                            </div>
                        </div>
                    </div>
                </div>
            `;

                if (item.product.stock > 0 && order.order_type === 'Yeni') {
                    orderFooter.innerHTML += `
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                    <button onclick="${UpdateOrderToCancel(orderId)}" type="button" class="btn btn-danger">Ləğv et</button>
                    <button onclick="${UpdateOrderToPackaged(orderId)}" type="button" class="btn btn-success">Təsdiq et</button>
                `;
                } else if (item.product.stock > 0 && order.order_type === 'Paketlənən') {
                    orderFooter.innerHTML += `
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                    <button type="button" class="btn btn-danger">Ləğv et</button>
                    <button onclick="${UpdateOrderToReadyForDelivery(orderId)}" type="button" class="btn btn-success">Paketləməni tamamla</button>
                `;
                } else if (item.product.stock > 0 && order.order_type === 'Təhvilə hazır') {
                    orderFooter.innerHTML += `
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                    <button type="button" class="btn btn-danger">Ləğv et</button>
                    <button onclick="${UpdateOrderToCompleted(orderId)}" type="button" class="btn btn-success">Sifariş göndərildi</button>
                `;
                } else if (item.product.stock > 0 && order.order_type === 'Tamamlanmış') {
                    orderFooter.innerHTML += `
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                    <button type="button" class="btn btn-success disabled">Sifariş tamamlanıb</button>
                `;
                } else {
                    orderFooter.innerHTML += `
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                    <button type="button" class="btn btn-danger disabled">Stokda yoxdur</button>
                    <button type="button" class="btn btn-danger">Ləğv et</button>
                `;
                }

            });

        } else {
            orderTitle.innerHTML = ''
            orderFooter.innerHTML = ''
            orderModalBody.innerHTML = 'Failed to fetch order details.';
        }
    });
});

