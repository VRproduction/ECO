function showNotification(type, message) {
    const notification = document.getElementById('notification');
    const notificationIcon = document.getElementById('notification-icon');
    const notificationMessage = document.getElementById('notification-message');

    const notificationTypes = {
        success: {
            bgColor: 'bg-green-500',
            textColor: 'text-white',
            icon: '✔️',
        },
        error: {
            bgColor: 'bg-red-500',
            textColor: 'text-white',
            icon: '❌',
        },
        info: {
            bgColor: 'bg-blue-500',
            textColor: 'text-white',
            icon: 'ℹ️',
        },
        warning: {
            bgColor: 'bg-yellow-500',
            textColor: 'text-black',
            icon: '⚠️',
        },
    };

    const { bgColor, textColor, icon } = notificationTypes[type];

    // Bildirim için sınıfları ekleyin ve görünür yap
    notification.className = `fixed top-4 right-4 left-4 max-w-xs mx-auto p-4 rounded-lg shadow-lg transform transition-transform translate-x-full z-[500] sm:max-w-md sm:right-4 sm:left-auto ${bgColor} ${textColor}`;
    notification.style.display = 'block';

    notificationIcon.textContent = icon;
    notificationMessage.textContent = message;

    // Bildirimi görünür yap
    requestAnimationFrame(() => {
        notification.classList.remove('translate-x-full');
        notification.classList.add('translate-x-0', 'animate-shake');
    });

    // 3 saniye sonra bildirimi gizle ve shake animasyonunu kaldır
    setTimeout(() => {
        notification.classList.remove('animate-shake', 'translate-x-0');
        notification.classList.add('translate-x-full');
    }, 3000);

    // Animasyon tamamlandığında bildirimi tamamen gizle
    notification.addEventListener('transitionend', () => {
        if (notification.classList.contains('translate-x-full')) {
            notification.style.display = 'none';
        }
    });
}

// Shake animasyonu tanımlama
const styleSheet = document.createElement('style');
styleSheet.type = 'text/css';
styleSheet.innerText = `
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
    20%, 40%, 60%, 80% { transform: translateX(10px); }
  }

  .animate-shake {
    animation: shake 0.5s;
  }
`;
document.head.appendChild(styleSheet);

// Örnek kullanım
// showNotification('success', 'İşlem başarılı!');