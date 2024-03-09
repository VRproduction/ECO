function getDataFromLocalStorage() {
    const data = {
        totalPrice: localStorage.getItem('totalPrice'),
        discount: localStorage.getItem('discount'),
        discountPrice: localStorage.getItem('discountPrice')
    };
    return data;
}

// localStorage'deki verileri alın
const data = getDataFromLocalStorage();

document.getElementById("map_total_price").innerText = "₼ " + data.totalPrice;
document.getElementById("map_discount").innerText = `₼ ${data.discount != 'undefined'? data.discount : 0}`;
document.getElementById("map_discount_price").innerText = `₼ ${data.discount != 'undefined'? data.discountPrice : data.totalPrice}`;

function getAddressInfo(streetName) {
    return new Promise((resolve, reject) => {
        // API'den sokak adına göre adres bilgisi al
        var url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(streetName)+'&accept-language=az';
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    // Azerbaycan'a ait adreslerin listelenmesi için filter işlemi
                    console.log(data)
                    const azerbaijanAddresses = data.filter(result => result.display_name.split(',').pop().trim() === 'Azərbaycan');
                    resolve(azerbaijanAddresses);
                } else {
                    reject('Adres bulunamadı');
                }
            })
            .catch(error => {
                reject('Hata:', error);
            });
    });
}

// Sokak adı input elementini seçiyoruz
const streetInput = document.getElementById('streetInput');

// Sokak adı inputunda her bir klavye tuşuna basıldığında işlenecek fonksiyon
const addressResultsDiv = document.getElementById('addressResults');

// Sokak adı inputunda her bir klavye tuşuna basıldığında işlenecek fonksiyon
streetInput.addEventListener('input', function() {
    const streetName = streetInput.value.trim(); 

    if (streetName.length >= 3) {
        getAddressInfo(streetName)
            .then(data => {
                addressResultsDiv.innerHTML = '';
                if (data.length > 0) {
                    const ul = document.createElement('ul');
                    data.forEach((result, index) => {
                        const li = document.createElement('li');
                        li.innerHTML = `<img style="width: 25px;" src="/static/assets/imgs/map-setting.png" alt=""><span class="ms-2">${result.display_name.split(', ').slice(0, -4).join(', ')}</span>`
                        li.classList.add("text-dark")
                        li.classList.add("my-2")
                        li.classList.add("mx-3")
                        li.classList.add("p-1")
                        li.classList.add("d-flex")
                        li.classList.add("align-items-center")
                        li.addEventListener('click', function() {
                            // Seçilen adresin içeriğini al ve input değerine ata
                            streetInput.value = result.display_name.split(', ').slice(0, -4).join(', ');
                        });
                        ul.appendChild(li);
                    });
                    addressResultsDiv.appendChild(ul);
                    addressResultsDiv.classList.remove("py-2")
                    addressResultsDiv.classList.remove("px-3")
                } else {
                    addressResultsDiv.textContent = 'Adress tapılmadı';
                    addressResultsDiv.classList.add("py-2")
                    addressResultsDiv.classList.add("px-3")
                }
                addressResultsDiv.classList.add("border")
                addressResultsDiv.classList.add("mt-2")
                addressResultsDiv.classList.add("rounded")
            })
            .catch(error => {
                console.error('Hata:', error);
            });

    } else {
        addressResultsDiv.textContent = 'Minimum 3 hərf daxil edin!';
    }
});

function addRadio(marker = false) {
    // Yeni bir radio düyməsi yarat
    var newRadio = document.createElement('div');
    newRadio.classList.add('form-check', 'my-2', 'ms-1')
    if (marker == true){
        var markerCoordinates = newMarker.getLatLng();
        locationInfo(markerCoordinates.lat, markerCoordinates.lng)
        .then(address => {
            newRadio.innerHTML = `
            <input class="form-check-input" type="radio" name="exampleRadios" id="address"
                value="option2">
            <label id="option1Label" class="form-check-label text-dark" for="address">
                ${address}
            </label>
        `   
        })
        .catch(error => {
            console.error('Hata:', error);
        });
    }else{
        newRadio.innerHTML = `
            <input class="form-check-input" type="radio" name="exampleRadios" id="address"
                value="option2">
            <label id="option1Label" class="form-check-label text-dark" for="address">
                ${streetInput.value}
            </label>
        `   
    }
    
    
    document.querySelector('#radio-list').appendChild(newRadio);
    closeMap()
}