let eco_lan = 40.3656998
let eco_lon = 49.8227329

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



//******************************************************************* */
//                           Main MAP                                 */
//******************************************************************* */

var map = L.map('map').setView([40.36815635,  49.8210362], 15);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);
var marker = L.marker([eco_lan, eco_lon]).addTo(map);
var circle = L.circle([eco_lan, eco_lon], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 100
}).addTo(map);
marker.bindPopup("ECO").openPopup();

var popup = L.popup();

var previousMarker = null; // Önceki işaretçiyi tutacak değişken

// Haritaya tıklandığında bir işaretçi (marker) oluşturan fonksiyon
var markerSelected = null; // Define marker variable outside to make it accessible globally
function createMarker(lat, lon, selectedRadio) {
    // Remove previous marker if exists
    if (markerSelected !== null) {
        map.removeLayer(markerSelected);
    }
    // Create new marker at given coordinates
    if (selectedRadio !== document.querySelector("#location1")) {
        markerSelected = L.marker([lat, lon]).addTo(map);
        markerSelected.bindPopup("Seçdiyiniz məkan").openPopup();
    }
    map.setView([lat, lon], 14);
}

function onMapClick(e) {
    // Önceki işaretçiyi kaldır
    if (previousMarker !== null) {
        map.removeLayer(previousMarker);
    }

    // Yeni işaretçi oluştur
    var clickedMarker = L.marker(e.latlng).addTo(map);
    clickedMarker.bindPopup("Buranı seçdiniz.").openPopup();

    // Önceki işaretçiyi güncelle
    previousMarker = clickedMarker;
    locationInfo(e.latlng.lat, e.latlng.lng)
    // Ters jeokodlama yapmak için Nominatim servisini kullan
    
}
function locationInfo(lat, lon){
    return new Promise((resolve, reject) => {
        var url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat=' + lat + '&lon=' + lon + '&accept-language=az'; // Azerbaycanca dilini kullanmak için
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data && data.display_name) {
                    const addressComponents = data.display_name.split(', ');
                    const filteredAddress = addressComponents.slice(0, -4);
                    const newAddress = filteredAddress.join(', ');
                    resolve(newAddress); // Adres bilgisini resolve ile döndür
                } else {
                    reject('Geçersiz veri');
                }
            })
            .catch(error => {
                reject('Hata:', error);
            });
    });
}

// Haritaya tıklama olayını dinleyen olay dinleyici ekleyin
// map.on('click', onMapClick);

// Kullanıcının konumunu güncelleyen fonksiyon
function updateCurrentLocation(onload = false) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            let currentInput = document.getElementById("location1")
            currentInput.setAttribute("data-lat", latitude);
            currentInput.setAttribute("data-lon", longitude);



            // Eğer kullanıcı daha önce bir işaretçi eklediyse kaldır
            if (currentLocationMarker) {
                map.removeLayer(currentLocationMarker);
                map.removeLayer(currentLocationCircle);
                map2.removeLayer(currentLocationMarker);
                map2.removeLayer(currentLocationCircle);
            }

            var icon = L.icon({
                iconUrl: '/static/assets/imgs/location.png', // Ok simgesi resmi
                iconSize: [38, 38], // Resim boyutu
                iconAnchor: [19, 38] // Okun konumu
            });

            currentLocationMarker = L.marker([latitude, longitude], {icon: icon, rotationAngle: position.coords.heading}).addTo(map);
            currentLocationMarker = L.marker([latitude, longitude], {icon: icon, rotationAngle: position.coords.heading}).addTo(map2);

            currentLocationCircle = L.circle([latitude, longitude], {
                color: 'transparent',
                fillColor: 'transparent',
                fillOpacity: 0.5,
                radius: 100
            }).addTo(map);
            currentLocationCircle = L.circle([latitude, longitude], {
                color: 'transparent',
                fillColor: 'transparent',
                fillOpacity: 0.5,
                radius: 100
            }).addTo(map2);

            if(onload == true){
                map.setView([latitude, longitude], 14); // Konumu merkez al ve yakınlaştır
                map2.setView([latitude, longitude], 14); // Konumu merkez al ve yakınlaştır

                // document.getElementById("map-location-info").innerText = locationInfo(latitude, longitude)
                locationInfo(latitude, longitude)
                .then(address => {
                    currentInput.value = address;
                    document.getElementById("option1Label").innerHTML = `${address} <span class="text-danger">(* Hal hazırda olduğunuz məkan)</span>`
                    updateMapLocationInfo(latitude, longitude, address)

                })
                .catch(error => {
                    console.error('Hata:', error);
                });

            }
        });
    } else {
        alert("Tarayıcınız konum belirleme özelliğini desteklemiyor.");
        console.log("geolocation xeta")

    }
}

