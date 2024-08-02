function showNotification(message) {
    var notification = document.getElementById('notification-message');
    notification.innerHTML = message;
    notification.style.display = 'block';
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000); 
}
