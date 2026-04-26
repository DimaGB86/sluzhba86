// Мобильное меню
function toggleMenu() {
    var menu = document.getElementById('navMenu');
    menu.classList.toggle('show');
}

// Закрытие меню при клике на ссылку (для мобильных)
document.querySelectorAll('.nav-menu a').forEach(function(link) {
    link.addEventListener('click', function() {
        var menu = document.getElementById('navMenu');
        if (menu.classList.contains('show')) {
            menu.classList.remove('show');
        }
    });
});

// Простая маска телефона
document.addEventListener('DOMContentLoaded', function() {
    var phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            var x = e.target.value.replace(/\D/g, '').match(/(\d{0,1})(\d{0,3})(\d{0,3})(\d{0,2})(\d{0,2})/);
            e.target.value = '+7';
            if (x[2]) e.target.value += ' (' + x[2];
            if (x[3]) e.target.value += ') ' + x[3];
            if (x[4]) e.target.value += '-' + x[4];
            if (x[5]) e.target.value += '-' + x[5];
        });
    }
});