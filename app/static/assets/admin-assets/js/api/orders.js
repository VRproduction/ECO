const BASE_ORDERS_URL = `${location.origin}/custom-admin/api/orders`;

document.addEventListener('DOMContentLoaded', function () {
    const modals = document.querySelectorAll('[id^="exampleScrollableModal-"]');

    modals.forEach(async function (modal) {
        const orderId = modal.id.split('-')[1];
        const orderModalBody = document.getElementById(`order-body-${orderId}`);
        const orderTitle = document.getElementById(`order-title-${orderId}`);
        const orderFooter = document.getElementById(`order-footer-${orderId}`);

        const order = await fetchOrders(orderId);

        if (order) {
            renderOrderDetails(order, orderModalBody, orderTitle);
            renderOrderFooter(order, orderFooter);
            setupButtonHandlers(orderId);
        } else {
            orderTitle.innerHTML = 'Failed to fetch order details.';
        }
    });

    async function fetchOrders(orderId) {
        try {
            const response = await fetch(`${BASE_ORDERS_URL}/?id=${orderId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch orders');
            }
            const responseData = await response.json();

            return Array.isArray(responseData) ? responseData[0] : responseData;
        } catch (error) {
            console.error('Error fetching orders:', error);
            return null;
        }
    }

    function renderOrderDetails(order, orderModalBody, orderTitle) {
        orderModalBody.innerHTML = '';
        orderTitle.innerHTML = `Sifariş No: ${order.id}`;

        if (order && order.order_items && Array.isArray(order.order_items)) {
            order.order_items.forEach(item => {

                let userContactInfo = `
                    <div class="d-flex align-items-center mb-3">
                        <i class="bi bi-person-fill me-2 text-success" style="font-size: 1.2rem;"></i>
                        <div>
                            <span style="font-size: 1.1rem;">${order.user.full_name}</span><br>
                            <span style="font-size: 1rem; color: #6c757d;">${order.user.email}</span>
                        </div>
                    </div>`;

                let dropp_off = 'Ofisdən götürülmə'
                if (order.is_wolt) {
                    userContactInfo += `<span style="font-size: 1rem; color: #6c757d;">${order.transaction.recipient_phone}</span>`;
                    dropp_off = `${order.transaction.dropoff_comment}`
                }

                let deliveryInfo = `
                    <div class="d-flex align-items-center">
                        <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                        <div>
                            <span style="font-size: 1.1rem;">${dropp_off}</span><br>
                        </div>
                    </div>`;

                let boxChoiceInfo = '';
                if (order.order_type === 'Paketlənən' && !order.box_choice) {
                    boxChoiceInfo = `
                        <div class="my-3">
                            <span style="font-size: 1.1rem;">Qutu seçimi:</span><br>
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="d-flex align-items-center my-1 cursor-pointer" id="smallBtn-${order.id}">
                                    <i id="smallBtn-${order.id}" class="bi bi-box text-info me-2" style="font-size: 1.5rem;"></i>
                                    <div id="smallBtn-${order.id}" >
                                        <span id="smallBtn-${order.id}" style="font-size: 1rem;">Kiçik</span><br>
                                    </div>
                                </div>
                                <div class="d-flex align-items-center my-1 cursor-pointer" id="mediumBtn-${order.id}">
                                    <i class="bi bi-box text-warning me-2" style="font-size: 1.5rem;" id="mediumBtn-${order.id}"></i>
                                    <div id="mediumBtn-${order.id}">
                                        <span id="mediumBtn-${order.id}" style="font-size: 1rem;">Orta</span><br>
                                    </div>
                                </div>
                                <div class="d-flex align-items-center my-1 cursor-pointer" id="largeBtn-${order.id}">
                                    <i class="bi bi-box text-danger me-2" style="font-size: 1.5rem;" id="largeBtn-${order.id}" ></i>
                                    <div id="largeBtn-${order.id}" >
                                        <span id="largeBtn-${order.id}" style="font-size: 1rem;">Böyük</span><br>
                                    </div>
                                </div>
                            </div>
                        </div>
                                        `;
                } else if (order.order_type === 'Paketlənən' && order.box_choice) {
                    boxChoiceInfo = `
                        <div class="my-3">
                            <span style="font-size: 1.1rem;">Qutu seçimi:</span><br>
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="d-flex align-items-center my-1 cursor-pointer">
                                    <i class="bi bi-check2-square text-success me-2" style="font-size: 1.5rem;"></i>
                                    <div>
                                        <span style="font-size: 1rem;">${order.box_choice}</span><br>
                                    </div>
                                </div>
                            </div>
                        </div>
                                        `;
                } else if (order.box_choice) {
                    boxChoiceInfo = `
                    <div class="my-3">
                        <span style="font-size: 1.1rem;">Qutu seçimi:</span><br>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="d-flex align-items-center my-1 cursor-pointer">
                                <i class="bi bi-check2-square text-success me-2" style="font-size: 1.5rem;"></i>
                                <div>
                                    <span style="font-size: 1rem;">${order.box_choice}</span><br>
                                </div>
                            </div>
                        </div>
                    </div>
                                    `;
                }


                orderModalBody.innerHTML += `
                    <div class="card mb-3">
                        <div class="row g-0">
                            <div class="col-md-4">
                                <img src="${item.product.image}" class="img-fluid rounded-start" style="max-height: 200px;" alt="Product Image">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title">${item.product.title}</h5>
                                    <div class="mb-3">
                                        <span class="d-inline-block me-3 mt-1"><i class="bi bi-clipboard-check text-primary me-1"></i> Quantity: ${item.quantity}</span>
                                        <span class="d-inline-block me-3 mt-1"><i class="bi bi-upc text-info me-1"></i> Barcode: ${item.product.barcode_code}</span>
                                        <span class="d-inline-block mt-1"><i class="bi bi-upc-scan text-warning me-1"></i> Product Code: ${item.product.product_code}</span>
                                    </div>
                                    
                                    ${userContactInfo}
                                    ${deliveryInfo}
                                    ${boxChoiceInfo}
                                    
                                </div>
                            </div>
                        </div>
                    </div>`;
            });
        } else {
            console.error('Order items are undefined or not an array.');
        }
    }

    function renderOrderFooter(order, orderFooter) {
        orderFooter.innerHTML = '';
        let hasOutOfStockItem = true;

        if (order && order.order_items) {
            order.order_items.forEach(item => {
                if (item.product.stock > 0) {
                    hasOutOfStockItem = false
                } else {
                    return hasOutOfStockItem
                }
            });
        } else {
            console.log('Error');
        }

        if (order.order_type === 'Yeni') {
            orderFooter.innerHTML += `
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
              ${hasOutOfStockItem ?
                    `<button type="button" class="btn btn-danger disabled">Stokda yoxdur</button>
                <button id="cancelBtn-${order.id}" type="button" class="btn btn-danger">Ləğv et</button>` :
                    `<button id="cancelBtn-${order.id}" type="button" class="btn btn-danger">Ləğv et</button>
                 <button id="packagedBtn-${order.id}" type="button" class="btn btn-success">Təsdiq et</button>`}
            `;
        } else if (order.order_type === 'Paketlənən') {
            orderFooter.innerHTML += `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                <button id="readyBtn-${order.id}" type="button" class="btn btn-success">Paketləməni tamamla</button>`;
        } else if (order.order_type === 'Təhvilə hazır') {
            orderFooter.innerHTML += `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                <button id="completedBtn-${order.id}" type="button" class="btn btn-success">Sifariş göndərildi</button>`;
        } else if (order.order_type === 'Tamamlanmış') {
            orderFooter.innerHTML += `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                <button type="button" class="btn btn-success disabled">Sifariş tamamlanıb</button>`;
        } else if (order.order_type === 'Ləğv edilib') {
            orderFooter.innerHTML += `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                <button type="button" class="btn btn-danger disabled">Ləğv edilib</button>`;
        } else {
            console.log('Unexpected order_type:', order.order_type);
            orderFooter.innerHTML += `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                <button type="button" class="btn btn-danger disabled">Stokda yoxdur</button>
                <button id="cancelBtn-${order.id}" type="button" class="btn btn-danger">Ləğv et</button>`;
        }
    }

    function setupButtonHandlers(orderId) {
        const orderFooter = document.getElementById(`order-footer-${orderId}`);
        const orderBody = document.getElementById(`order-body-${orderId}`);
        orderFooter.addEventListener('click', async function (event) {
            const buttonId = event.target.id;
            const button = document.getElementById(buttonId);

            if (!button || !buttonId.startsWith('cancelBtn-') && !buttonId.startsWith('packagedBtn-') &&
                !buttonId.startsWith('readyBtn-') && !buttonId.startsWith('completedBtn-')) {
                return;
            }

            const status = getStatusFromButtonId(buttonId);
            if (!status) return;

            await updateOrderStatus(orderId, status);
        });

        orderBody.addEventListener('click', async function (event) {
            const buttonId = event.target.id;
            console.log(buttonId);
            const button = document.getElementById(buttonId);

            if (!button || !buttonId.startsWith('smallBtn-') && !buttonId.startsWith('mediumBtn-') &&
                !buttonId.startsWith('largeBtn-')) {
                return;
            }

            const boxChoice = getChoiceFromButtonId(buttonId);
            if (!boxChoice) return;

            await updateOrderBoxChoice(orderId, boxChoice);
        });

    }

    function getStatusFromButtonId(buttonId) {
        if (buttonId.startsWith('cancelBtn-')) {
            return 'Ləğv edilib';
        } else if (buttonId.startsWith('packagedBtn-')) {
            return 'Paketlənən';
        } else if (buttonId.startsWith('readyBtn-')) {
            return 'Təhvilə hazır';
        } else if (buttonId.startsWith('completedBtn-')) {
            return 'Tamamlanmış';
        } else if (buttonId.startsWith('smallBtn-')) {
            return 'Kiçik'
        } else if (buttonId.startsWith('mediumBtn-')) {
            return 'Orta'
        } else if (buttonId.startsWith('largeBtn-')) {
            return 'Böyük'
        } else {
            return null;
        }
    }

    function getChoiceFromButtonId(buttonId) {
        if (buttonId.startsWith('smallBtn-')) {
            return 'Kiçik'
        } else if (buttonId.startsWith('mediumBtn-')) {
            return 'Orta'
        } else if (buttonId.startsWith('largeBtn-')) {
            return 'Böyük'
        } else {
            return null;
        }
    }

    async function updateOrderStatus(orderId, status) {
        const url = `${BASE_ORDERS_URL}/${orderId}/`;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const updatedOrderData = {
            order_type: status
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
            updateOrderUI(updatedOrder);
        } catch (error) {
            console.error('Error updating order:', error.message);
        }
    }

    async function updateOrderBoxChoice(orderId, boxChoice) {
        const url = `${BASE_ORDERS_URL}/${orderId}/`;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const updatedOrderData = {
            box_choice: boxChoice
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
            updateOrderUI(updatedOrder);
        } catch (error) {
            console.error('Error updating order:', error.message);
        }
    }

    function updateOrderUI(updatedOrder) {
        const orderId = updatedOrder.id;
        const orderFooter = document.getElementById(`order-footer-${orderId}`);
        const orderModalBody = document.getElementById(`order-body-${orderId}`);
        const orderTitle = document.getElementById(`order-title-${orderId}`);
        renderOrderFooter(updatedOrder, orderFooter);
        renderOrderDetails(updatedOrder, orderModalBody, orderTitle)
    }
});
