/*Bunun olayı sss kısmında soruya tıklayınca cevap kısmını göstermesi */
document.addEventListener('DOMContentLoaded', function() {
    const soruBasliklari = document.querySelectorAll('.soru-baslik');

    soruBasliklari.forEach(baslik => {
        baslik.addEventListener('click', () => {
            const soru = baslik.parentElement;
            soru.classList.toggle('active'); // Aktif sınıfını ekle/çıkar
        }); 
    });
});