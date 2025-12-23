/* /static/js/calendar.js */
// Logika untuk merender Gantt Chart dengan presisi tinggi

const DAY_WIDTH = 50;
const MS_PER_DAY = 24 * 60 * 60 * 1000;

let viewStartDate = new Date();
// Normalisasi SANGAT PENTING: Set ke jam 00:00:00 tepat agar grid selaras
viewStartDate.setHours(0, 0, 0, 0);
viewStartDate.setDate(viewStartDate.getDate() - 5);

let activeFilters = [];

document.addEventListener('DOMContentLoaded', () => {
    // Inisialisasi filter: Pilih semua nama iklan unik
    activeFilters = [...new Set(ADS_DATA.map(ad => ad.nama_ads))];
    
    renderFilters();
    renderGantt();

    // Tutup dropdown jika klik di luar
    document.addEventListener('click', (e) => {
        const dropdown = document.getElementById('dropdown-filter');
        if (dropdown && !dropdown.contains(e.target)) {
            dropdown.classList.remove('open');
        }
    });
});

function toggleDropdown() {
    const dropdown = document.getElementById('dropdown-filter');
    dropdown.classList.toggle('open');
}

function renderFilters() {
    const container = document.getElementById('filter-container');
    const label = document.getElementById('dropdown-label');
    if (!container || !label) return;

    const uniqueNames = [...new Set(ADS_DATA.map(ad => ad.nama_ads))];

    if (activeFilters.length === 0) {
        label.innerText = "Tidak Ada Dipilih";
    } else if (activeFilters.length === uniqueNames.length) {
        label.innerText = "Semua Iklan Dipilih";
    } else {
        label.innerText = `${activeFilters.length} Iklan Dipilih`;
    }

    let html = '';
    uniqueNames.forEach(name => {
        const isActive = activeFilters.includes(name);
        html += `
            <div class="filter-item" onclick="toggleFilter(event, '${name}')">
                <input type="checkbox" ${isActive ? 'checked' : ''} onclick="event.stopPropagation()">
                <span>${name}</span>
            </div>
        `;
    });

    container.innerHTML = html;
}

function toggleFilter(event, name) {
    if (activeFilters.includes(name)) {
        activeFilters = activeFilters.filter(f => f !== name);
    } else {
        activeFilters.push(name);
    }
    renderFilters(); 
    renderGantt();   
}

function renderGantt() {
    const root = document.getElementById('gantt-chart-root');
    const days = 60; 
    const dates = [];
    
    const filteredAds = ADS_DATA.filter(ad => activeFilters.includes(ad.nama_ads));

    for(let i=0; i<days; i++) {
        let d = new Date(viewStartDate);
        d.setDate(d.getDate() + i);
        dates.push(d);
    }

    updateMonthLabel(viewStartDate);

    if (filteredAds.length === 0) {
        root.innerHTML = `<div class="empty-chart">Pilih iklan di filter untuk melihat grafik.</div>`;
        return;
    }

    let html = `<div class="gantt-container">`;

    // 1. Sidebar Label
    html += `<div class="gantt-sidebar">`;
    html += `<div class="gantt-label-header">NAMA IKLAN</div>`;
    filteredAds.forEach((ad, index) => {
        html += `<div class="gantt-label-item" onclick="focusAd(${index})">${ad.nama_ads}</div>`;
    });
    html += `</div>`;

    // 2. Area Grafik Scrollable
    html += `<div class="gantt-scroll" id="gantt-scroll-area">`;
    
    // Header Tanggal
    html += `<div class="gantt-header">`;
    const todayStr = new Date().toDateString();
    dates.forEach(d => {
        const isToday = d.toDateString() === todayStr;
        html += `<div class="gantt-day-head ${isToday?'today':''}"><div>${d.toLocaleDateString('id-ID',{weekday:'short'})}</div><div>${d.getDate()}</div></div>`;
    });
    html += `</div>`;

    // Render Bar Iklan
    filteredAds.forEach((ad, index) => {
        const start = new Date(ad.start_datetime);
        const stop = new Date(ad.stop_datetime);
        
        // Hitung jarak dari titik 00:00 viewStartDate dalam milidetik
        const diffStartMs = start.getTime() - viewStartDate.getTime();
        const diffDurMs = stop.getTime() - start.getTime();
        
        // Konversi milidetik ke piksel secara presisi
        const left = (diffStartMs / MS_PER_DAY) * DAY_WIDTH;
        const width = (diffDurMs / MS_PER_DAY) * DAY_WIDTH;
        
        // Format jam berakhir
        const stopTimeStr = stop.getHours().toString().padStart(2,'0') + ":" + stop.getMinutes().toString().padStart(2,'0');

        html += `
            <div class="gantt-row">
                <div class="ad-bar" id="ad-bar-${index}" style="left:${left}px; width:${width}px;">
                    <span class="ad-name-text">${ad.nama_ads}</span>
                    <div class="stop-label">${stopTimeStr}</div>
                </div>
            </div>`;
    });

    html += `</div></div>`;
    root.innerHTML = html;

    const scrollArea = document.getElementById('gantt-scroll-area');
    if (scrollArea) {
        scrollArea.addEventListener('scroll', handleScrollLabelUpdate);
    }
}

function updateMonthLabel(date) {
    const label = document.getElementById('month-label');
    if (label) {
        label.innerText = date.toLocaleDateString('id-ID', { month: 'long', year: 'numeric' });
    }
}

function handleScrollLabelUpdate(e) {
    const scrollLeft = e.target.scrollLeft;
    const dayOffset = Math.round(scrollLeft / DAY_WIDTH);
    const currentDate = new Date(viewStartDate);
    currentDate.setDate(currentDate.getDate() + dayOffset);
    updateMonthLabel(currentDate);
}

function focusAd(index) {
    const filteredAds = ADS_DATA.filter(ad => activeFilters.includes(ad.nama_ads));
    const ad = filteredAds[index];
    if(!ad) return;

    const adStart = new Date(ad.start_datetime);
    const diffDays = (adStart.getTime() - viewStartDate.getTime()) / MS_PER_DAY;
    
    if (diffDays < 0 || diffDays > 55) {
        viewStartDate = new Date(adStart);
        viewStartDate.setHours(0,0,0,0);
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
        scrollArea.scrollTo({ left: targetScroll, behavior: 'smooth' });
        setTimeout(() => bar.classList.remove('highlight'), 3000);
    }, 100);
}

function changeViewRange(days) { 
    viewStartDate.setDate(viewStartDate.getDate() + days); 
    renderGantt(); 
}

function resetToToday() { 
    viewStartDate = new Date(); 
    viewStartDate.setHours(0,0,0,0);
    viewStartDate.setDate(viewStartDate.getDate() - 5); 
    renderGantt(); 
}