var currentLocationMarker = null;
var currentLocationCircle = null;

window.onload = updateCurrentLocation(onload = true)
// Konumu güncelleme işlemini belirli aralıklarla yapmak için setInterval kullanarak fonksiyonu çağırın
setInterval(updateCurrentLocation, 5000); // Her 10 saniyede bir güncelle
function centerMapToCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            map.setView([latitude, longitude], 14); // Konumu merkez al ve yakınlaştır
            map2.setView([latitude, longitude], 14); // Konumu merkez al ve yakınlaştır
        });
    } else {
        alert("Tarayıcınız konum belirleme özelliğini desteklemiyor.");
        console.log("geolocation xeta")
    }
}

//******************************************************************* */
//                            Main MAP END                            */
//******************************************************************* */


//******************************************************************* */
//                           Modal MAP                                */
//******************************************************************* */
var map2 = L.map('map2').setView([40.36815635,  49.8210362], 15);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map2);

    var marker2 = L.marker([eco_lan, eco_lon]).addTo(map2);
    var circle2 = L.circle([eco_lan, eco_lon], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 100
    }).addTo(map2);
    marker2.bindPopup("ECO").openPopup();
    
    var popup2 = L.popup();

    var mapCenter = map2.getCenter();

    // Yeni işaretçiyi ekranın ortasına sabitle
    var newMarker = L.marker(mapCenter).addTo(map2);

    // Yeni işaretçi konumunu değiştirdiğinizde enlem ve boylam değerlerini güncelle
    map2.on('move', function(){
        var newLatLng = map2.getCenter();
        newMarker.setLatLng(newLatLng);
    });   
//******************************************************************* */
//                           Modal MAP End                            */
//******************************************************************* */


function getAddressInfo(streetName) {
    return new Promise((resolve, reject) => {
        // API'den sokak adına göre adres bilgisi al
        var url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(streetName)+'&accept-language=az';
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    // Azerbaycan'a ait adreslerin listelenmesi için filter işlemi
                    const azerbaijanAddresses = data.filter(result => result.display_name.split(',').pop().trim() === 'Azərbaycan').slice(0, 5);
                    console.log(azerbaijanAddresses)

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
//Secilmis inputun hazirki inputla eyniliyini yoxlayir. Eger eyni deyilse ve ya bosdursa bitton disabled olmalidi
const addressResultsDiv = document.getElementById('addressResults');
let canAddRadioList = false;
let selectedInputValue;
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
                        li.innerHTML = `<img style="width: 25px;" src="/static/assets/imgs/map-setting.png" alt=""><span class="ms-2">${result.display_name}</span>`
                        // li.innerHTML = `<img style="width: 25px;" src="/static/assets/imgs/map-setting.png" alt=""><span class="ms-2">${result.display_name.split(', ').slice(0, -4).join(', ')}</span>`
                        li.classList.add("text-dark")
                        li.classList.add("my-2")
                        li.classList.add("mx-3")
                        li.classList.add("p-1")
                        li.classList.add("d-flex")
                        li.classList.add("align-items-center")
                        li.addEventListener('click', function() {
                            // Seçilen adresin içeriğini al ve input değerine ata
                            // streetInput.value = result.display_name.split(', ').slice(0, -4).join(', ');
                            streetInput.value = result.display_name
                            streetInput.setAttribute("data-lat", result.lat);
                            streetInput.setAttribute("data-lon", result.lon);
                            selectedInputValue = result.display_name
                            // selectedInputValue = result.display_name.split(', ').slice(0, -4).join(', ');
                            canAddRadioList = true
                            document.getElementById("modalAddressBtn").disabled = false;

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
            });

    } else {
        addressResultsDiv.textContent = 'Minimum 3 hərf daxil edin!';
        addressResultsDiv.classList.add("py-2")
        addressResultsDiv.classList.add("px-3")
        canAddRadioList = false
    }
    if (streetInput.value === selectedInputValue) {
        canAddRadioList = true
        document.getElementById("modalAddressBtn").disabled = false;
    } else {
        canAddRadioList = false
        document.getElementById("modalAddressBtn").disabled = true;
    }
    let errorDiv = document.getElementById("addressError")
    errorDiv.innerText = ""
    errorDiv.classList.remove("text-danger", "mb-2")
});

