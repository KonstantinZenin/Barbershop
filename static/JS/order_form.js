// static/js/order_form.js
document.addEventListener('DOMContentLoaded', function() {
    const masterSelect = document.getElementById('id_master');
    const servicesSection = document.getElementById('services-section');
    const servicesContainer = document.getElementById('services-container');
    const servicesUrl = document.getElementById('data_div').dataset.servicesUrl;
    
    // Обработчик изменения мастера
    if (masterSelect) {
        masterSelect.addEventListener('change', function() {
            const masterId = this.value;
            
            if (masterId) {
                // Показываем раздел услуг
                servicesSection.style.display = 'block';
                
                // Загружаем услуги для выбранного мастера
                fetch(`${servicesUrl}?master_id=${masterId}`, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        renderServices(data.services);
                    } else {
                        servicesContainer.innerHTML = `<div class="alert alert-quantum">${data.error}</div>`;
                    }
                })
                .catch(error => {
                    servicesContainer.innerHTML = '<div class="alert alert-quantum">Ошибка загрузки услуг</div>';
                });
            } else {
                // Скрываем раздел услуг, если мастер не выбран
                servicesSection.style.display = 'none';
            }
        });
    }
    
    // Функция отрисовки услуг
    function renderServices(services) {
    if (services.length === 0) {
        servicesContainer.innerHTML = '<p class="text-quantum">У этого мастера пока нет доступных услуг</p>';
        return;
    }
    
    let html = '';
    services.forEach(service => {
        html += `
        <div class="quantum-checkbox mb-2">
            <input class="form-check-input" type="checkbox" name="services" value="${service.id}" id="service-${service.id}">
            <label class="form-check-label" for="service-${service.id}">
            ${service.name}
            </label>
        </div>
        `;
    });
    
    servicesContainer.innerHTML = html;
    }
    
    // Инициализация формы, если мастер уже выбран
    if (masterSelect.value) {
        masterSelect.dispatchEvent(new Event('change'));
    }
});
