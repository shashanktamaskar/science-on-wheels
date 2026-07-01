(function () {
    const MOUNT_ID = 'heroCarouselMount';
    const MANIFEST_URL = 'assets-hero/manifest.json';
    const DEFAULT_IMAGE_MS = 6000;
    const CAPTION_AUTO_HIDE_MS = 1500;

    const FALLBACK_ITEMS = [
        {
            src: 'https://plakshauniversity1-my.sharepoint.com/:v:/g/personal/scienceonwheels_plaksha_edu_in/IQD9brC6Rk8RRaMQHFeRplwhAUP93T0sRg6fpOysAXaRTOE?e=obJn33',
            type: 'video',
            title: 'Science on Wheels in motion',
            description: 'The mobile science van bringing hands-on STEM to schools and communities across the region.',
            poster: 'assets-hero/Science_on_wheels_project_banner.jpg'
        },
        {
            src: 'assets-hero/Science_on_wheels_project_banner.jpg',
            type: 'image',
            title: 'Project banner',
            description: 'The Science on Wheels project banner and visual identity.',
            displayMs: DEFAULT_IMAGE_MS
        }
    ];

    const state = {
        items: [],
        index: 0,
        currentToken: 0,
        imageTimer: null,
        captionTimer: null,
        captionVisible: true,
        soundEnabled: false,
        autoplayBlocked: false
    };

    function mount() {
        return document.getElementById(MOUNT_ID);
    }

    function inferType(src, explicitType) {
        if (explicitType) return explicitType;
        const value = String(src || '').toLowerCase();
        if (/\.(mp4|webm|ogg)$/i.test(value)) return 'video';
        return 'image';
    }

    function isOneDriveOrSharePointUrl(src) {
        return /(?:sharepoint\.com|onedrive\.live\.com|1drv\.ms)/i.test(String(src || ''));
    }

    function addQueryParam(url, key, value) {
        try {
            const parsed = new URL(url, window.location.href);
            parsed.searchParams.set(key, value);
            return parsed.toString();
        } catch (error) {
            return url;
        }
    }

    function buildVideoCandidates(src) {
        const candidates = [];
        if (isOneDriveOrSharePointUrl(src)) {
            const downloadUrl = addQueryParam(src, 'download', '1');
            if (!candidates.includes(downloadUrl)) {
                candidates.push(downloadUrl);
            }
        }
        if (!candidates.includes(src)) {
            candidates.push(src);
        }
        return candidates;
    }

    function normalizeItem(item) {
        if (!item || !item.src) return null;
        return {
            src: item.src,
            type: inferType(item.src, item.type),
            mode: item.mode || '',
            title: item.title || '',
            description: item.description || '',
            poster: item.poster || '',
            displayMs: Number.isFinite(Number(item.displayMs)) ? Number(item.displayMs) : DEFAULT_IMAGE_MS
        };
    }

    function clearTimer() {
        if (state.imageTimer) {
            window.clearTimeout(state.imageTimer);
            state.imageTimer = null;
        }
    }

    function clearCaptionTimer() {
        if (state.captionTimer) {
            window.clearTimeout(state.captionTimer);
            state.captionTimer = null;
        }
    }

    function getCurrentItem() {
        return state.items[state.index];
    }

    function getSlideElement() {
        return document.getElementById('heroCarouselSlide');
    }

    function getSoundButton() {
        return document.getElementById('heroCarouselSound');
    }

    function getPlayButton() {
        return document.getElementById('heroCarouselPlay');
    }

    function getVideoElement() {
        return getSlideElement()?.querySelector('video');
    }

    function getIframeElement() {
        return getSlideElement()?.querySelector('iframe');
    }

    function getCounter() {
        return document.getElementById('heroCarouselCounter');
    }

    function getCaption() {
        return document.getElementById('heroCarouselCaption');
    }

    function getStage() {
        return document.getElementById('heroCarouselStage');
    }

    function isInsideStage(node) {
        const stage = getStage();
        return !!(stage && node && stage.contains(node));
    }

    function updateDots() {
        document.querySelectorAll('[data-hero-dot]').forEach((dot, index) => {
            dot.classList.toggle('is-active', index === state.index);
            dot.setAttribute('aria-current', index === state.index ? 'true' : 'false');
        });
    }

    function updateCounter() {
        const counter = getCounter();
        if (!counter) return;
        counter.textContent = `${String(state.index + 1).padStart(2, '0')} of ${String(state.items.length).padStart(2, '0')}`;
    }

    function setCaptionVisible(visible) {
        state.captionVisible = visible;
        const caption = getCaption();
        if (!caption) return;
        caption.classList.toggle('is-hidden', !visible);
    }

    function scheduleCaptionHide() {
        clearCaptionTimer();
        state.captionTimer = window.setTimeout(() => {
            setCaptionVisible(false);
        }, CAPTION_AUTO_HIDE_MS);
    }

    function showCaptionTemporarily() {
        setCaptionVisible(true);
        scheduleCaptionHide();
    }

    function updateSoundButton() {
        const button = getSoundButton();
        const item = getCurrentItem();
        if (!button) return;
        if (!item || item.type !== 'video' || item.mode === 'iframe' || /\/_layouts\/15\/embed\.aspx/i.test(item.src)) {
            button.classList.add('hidden');
            return;
        }
        button.classList.remove('hidden');
        button.setAttribute('aria-pressed', state.soundEnabled ? 'true' : 'false');
        button.innerHTML = state.soundEnabled
            ? '<span>Sound on</span><span aria-hidden="true">🔊</span>'
            : '<span>Muted</span><span aria-hidden="true">🔇</span>';
    }

    function hidePlayButton() {
        const button = getPlayButton();
        if (button) button.classList.add('hidden');
    }

    function showPlayButton(message) {
        const button = getPlayButton();
        if (!button) return;
        button.classList.remove('hidden');
        button.innerHTML = `<span>${message || 'Tap to play'}</span><span aria-hidden="true">▶</span>`;
    }

    function stopCurrentMedia() {
        clearTimer();
        clearCaptionTimer();
        const video = getVideoElement();
        if (video) {
            video.pause();
            video.removeAttribute('src');
            const source = video.querySelector('source');
            if (source) source.removeAttribute('src');
            video.load();
        }
        const iframe = getIframeElement();
        if (iframe) {
            iframe.src = 'about:blank';
        }
    }

    function scheduleImageAdvance(item, token) {
        clearTimer();
        state.imageTimer = window.setTimeout(() => {
            if (token !== state.currentToken) return;
            goTo(state.index + 1);
        }, item.displayMs || DEFAULT_IMAGE_MS);
    }

    function goTo(index) {
        if (!state.items.length) return;
        const nextIndex = ((index % state.items.length) + state.items.length) % state.items.length;
        state.index = nextIndex;
        renderSlide();
    }

    function next() {
        goTo(state.index + 1);
    }

    function prev() {
        goTo(state.index - 1);
    }

    function toggleSound() {
        const item = getCurrentItem();
        if (!item || item.type !== 'video' || item.mode === 'iframe' || /\/_layouts\/15\/embed\.aspx/i.test(item.src)) return;
        state.soundEnabled = !state.soundEnabled;
        const video = getSlideElement()?.querySelector('video');
        if (video) {
            video.muted = !state.soundEnabled;
            if (state.soundEnabled && video.paused) {
                video.play().catch(() => {
                    state.autoplayBlocked = true;
                    showPlayButton('Tap to play');
                });
            }
        }
        updateSoundButton();
    }

    function bindControls() {
        const prevButton = document.getElementById('heroCarouselPrev');
        const nextButton = document.getElementById('heroCarouselNext');
        const soundButton = getSoundButton();
        const playButton = getPlayButton();
        const dotButtons = document.querySelectorAll('[data-hero-dot]');

        if (prevButton) prevButton.onclick = prev;
        if (nextButton) nextButton.onclick = next;
        if (soundButton) soundButton.onclick = toggleSound;
        if (playButton) {
            playButton.onclick = () => {
                const video = getSlideElement()?.querySelector('video');
                if (!video) return;
                state.autoplayBlocked = false;
                video.play().then(() => {
                    video.muted = !state.soundEnabled;
                    hidePlayButton();
                }).catch(() => {
                    showPlayButton('Tap to play');
                });
            };
        }
        dotButtons.forEach(button => {
            button.onclick = () => goTo(Number(button.dataset.heroDot));
        });
    }

    function attachVideoHandlers(video, token) {
        video.addEventListener('ended', () => {
            if (token !== state.currentToken) return;
            next();
        });
        video.addEventListener('play', hidePlayButton);
        video.addEventListener('error', () => {
            if (token !== state.currentToken) return;
            const remaining = video.dataset.heroCandidates ? JSON.parse(video.dataset.heroCandidates) : [];
            const currentIndex = Number(video.dataset.heroCandidateIndex || '0');
            const nextIndex = currentIndex + 1;
            if (nextIndex < remaining.length) {
                playVideoCandidate(video, remaining, nextIndex, token);
                return;
            }
            showPlayButton('Video unavailable');
        });
    }

    function playVideoCandidate(video, candidates, candidateIndex, token) {
        if (!video || !Array.isArray(candidates) || candidateIndex >= candidates.length) return;
        video.dataset.heroCandidates = JSON.stringify(candidates);
        video.dataset.heroCandidateIndex = String(candidateIndex);
        video.muted = true;
        video.src = candidates[candidateIndex];
        video.load();
        const tryPlay = () => {
            if (token !== state.currentToken) return;
            video.play().then(() => {
                if (token !== state.currentToken) return;
                hidePlayButton();
                if (state.soundEnabled) {
                    video.muted = false;
                }
                showCaptionTemporarily();
            }).catch(() => {
                if (token !== state.currentToken) return;
                state.autoplayBlocked = true;
                showPlayButton('Tap to play');
                showCaptionTemporarily();
            });
        };
        if (video.readyState >= 1) {
            tryPlay();
        } else {
            video.addEventListener('loadedmetadata', tryPlay, { once: true });
        }
    }

    function renderShell() {
        const el = mount();
        if (!el) return;

        el.innerHTML = `
            <div class="hero-carousel-shell">
                <div class="hero-carousel-stage" id="heroCarouselStage" tabindex="0" aria-label="Hero media carousel">
                    <div id="heroCarouselSlide" class="absolute inset-0"></div>
                    <div class="hero-carousel-overlay"></div>
                    <div id="heroCarouselCaption" class="hero-carousel-caption">
                        <div class="flex flex-col gap-4">
                            <div>
                                <div id="heroCarouselCounter" class="hero-carousel-counter mb-2"></div>
                                <h3 id="heroCarouselTitle" class="text-2xl lg:text-3xl font-extrabold leading-tight"></h3>
                                <p id="heroCarouselDescription" class="mt-2 max-w-lg text-sm lg:text-[0.95rem] text-slate-200"></p>
                            </div>
                            <div class="flex flex-wrap items-center gap-3">
                                <button id="heroCarouselSound" type="button" class="hero-carousel-sound hidden" aria-pressed="false"></button>
                                <button id="heroCarouselPlay" type="button" class="hero-carousel-play hidden"></button>
                            </div>
                        </div>
                    </div>
                    <div class="hero-carousel-controls">
                        <button id="heroCarouselPrev" type="button" class="hero-carousel-nav" aria-label="Previous hero slide">
                            <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M15 19l-7-7 7-7"></path>
                            </svg>
                        </button>
                        <div class="hero-carousel-dots" id="heroCarouselDots"></div>
                        <button id="heroCarouselNext" type="button" class="hero-carousel-nav" aria-label="Next hero slide">
                            <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;

        const dots = document.getElementById('heroCarouselDots');
        dots.innerHTML = state.items.map((_, index) => `
            <button
                type="button"
                class="hero-carousel-dot"
                data-hero-dot="${index}"
                aria-label="Go to hero slide ${index + 1}">
            </button>
        `).join('');

        bindControls();
        const stage = getStage();
        if (stage) {
            stage.addEventListener('mouseenter', () => {
                clearCaptionTimer();
                setCaptionVisible(true);
            });
            stage.addEventListener('mouseleave', () => {
                scheduleCaptionHide();
            });
            stage.addEventListener('focusin', () => {
                clearCaptionTimer();
                setCaptionVisible(true);
            });
            stage.addEventListener('focusout', event => {
                if (isInsideStage(event.relatedTarget)) return;
                scheduleCaptionHide();
            });
        }
        renderSlide();
    }

    function renderSlide() {
        const slide = getSlideElement();
        const title = document.getElementById('heroCarouselTitle');
        const description = document.getElementById('heroCarouselDescription');
        if (!slide || !title || !description) return;

        stopCurrentMedia();
        state.currentToken += 1;
        const token = state.currentToken;
        const item = getCurrentItem();
        if (!item) return;

        slide.innerHTML = '';
        title.textContent = item.title || 'Science on Wheels';
        description.textContent = item.description || '';
        updateCounter();
        updateDots();
        updateSoundButton();
        hidePlayButton();
        showCaptionTemporarily();

        const useIframe = item.type === 'video' && (
            item.mode === 'iframe' || /\/_layouts\/15\/embed\.aspx/i.test(item.src)
        );

        if (useIframe) {
            const wrapper = document.createElement('div');
            wrapper.className = 'absolute inset-0 bg-slate-950';
            wrapper.innerHTML = `
                <iframe
                    class="hero-carousel-iframe"
                    src="${item.src}"
                    title="${item.title || 'Science on Wheels video'}"
                    allow="autoplay; encrypted-media; fullscreen; picture-in-picture"
                    allowfullscreen
                    loading="eager"
                    scrolling="no"
                    referrerpolicy="no-referrer-when-downgrade"></iframe>
            `;
            slide.appendChild(wrapper);
            updateSoundButton();
            hidePlayButton();
            clearTimer();
        } else if (item.type === 'video') {
            const wrapper = document.createElement('div');
            wrapper.className = 'absolute inset-0';
            wrapper.innerHTML = `
                <video
                    class="hero-carousel-media"
                    playsinline
                    muted
                    preload="metadata"
                    autoplay
                    ${item.poster ? `poster="${item.poster}"` : ''}></video>
            `;
            slide.appendChild(wrapper);

            const video = wrapper.querySelector('video');
            if (video) {
                const candidates = buildVideoCandidates(item.src);
                attachVideoHandlers(video, token);
                playVideoCandidate(video, candidates, 0, token);
            }
        } else {
            const img = document.createElement('img');
            img.className = 'hero-carousel-media';
            img.alt = item.title || 'Science on Wheels hero slide';
            img.src = item.src;
            slide.appendChild(img);
            scheduleImageAdvance(item, token);
        }
    }

    async function init() {
        const el = mount();
        if (!el) return;

        let items = FALLBACK_ITEMS;
        try {
            const response = await fetch(`${MANIFEST_URL}?v=${Date.now()}`);
            if (response.ok) {
                const data = await response.json();
                if (Array.isArray(data?.items) && data.items.length) {
                    items = data.items;
                }
            }
        } catch (error) {
            console.warn('Hero manifest unavailable, using fallback items.', error);
        }

        state.items = items.map(normalizeItem).filter(Boolean);
        if (!state.items.length) {
            el.innerHTML = `
                <div class="hero-carousel-shell">
                    <div class="hero-carousel-stage flex items-center justify-center p-8 text-center">
                        <p class="text-sm font-semibold uppercase tracking-wide text-slate-300">Hero media unavailable</p>
                    </div>
                </div>
            `;
            return;
        }

        renderShell();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init, { once: true });
    } else {
        init();
    }
})();
