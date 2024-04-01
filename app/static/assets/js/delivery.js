function getDataFromLocalStorage() {
    const data = {
        totalPrice: localStorage.getItem('totalPrice'),
        discount: localStorage.getItem('discount'),
        discountPrice: localStorage.getItem('discountPrice')
    };
    return data;
}
const localStorageData = getDataFromLocalStorage();

localStorage.removeItem('delivery_amount');



function sendShipmentPromises(lat, lon, street) {
    const url = `/payment/map/shipment_promises/?lat=${lat}&lon=${lon}&street=${street}`;
  
    return fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP Hatası! ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        return data;
      })
      .catch(error => {
        console.error('Hata:', error);
        throw error;  
      });
  }

  function sendDeliveryCreationRequest(lat, lon, amount, recipient_name, recipient_phone, shipment_promise_id) {
    return new Promise((resolve, reject) => {
      const requestData = {
        lat: lat,
        lon: lon,
        amount: amount,
        recipient_name: recipient_name,
        recipient_phone: recipient_phone,
        shipment_promise_id: shipment_promise_id,
      };
  
      fetch(`/payment/map/deliveries/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
        },
        body: JSON.stringify(requestData),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('HTTP error, status = ' + response.status);
        }
        return response.json();
      })
      .then(data => {
        resolve(data); // HTTP isteğinin başarılı bir şekilde tamamlanması durumunda veriyi döndür
      })
      .catch(error => {
        reject(error); // Hata durumunda hatayı döndür
      });
    });
  }

  function sendOrderCreationRequest(tracking_url, tracking_id, wolt_order_reference_id){
    return new Promise((resolve, reject) => {
      const requestData = {
        tracking_url: tracking_url,
        tracking_id: tracking_id,
        wolt_order_reference_id: wolt_order_reference_id,
      };
  
      fetch(`/checkout/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
        },
        body: JSON.stringify(requestData),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('HTTP error, status = ' + response.status);
        }
        return response.json();
      })
      .then(data => {
        resolve(data); // HTTP isteğinin başarılı bir şekilde tamamlanması durumunda veriyi döndür
      })
      .catch(error => {
        reject(error); // Hata durumunda hatayı döndür
      });
    });
  }
  
  function sendPaymentRequest(amount){
    return new Promise((resolve, reject) => {
      const requestData = {
        amount: amount,
      };
  
      fetch(`/payment/checkout-request-api-view/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
        },
        body: JSON.stringify(requestData),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('HTTP error, status = ' + response.status);
        }
        return response.json();
      })
      .then(data => {
        resolve(data); // HTTP isteğinin başarılı bir şekilde tamamlanması durumunda veriyi döndür
      })
      .catch(error => {
        reject(error); // Hata durumunda hatayı döndür
      });
    });
  }

  function sendTransactionCreateRequest(transaction, payment_redirect_url, coupon_code, lat, lon, amount, recipient_name, recipient_phone, dropoff_comment, shipment_promise_id, is_wolt = false){
    return new Promise((resolve, reject) => {
      let requestData;

      if (is_wolt) {
        requestData = {
          value: transaction,
          payment_redirect_url: payment_redirect_url,
          lat: lat,
          lon: lon,
          amount: amount,
          recipient_name: recipient_name,
          recipient_phone: recipient_phone,
          dropoff_comment: dropoff_comment,
          shipment_promise_id: shipment_promise_id,
          is_wolt: true
        }
      } else {
        requestData = {
          value: transaction,
          payment_redirect_url: payment_redirect_url,
        }
      }
      if (coupon_code) {
        requestData["coupon_code"] = coupon_code
      }
      console.log(coupon_code)
  
      fetch(`/payment/transactions/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
        },
        body: JSON.stringify(requestData),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('HTTP error, status = ' + response.status);
        }
        return response.json();
      })
      .then(data => {
        resolve(data); // HTTP isteğinin başarılı bir şekilde tamamlanması durumunda veriyi döndür
      })
      .catch(error => {
        reject(error); // Hata durumunda hatayı döndür
      });
    });
  }

