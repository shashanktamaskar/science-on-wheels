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

function isNonEmptyText(value) {
    return typeof value === 'string' ? value.trim().length > 0 : value !== null && value !== undefined;
}

function isNonEmptyArray(value) {
    return Array.isArray(value) && value.length > 0;
}

function setHidden(el, hidden) {
    if (!el) return;
    el.classList.toggle('hidden', hidden);
}

function formatDate(value) {
    const date = new Date(`${value}T00:00:00`);
    if (Number.isNaN(date.getTime())) return value || '';
    return new Intl.DateTimeFormat('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    }).format(date);
}

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

function renderDashboard(data) {
    const dashboard = data.dashboard || {};
    const mission = data.mission || {};
    const projectInfo = data.projectInfo || {};
    const dailyUpdates = Array.isArray(data.dailyUpdates) ? data.dailyUpdates : [];

    const phaseBadge = document.getElementById('dashboardPhaseBadge');
    if (phaseBadge) {
        phaseBadge.textContent = projectInfo.phase || '';
        setHidden(phaseBadge, !isNonEmptyText(projectInfo.phase));
    }

    const headline = document.getElementById('dashboardHeadline');
    if (headline) {
        headline.textContent = dashboard.headline || '';
        setHidden(headline, !isNonEmptyText(dashboard.headline));
    }

    const intro = document.getElementById('dashboardIntro');
    if (intro) {
        intro.textContent = dashboard.intro || '';
        setHidden(intro, !isNonEmptyText(dashboard.intro));
    }

    const summaryCards = [
        { label: 'States covered', value: `${mission.statesCovered?.current || 0}/${mission.statesCovered?.total || 0}` },
        { label: 'Districts covered', value: `${mission.districtsCovered?.current || 0}/${mission.districtsCovered?.total || 0}` },
        { label: 'Schools visited', value: fmt(mission.schoolsCovered?.current || 0) },
        { label: 'Students reached', value: fmt(mission.studentsImpacted || 0) },
        { label: 'Km travelled', value: fmt(mission.distanceTravelled || 0) }
    ];
    document.getElementById('dashboardSummary').innerHTML = summaryCards.map(card => `
        <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs font-bold uppercase tracking-wide text-slate-500">${card.label}</p>
            <p class="mt-2 text-3xl font-extrabold text-slate-900">${card.value}</p>
        </div>
    `).join('');

    const highlightsSection = document.getElementById('dashboardHighlightsSection');
    const highlightsMount = document.getElementById('dashboardHighlights');
    if (highlightsSection && highlightsMount) {
        const highlights = (dashboard.highlights || []).filter(item =>
            isNonEmptyText(item?.eyebrow) || isNonEmptyText(item?.title) || isNonEmptyText(item?.description)
        );
        if (isNonEmptyArray(highlights)) {
            highlightsMount.innerHTML = highlights.map(item => `
                <div class="rounded-xl border border-slate-200 bg-slate-50 p-5 shadow-sm">
                    ${isNonEmptyText(item.eyebrow) ? `<p class="mb-2 text-xs font-bold uppercase tracking-wide text-slate-500">${item.eyebrow}</p>` : ''}
                    <h5 class="font-extrabold text-slate-900">${item.title || ''}</h5>
                    ${isNonEmptyText(item.description) ? `<p class="mt-2 text-sm text-slate-600 text-justify">${item.description}</p>` : ''}
                </div>
            `).join('');
            setHidden(highlightsSection, false);
        } else {
            highlightsMount.innerHTML = '';
            setHidden(highlightsSection, true);
        }
    }

    const milestonesSection = document.getElementById('dashboardMilestonesSection');
    const milestonesMount = document.getElementById('dashboardMilestones');
    if (milestonesSection && milestonesMount) {
        const milestones = (dashboard.milestones || []).filter(item =>
            isNonEmptyText(item?.title) || isNonEmptyText(item?.description) || isNonEmptyText(item?.status) || isNonEmptyText(item?.state) || isNonEmptyText(item?.targetDate)
        );
        if (isNonEmptyArray(milestones)) {
            milestonesMount.innerHTML = milestones.map(item => {
                const status = item.status || '';
                const statusClass = /planned|upcoming/i.test(status) ? 'pill-planning' : 'pill-execution';
                return `
                    <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
                        <div class="flex items-start justify-between gap-3">
                            <div>
                                <h5 class="font-extrabold text-slate-900">${item.title || ''}</h5>
                                ${isNonEmptyText(item.state) ? `<p class="mt-1 text-xs font-semibold uppercase tracking-wide text-slate-500">${item.state}</p>` : ''}
                            </div>
                            ${isNonEmptyText(status) ? `<span class="phase-pill ${statusClass}">${status}</span>` : ''}
                        </div>
                        ${isNonEmptyText(item.targetDate) ? `<p class="mt-3 text-xs uppercase tracking-wide text-slate-500">${formatDate(item.targetDate)}</p>` : ''}
                        ${isNonEmptyText(item.description) ? `<p class="mt-2 text-sm text-slate-600 text-justify">${item.description}</p>` : ''}
                    </div>
                `;
            }).join('');
            setHidden(milestonesSection, false);
        } else {
            milestonesMount.innerHTML = '';
            setHidden(milestonesSection, true);
        }
    }

    const stateCoverage = (dashboard.stateCoverage || [])
        .filter(state => isNonEmptyText(state?.state) || isNonEmptyArray(state?.schools));

    const stateCoverageSection = document.getElementById('dashboardStateCoverageSection');
    const stateProgress = document.getElementById('stateProgress');
    if (stateProgress && stateCoverageSection) {
        if (isNonEmptyArray(stateCoverage)) {
            stateProgress.innerHTML = stateCoverage.slice(0, 3).map(state => {
                const schools = (state.schools || []).filter(school =>
                    isNonEmptyText(school?.name) ||
                    isNonEmptyText(school?.district) ||
                    isNonEmptyText(school?.date) ||
                    isNonEmptyText(school?.mapLink) ||
                    isNonEmptyText(school?.mediaLink)
                );
                const color = state.color || '#0f172a';
                return `
                    <article class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm card-hover">
                        <div class="px-5 py-4 text-white" style="background: linear-gradient(135deg, ${color} 0%, ${color}CC 100%);">
                            <div class="flex items-start justify-between gap-3">
                                <div>
                                    <h4 class="text-lg font-extrabold">${state.state}</h4>
                                    ${isNonEmptyText(state.base) ? `<p class="mt-1 text-sm text-white/85">Base: ${state.base}</p>` : ''}
                                </div>
                                <span class="whitespace-nowrap rounded-full bg-white/15 px-3 py-1 text-xs font-bold uppercase tracking-wide">${schools.length} schools</span>
                            </div>
                        </div>
                        <div class="space-y-3 p-5">
                            ${schools.map(school => {
                                const actionButtons = [
                                    isNonEmptyText(school.mapLink) ? `<a href="${school.mapLink}" target="_blank" rel="noopener" class="inline-flex items-center rounded-full bg-slate-900 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-slate-700">Google Map</a>` : '',
                                    isNonEmptyText(school.mediaLink) ? `<a href="${school.mediaLink}" target="_blank" rel="noopener" class="inline-flex items-center rounded-full bg-amber-400 px-3 py-1.5 text-xs font-semibold text-slate-900 transition hover:bg-amber-300">Media</a>` : ''
                                ].filter(Boolean).join('');
                                return `
                                    <div class="rounded-xl border border-slate-200 bg-slate-50 p-4">
                                        <div class="flex items-start justify-between gap-3">
                                            <div>
                                                <h5 class="font-extrabold text-slate-900">${school.name || ''}</h5>
                                                <div class="mt-1 flex flex-wrap gap-x-3 gap-y-1 text-xs text-slate-500">
                                                    ${isNonEmptyText(school.district) ? `<span>${school.district}</span>` : ''}
                                                    ${isNonEmptyText(school.date) ? `<span>${formatDate(school.date)}</span>` : ''}
                                                    ${isNonEmptyText(school.students) ? `<span>${fmt(school.students)} students</span>` : ''}
                                                </div>
                                            </div>
                                        </div>
                                        ${actionButtons ? `<div class="mt-3 flex flex-wrap gap-2">${actionButtons}</div>` : ''}
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </article>
                `;
            }).join('');
            setHidden(stateCoverageSection, false);
        } else {
            stateProgress.innerHTML = '';
            setHidden(stateCoverageSection, true);
        }
    }

    const recentSection = document.getElementById('dashboardRecentSection');
    const visitsTable = document.getElementById('visitsTable');
    if (recentSection && visitsTable) {
        if (dailyUpdates.length) {
            const rows = [];
            [...dailyUpdates].sort((a, b) => (b.date || '').localeCompare(a.date || '')).forEach(update =>
                (update.schools || []).forEach(sc => rows.push({ date: update.date, ...sc })));
            visitsTable.innerHTML = rows.slice(0, 15).map(row => `
                <tr class="border-t border-slate-100">
                    <td class="px-4 py-2 whitespace-nowrap">${row.date}</td>
                    <td class="px-4 py-2 font-semibold">${row.galleryLink ? `<a class="text-blue-700 hover:underline" target="_blank" rel="noopener" href="${row.galleryLink}">${row.name}</a>` : row.name}</td>
                    <td class="px-4 py-2">${row.district || ''}</td>
                    <td class="px-4 py-2">${row.state || ''}</td>
                    <td class="px-4 py-2 text-right">${fmt(row.studentsReached || 0)}</td>
                    <td class="px-4 py-2 text-right">${fmt(row.girlsCount || 0)}</td>
                    <td class="px-4 py-2 text-right">${fmt(row.boysCount || 0)}</td>
                </tr>
            `).join('');
            setHidden(recentSection, false);
        } else {
            visitsTable.innerHTML = '';
            setHidden(recentSection, true);
        }
    }
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

    renderDashboard(data);

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
