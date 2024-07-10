document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        // Sayfa tamamen yüklendiğinde yükleyiciyi gizle
        setTimeout(function () {
            document.getElementById("loader").style.display = "none";
        }, 1000); // 1000 milisaniye = 1 saniye, süreyi isteğinize göre ayarlayabilirsiniz
    } else {
        // Sayfa yüklenirken yükleyiciyi göster
        document.getElementById("loader").style.display = "block";
    }
};