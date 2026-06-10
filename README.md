# Science on Wheels — Local to Global Impact

A mobile science van initiative bringing hands-on STEM education to schools in rural, border,
remote and tribal areas of **Chhattisgarh, Punjab and Himachal Pradesh**.

An initiative by **Plaksha University**, **IIT Mandi** and **IDYM Foundation** (ISRO's Space Tutor).

## The Project

One van carries four educational modules to 45–50 schools per state per year, over two years
(Aug 2025 – Jul 2027):

1. 🚀 Space tech education equipment
2. 🤖 Robotics station with applications
3. 💧 Water testing station
4. 🌱 Interactive sustainability education models

Target districts:

- **Chhattisgarh:** Rajnandgaon, Mungeli, Jashpur, Kanker, Gariyaband
- **Punjab:** Faridkot, Fazilka, Ferozepur, Pathankot, Hoshiarpur, Mansa
- **Himachal Pradesh:** Mandi, Kullu, Bilaspur, Hamirpur, Kangra

## Site structure

| File | Purpose |
|---|---|
| `index.html` | Main website (new Local-to-Global project). Reads `data-v2.json`. |
| `data-v2.json` | All content + live mission data for the new project. |
| `admin.html` | **Streamlined data entry** — fill a form, totals auto-calculated, publish in one click. See `HOW_TO_UPDATE_DATA.md`. |
| `punjab.html` | **Archived** Punjab 2025–26 phase website (241 schools, 1,19,670 students). Reads `data.json`. Do not delete. |
| `data.json`, `schools-gallery.json`, `gallery_school_collage/` | Original Punjab phase data — preserved as-is. |
| `data-entry.html` + `*.py` + `HOW_TO_*` / `DAILY_*` guides | Legacy Punjab-era update workflow — kept for reference. |

## Updating the website

Open `admin.html` on the live site, enter the day's visits, click **Calculate & preview**, then
**Publish**. Full instructions in [`HOW_TO_UPDATE_DATA.md`](HOW_TO_UPDATE_DATA.md).

## Technology

HTML5, Tailwind CSS, Leaflet.js maps, JSON data — hosted on GitHub Pages. Open `index.html`
via any static server for local development.

## Contact

- scienceonwheels@plaksha.edu.in
- Dr. Rucha Joshi (PI) — rucha.joshi@plaksha.edu.in

---

**© 2026 Plaksha University · IIT Mandi · IDYM Foundation. All rights reserved.**
