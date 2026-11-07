// A casual-access gate for this static site, not server-side authentication.
(function () {
    const PASSWORD_HASH = 'f6be67a7fb464f2f82789cf238fd27ddce279bd83e5f571b95f8acc3f96aa8cd';
    const SESSION_KEY = 'sow-gallery-access';
    let unlocked = false;
    try { unlocked = sessionStorage.getItem(SESSION_KEY) === PASSWORD_HASH; } catch (_) {}

    function isUnlocked() { return unlocked; }

    function mount(container, onUnlock) {
        if (unlocked) { onUnlock(); return; }
        container.innerHTML = `
            <form class="gallery-access" aria-label="Unlock photo album">
                <h3>Full photo albums</h3>
                <p>Enter the password to open the full photo album in OneDrive. Picture collages are available to everyone.</p>
                <label for="gallery-password">Password</label>
                <input id="gallery-password" name="password" type="password" autocomplete="current-password" required aria-describedby="gallery-password-error">
                <p id="gallery-password-error" role="alert" class="gallery-access-error"></p>
                <button type="submit">Unlock photo album</button>
            </form>`;
        const form = container.querySelector('form');
        const input = form.elements.password;
        const error = container.querySelector('[role="alert"]');
        const button = form.querySelector('button');
        input.addEventListener('input', () => {
            error.textContent = '';
            input.removeAttribute('aria-invalid');
        });
        form.addEventListener('submit', async event => {
            event.preventDefault();
            button.disabled = true;
            try {
                const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(input.value));
                const hash = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
                if (hash !== PASSWORD_HASH) {
                    input.setAttribute('aria-invalid', 'true');
                    error.textContent = 'Incorrect password. Please try again.';
                    input.select();
                    return;
                }
                unlocked = true;
                try { sessionStorage.setItem(SESSION_KEY, PASSWORD_HASH); } catch (_) {}
                input.value = '';
                onUnlock();
            } catch (_) {
                error.textContent = 'Unable to unlock the gallery. Please refresh and try again using HTTPS.';
            } finally {
                button.disabled = false;
            }
        });
    }

    function openAlbum(link) {
        const url = new URL(link.dataset.galleryUrl, location.href);
        if (url.protocol !== 'https:') return;
        if (isUnlocked()) {
            window.open(url.href, '_blank', 'noopener,noreferrer');
            return;
        }
        const dialog = document.createElement('dialog');
        dialog.className = 'gallery-access-dialog';
        dialog.setAttribute('aria-label', 'Unlock full photo album');
        const close = document.createElement('button');
        close.type = 'button';
        close.className = 'gallery-access-close';
        close.textContent = 'Close';
        close.addEventListener('click', () => dialog.close());
        const content = document.createElement('div');
        dialog.append(close, content);
        document.body.append(dialog);
        dialog.addEventListener('close', () => {
            dialog.remove();
            link.focus();
        }, { once: true });
        mount(content, () => {
            content.innerHTML = '<div class="gallery-access"><h3>Album unlocked</h3><p>You can now open full photo albums in this tab.</p></div>';
            const next = document.createElement('a');
            next.href = url.href;
            next.target = '_blank';
            next.rel = 'noopener noreferrer';
            next.className = 'gallery-access-open';
            next.textContent = 'Open photo album in OneDrive';
            next.addEventListener('click', () => dialog.close());
            content.firstElementChild.append(next);
            next.focus();
        });
        dialog.showModal();
    }

    document.addEventListener('click', event => {
        const link = event.target.closest('a[data-gallery-url]');
        if (!link) return;
        event.preventDefault();
        openAlbum(link);
    });
})();
