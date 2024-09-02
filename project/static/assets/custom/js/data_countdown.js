document.addEventListener("DOMContentLoaded", function() {
    const countdownElements = document.querySelectorAll('.grid[data-end-time]');

    countdownElements.forEach(function(element) {
        const endTime = new Date(element.getAttribute('data-end-time')).getTime();

        function updateCountdown() {
            const now = new Date().getTime();
            const timeRemaining = endTime - now;

            if (timeRemaining < 0) {
                element.querySelector('.days').textContent = '00';
                element.querySelector('.hours').textContent = '00';
                element.querySelector('.minutes').textContent = '00';
                element.querySelector('.seconds').textContent = '00';
                return;
            }

            const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
            const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

            element.querySelector('.days').textContent = String(days).padStart(2, '0');
            element.querySelector('.hours').textContent = String(hours).padStart(2, '0');
            element.querySelector('.minutes').textContent = String(minutes).padStart(2, '0');
            element.querySelector('.seconds').textContent = String(seconds).padStart(2, '0');
        }

        updateCountdown();
        setInterval(updateCountdown, 1000);
    });
});
