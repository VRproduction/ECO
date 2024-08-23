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

function sendOrderCreationRequest(tracking_url, tracking_id, wolt_order_reference_id) {
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

function sendPaymentRequest(amount) {
  return new Promise((resolve, reject) => {
    const requestData = {
      amount: amount,
      language: getCookie("django_language") || "az",
      // language: "en",
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

function sendTransactionCreateRequest(value, payment_redirect_url, coupon_code, lat, lon, delivery_amount, recipient_name, recipient_phone, dropoff_comment, shipment_promise_id, is_wolt = false) {
  return new Promise((resolve, reject) => {
    let requestData;

    if (is_wolt) {
      requestData = {
        value: value,
        payment_redirect_url: payment_redirect_url,
        lat: lat,
        lon: lon,
        delivery_amount: delivery_amount,
        recipient_name: recipient_name,
        recipient_phone: recipient_phone,
        dropoff_comment: dropoff_comment,
        shipment_promise_id: shipment_promise_id,
        is_wolt: true
      }
    } else {
      requestData = {
        value: value,
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

function translate(translations, key, params = {}) {
  const language = getCookie("django_language") || "az"; // Dil ayarı yoksa "az" dilini kullan
  let translation = translations[language][key] || key; // Dil desteklenmiyorsa anahtar kelimeyi geri döndür
  // Eğer çeviride parametreler varsa, bunları yerine koy
  Object.keys(params).forEach(param => {
      translation = translation.replace(`{{${param}}}`, params[param]);
  });
  return translation;
}

function updateMapLocationInfo(lat, lon, street) {
  const translations = {
      'en': {
          'delivery_not_available': 'Delivery is not available here!',
          'unknown_error': 'Unknown error occurred.',
          'delivery_time': 'Delivery in {{time_estimate}} minutes',
          // Diğer çeviriler
      },
      'ru': {
          'delivery_not_available': 'Доставка здесь недоступна!',
          'unknown_error': 'Произошла неизвестная ошибка.',
          'delivery_time': 'Доставка за {{time_estimate}} минут',
          // Diğer çeviriler
      },
      'az': {
          'delivery_not_available': 'Bu yerə çatdırılma yoxdur!',
          'unknown_error': 'Bilinməyən bir səhv baş verdi.',
          'delivery_time': '{{time_estimate}} dəqiqəyə çatdırılma',
          // Diğer çeviriler
      }
      // İhtiyaç duyulursa buraya başka diller eklenebilir
  };
  sendShipmentPromises(lat, lon, street)
      .then(data => {
          document.getElementById("map-location-info").innerText = `${street.length > 70 ? street.slice(0, 70) + ' . . .' : street}`;
          document.getElementById("map-location-info").classList.remove("text-danger");
          var delivery_time = document.getElementById("delivery_time");
          if ('error_code' in data) {
              if (data['error_code'] === 'DROPOFF_OUTSIDE_OF_DELIVERY_AREA') {
                  console.log(data);
                  delivery_time.innerText = translate(translations,'delivery_not_available');
                  delivery_time.classList.remove("text-success", "border-success");
                  delivery_time.classList.add("border-1", "border-solid", "border-danger", "rounded", "p-1", "text-danger");
                  document.getElementById("map_total_delivery").innerText = `₼ 0`;
                  document.getElementById("map_discount_price").innerText = `₼ ${localStorageData.discount != 'undefined' ? localStorageData.discountPrice : localStorageData.totalPrice}`;
                  document.getElementById("checkout_address_error").classList.remove('d-none');
                  localStorage.removeItem('delivery_amount');
                  localStorage.removeItem('shipment_promise_id');
              } else {
                  console.log('Bilinmeyen hata:', data['error_code']);
              }
          } else {
              delivery_time.innerText = translate(translations,'delivery_time', { time_estimate: data["time_estimate_minutes"] });
              delivery_time.classList.remove("text-danger", "border-danger");
              delivery_time.classList.add("text-success", "border-success");
              document.getElementById("checkout_address_error").classList.add('d-none');
              localStorage.setItem('delivery_amount', Number(data["price"]["amount"]) / 100);
              localStorage.setItem('shipment_promise_id', data["id"]);

              if (localStorageData.discount != 'undefined') {
                  if (Number(localStorageData.discountPrice) < 30) {
                      document.getElementById("map_total_delivery").innerText = `₼ ${Number(data["price"]["amount"]) / 100}`;
                      document.getElementById("map_discount_price").innerText = `₼ ${localStorageData.discount != 'undefined' ? (Number(localStorageData.discountPrice) + Number(data["price"]["amount"]) / 100).toFixed(2) : (Number(localStorageData.totalPrice) + Number(data["price"]["amount"]) / 100).toFixed(2)}`;
                  } else {
                      document.getElementById("map_total_delivery").innerText = `₼ 0`;
                      document.getElementById("map_discount_price").innerText = `₼ ${localStorageData.discount != 'undefined' ? (Number(localStorageData.discountPrice)).toFixed(2) : (Number(localStorageData.totalPrice)).toFixed(2)}`;
                  }
              } else {
                  if (Number(localStorageData.totalPrice) < 30) {
                      document.getElementById("map_total_delivery").innerText = `₼ ${Number(data["price"]["amount"]) / 100}`;
                      document.getElementById("map_discount_price").innerText = `₼ ${localStorageData.discount != 'undefined' ? (Number(localStorageData.discountPrice) + Number(data["price"]["amount"]) / 100).toFixed(2) : (Number(localStorageData.totalPrice) + Number(data["price"]["amount"]) / 100).toFixed(2)}`;
                  } else {
                      document.getElementById("map_total_delivery").innerText = `₼ 0`;
                      document.getElementById("map_discount_price").innerText = `₼ ${localStorageData.discount != 'undefined' ? (Number(localStorageData.discountPrice)).toFixed(2) : (Number(localStorageData.totalPrice)).toFixed(2)}`;
                  
                  }
              }
          }
          checkCheckoutButtonStatus();
      })
      .catch(error => {
          console.error('Hata:', error);
      });
}

function checkoutButton() {
  var delivery_amount = localStorage.getItem('delivery_amount');
  var total_price_with_delivery;
  var coupon_code = localStorage.getItem('coupon_code');
  if (delivery_amount) {
    if (localStorageData.discount != 'undefined') {
      if (Number(localStorageData.discountPrice) < 30) {
        total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined' ? Number(localStorage.getItem('discountPrice')) + Number(delivery_amount) : Number(localStorage.getItem('totalPrice')) + Number(delivery_amount)}`);
      } else {
        total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined'? Number(localStorage.getItem('discountPrice')) : Number(localStorage.getItem('totalPrice'))}`);
      }
    } else {
      if (Number(localStorageData.totalPrice) < 30) {
        total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined'? Number(localStorage.getItem('discountPrice'))+Number(delivery_amount) : Number(localStorage.getItem('totalPrice'))+Number(delivery_amount)}`);
      } else {
        total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined'? Number(localStorage.getItem('discountPrice')) : Number(localStorage.getItem('totalPrice'))}`);
      }
    }
  } else {
    total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined' ? Number(localStorage.getItem('discountPrice')) : Number(localStorage.getItem('totalPrice'))}`);
  }
  sendPaymentRequest(total_price_with_delivery)
    .then(responseData => {
      if (responseData["status"] === "success") {
        console.log(responseData)
        if (window.location.pathname === '/payment/map/') {
          delivery_data = getDeliveryData()
          sendTransactionCreateRequest(value = responseData["transaction"], payment_redirect_url = responseData["redirect_url"], coupon_code = coupon_code, lat = delivery_data["lat"], lon = delivery_data["lon"], delivery_amount = delivery_data["amount"], recipient_name = delivery_data["recipient_name"], recipient_phone = delivery_data["recipient_phone"], dropoff_comment = delivery_data["dropoff_comment"], shipment_promise_id = delivery_data["shipment_promise_id"], is_wolt = true)
            .then(transactionData => {
              // console.log(transactionData)
              window.location.href = responseData["redirect_url"];
            })
            .catch(error => {
              console.error('HTTP isteği sırasında bir hata oluştu:', error);
            });
        } else {
          sendTransactionCreateRequest(value = responseData["transaction"], payment_redirect_url = responseData["redirect_url"], coupon_code = coupon_code)
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
// function checkoutButton() {
//   var delivery_amount = localStorage.getItem('delivery_amount');
//   var total_price_with_delivery;
//   var coupon_code = localStorage.getItem('coupon_code');
//   if (delivery_amount) {
//     if (localStorageData.discount != 'undefined') {
//       if (Number(localStorageData.discountPrice) < 30) {
//         total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined' ? Number(localStorage.getItem('discountPrice')) + Number(delivery_amount) : Number(localStorage.getItem('totalPrice')) + Number(delivery_amount)}`);
//       } else {
//         total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined'? Number(localStorage.getItem('discountPrice')) : Number(localStorage.getItem('totalPrice'))}`);
//       }
//     } else {
//       if (Number(localStorageData.totalPrice) < 30) {
//         total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined'? Number(localStorage.getItem('discountPrice'))+Number(delivery_amount) : Number(localStorage.getItem('totalPrice'))+Number(delivery_amount)}`);
//       } else {
//         total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined'? Number(localStorage.getItem('discountPrice')) : Number(localStorage.getItem('totalPrice'))}`);
//       }
//     }
//   } else {
//     total_price_with_delivery = Number(`${localStorage.getItem('discount') != 'undefined' ? Number(localStorage.getItem('discountPrice')) : Number(localStorage.getItem('totalPrice'))}`);
//   }
//   if (window.location.pathname === '/payment/map/') {
//     delivery_data = getDeliveryData()
//     console.log(delivery_data)
//     sendTransactionCreateRequest(value = NaN, payment_redirect_url = NaN, coupon_code = coupon_code, lat = delivery_data["lat"], lon = delivery_data["lon"], delivery_amount = delivery_data["amount"], recipient_name = delivery_data["recipient_name"], recipient_phone = delivery_data["recipient_phone"], dropoff_comment = delivery_data["dropoff_comment"], shipment_promise_id = delivery_data["shipment_promise_id"], is_wolt = true)
//       .then(transactionData => {
//         // console.log(transactionData)
//         window.location.href = "http://localhost:8000/payment/success"
//       })
//       .catch(error => {
//         console.error('HTTP isteği sırasında bir hata oluştu:', error);
//       });
//   } else {
//     sendTransactionCreateRequest(value = NaN, payment_redirect_url = NaN, coupon_code = coupon_code)
//       .then(transactionData => {
//         // console.log(transactionData)
//         window.location.href = "http://localhost:8000/payment/success"
//       })
//       .catch(error => {
//         console.error('HTTP isteği sırasında bir hata oluştu:', error);
//       });
//   }
// }