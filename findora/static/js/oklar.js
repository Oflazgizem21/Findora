// proje.js

// Initialize Swiper
var swiper = new Swiper(".swiper", {
    loop: true, // Sonsuz döngü
    autoplay: {
        delay: 3000, // 3 saniye sonra otomatik geçiş
        disableOnInteraction: false,
    },
    effect: "slide",
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
});

// Comment scroll functionality
document.addEventListener('DOMContentLoaded', function() {
    // Sol ok için kaydırma fonksiyonu
    function scrollLeft() {
        const container = document.querySelector('.yorum-wrapper');
        container.scrollBy({
            left: -300, // Sol kaydırma için negatif değer
            behavior: 'smooth' // Kaydırma yumuşak olmalı
        });
    }

    // Sağ ok için kaydırma fonksiyonu
    function scrollRight() {
        const container = document.querySelector('.yorum-wrapper');
        container.scrollBy({
            left: 300, // Sağ kaydırma için pozitif değer
            behavior: 'smooth' // Kaydırma yumuşak olmalı
        });
    }

    // Event listener'ları ekleyelim
    document.getElementById('leftBtn').addEventListener('click', scrollLeft);
    document.getElementById('rightBtn').addEventListener('click', scrollRight);
});