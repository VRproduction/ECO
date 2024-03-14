function getDataFromLocalStorage() {
    const data = {
        totalPrice: localStorage.getItem('totalPrice'),
        discount: localStorage.getItem('discount'),
        discountPrice: localStorage.getItem('discountPrice')
    };
    return data;
}
const localStorageData = getDataFromLocalStorage();

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

function sendDeliveryCreation(lat, lon, amount, recipient_name, recipient_phone, shipment_promise_id){
  const requestData = {
    lat: lat,
    lon: lon,
    amount: amount,
    recipient_name: recipient_name,
    recipient_phone: recipient_phone,
    shipment_promise_id: shipment_promise_id,
  };
  fetch(`/payment/map/deliveries/`,{
      method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Add this function to get the CSRF token
        },
        body: JSON.stringify(requestData),
  })
  .then(data => {
    console.log(data)
    if (data) {
      // console.log(data)        
    } else {
       console.log('Bir hata oluştu.');
    }
  })
  .catch(error => console.error('Error:', error));

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
            document.getElementById("map_total_delivery").innerText = `₼ ${data["price"]["amount"]}`;
            localStorage.setItem('delivery_amount', data["price"]["amount"]);
            localStorage.setItem('shipment_promise_id', data["id"]);
            document.getElementById("map_discount_price").innerText = `₼ ${localStorageData.discount != 'undefined'? Number(localStorageData.discountPrice)+Number(data["price"]["amount"]) : Number(localStorageData.totalPrice)+Number(data["price"]["amount"])}`;

            console.log(data)
        }
        checkCheckoutButtonStatus()
    })
    .catch(error => {
        console.error('Hata:', error);
    });
  }
  