document.addEventListener('DOMContentLoaded', function() {
    const countdownData = document.getElementById('countdown-data');
    if (!countdownData) return;

    let seconds = parseInt(countdownData.dataset.seconds) || 5;
    const redirectUrl = countdownData.dataset.redirectUrl || '/';
    const countdownElement = document.getElementById('countdown');

    function updateTimer() {
        if (seconds <= 1) {
            window.location.href = redirectUrl;
            return;
        }
        
        seconds--;
        countdownElement.textContent = seconds;
        
        // Сброс анимации для плавного пульса
        countdownElement.style.animation = 'none';
        void countdownElement.offsetWidth; // Принудительный рефлоу
        countdownElement.style.animation = 'quantum-pulse 1s infinite';
    }

    // Запускаем сразу первую итерацию
    updateTimer();
    const timerInterval = setInterval(updateTimer, 1000);
});