//***************************************************************** */
//Map modalinin aclib baglanmasi
var map2Shown = false; // Harita başlangıçta gizli

function closeMap(for_add = false){
    document.getElementById("modalMap").style.display = "none"
    document.getElementById("modalMap").style.opacity = 0
    if (map2Shown) {
        hideMap();
        if (for_add == false) {
            showAddressModal()
        }
    } else {
        showMap();
        hideAddressModal()
        // hideDeliveryModal()
    }
    if (for_add == false) {
        map2Shown = false // Durumu tersine çevir
    }else{
        map2Shown = !map2Shown; // Durumu tersine çevir
    }
    var modalElement = document.getElementById("modalMap");
    var modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
}


function toggleMap() {
    map2Shown = false;
    hideAddressModal()
    document.getElementById("modalMap").style.display = "block"
    document.getElementById("modalMap").style.opacity = 1
    if (map2Shown) {
        hideMap();
    } else {
        showMap();
    }
    map2Shown = !map2Shown; // Durumu tersine çevir
}

function showMap() {
    document.getElementById("map2-container").style.display = "block"; // Haritayı göster
    map2.invalidateSize(); // Harita boyutunu güncelle
}

function hideMap() {
    document.getElementById("map2-container").style.display = "none"; // Haritayı gizle

}
//Map modalinin aclib baglanmasi
//***************************************************************** */


//***************************************************************** */
//Address modalinin aclib baglanmasi

function showAddressModal(){
    var modalElement = document.getElementById("modalAddress");
    var modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.show();
    hideDeliveryModal()
}
function hideAddressModal(){
    var modalElement = document.getElementById("modalAddress");
    var modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
    showDeliveryModal()
}

//Address modalinin aclib baglanmasi
//***************************************************************** */

//Delivery modalinin aclib baglanmasi

function showDeliveryModal(){
    var modalElement = document.getElementById("modelDelivery");
    var modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.show();
}
function hideDeliveryModal(){
    var modalElement = document.getElementById("modelDelivery");
    var modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
}

//Delivery modalinin aclib baglanmasi
//***************************************************************** */


let radioList = [];

function addRadio(marker = false) {
    var newRadio = document.createElement('div');
    newRadio.classList.add('form-check', 'my-2', 'ms-1', 'd-flex', 'justify-content-between');
    var radioId = generateUniqueId();

    if (marker == true) {
        var markerCoordinates = newMarker.getLatLng();
        locationInfo(markerCoordinates.lat, markerCoordinates.lng)
            .then(address => {
                if (!radioList.some(item => item.address === address)) {
                    var radioData = {
                        address: address,
                        lat: markerCoordinates.lat,
                        lon: markerCoordinates.lng
                    };

                    newRadio.innerHTML = `
                        <div class="w-100"> 
                            <input class="form-check-input" type="radio" name="location" id="location${radioId}"
                                value="${address}" data-lat="${markerCoordinates.lat}" data-lon="${markerCoordinates.lng}">
                            <label class="form-check-label text-dark" for="location${radioId}">
                                ${address}
                            </label>
                        </div>
                    `;

                    radioList.push(radioData);
                    saveToLocalStorage('radioList', radioList);
                    var modalElement = document.getElementById("modalAddress");
                    var modalInstance = bootstrap.Modal.getInstance(modalElement);
                    modalInstance.hide();
                    document.querySelector('#radio-list').appendChild(newRadio);

                    // Silme düğmesini ekle
                    var deleteButton = addRadioDeleteButton(radioData);
                    newRadio.appendChild(deleteButton);

                    closeMap(for_add = true);
                }
            })
            .catch(error => {
                console.error('Hata:', error);
            });

    } else {
        if (canAddRadioList == true) {
            let streetValue = streetInput.value;
            let errorDiv = document.getElementById("addressError")
            if (!radioList.some(item => item.address === streetValue)) {
                var radioData = {
                    address: streetValue,
                    lat: streetInput.getAttribute("data-lat"),
                    lon: streetInput.getAttribute("data-lon")
                };

                newRadio.innerHTML = `
                    <div class="w-100">
                        <input class="form-check-input" type="radio" name="location" id="location${radioId}"
                            value="${streetValue}" data-lat="${streetInput.getAttribute("data-lat")}" data-lon="${streetInput.getAttribute("data-lon")}">
                        <label class="form-check-label text-dark" for="location${radioId}">
                            ${streetValue}
                        </label>
                    </div>
                `;

                radioList.push(radioData);
                saveToLocalStorage('radioList', radioList);
                errorDiv.innerText = "";
                errorDiv.classList.remove("text-danger", "mb-2");
                document.querySelector('#radio-list').appendChild(newRadio);

                // Silme düğmesini ekle
                var deleteButton = addRadioDeleteButton(radioData);
                newRadio.appendChild(deleteButton);

                hideAddressModal();
            } else {
                errorDiv.innerText = "* Bu adres zaten eklenmiş!";
                errorDiv.classList.add("text-danger", "mb-2");
            }
        }
    }
}

