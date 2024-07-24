const BASE_ORDERS_URL = `${location.origin}/custom-admin/api/orders`;

document.addEventListener('DOMContentLoaded', function () {
    const modals = document.querySelectorAll('[id^="exampleScrollableModal-"]');

    modals.forEach(async function (modal) {
        const orderId = modal.id.split('-')[1];
        const orderModalBody = document.getElementById(`order-body-${orderId}`);
        const orderTitle = document.getElementById(`order-title-${orderId}`);
        const orderFooter = document.getElementById(`order-footer-${orderId}`);
        const orderType = document.getElementById(`order-type-${orderId}`)

        const order = await fetchOrders(orderId);

        if (order) {
            renderOrderDetails(order, orderModalBody, orderTitle, orderType);
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

    function renderOrderDetails(order, orderModalBody, orderTitle, orderType) {
        orderModalBody.innerHTML = '';
        orderTitle.innerHTML = `Sifariş No: ${order.id}`;
        orderType.innerHTML = ''
        orderType.innerHTML = `<i class='bx bxs-circle me-1'></i>${order.order_type}`

        // User Contact Information
        let userContactInfo = `
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title mb-3">Müştəri məlumatları</h5>
                    <div class="d-flex align-items-center mb-3">
                        <div>
                            <i class="bi bi-person-fill me-2 text-success" style="font-size: 1.2rem;"></i>
                            <span style="font-size: 1.1rem;">${order.user.full_name}</span><br>
                            <i class="bi bi-envelope-at-fill me-2 text-warning"></i>
                            <span style="font-size: 1rem; color: #6c757d;">${order.user.email}</span><br>
                            ${order.is_wolt ?
                `<i class="bi bi-telephone-forward-fill me-3 text-info"></i><span style="font-size: 1rem; color: #6c757d;">${order.transaction.recipient_phone}</span>`
                : ''}
                        </div>
                    </div>
                </div>
            </div>`;

        // Delivery Information
        let dropOffInfo = 'Ofisdən götürülmə';
        if (order.is_wolt) {
            dropOffInfo = `${order.transaction.dropoff_comment}`;
        }

        let deliveryInfo = `
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title mb-3">Çatdırılma</h5>
                    <div class="d-flex align-items-center">
                        <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                        <div>
                            <span style="font-size: 1.1rem;">${dropOffInfo}</span><br>
                        </div>
                    </div>
                </div>
            </div>`;

        // Box Choice Information
        let boxChoiceInfo = '';
        if (order.order_type === 'Paketlənən' && !order.box_choice) {
            boxChoiceInfo = `
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Qutu Seçimi</h5>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="d-flex align-items-center my-1 cursor-pointer" id="smallBtn-${order.id}">
                                <i id="smallBtn-${order.id}" class="bi bi-box text-info me-2" style="font-size: 1.5rem;"></i>
                                <div id="smallBtn-${order.id}">
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
                                <i class="bi bi-box text-danger me-2" style="font-size: 1.5rem;" id="largeBtn-${order.id}"></i>
                                <div id="largeBtn-${order.id}">
                                    <span id="largeBtn-${order.id}" style="font-size: 1rem;">Böyük</span><br>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
        } else if (order.order_type === 'Paketlənən' && order.box_choice) {
            boxChoiceInfo = `
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Qutu Seçimi</h5>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="d-flex align-items-center my-1">
                                <i class="bi bi-check2-square text-success me-2" style="font-size: 1.5rem;"></i>
                                <div>
                                    <span style="font-size: 1rem;">${order.box_choice}</span><br>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
        } else if (order.box_choice) {
            boxChoiceInfo = `
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Qutu Seçimi</h5>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="d-flex align-items-center my-1">
                                <i class="bi bi-check2-square text-success me-2" style="font-size: 1.5rem;"></i>
                                <div>
                                    <span style="font-size: 1rem;">${order.box_choice}</span><br>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
        }

        // Append user info and order details to orderModalBody
        orderModalBody.innerHTML = `
            ${userContactInfo}
            ${deliveryInfo}
            ${boxChoiceInfo}`;

        // Render each order item
        if (order && order.order_items && Array.isArray(order.order_items)) {
            order.order_items.forEach(item => {
                orderModalBody.innerHTML += `
                    <div class="card mb-3" id="invoiceBtn-${order.id}">
                        <div class="row g-0">
                            <div class="col-md-4">
                                <img src="${item.product.image}" class="img-fluid rounded-start" style="max-height: 200px;" alt="Product Image">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title">${item.product.title}</h5>
                                    <div class="mb-3">
                                        <span class="d-inline-block me-3 mt-1"><i class="bi bi-clipboard-check text-primary me-1"></i> Kəmiyyət: ${item.quantity}</span>
                                        <span class="d-inline-block me-3 mt-1"><i class="bi bi-upc text-info me-1"></i> Barkod: ${item.product.barcode_code}</span>
                                        <span class="d-inline-block mt-1"><i class="bi bi-upc-scan text-warning me-1"></i> Məhsul Kodu: ${item.product.product_code}</span>
                                    </div>
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

        if (order.order_items.length > 0 && order.order_type === 'Yeni') {
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
                <button id="readyBtn-${order.id}" type="button" class="btn btn-success">Paketləməni tamamla</button>
                <button id="invoiceBtn-${order.id}" type="button" class="btn btn-success">Qaimə yüklə</button>`;
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
            orderFooter.innerHTML += `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bağla</button>
                <button type="button" class="btn btn-danger disabled">Sifarişdə məhsul qeydə alınmayıb</button>`
        }
    }

    function setupButtonHandlers(orderId) {
        const orderFooter = document.getElementById(`order-footer-${orderId}`);
        const orderBody = document.getElementById(`order-body-${orderId}`);
        orderFooter.addEventListener('click', async function (event) {
            const buttonId = event.target.id;
            const button = document.getElementById(buttonId);

            if (!button || !buttonId.startsWith('cancelBtn-') && !buttonId.startsWith('packagedBtn-') &&
                !buttonId.startsWith('readyBtn-') && !buttonId.startsWith('completedBtn-') && !buttonId.startsWith('invoiceBtn-')) {
                return;
            }

            const status = getStatusFromButtonId(buttonId);
            if (!status) return;

            if (status === 'Invoice') {
                generatePDF(orderId)
            } else {
                await updateOrderStatus(orderId, status);
            }
        });

        orderBody.addEventListener('click', async function (event) {
            const buttonId = event.target.id;
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
        } else if (buttonId.startsWith('invoiceBtn-')) {
            return 'Invoice'
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
        const orderType = document.getElementById(`order-type-${orderId}`)
        renderOrderFooter(updatedOrder, orderFooter);
        renderOrderDetails(updatedOrder, orderModalBody, orderTitle, orderType)
    }

    async function generatePDF(orderId) {
        const order = await fetchOrders(orderId)
        const content = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Qaimə #${orderId}</title>
            <style>
                body {
                    font-family: 'Roboto', sans-serif;
                    background-color: #fff;
                    margin: 0;
                    padding: 0;
                    color: #333;
                }
    
                .invoice-container {
                    max-width: 800px;
                    margin: 20px auto;
                    background-color: #f8f9fa;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    border-radius: 5px;
                    padding: 30px;
                }
    
                .invoice-header {
                    background-color: #4CAF50;
                    color: #fff;
                    text-align: center;
                    padding: 20px 0;
                    border-radius: 5px 5px 0 0;
                }
    
                .invoice-header h2 {
                    margin: 0;
                    font-size: 28px;
                    font-weight: 500;
                    letter-spacing: 1px;
                }
    
                .invoice-body {
                    padding: 30px;
                    margin-bottom: 30px;
                }
    
                .invoice-body table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }
    
                .invoice-body th,
                .invoice-body td {
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                    text-align: left;
                }
    
                .invoice-body th,
                .prodduct-table th {
                    background-color: #f2f2f2;
                    color: #333;
                    font-size: 14px;
                    font-weight: bold;
                }
    
                .user-details,
                .order-details,
                .product-table {
                    margin-bottom: 70px;
                }
    
                .user-details h2,
                .order-details h2 {
                    font-size: 20px;
                    font-weight: 500;
                    color: #4CAF50;
                    margin-bottom: 10px;
                }
    
                .product-table {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
    
                .product-table th {
                    background-color: #f2f2f2;
                    padding: 15px;
                }
    
                .total-section {
                    margin-top: 60px;
                    text-align: right;
                }
    
                .total-section h2 {
                    color: #E53935;
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 0;
                }
    
                .green-text {
                    color: #4CAF50;
                    font-size: 20px;
                }
    
                .invoice-footer {
                    background-color: #f0f0f0;
                    text-align: center;
                    padding: 15px 0;
                    border-radius: 0 0 5px 5px;
                }
    
                .invoice-footer p {
                    margin: 0;
                    font-size: 12px;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <div class="invoice-container">
                <div class="invoice-header">
                    <h2>Qaimə #${orderId}</h2>
                </div>
                <div class="invoice-body">
                    <div class="user-details">
                        <h2>Müştəri məlumatları</h2>
                        <table>
                            <tr>
                                <th>Ad, Soyad</th>
                                <td>${order.user.full_name}</td>
                            </tr>
                            <tr>
                                <th>Email</th>
                                <td>${order.user.email}</td>
                            </tr>
                            ${order.is_wolt ? 
                            `<tr>
                                <th>Əlaqə nömrəsi</th>
                                <td>${order.transaction.recipient_phone}</td>
                            </tr>` : null
                            }
                            <tr>
                                <th>Sifariş tarixi</th>
                                <td>${order.created_at}</td>
                            </tr>
                        </table>
                    </div>
                    <h2 class="green-text">Sifariş</h2>
                    <table class="product-table">
                        <thead>
                            <tr>
                                <th>Məhsul</th>
                                <th>Barkod</th>
                                <th>Kəmiyyət</th>
                                <th>Qiymət</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${order.order_items.map(item => `
                                <tr>
                                    <td>${item.product.title}</td>
                                    <td>${item.product.barcode_code}</td>
                                    <td>${item.quantity}</td>
                                    <td>${item.product.price.toFixed(2)} AZN</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                    <div class="total-section">
                        <h2>Ümumi məbləğ: ${order.total_amount.toFixed(2)} AZN</h2>
                    </div>
                </div>
                <div class="invoice-footer">
                    <p>Generated on ${new Date().toLocaleDateString()}</p>
                </div>
            </div>
        </body>
        </html>
        `;

        html2pdf()
            .from(content)
            .set({
                filename: `invoice_${orderId}.pdf`,
                html2canvas: { scale: 2 },
                jsPDF: { orientation: 'portrait', unit: 'in', format: 'letter' }
            })
            .save();
    }
});
