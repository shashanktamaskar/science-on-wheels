(function () {
    const MOUNT_ID = 'galleryCarouselMount';
    const DATA_URL = 'schools-gallery-sow.json';
    const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP'];

    const state = {
        collageFolder: '',
        schools: [],
        index: 0,
        keyboardBound: false
    };

    function mount() {
        return document.getElementById(MOUNT_ID);
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

    function buildImagePaths(name) {
        const folder = state.collageFolder.replace(/\/+$/, '');
        return IMAGE_EXTENSIONS.map(ext => `${folder}/${encodeURIComponent(name)}${ext}`);
    }

    function showMessage(title, body, buttonText, buttonHref) {
        const el = mount();
        if (!el) return;
        el.innerHTML = `
            <div class="rounded-2xl border border-slate-200 bg-slate-50 p-8 text-center shadow-sm">
                <h4 class="text-xl font-extrabold text-slate-900 mb-2">${title}</h4>
                <p class="text-slate-600 mb-5">${body}</p>
                ${buttonText && buttonHref ? `
                    <a href="${buttonHref}" target="_blank"
                        class="inline-flex items-center justify-center rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-bold text-amber-300 transition hover:bg-slate-800">
                        ${buttonText}
                    </a>` : ''}
            </div>
        `;
    }

    function renderShell() {
        const el = mount();
        if (!el) return;

        const showDots = state.schools.length > 1 && state.schools.length <= 10;

        el.innerHTML = `
            <div class="rounded-2xl border border-slate-200 bg-white shadow-xl overflow-hidden">
                <div class="relative bg-slate-100">
                    <div id="gallerySlide" class="relative min-h-[420px]"></div>
                    <button id="galleryPrev"
                        class="absolute left-4 top-1/2 -translate-y-1/2 rounded-full bg-white/90 p-3 text-slate-800 shadow-lg transition hover:scale-110 disabled:cursor-not-allowed disabled:opacity-40"
                        type="button" aria-label="Previous collage">
                        <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M15 19l-7-7 7-7"></path>
                        </svg>
                    </button>
                    <button id="galleryNext"
                        class="absolute right-4 top-1/2 -translate-y-1/2 rounded-full bg-white/90 p-3 text-slate-800 shadow-lg transition hover:scale-110 disabled:cursor-not-allowed disabled:opacity-40"
                        type="button" aria-label="Next collage">
                        <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7"></path>
                        </svg>
                    </button>
                </div>

                <div class="border-t border-slate-200 px-5 py-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                    <div class="text-sm text-slate-600 font-medium" id="galleryCounter"></div>
                    <div id="galleryDots" class="flex flex-wrap justify-center md:justify-end gap-2 ${showDots ? '' : 'hidden'}"></div>
                </div>
            </div>
        `;

        const prev = document.getElementById('galleryPrev');
        const next = document.getElementById('galleryNext');

        prev.addEventListener('click', () => goTo(state.index - 1));
        next.addEventListener('click', () => goTo(state.index + 1));

        if (!state.keyboardBound) {
            document.addEventListener('keydown', onKeydown);
            state.keyboardBound = true;
        }

        if (showDots) {
            const dots = document.getElementById('galleryDots');
            dots.innerHTML = state.schools.map((_, index) => `
                <button type="button" class="gallery-dot h-2 w-2 rounded-full transition-all bg-slate-300" aria-label="Go to collage ${index + 1}"
                    data-index="${index}"></button>
            `).join('');

            dots.querySelectorAll('button').forEach(button => {
                button.addEventListener('click', () => goTo(Number(button.dataset.index)));
            });
        }

        renderSlide();
    }

    function renderSlide() {
        const el = document.getElementById('gallerySlide');
        const counter = document.getElementById('galleryCounter');
        if (!el || !counter) return;

        const school = state.schools[state.index];
        const imagePaths = buildImagePaths(school.name);

        counter.textContent = `${state.index + 1} / ${state.schools.length} school collages`;

        el.innerHTML = `
            <div class="relative min-h-[420px] bg-gradient-to-br from-slate-100 to-slate-200">
                <img id="galleryImage"
                    alt="${school.name} collage"
                    class="h-full w-full object-contain"
                    loading="eager"
                    decoding="async">
                <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 via-black/50 to-transparent p-5 md:p-6">
                    <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
                        <div>
                            <h4 class="text-2xl font-extrabold text-white">${school.name}</h4>
                            <p class="mt-1 text-sm font-medium text-slate-200">${school.district || ''}${school.district ? ' District' : ''}</p>
                            <p class="text-sm text-slate-300">${formatDate(school.visitDate)}</p>
                        </div>
                        <div class="flex flex-wrap gap-3">
                            ${school.folderUrl ? `
                                <a href="${school.folderUrl}" target="_blank" rel="noopener"
                                    class="inline-flex items-center justify-center rounded-lg bg-cyan-600 px-4 py-2.5 text-sm font-bold text-white transition hover:bg-cyan-700">
                                    See this visit only
                                </a>` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;

        const image = document.getElementById('galleryImage');
        loadFirstAvailableImage(image, imagePaths, 0);

        updateControls();
        updateDots();
    }

    function loadFirstAvailableImage(image, imagePaths, attemptIndex) {
        if (!image) return;
        if (attemptIndex >= imagePaths.length) {
            image.outerHTML = `
                <div class="flex min-h-[420px] items-center justify-center p-8 text-center text-slate-500">
                    <div>
                        <p class="text-lg font-bold text-slate-700 mb-2">Collage not available</p>
                        <p class="text-sm">The image file for this school is missing from the configured collage folder.</p>
                    </div>
                </div>
            `;
            return;
        }

        image.onerror = () => loadFirstAvailableImage(image, imagePaths, attemptIndex + 1);
        image.src = imagePaths[attemptIndex];
    }

    function updateControls() {
        const prev = document.getElementById('galleryPrev');
        const next = document.getElementById('galleryNext');
        if (!prev || !next) return;

        prev.disabled = state.index === 0;
        next.disabled = state.index === state.schools.length - 1;
    }

    function updateDots() {
        const dots = document.querySelectorAll('.gallery-dot');
        dots.forEach((dot, index) => {
            if (index === state.index) {
                dot.className = 'gallery-dot h-2 w-8 rounded-full transition-all bg-cyan-600';
            } else {
                dot.className = 'gallery-dot h-2 w-2 rounded-full transition-all bg-slate-300';
            }
        });
    }

    function goTo(index) {
        if (index < 0 || index >= state.schools.length) return;
        state.index = index;
        renderSlide();
    }

    function onKeydown(event) {
        if (event.target && ['INPUT', 'TEXTAREA', 'SELECT'].includes(event.target.tagName)) return;
        if (event.key === 'ArrowLeft') {
            goTo(state.index - 1);
        } else if (event.key === 'ArrowRight') {
            goTo(state.index + 1);
        }
    }

    async function init() {
        const el = mount();
        if (!el) return;

        try {
            const response = await fetch(`${DATA_URL}?v=${Date.now()}`);
            const data = await response.json();
            state.collageFolder = data.collageFolder || '';
            state.schools = Array.isArray(data.schools) ? data.schools
                .filter(s => s && s.name)
                .slice()
                .sort((a, b) => new Date(b.visitDate) - new Date(a.visitDate)) : [];

            if (!state.collageFolder) {
                showMessage(
                    'Gallery folder not configured',
                    'Add a collageFolder value to schools-gallery.json so the index carousel knows where to load images from.'
                );
                return;
            }

            if (state.schools.length === 0) {
                showMessage(
                    'No collages yet',
                    'The gallery data file loaded correctly, but there are no school entries to show yet.',
                    'View the Punjab archive',
                    'punjab.html'
                );
                return;
            }

            renderShell();
        } catch (error) {
            console.error('Failed to load index gallery data', error);
            showMessage(
                'Gallery unavailable',
                'The gallery data file could not be loaded. Check schools-gallery.json and the collage folder path.'
            );
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init, { once: true });
    } else {
        init();
    }
})();