function saveToLocalStorage(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
}

function addRadioDeleteButton(radioData) {
    var deleteButton = document.createElement('button');
    deleteButton.innerHTML = '<img src="/static/assets/imgs/rubbish-bin.png" alt="" style="width:20px;">'; // Silme simgesi ekleniyor
    deleteButton.classList.add("border-0", "bg-transparent", "m-0", "p-0")
    deleteButton.addEventListener('click', function() {
        deleteRadio(radioData);
    });

    return deleteButton;
}
function deleteRadio(radioData) {
    // Radio listesinden radyoyu kaldır
    radioList = radioList.filter(item => item.address !== radioData.address);

    // LocalStorage'deki veriyi güncelle
    saveToLocalStorage('radioList', radioList);

    // Radio butonlarını güncelle
    updateRadioButtons();
}

function updateRadioButtons() {
    var radioListContainer = document.getElementById('radio-list');

    // İlk input elementini sakla
    var firstRadio = radioListContainer.firstElementChild;

    // Var olan içeriği temizle
    radioListContainer.innerHTML = '';

    // Eğer ilk input elementi varsa tekrar ekle
    if (firstRadio) {
        radioListContainer.appendChild(firstRadio);
    }

    for (var i = 0; i < radioList.length; i++) {
        var radioId = generateUniqueId();
        var newRadio = document.createElement('div');
        newRadio.classList.add('form-check', 'my-2', 'ms-1', 'd-flex', 'justify-content-between');

        newRadio.innerHTML = `
            <div class="w-100">
                <input class="form-check-input" type="radio" name="location" id="location${radioId}"
                    value="${radioList[i].address}" data-lat="${radioList[i].lat}" data-lon="${radioList[i].lon}">
                <label class="form-check-label text-dark" for="location${radioId}">
                    ${radioList[i].address}
                </label>
            </div>
        `;

        // Silme düğmesini ekleyin ve radyo butonuyla birlikte yerleştirin
        var deleteButton = addRadioDeleteButton(radioList[i]);
        newRadio.appendChild(deleteButton);

        radioListContainer.appendChild(newRadio);
    }
}


document.addEventListener("DOMContentLoaded", function () {
    // Sayfa yüklendiğinde localStorage'den veriyi çek
    var storedRadioList = getFromLocalStorage('radioList');

    if (storedRadioList) {
        // localStorage'den çekilen veriyi mevcut radioList'e ekle
        radioList = radioList.concat(storedRadioList);

        // Var olan radioList ile sayfadaki radio butonları güncellenir
        updateRadioButtons();
    }
});

// LocalStorage'dan veri çeken yardımcı fonksiyon
function getFromLocalStorage(key) {
    var storedData = localStorage.getItem(key);

    // JSON formatındaki veriyi parse ederek döndür
    return storedData ? JSON.parse(storedData) : null;
}



