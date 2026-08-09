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

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    })[ch]);
}

function uniqueSorted(values) {
    return [...new Set((values || []).map(value => typeof value === 'string' ? value.trim() : '').filter(Boolean))]
        .sort((a, b) => a.localeCompare(b, 'en', { sensitivity: 'base' }));
}

function hexToRgba(hex, alpha) {
    const clean = String(hex || '').trim().replace('#', '');
    if (!/^[0-9a-fA-F]{6}$/.test(clean)) {
        return `rgba(15, 23, 42, ${alpha})`;
    }
    const r = parseInt(clean.slice(0, 2), 16);
    const g = parseInt(clean.slice(2, 4), 16);
    const b = parseInt(clean.slice(4, 6), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function readCoordinate(point) {
    const lat = Number(point?.lat);
    const lng = Number(point?.lng);
    if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
        return null;
    }
    return { lat, lng };
}

function buildSchoolPopup(school) {
    const title = escapeHtml(school?.school_name || 'School visit');
    const state = escapeHtml(school?.state || '');
    const district = escapeHtml(school?.district || '');
    const visitDate = escapeHtml(formatDate(school?.visitDate || school?.date || '') || '');
    const locationLink = isNonEmptyText(school?.locationLink) ? String(school.locationLink) : '';
    const mediaLink = isNonEmptyText(school?.mediaLink) ? String(school.mediaLink) : '';

    return `
        <div style="min-width:220px;max-width:280px">
            <div style="font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#64748b;margin-bottom:6px">School visit</div>
            <div style="font-size:15px;font-weight:800;line-height:1.3;color:#0f172a">${title}</div>
            <div style="margin-top:6px;font-size:13px;color:#475569">${district}${state ? `, ${state}` : ''}</div>
            ${visitDate ? `<div style="margin-top:4px;font-size:12px;color:#64748b">${visitDate}</div>` : ''}
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">
                ${locationLink ? `<a href="${escapeHtml(locationLink)}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;border-radius:9999px;background:#0f172a;color:#fff;padding:6px 10px;font-size:12px;font-weight:700;text-decoration:none">Open location</a>` : ''}
                ${mediaLink ? `<a href="${escapeHtml(mediaLink)}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;border-radius:9999px;background:#0ea5e9;color:#fff;padding:6px 10px;font-size:12px;font-weight:700;text-decoration:none">View media</a>` : ''}
            </div>
        </div>
    `;
}

function buildCoverageRows(data) {
    const rows = [];
    const directSchools = Array.isArray(data?.schools) ? data.schools : [];
    if (directSchools.length) {
        directSchools.forEach(school => {
            const state = school?.state || '';
            const district = school?.district || '';
            const date = school?.visitDate || school?.date || '';
            const name = school?.school_name || '';
            if (!isNonEmptyText(name) && !isNonEmptyText(district) && !isNonEmptyText(date)) {
                return;
            }
            const girls = Number(school?.girlsCount ?? school?.girls ?? school?.counts?.girls ?? NaN);
            const boys = Number(school?.boysCount ?? school?.boys ?? school?.counts?.boys ?? NaN);
            const students = Number(school?.students ?? school?.studentsReached ?? NaN);
            const normalizedGirls = Number.isFinite(girls) ? girls : (Number.isFinite(students) ? Math.floor(students / 2) : 0);
            const normalizedBoys = Number.isFinite(boys) ? boys : (Number.isFinite(students) ? students - normalizedGirls : 0);
            const locationLink = school?.locationLink || '';
            rows.push({
                state,
                name,
                district,
                date,
                locationLink,
                mediaLink: school?.media?.link || school?.mediaLink || '',
                girlsCount: normalizedGirls,
                boysCount: normalizedBoys,
                students: normalizedGirls + normalizedBoys,
                imageName: school?.gallery?.imageName || school?.imageName || ''
            });
        });
        return rows;
    }

    (data?.dashboard?.stateCoverage || []).forEach(group => {
        const state = group?.state || '';
        const color = group?.color || STATE_FILL[state] || '#0f172a';
        (group?.schools || []).forEach(school => {
            if (!isNonEmptyText(school?.name) && !isNonEmptyText(school?.district) && !isNonEmptyText(school?.date)) {
                return;
            }
            const girls = Number(school?.girlsCount ?? school?.girls ?? NaN);
            const boys = Number(school?.boysCount ?? school?.boys ?? NaN);
            const students = Number(school?.students ?? school?.studentsReached ?? NaN);
            const normalizedGirls = Number.isFinite(girls) ? girls : (Number.isFinite(students) ? Math.floor(students / 2) : 0);
            const normalizedBoys = Number.isFinite(boys) ? boys : (Number.isFinite(students) ? students - normalizedGirls : 0);
            rows.push({
                state,
                color,
                name: school?.name || '',
                district: school?.district || '',
                date: school?.date || '',
                locationLink: school?.locationLink || '',
                mediaLink: school?.mediaLink || '',
                girlsCount: normalizedGirls,
                boysCount: normalizedBoys,
                students: normalizedGirls + normalizedBoys
            });
        });
    });
    return rows;
}

function summarizeCoverageRows(rows, mission = {}) {
    const states = new Set();
    const districts = new Set();
    let students = 0;
    let girls = 0;
    let boys = 0;

    rows.forEach(row => {
        if (row.state) states.add(row.state);
        if (row.district) districts.add(row.district);
        students += Number(row.students || 0);
        girls += Number(row.girlsCount || 0);
        boys += Number(row.boysCount || 0);
    });

    return {
        schools: rows.length || mission.schoolsCovered?.current || 0,
        states: states.size || mission.statesCovered?.current || 0,
        districts: districts.size || mission.districtsCovered?.current || 0,
        students: students || mission.studentsImpacted || 0,
        girls: girls || mission.genderBreakdown?.girls || 0,
        boys: boys || mission.genderBreakdown?.boys || 0
    };
}

function renderMap(data) {
    const map = L.map('map', { scrollWheelZoom: false }).setView([26.2, 78.8], 5);
    L.tileLayer('https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
        attribution: '© Google Maps'
    }).addTo(map);
    const pointCounts = new Map();
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
    (data.schools || []).forEach(school => {
        const c = readCoordinate(school?.coordinates);
        if (!c) return;
        const pointKey = `${c.lat.toFixed(6)},${c.lng.toFixed(6)}`;
        const count = pointCounts.get(pointKey) || 0;
        pointCounts.set(pointKey, count + 1);
        const offsetAngle = (count % 6) * (Math.PI / 3);
        const offsetDistance = 0.035 + (Math.floor(count / 6) * 0.012);
        const lat = c.lat + Math.cos(offsetAngle) * offsetDistance;
        const lng = c.lng + Math.sin(offsetAngle) * offsetDistance;
        L.circleMarker([lat, lng], {
            radius: 5,
            color: '#ffffff',
            weight: 1.5,
            fillColor: '#dc2626',
            fillOpacity: 0.95
        }).addTo(map).bindPopup(buildSchoolPopup(school));
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
    const coverageRows = buildCoverageRows(data);
    const coverageSummary = summarizeCoverageRows(coverageRows, mission);
    const coverageSection = document.getElementById('dashboardStateCoverageSection');
    const coverageRail = document.getElementById('stateProgress');
    const coverageEmpty = document.getElementById('coverageEmptyState');
    const coverageLatestBtn = document.getElementById('coverageLatestBtn');
    const coverageStateSelect = document.getElementById('coverageStateSelect');
    const coverageDistrictSelect = document.getElementById('coverageDistrictSelect');

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
        { label: 'States covered', value: `${coverageSummary.states}/${mission.statesCovered?.total || 0}` },
        { label: 'Districts covered', value: `${coverageSummary.districts}/${mission.districtsCovered?.total || 0}` },
        { label: 'Schools visited', value: fmt(coverageSummary.schools) },
        { label: 'Students reached', value: fmt(coverageSummary.students) },
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

    if (coverageSection && coverageRail && coverageEmpty && coverageLatestBtn && coverageStateSelect && coverageDistrictSelect) {
        const stateNames = uniqueSorted(coverageRows.map(row => row.state));
        const districtsByState = new Map();
        const allDistricts = uniqueSorted(coverageRows.map(row => row.district));

        coverageRows.forEach(row => {
            if (!districtsByState.has(row.state)) {
                districtsByState.set(row.state, new Set());
            }
            if (row.district) {
                districtsByState.get(row.state).add(row.district);
            }
        });

        const coverageFilters = {
            state: '',
            district: ''
        };

        const compareByName = (a, b) => (a.name || '').localeCompare(b.name || '', 'en', { sensitivity: 'base' });
        const compareByLatest = (a, b) => {
            const byDate = (b.date || '').localeCompare(a.date || '');
            return byDate !== 0 ? byDate : compareByName(a, b);
        };

        const coverageOptions = (items, label) => {
            const options = [`<option value="">${escapeHtml(label)}</option>`];
            items.forEach(item => {
                options.push(`<option value="${escapeHtml(item)}">${escapeHtml(item)}</option>`);
            });
            return options.join('');
        };

        const refreshDistrictOptions = () => {
            const districtPool = coverageFilters.state
                ? uniqueSorted(Array.from(districtsByState.get(coverageFilters.state) || []))
                : allDistricts;
            coverageDistrictSelect.innerHTML = coverageOptions(districtPool, 'All districts');
            if (coverageFilters.district && !districtPool.includes(coverageFilters.district)) {
                coverageFilters.district = '';
            }
            coverageDistrictSelect.value = coverageFilters.district;
        };

        const filteredRows = () => {
            const isLatestMode = !coverageFilters.state && !coverageFilters.district;
            if (isLatestMode) {
                return [...coverageRows].sort(compareByLatest).slice(0, 4);
            }
            return [...coverageRows]
                .filter(row => !coverageFilters.state || row.state === coverageFilters.state)
                .filter(row => !coverageFilters.district || row.district === coverageFilters.district)
                .sort(compareByName);
        };

        const renderCoverageCards = () => {
            const activeRows = filteredRows();
            const isLatestMode = !coverageFilters.state && !coverageFilters.district;
            coverageLatestBtn.classList.toggle('is-active', isLatestMode);
            coverageRail.innerHTML = activeRows.map(row => {
                const hasLinks = isNonEmptyText(row.locationLink) || isNonEmptyText(row.mediaLink);
                return `
                    <article class="coverage-card card-hover">
                        <div class="coverage-card-shell">
                            <div class="coverage-card-head">
                                <div class="flex items-center justify-between gap-3">
                                    <h5 class="min-w-0 flex-1 truncate text-sm font-extrabold leading-tight text-slate-900">${escapeHtml(row.name || 'School visit')}</h5>
                                    <span class="whitespace-nowrap rounded-full bg-slate-100 px-2.5 py-1 text-[0.65rem] font-bold uppercase tracking-[0.2em] text-slate-500">${escapeHtml(formatDate(row.date) || 'Date pending')}</span>
                                </div>
                            </div>
                            <div class="space-y-2.5 p-3">
                                <div class="flex flex-wrap gap-2 text-[0.7rem] font-semibold text-slate-600">
                                    ${isNonEmptyText(row.district) ? `<span class="coverage-tag">${escapeHtml(row.district)}</span>` : ''}
                                    <span class="coverage-tag">${escapeHtml(row.state)}</span>
                                </div>
                                <div class="flex items-center justify-between gap-3">
                                    ${hasLinks ? `
                                        <div class="flex flex-wrap justify-end gap-2">
                                            ${isNonEmptyText(row.locationLink) ? `<a href="${escapeHtml(row.locationLink)}" target="_blank" rel="noopener" class="inline-flex items-center rounded-full bg-slate-900 px-2.5 py-1.5 text-[0.72rem] font-semibold text-white transition hover:bg-slate-700">Location</a>` : ''}
                                            ${isNonEmptyText(row.mediaLink) ? `<a href="${escapeHtml(row.mediaLink)}" target="_blank" rel="noopener" class="inline-flex items-center rounded-full bg-sky-600 px-2.5 py-1.5 text-[0.72rem] font-semibold text-white transition hover:bg-sky-500">Media</a>` : ''}
                                        </div>
                                    ` : ''}
                                </div>
                            </div>
                        </div>
                    </article>
                `;
            }).join('');

            if (activeRows.length) {
                setHidden(coverageEmpty, true);
                coverageEmpty.textContent = '';
            } else {
                coverageRail.innerHTML = '';
                coverageEmpty.textContent = coverageFilters.state || coverageFilters.district
                    ? 'No schools match the selected state or district.'
                    : 'Coverage data is not available yet.';
                setHidden(coverageEmpty, false);
            }
        };

        coverageStateSelect.innerHTML = coverageOptions(stateNames, 'All states');
        refreshDistrictOptions();

        coverageLatestBtn.addEventListener('click', () => {
            coverageFilters.state = '';
            coverageFilters.district = '';
            coverageStateSelect.value = '';
            refreshDistrictOptions();
            renderCoverageCards();
        });

        coverageStateSelect.addEventListener('change', () => {
            coverageFilters.state = coverageStateSelect.value;
            refreshDistrictOptions();
            renderCoverageCards();
        });

        coverageDistrictSelect.addEventListener('change', () => {
            coverageFilters.district = coverageDistrictSelect.value;
            renderCoverageCards();
        });

        if (coverageRows.length) {
            setHidden(coverageSection, false);
            renderCoverageCards();
        } else {
            coverageRail.innerHTML = '';
            coverageEmpty.textContent = 'Coverage data is not available yet.';
            setHidden(coverageEmpty, false);
            setHidden(coverageSection, true);
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
    const coverageSummary = summarizeCoverageRows(buildCoverageRows(data), data.mission || {});
    document.getElementById('stat-states').textContent = `${coverageSummary.states}/${data.mission.statesCovered?.total || 0}`;
    document.getElementById('stat-districts').textContent = `${coverageSummary.districts}/${data.mission.districtsCovered?.total || 0}`;
    document.getElementById('stat-schools').textContent = fmt(coverageSummary.schools);
    document.getElementById('stat-students').textContent = fmt(coverageSummary.students);
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
