const STATE_FILL = {
    "Chhattisgarh": "#f59e0b",
    "Punjab": "#0ea5e9",
    "Himachal Pradesh": "#10b981"
};
const BASES = [
    { name: "Plaksha University, Mohali (Punjab base)", lat: 30.6346, lng: 76.7179 },
    { name: "IIT Mandi, Kamand (Himachal base)", lat: 31.7754, lng: 76.9861 },
    { name: "IDYM Antariksh Prayogshala, Nava Raipur — Atal Nagar (Chhattisgarh base)", lat: 21.161, lng: 81.787 }
];
const fmt = n => n.toLocaleString('en-IN');

function renderMap(data) {
    const map = L.map('map', { scrollWheelZoom: false }).setView([26.2, 78.8], 5);
    L.tileLayer('https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
        attribution: '© Google Maps'
    }).addTo(map);
    data.states.forEach(s => {
        s.districts.forEach(d => {
            const c = data.districtCoordinates[d];
            if (!c) return;
            L.circleMarker([c.lat, c.lng], {
                radius: 9, color: '#fff', weight: 2, fillColor: s.color, fillOpacity: .9
            }).addTo(map).bindPopup(`<strong>${d}</strong><br>${s.name}`);
        });
    });
    const baseIcon = L.divIcon({
        className: '',
        html: '<div style="width:18px;height:18px;background:#fbbf24;border:2.5px solid #0f172a;transform:rotate(45deg);box-shadow:0 0 0 2px #fff,0 1px 4px rgba(0,0,0,.4);"></div>',
        iconSize: [22, 22],
        iconAnchor: [11, 11],
        popupAnchor: [0, -11]
    });
    BASES.forEach(b => {
        L.marker([b.lat, b.lng], { icon: baseIcon, zIndexOffset: 1000 })
            .addTo(map).bindPopup(`◆ <strong>Base hub</strong><br>${b.name}`);
    });
    // Visited schools
    (data.dailyUpdates || []).forEach(u => (u.schools || []).forEach(sc => {
        if (!sc.location) return;
        L.circleMarker([sc.location.lat, sc.location.lng], {
            radius: 5, color: '#fff', weight: 1, fillColor: '#dc2626', fillOpacity: .95
        }).addTo(map).bindPopup(`<strong>${sc.name}</strong><br>${sc.district}, ${sc.state || ''}<br>${sc.studentsReached || 0} students`);
    }));
}

