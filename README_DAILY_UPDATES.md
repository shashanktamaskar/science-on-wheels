# Daily Updates Guide

## Quick Start

To update the website with daily school visits, use one of these methods:

### Method 1: Use the Prompt Template (Easiest)

1. Open `DAILY_UPDATE_PROMPT_TEMPLATE.txt`
2. Copy the template
3. Fill in your school data
4. Paste into any AI assistant (Claude, ChatGPT, etc.)
5. The AI will handle everything automatically

### Method 2: Provide Data Directly

Simply give this information to an AI assistant:

```
Update Science on Wheels website with today's school visits:

Date: 2025-10-29
Schools:
- School Name (lat, lng) - XXX students - District
- School Name (lat, lng) - XXX students - District

Gallery:
- School Name: [OneDrive link]
- School Name: [OneDrive link]

Start/End: Plaksha University
```

## Files in This Repository

- **DAILY_UPDATE_INSTRUCTIONS.md** - Complete step-by-step guide for AI models
- **DAILY_UPDATE_PROMPT_TEMPLATE.txt** - Copy-paste template for daily updates
- **data.json** - Main data file with mission stats and daily updates
- **schools-gallery.json** - Gallery data with photo links
- **index.html** - Website (automatically reads from JSON files)

## What Gets Updated

1. **Mission Statistics** (data.json)
   - Total schools covered
   - Total students impacted
   - Total distance travelled
   - Districts covered

2. **Daily Updates** (data.json)
   - New entry with today's schools, students, and route

3. **Gallery** (schools-gallery.json)
   - New entries with OneDrive photo links

## Example

**Input:**
```
Date: 2025-10-29
Schools:
- GHS-Balongi (30.7234, 76.7123) - 300 students - SAS Nagar
- GHS-Kurali (30.7845, 76.7956) - 275 students - SAS Nagar

Gallery:
- GHS-Balongi: https://plakshauniversity1-my.sharepoint.com/:f:/g/...
- GHS-Kurali: https://plakshauniversity1-my.sharepoint.com/:f:/g/...
```

**What the AI will do:**
1. Calculate route distance (~39 km)
2. Update mission stats (6 schools, 1916 students, 86 km total)
3. Add daily entry to data.json
4. Add schools to gallery
5. Commit and push changes
6. Create PR link for you

## Need Help?

- Read **DAILY_UPDATE_INSTRUCTIONS.md** for complete technical details
- Check commit history for examples: `git log`
- View website: https://shashanktamaskar.github.io/science-on-wheels/

---

**Project:** Science on Wheels for Punjab
**Repository:** https://github.com/shashanktamaskar/science-on-wheels
**Maintained by:** Plaksha University, IIT Mandi, IDYM Foundation
