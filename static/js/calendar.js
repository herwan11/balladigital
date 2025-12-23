/* /static/js/calendar.js */
// Logika untuk merender Gantt Chart dengan Sidebar Label, Interaksi Sorot, dan Label Bulan Dinamis

const DAY_WIDTH = 50;
let viewStartDate = new Date();
viewStartDate.setDate(viewStartDate.getDate() - 5);

document.addEventListener('DOMContentLoaded', renderGantt);

/**
 * Fungsi utama untuk merender struktur Gantt Chart
 */
function renderGantt() {
    const root = document.getElementById('gantt-chart-root');
    const label = document.getElementById('month-label');
    const days = 60; // Menampilkan rentang 60 hari dalam satu render
    const dates = [];
    
    for(let i=0; i<days; i++) {
        let d = new Date(viewStartDate);
        d.setDate(d.getDate() + i);
        dates.push(d);
    }

    // Set label awal berdasarkan tanggal pertama yang dirender
    updateMonthLabel(viewStartDate);

    // Container Utama
    let html = `<div class="gantt-container">`;

    // 1. Sidebar untuk Label Nama Iklan
    html += `<div class="gantt-sidebar">`;
    html += `<div class="gantt-label-header">NAMA IKLAN</div>`;
    ADS_DATA.forEach((ad, index) => {
        html += `<div class="gantt-label-item" onclick="focusAd(${index})">${ad.nama_ads}</div>`;
    });
    html += `</div>`;

    // 2. Area Scrollable Timeline
    html += `<div class="gantt-scroll" id="gantt-scroll-area">`;
    
    // Header Tanggal
    html += `<div class="gantt-header">`;
    const today = new Date().toDateString();
    dates.forEach(d => {
        const isToday = d.toDateString() === today;
        html += `<div class="gantt-day-head ${isToday?'today':''}"><div>${d.toLocaleDateString('id-ID',{weekday:'short'})}</div><div>${d.getDate()}</div></div>`;
    });
    html += `</div>`;

    // Bar Iklan
    ADS_DATA.forEach((ad, index) => {
        const start = new Date(ad.start_datetime), stop = new Date(ad.stop_datetime);
        const diffStart = (start - viewStartDate) / (1000*60*60*24);
        const diffDur = (stop - start) / (1000*60*60*24);
        
        const left = diffStart * DAY_WIDTH;
        const width = diffDur * DAY_WIDTH;
        const time = stop.getHours().toString().padStart(2,'0') + ":" + stop.getMinutes().toString().padStart(2,'0');

        html += `
            <div class="gantt-row">
                <div class="ad-bar" id="ad-bar-${index}" style="left:${left}px; width:${width}px;">
                    ${ad.nama_ads}
                    <div class="stop-label">${time}</div>
                </div>
            </div>`;
    });

    html += `</div></div>`;
    root.innerHTML = html;

    // Tambahkan event listener untuk mendeteksi scroll dan memperbarui label bulan secara dinamis
    const scrollArea = document.getElementById('gantt-scroll-area');
    scrollArea.addEventListener('scroll', handleScrollLabelUpdate);
}

/**
 * Memperbarui teks label bulan di UI
 * @param {Date} date 
 */
function updateMonthLabel(date) {
    const label = document.getElementById('month-label');
    if (label) {
        label.innerText = date.toLocaleDateString('id-ID', { month: 'long', year: 'numeric' });
    }
}

/**
 * Menangani perubahan label bulan saat pengguna melakukan scroll horizontal
 */
function handleScrollLabelUpdate(e) {
    const scrollLeft = e.target.scrollLeft;
    // Hitung berapa hari offset dari posisi scroll saat ini
    const dayOffset = Math.round(scrollLeft / DAY_WIDTH);
    
    const currentDate = new Date(viewStartDate);
    currentDate.setDate(currentDate.getDate() + dayOffset);
    
    updateMonthLabel(currentDate);
}

/**
 * Fungsi untuk menyoroti bar iklan dan melakukan scroll otomatis
 * Mendukung pencarian lintas bulan/periode
 * @param {number} index - Index data iklan dalam ADS_DATA
 */
function focusAd(index) {
    const ad = ADS_DATA[index];
    const adStart = new Date(ad.start_datetime);
    
    const diffDays = (adStart - viewStartDate) / (1000 * 60 * 60 * 24);
    
    if (diffDays < 0 || diffDays > 55) {
        viewStartDate = new Date(adStart);
        viewStartDate.setDate(viewStartDate.getDate() - 5);
        renderGantt();
    }

    setTimeout(() => {
        const bar = document.getElementById(`ad-bar-${index}`);
        const scrollArea = document.getElementById('gantt-scroll-area');
        
        if (!bar || !scrollArea) return;

        document.querySelectorAll('.ad-bar').forEach(el => el.classList.remove('highlight'));
        bar.classList.add('highlight');

        const barLeft = parseFloat(bar.style.left);
        const targetScroll = barLeft - (scrollArea.offsetWidth / 4);
        
        scrollArea.scrollTo({
            left: targetScroll,
            behavior: 'smooth'
        });

        setTimeout(() => {
            bar.classList.remove('highlight');
        }, 3000);
    }, 100);
}

function changeViewRange(days) { 
    viewStartDate.setDate(viewStartDate.getDate() + days); 
    renderGantt(); 
}

function resetToToday() { 
    viewStartDate = new Date(); 
    viewStartDate.setDate(viewStartDate.getDate() - 5); 
    renderGantt(); 
}