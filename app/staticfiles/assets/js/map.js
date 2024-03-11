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
                            selectedInputValue = result.display_name.split(', ').slice(0, -4).join(', ');
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
    // Yeni bir radio düğmesi yarat
    var newRadio = document.createElement('div');
    newRadio.classList.add('form-check', 'my-2', 'ms-1');
    var radioId = generateUniqueId(); // Benzersiz bir id oluştur

    if (marker == true) {
        var markerCoordinates = newMarker.getLatLng();
        locationInfo(markerCoordinates.lat, markerCoordinates.lng)
        .then(address => {
            if (!radioList.includes(address)) {
                newRadio.innerHTML = `
                <input class="form-check-input" type="radio" name="location" id="location${radioId}"
                    value="${address}">
                <label class="form-check-label text-dark" for="location${radioId}">
                    ${address}
                </label>
                `;  
                radioList.push(address);
                var modalElement = document.getElementById("modalAddress");
                var modalInstance = bootstrap.Modal.getInstance(modalElement);
                modalInstance.hide();
                document.querySelector('#radio-list').appendChild(newRadio);
                closeMap(for_add = true);
            } else {
            }
        })
        .catch(error => {
            console.error('Hata:', error);
        });

    } else {  
        if (canAddRadioList == true) {
            let streetValue = streetInput.value;
            let errorDiv = document.getElementById("addressError")
            if (!radioList.includes(streetValue)) {
                newRadio.innerHTML = `
                <input class="form-check-input" type="radio" name="location" id="location${radioId}"
                    value="${streetValue}">
                <label class="form-check-label text-dark" for="location${radioId}">
                    ${streetValue}
                </label>
                `; 
                radioList.push(streetValue);
                errorDiv.innerText = "";
                errorDiv.classList.remove("text-danger", "mb-2");
                document.querySelector('#radio-list').appendChild(newRadio);
                hideAddressModal();
            } else {
                errorDiv.innerText = "* Bu address artıq əlavə edilib!";
                errorDiv.classList.add("text-danger", "mb-2");
            }
        }
    }
}

// Benzersiz bir ID oluşturmak için kullanılabilir bir fonksiyon
function generateUniqueId() {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

//******************************************************************* */
//                        Delivery Button                             */
//******************************************************************* */

function deilveryButton() {
    var selectedValue = document.querySelector('input[name="location"]:checked').value;
    console.log("Seçilen değer:", selectedValue);
    // Burada seçilen değeri kullanabilirsiniz, örneğin bir AJAX isteği gönderebilirsiniz.
}


//******************************************************************* */
//                        Delivery Button End                         */
//******************************************************************* */