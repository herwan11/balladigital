// File: static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.querySelector('.toggle-btn');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (toggleBtn && sidebar && mainContent) {
        toggleBtn.addEventListener('click', () => {
            // Toggle class 'collapsed' pada sidebar
            sidebar.classList.toggle('collapsed');
            
            // Toggle class 'full-width' pada main-content untuk menyesuaikan margin
            mainContent.classList.toggle('full-width');
        });
    }

    // Animasi ringan: Hilangkan flash message setelah beberapa detik
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.display = 'none';
        }, 5000); // Hilang setelah 5 detik
    });
});

// Font Awesome fallback (for icons)
// Tambahkan script ini di HTML jika tidak ada CDN
// <script src="https://kit.fontawesome.com/your-fontawesome-kit.js"></script>