//***************************************************************** */
//Map modalinin aclib baglanmasi
var map2Shown = false; // Harita başlangıçta gizli

function closeMap(){
    document.getElementById("modalMap").style.display = "none"
    document.getElementById("modalMap").style.opacity = 0
    if (map2Shown) {
        hideMap();
        // showAddressModal()
    } else {
        showMap();
        // hideAddressModal()
        // hideDeliveryModal()
    }
    map2Shown = !map2Shown; // Durumu tersine çevir
}

function toggleMap() {
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