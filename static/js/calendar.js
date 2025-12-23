/* /static/js/calendar.js */
// Logika untuk merender Gantt Chart secara horizontal

const DAY_WIDTH = 50;
let viewStartDate = new Date();
viewStartDate.setDate(viewStartDate.getDate() - 5);

document.addEventListener('DOMContentLoaded', renderGantt);

function renderGantt() {
    const root = document.getElementById('gantt-chart-root');
    const label = document.getElementById('month-label');
    const days = 60;
    const dates = [];
    
    for(let i=0; i<days; i++) {
        let d = new Date(viewStartDate);
        d.setDate(d.getDate() + i);
        dates.push(d);
    }

    label.innerText = dates[0].toLocaleDateString('id-ID', {month: 'long', year: 'numeric'});

    let html = `<div class="gantt-header">`;
    const today = new Date().toDateString();
    dates.forEach(d => {
        const isToday = d.toDateString() === today;
        html += `<div class="gantt-day-head ${isToday?'today':''}"><div>${d.toLocaleDateString('id-ID',{weekday:'short'})}</div><div>${d.getDate()}</div></div>`;
    });
    html += `</div>`;

    ADS_DATA.forEach(ad => {
        const start = new Date(ad.start_datetime), stop = new Date(ad.stop_datetime);
        const diffStart = (start - viewStartDate) / (1000*60*60*24);
        const diffDur = (stop - start) / (1000*60*60*24);
        const left = diffStart * DAY_WIDTH;
        const width = diffDur * DAY_WIDTH;
        const time = stop.getHours().toString().padStart(2,'0') + ":" + stop.getMinutes().toString().padStart(2,'0');

        html += `<div class="gantt-row"><div class="ad-bar" style="left:${left}px; width:${width}px;">${ad.nama_ads}<div class="stop-label">${time}</div></div></div>`;
    });

    root.innerHTML = html;
}

function changeViewRange(days) { viewStartDate.setDate(viewStartDate.getDate() + days); renderGantt(); }
function resetToToday() { viewStartDate = new Date(); viewStartDate.setDate(viewStartDate.getDate() - 5); renderGantt(); }