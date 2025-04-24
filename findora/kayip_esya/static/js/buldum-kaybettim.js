// "Diğer" seçilince textbox göster
function toggleCustomInput(field) {
    const select = document.getElementById(`id_${field}`);
    const customBox = document.getElementById(`custom_${field}_box`);
    
    if (select.value === 'diger') {
        customBox.style.display = 'block';
    } else {
        customBox.style.display = 'none';
    }
}

// Sayfa yüklendiğinde kontrol et (form geri döndüyse)
document.addEventListener('DOMContentLoaded', function() {
    toggleCustomInput('tur');
    toggleCustomInput('renk');
});