async function init() {
    let data;
    try {
        const res = await fetch('data-sow.json?v=' + Date.now());
        data = await res.json();
    } catch (e) {
        // Opening the page directly from a folder (file://) blocks fetch;
        // fall back to the data snapshot embedded below.
        data = JSON.parse(document.getElementById('data-fallback').textContent);
    }

    // Stats strip
    document.getElementById('stat-states').textContent = `${data.mission.statesCovered.current}/${data.mission.statesCovered.total}`;
    document.getElementById('stat-districts').textContent = `${data.mission.districtsCovered.current}/${data.mission.districtsCovered.total}`;
    document.getElementById('stat-schools').textContent = fmt(data.mission.schoolsCovered.current);
    document.getElementById('stat-students').textContent = fmt(data.mission.studentsImpacted);
    document.getElementById('stat-distance').textContent = fmt(data.mission.distanceTravelled);
    document.getElementById('footerUpdated').textContent = 'Last updated: ' + data.lastUpdated;

    // Objectives
    document.getElementById('objectivesGrid').innerHTML = data.objectives.map((o, i) => `
        <div class="bg-white rounded-xl p-6 shadow border border-slate-200 card-hover">
            <p class="text-3xl font-extrabold text-blue-800 mb-3">${String(i + 1).padStart(2, '0')}</p>
            <p class="text-slate-700 text-sm text-justify">${o}</p>
        </div>`).join('');

    // Modules
    document.getElementById('modulesGrid').innerHTML = data.modules.map(m => `
        <div class="bg-slate-50 rounded-xl p-6 border border-slate-200 card-hover">
            <p class="text-4xl mb-3">${m.icon}</p>
            <h4 class="font-extrabold text-slate-900 mb-2">${m.name}</h4>
            <p class="text-slate-600 text-sm text-justify">${m.description}</p>
        </div>`).join('');

    // States cards
    document.getElementById('statesGrid').innerHTML = data.states.map(s => `
        <div class="bg-white rounded-xl p-6 shadow border border-slate-200 card-hover">
            <h4 class="font-extrabold text-lg mb-1"><span class="state-dot" style="background:${s.color}"></span>${s.name}</h4>
            <p class="text-xs text-slate-500 mb-3">Base: ${s.base}</p>
            <p class="text-sm text-slate-600 mb-3 text-justify">${s.focus}</p>
            <div class="flex flex-wrap gap-2">${s.districts.map(d =>
                `<span class="text-xs font-semibold px-2 py-1 rounded-full" style="background:${s.color}22;color:#334155">${d}</span>`).join('')}
            </div>
        </div>`).join('');

    // Map (skipped gracefully if Leaflet failed to load)
    try { renderMap(data); } catch (e) { console.error('Map unavailable:', e); }

    // Legacy
    const lg = data.legacy;
    document.getElementById('legacyTitle').textContent = lg.title;
    document.getElementById('legacyDesc').textContent = lg.description;
    document.getElementById('legacyStats').innerHTML = [
        [lg.schools, 'Schools'], [lg.students, 'Students'], [lg.girls, 'Girls'],
        [lg.districts, 'Districts'], [lg.distanceKm, 'Km travelled']
    ].map(([v, l]) => `<div><p class="text-4xl font-extrabold text-amber-300">${fmt(v)}</p><p class="text-xs uppercase tracking-wide text-cyan-200 mt-1">${l}</p></div>`).join('');

    // Dashboard
    const updates = data.dailyUpdates || [];
    if (updates.length) {
        document.getElementById('noUpdates').classList.add('hidden');
        document.getElementById('updatesWrap').classList.remove('hidden');
        // per-state progress
        const byState = {};
        updates.forEach(u => (u.schools || []).forEach(sc => {
            const st = sc.state || 'Unknown';
            byState[st] = byState[st] || { schools: 0, students: 0 };
            byState[st].schools++;
            byState[st].students += sc.studentsReached || 0;
        }));
        document.getElementById('stateProgress').innerHTML = data.states.map(s => {
            const p = byState[s.name] || { schools: 0, students: 0 };
            return `<div class="bg-white rounded-xl p-5 shadow border border-slate-200">
                <p class="font-extrabold"><span class="state-dot" style="background:${s.color}"></span>${s.name}</p>
                <p class="text-sm text-slate-600 mt-2">${p.schools} schools · ${fmt(p.students)} students</p>
            </div>`;
        }).join('');
        // table of last 15 visits
        const rows = [];
        [...updates].sort((a, b) => b.date.localeCompare(a.date)).forEach(u =>
            (u.schools || []).forEach(sc => rows.push({ date: u.date, ...sc })));
        document.getElementById('visitsTable').innerHTML = rows.slice(0, 15).map(r => `
            <tr class="border-t border-slate-100">
                <td class="px-4 py-2 whitespace-nowrap">${r.date}</td>
                <td class="px-4 py-2 font-semibold">${r.galleryLink ? `<a class="text-blue-700 hover:underline" target="_blank" rel="noopener" href="${r.galleryLink}">${r.name}</a>` : r.name}</td>
                <td class="px-4 py-2">${r.district || ''}</td>
                <td class="px-4 py-2">${r.state || ''}</td>
                <td class="px-4 py-2 text-right">${fmt(r.studentsReached || 0)}</td>
                <td class="px-4 py-2 text-right">${fmt(r.girlsCount || 0)}</td>
                <td class="px-4 py-2 text-right">${fmt(r.boysCount || 0)}</td>
            </tr>`).join('');
    }

    // Student corner
    if (data.studentCorner) {
        document.getElementById('studentHeading').textContent = data.studentCorner.heading;
        document.getElementById('studentText').textContent = data.studentCorner.text;
        document.getElementById('studentFormWrap').innerHTML = data.studentCorner.formUrl
            ? `<a href="${data.studentCorner.formUrl}" target="_blank" rel="noopener"
                class="inline-block bg-slate-900 text-amber-300 font-extrabold px-8 py-3 rounded-lg hover:bg-slate-800 transition">📝 Fill the Student Form</a>`
            : `<p class="inline-block bg-white/60 px-6 py-3 rounded-lg font-bold text-sm">📝 Student sign-up form opening soon — watch this space!</p>`;
    }

    // Base hubs with contact person and social handle
    document.getElementById('hubsList').innerHTML = data.states.map(s => {
        const h = s.hubContact || {};
        return `<li>
            <p>◆ <strong class="text-white">${s.name}:</strong> ${s.base}</p>
            ${h.person ? `<p class="ml-4 mt-1">${h.person}</p>` : ''}
            ${h.instagram ? `<p class="ml-4"><svg class="ig-icon"><use href="#icon-instagram"/></svg> <a class="text-amber-300 hover:underline" target="_blank" rel="noopener" href="https://instagram.com/${h.instagram}">@${h.instagram}</a></p>` : ''}
        </li>`;
    }).join('') + `<li class="pt-2 border-t border-white/10">📧 Official contact:
        <a class="text-amber-300 hover:underline" href="mailto:scienceonwheels@plaksha.edu.in">scienceonwheels@plaksha.edu.in</a></li>`;

    // Team
    const members = [...data.teamMembers.plaksha, ...data.teamMembers.iitMandi, ...data.teamMembers.idym];
    document.getElementById('teamGrid').innerHTML = members.map(m => `
        <div class="text-center">
            <img src="${m.photo}" alt="${m.name}" class="team-photo mx-auto mb-4">
            <p class="font-extrabold text-slate-900">${m.name}</p>
            <p class="text-sm text-slate-600 mb-1">${m.designation}</p>
            <a href="mailto:${m.email}" class="text-xs text-blue-700 hover:underline">${m.email}</a>
        </div>`).join('');

    // Partners
    document.getElementById('partnersGrid').innerHTML = data.partners.map(p => `
        <div class="text-center bg-white rounded-xl p-5 shadow border border-slate-200 card-hover">
            <img src="${p.logo}" alt="${p.name}" class="partner-logo mx-auto mb-3">
            <p class="font-bold text-sm text-slate-900">${p.name}</p>
            <p class="text-xs text-slate-500">${p.role}</p>
        </div>`).join('');
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        init().catch(err => console.error('Failed to load data-v2.json', err));
    }, { once: true });
} else {
    init().catch(err => console.error('Failed to load data-v2.json', err));
}
