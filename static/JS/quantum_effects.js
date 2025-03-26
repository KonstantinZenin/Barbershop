document.addEventListener('DOMContentLoaded', function() {
    // Добавляем эффект глитча для элементов с классом glitch
    const glitchElements = document.querySelectorAll('.glitch');
    
    glitchElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.textShadow = '2px 2px 0 #ff2d7b, -2px -2px 0 #0ff0fc';
            this.style.position = 'relative';
            this.style.left = '2px';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.textShadow = '';
            this.style.position = '';
            this.style.left = '';
        });
    });
    
    // Эффект параллакса для фона
    if (window.innerWidth > 768) {
        document.body.addEventListener('mousemove', function(e) {
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            const glitchEffect = document.querySelector('.glitch-effect');
            glitchEffect.style.backgroundPosition = `${x * 30}px ${y * 30}px`;
        });
    }
    
    // Анимация появления элементов при скролле
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.quantum-animate');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.classList.add('animated');
            }
        });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Запускаем сразу для видимых элементов
});