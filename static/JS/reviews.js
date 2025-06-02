// Функция для обновления звезд
function updateStars(rating) {
    document.querySelectorAll('.star-rating i').forEach(star => {
        const starValue = star.getAttribute('data-rating');
        if (starValue <= rating) {
            star.classList.remove('bi-star');
            star.classList.add('bi-star-fill', 'text-warning');
        } else {
            star.classList.remove('bi-star-fill', 'text-warning');
            star.classList.add('bi-star');
        }
    });
}

// Инициализация звездного рейтинга
document.addEventListener('DOMContentLoaded', function() {
    const starContainer = document.querySelector('.star-rating');
    const ratingInput = document.getElementById('id_rating');
    
    if (starContainer) {
        // Обработка клика по звезде
        starContainer.querySelectorAll('i').forEach(star => {
            star.addEventListener('click', function() {
                const rating = this.getAttribute('data-rating');
                ratingInput.value = rating;
                updateStars(rating);
            });
            
            // Эффект при наведении
            star.addEventListener('mouseenter', function() {
                const hoverRating = this.getAttribute('data-rating');
                updateStars(hoverRating);
            });
            
            star.addEventListener('mouseleave', function() {
                updateStars(ratingInput.value || 0);
            });
        });
        
        // Инициализация текущего значения
        if (ratingInput.value) {
            updateStars(ratingInput.value);
        }
    }
    
    // AJAX подгрузка информации о мастере
    const masterSelect = document.getElementById('id_master');
    if (masterSelect) {
        masterSelect.addEventListener('change', function() {
            const masterId = this.value;
            const infoDiv = document.getElementById('master-info');
            
            if (masterId) {
                fetch(`/api/master-info/?master_id=${masterId}`, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        displayMasterInfo(data.master);
                    } else {
                        infoDiv.innerHTML = `<div class="alert alert-quantum">${data.error}</div>`;
                    }
                })
                .catch(error => {
                    infoDiv.innerHTML = '<div class="alert alert-quantum">Ошибка загрузки данных</div>';
                });
            } else {
                infoDiv.innerHTML = '';
            }
        });
    }
    
    // Функция отображения информации о мастере
    function displayMasterInfo(master) {
        const infoDiv = document.getElementById('master-info');
        infoDiv.innerHTML = `
            <div class="quantum-master-card p-3">
                <div class="d-flex align-items-center">
                    ${master.photo ? `<img src="${master.photo}" class="rounded-circle me-3" width="80" height="80" alt="${master.name}">` : ''}
                    <div>
                        <h5 class="glow-text">${master.name}</h5>
                        <p class="mb-1"><i class="fas fa-award me-2"></i>Опыт: ${master.experience} лет</p>
                        ${master.services.length ? `<p class="mb-0"><i class="fas fa-scissors me-2"></i>Специализация: ${master.services.map(s => s.name).join(', ')}</p>` : ''}
                    </div>
                </div>
            </div>
        `;
    }
    
    // Клиентская валидация формы
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(event) {
            if (!validateReviewForm()) {
                event.preventDefault();
            }
        });
    }
    
    function validateReviewForm() {
        let isValid = true;
        const fields = [
            { id: 'id_client_name', message: 'Пожалуйста, укажите ваше имя' },
            { id: 'id_text', message: 'Пожалуйста, напишите текст отзыва' },
            { id: 'id_master', message: 'Пожалуйста, выберите мастера' }
        ];
        
        // Проверка обязательных полей
        fields.forEach(field => {
            const element = document.getElementById(field.id);
            if (!element.value.trim()) {
                showError(element, field.message);
                isValid = false;
            } else {
                clearError(element);
            }
        });
        
        // Проверка рейтинга
        const ratingInput = document.getElementById('id_rating');
        if (!ratingInput.value) {
            showError(document.querySelector('.star-rating'), 'Пожалуйста, поставьте оценку');
            isValid = false;
        } else {
            clearError(document.querySelector('.star-rating'));
        }
        
        return isValid;
    }
    
    function showError(element, message) {
        clearError(element);
        element.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback quantum-error';
        errorDiv.textContent = message;
        
        element.parentNode.appendChild(errorDiv);
    }
    
    function clearError(element) {
        element.classList.remove('is-invalid');
        const errorDiv = element.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
});