function updateMapLocationInfo(lat, lon, street){
    sendShipmentPromises(lat, lon, street)
    .then(data => {
        document.getElementById("map-location-info").innerText = `${street.length > 70 ? street.slice(0,70)+' . . .': street}`
        var delivery_time = document.getElementById("delivery_time")
        if ('error_code' in data) {
            if (data['error_code'] === 'DROPOFF_OUTSIDE_OF_DELIVERY_AREA') {
                delivery_time.innerText = 'Buraya çatdırılma yoxdur!'
                delivery_time.classList.remove("text-success", "border-success")
                delivery_time.classList.add("border-1", "border-solid", "border-danger","rounded", "p-1", "text-danger")
                document.getElementById("map_total_delivery").innerText = `₼ 0`;
                document.getElementById("map_discount_price").innerText = `₼ ${localStorageData.discount != 'undefined'? localStorageData.discountPrice : localStorageData.totalPrice}`;
                document.getElementById("checkout_address_error").classList.remove('d-none');
                localStorage.removeItem('delivery_amount');
                localStorage.removeItem('shipment_promise_id');

            }else {
                console.log('Bilinmeyen hata:', data['error_code']);
            }
        }else {
            delivery_time.innerText = `${data["time_estimate_minutes"]} dəqiqəyə çatdırılma`
            delivery_time.classList.remove("text-danger", "border-danger")
            delivery_time.classList.add("text-success", "border-success")
            document.getElementById("checkout_address_error").classList.add('d-none');
            document.getElementById("map_total_delivery").innerText = `₼ ${Number(data["price"]["amount"])/100}`;
            localStorage.setItem('delivery_amount', Number(data["price"]["amount"])/100);
            localStorage.setItem('shipment_promise_id', data["id"]);
            document.getElementById("map_discount_price").innerText = `₼ ${localStorageData.discount != 'undefined'? Number(localStorageData.discountPrice)+Number(data["price"]["amount"])/100 : Number(localStorageData.totalPrice)+Number(data["price"]["amount"])/100}`;

            console.log(data)
        }
        checkCheckoutButtonStatus()
    })
    .catch(error => {
        console.error('Hata:', error);
    });
  }
  
  // function checkStockStatus(amount){
  //   return new Promise((resolve, reject) => {
  //     fetch(`/check-stock-status/`, {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //         'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
  //       },
  //     })
  //     .then(response => {
  //       if (!response.ok) {
  //         throw new Error('HTTP error, status = ' + response.status);
  //       }
  //       return response.json();
  //     })
  //     .then(data => {
  //       resolve(data); // HTTP isteğinin başarılı bir şekilde tamamlanması durumunda veriyi döndür
  //     })
  //     .catch(error => {
  //       reject(error); // Hata durumunda hatayı döndür
  //     });
  //   });
  // }

  function checkoutButton(){
    var delivery_amount = localStorage.getItem('delivery_amount');
    var total_price_with_delivery;
    var coupon_code = localStorage.getItem('coupon_code');
    if (delivery_amount) {
        total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined'? Number(localStorage.getItem('discountPrice'))+Number(delivery_amount) : Number(localStorage.getItem('totalPrice'))+Number(delivery_amount)}`);
    }else{
      total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined'? Number(localStorage.getItem('discountPrice')) : Number(localStorage.getItem('totalPrice'))}`);
    }
    sendPaymentRequest(total_price_with_delivery)
    .then(responseData => {
        if (responseData["status"] === "success") {
            console.log(responseData)
            if (window.location.pathname === '/payment/map/') {
              delivery_data = getDeliveryData()
              sendTransactionCreateRequest(transaction = responseData["transaction"], payment_redirect_url = responseData["redirect_url"], coupon_code = coupon_code, lat = delivery_data["lat"], lon = delivery_data["lon"], amount = delivery_data["amount"], recipient_name = delivery_data["recipient_name"], recipient_phone = delivery_data["recipient_phone"], dropoff_comment = delivery_data["dropoff_comment"], shipment_promise_id = delivery_data["shipment_promise_id"], is_wolt = true)
              .then(transactionData => {
                  // console.log(transactionData)
                  window.location.href = responseData["redirect_url"];
              })
              .catch(error => {
                  console.error('HTTP isteği sırasında bir hata oluştu:', error);
              });
            }else{
              sendTransactionCreateRequest(transaction = responseData["transaction"], payment_redirect_url = responseData["redirect_url"], coupon_code = coupon_code)
              .then(transactionData => {
                  // console.log(transactionData)
                  window.location.href = responseData["redirect_url"];
              })
              .catch(error => {
                  console.error('HTTP isteği sırasında bir hata oluştu:', error);
              });
            }
        }
    })
    .catch(error => {
        console.error('HTTP isteği sırasında bir hata oluştu:', error);
    });
}