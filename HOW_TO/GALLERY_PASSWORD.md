# Full photo album password

Collages remain public. Full photo album links on both the main site and the Punjab archive open a password dialog. Successful access is remembered in sessionStorage for the current tab; closing the tab ends that session.

The shared gate is in `scripts/gallery-access.js`, styled by `styles/gallery-access.css`. Album links use `href="#gallery"` and `data-gallery-url` so opening them without JavaScript does not navigate straight to the album. New album links should follow that pattern.

To change the password, replace `PASSWORD_HASH` with the SHA-256 hexadecimal digest of the new password. Changing it also invalidates saved sessions. Do not put the plaintext password in the repository.

This is a casual-access prompt on a static GitHub Pages site. Album URLs remain present in public site data and source. It does not change OneDrive sharing permissions or protect previously shared URLs. Use OneDrive access restrictions if the original photos must be private.