// Benzersiz bir ID oluşturmak için kullanılabilir bir fonksiyon
function generateUniqueId() {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

//******************************************************************* */
//                        Delivery Button                             */
//******************************************************************* */

function deilveryButton() {
    var selectedRadio = document.querySelector('input[name="location"]:checked');
    updateMapLocationInfo(selectedRadio.getAttribute("data-lat"),  selectedRadio.getAttribute("data-lon"), selectedRadio.value);
    var eco_lan = parseFloat(selectedRadio.getAttribute("data-lat"));
    var eco_lon = parseFloat(selectedRadio.getAttribute("data-lon"));
    createMarker(eco_lan, eco_lon, selectedRadio);
    hideDeliveryModal()
}

//******************************************************************* */
//                        Delivery Button End                         */
//******************************************************************* */

//******************************************************************* */
//                        Phone Button                                */
//******************************************************************* */

function hidePhoneModal(){
    var modalElement = document.getElementById("modalPhone");
    var modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
}

function validateName() {
    var nameInput = document.getElementById('nameInput');
    var nameErrorMessages = document.getElementById('nameErrorMessages');
    var phoneButton = document.getElementById('phoneButton');
    var name = nameInput.value.trim();

    var errors = [];
    if (name.length == 0) {
        errors.push('* Ad Soyad edilməlidir.');
    } else if (name.length < 3) {
        errors.push('* Ad Soyad minimum 3 hərf olmalıdır.');
    }

    // Display errors
    nameErrorMessages.innerHTML = errors.join('<br>');
    // Disable phoneButton if any error is present in any field
    if (errors.length > 0 || validateDescriptionErrors() || validatePhoneNumberErrors()) {
        phoneButton.disabled = true;
    } else {
        phoneButton.disabled = false;
    }
}

function validateDescription() {
    var descriptionInput = document.getElementById('descriptionInput');
    var descriptionErrorMessages = document.getElementById('descriptionErrorMessages');
    var phoneButton = document.getElementById('phoneButton');
    var name = descriptionInput.value.trim();
    var errors = [];
    if (name.length == 0) {
        errors.push('* Tələb olunur.');
    }

    // Display errors
    descriptionErrorMessages.innerHTML = errors.join('<br>');
    // Disable phoneButton if any error is present in any field
    if (errors.length > 0 || validateNameErrors() || validatePhoneNumberErrors()) {
        phoneButton.disabled = true;
    } else {
        phoneButton.disabled = false;
    }
}

function validatePhoneNumber() {
    var phoneNumberInput = document.getElementById('phoneNumberInput');
    var errorMessages = document.getElementById('errorMessages');
    var phoneButton = document.getElementById('phoneButton');
    var phoneNumber = phoneNumberInput.value.replace(/\s+/g, ''); // Remove whitespaces

    var validPrefixes = ['050', '070', '077', '055', '099', '060', '051', '010'];

    var errors = [];

    if (!phoneNumber.trim()) {
        errors.push('* Nömrə daxil edilməlidir.');
    } else if (!/^\d{10}$/.test(phoneNumber) || validPrefixes.indexOf(phoneNumber.substr(0, 3)) === -1 || /[01]/.test(phoneNumber.charAt(3))) {
        errors.push('* Nömrəni düzgün daxil edin.');
    }

    // Display errors
    errorMessages.innerHTML = errors.join('<br>');
    // Disable phoneButton if any error is present in any field
    if (errors.length > 0 || validateNameErrors() || validateDescriptionErrors()) {
        phoneButton.disabled = true;
    } else {
        phoneButton.disabled = false;
    }
}

// Function to check if there are errors in name validation
function validateNameErrors() {
    var nameInput = document.getElementById('nameInput');
    var name = nameInput.value.trim();

    return name.length == 0 || name.length < 3;
}

// Function to check if there are errors in description validation
function validateDescriptionErrors() {
    var descriptionInput = document.getElementById('descriptionInput');
    var description = descriptionInput.value.trim();

    return description.length == 0;
}

// Function to check if there are errors in phone number validation
function validatePhoneNumberErrors() {
    var phoneNumberInput = document.getElementById('phoneNumberInput');
    var phoneNumber = phoneNumberInput.value.replace(/\s+/g, ''); // Remove whitespaces

    var validPrefixes = ['050', '070', '077', '055', '099', '060', '051', '010'];

    return !phoneNumber.trim() || !/^\d{10}$/.test(phoneNumber) || validPrefixes.indexOf(phoneNumber.substr(0, 3)) === -1 || /[01]/.test(phoneNumber.charAt(3));
}


function phoneButton() {
    var phoneNumberInput = document.getElementById('phoneNumberInput');
    var nameInput = document.getElementById('nameInput');

    var phoneNumber = phoneNumberInput.value.replace(/\s+/g, ''); // Remove whitespaces
    var name = nameInput.value.trim();

    localStorage.setItem('phoneNumber', phoneNumber);
    localStorage.setItem('name', name);
    document.getElementById('phone-info').innerHTML = `<span class="text-dark">${name}</span>
    <span class="ms-2 text-success border-1 border-solid rounded p-1 border-success " style="font-size:10px;">${phoneNumber}</span>`;
    document.getElementById('phoneNumberInput').value = phoneNumber;
    document.getElementById('checkout_phone_error').classList.add("d-none");

    checkCheckoutButtonStatus();
    hidePhoneModal();
}

document.addEventListener("DOMContentLoaded", function () {
    // Sayfa yüklendiğinde localStorage'den telefon numarasını al ve buton metin içeriğine yerleştir
    var phoneNumber = localStorage.getItem('phoneNumber');
    var name = localStorage.getItem('name');
    if (phoneNumber) {
        // document.getElementById('phone-info').innerHTML = `<span class="text-dark">${name}</span>
        // <span class="ms-2 text-success border-1 border-solid rounded p-1 border-success " style="font-size:10px;">${phoneNumber}</span>`;
        document.getElementById('phoneNumberInput').value = phoneNumber;
        document.getElementById('nameInput').value = name;

    }
});
document.addEventListener("DOMContentLoaded", function () {
    validatePhoneNumber();
    validateName();
    validateDescription();
});

document.addEventListener("DOMContentLoaded", function () {
    var phoneNumber = document.querySelector("#nameInput")
    var phoneNumberInput = document.querySelector("#phoneNumberInput")
    var descriptionInput = document.querySelector("#descriptionInput")
    if (phoneNumber.value!=='' && phoneNumberInput.value!=='' && descriptionInput.value!=='') {
        // localStorage'de phonenumber varsa, checkout_phone_error'ı gizle
        var phoneErrorElement = document.getElementById('checkout_phone_error');
        if (phoneErrorElement) {
            phoneErrorElement.classList.add('d-none');
        }
    }
});

//******************************************************************* */
//                           Phone Button End                         */
//******************************************************************* */


//************************************************************************/
//                           Checkout Button                             */
//************************************************************************/
function checkCheckoutButtonStatus() {
    var addressErrorElement = document.getElementById('checkout_address_error');
    var phoneErrorElement = document.getElementById('checkout_phone_error');
    var checkoutButton = document.getElementById('checkout_button');

    // En az bir hata varsa veya her ikisi de görünürse, checkout_button'u devre dışı bırak
    if ((addressErrorElement && !addressErrorElement.classList.contains('d-none')) ||
        (phoneErrorElement && !phoneErrorElement.classList.contains('d-none'))) {
        checkoutButton.disabled = true;
    } else {
        checkoutButton.disabled = false;
    }
}
document.addEventListener("DOMContentLoaded", function () {
    checkCheckoutButtonStatus();
});

function getDeliveryData(){
    var selectedRadio = document.querySelector('input[name="location"]:checked');
    var lat = selectedRadio.getAttribute("data-lat");
    var lon = selectedRadio.getAttribute("data-lon");
    var amount = localStorage.getItem('delivery_amount')
    var recipient_name = document.querySelector('#nameInput').value;
    var recipient_phone = document.querySelector('#phoneNumberInput').value;
    var dropoff_comment = document.querySelector('#descriptionInput').value;
    var shipment_promise_id = localStorage.getItem('shipment_promise_id')

    var deliveryData = {
        lat: lat,
        lon: lon,
        amount: amount,
        recipient_name: recipient_name,
        recipient_phone: recipient_phone,
        dropoff_comment: dropoff_comment,
        shipment_promise_id: shipment_promise_id
      };
    return deliveryData
    
}

//************************************************************************/
//                           Checkout Button End                         */
//************************************************************************/