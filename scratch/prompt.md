<USER_REQUEST>
Redesign the FoodFactsIndia product detail page (currently showing Coca-Cola Original Taste) 
into a simplified, scannable layout suitable for general consumers, including kids and 
non-technical users. The current version is too dense and text-heavy — replace it with a 
clean, collapsible-section design where each section shows only a rating + short summary 
by default, and expands into a full detailed report only when the user clicks/taps on it.

DESIGN PRINCIPLES:
- Minimal by default, detailed on demand (progressive disclosure)
- Every section follows the same visual pattern: [Rating/Badge] + [1-2 line key takeaway] 
  + [Click to expand for full report]
- Friendly, simple language over technical/regulatory jargon
- Mobile-first, card-based layout with generous spacing

PAGE STRUCTURE (top to bottom):

1. Product Header (always visible, no collapse)
   - Left side: Product image placeholder, product name, brand, category tag, pack size, GTIN/barcode
   - Right side: Overall grade badge (A-E letter + score out of 100) and total concerns count 
     (e.g., "2 Concerns") shown as a small badge/pill

2. Banned/Restricted Status Banner (new section — only show if applicable)
   - If any ingredient, additive, or color in this product is banned or restricted in any 
     country, display a highlighted alert card directly below the header
   - Each banned item shows: ingredient/color name, country/region where banned, and a 
     one-line plain-language reason for the ban
   - Clicking expands to show regulatory source/citation
   - If nothing is banned, hide this section entirely (don't show empty state)

3. Multi-Jurisdictional Front-of-Package Ratings
   - Collapsed view: show the 3 rating badges side by side (EU Nutri-Score, India Benchmark 
     0-100, US FDA proposed %DV) with just the grade/score, no extra text
   - Expanded view: show full breakdown (fat/salt/sugar %, formula version, methodology link)

4. Health Warning Labels
   - Collapsed view: show warning icon + which countries would require a warning label 
     (e.g., "Would carry warnings in Mexico & Chile") with one-line reason
   - Expanded view: show full Mexico/Chile warning text and regulatory citation (NOM-051 etc.)

5. Key Concerns & Findings
   - Collapsed view: list each concern as a single line with severity tag (e.g., 
     "⚠ Elevated Added Sugar (35g)")
   - Expanded view: full explanation, health context, and comparison to daily limits

6. Ingredient & Additive Analysis
   - Collapsed view: simple list of ingredients with a color-coded risk dot (green/yellow/red) 
     — no table, no E-codes visible upfront
   - Expanded view (per ingredient, click to open): E-code, category, full risk profile, 
     evidence/source links

FOOTER (unchanged, keep as-is):
- Regulatory sources, "Evidence First," "Public Interest Neutrality," and disclaimer sections 
  stay collapsed/minimized at the bottom, low visual priority.

INTERACTION NOTES:
- Use accordion or expandable card components for each section
- Default state = all sections collapsed except header and banned-status banner
- Use consistent iconography and color coding (green/yellow/orange/red) for risk levels 
  across all sections
- Keep expand/collapse animation smooth and lightweight for mobile performance
</USER_REQUEST>
<ADDITIONAL_METADATA>
The current local time is: 2026-08-06T18:42:18+05:30.
</ADDITIONAL_METADATA>
<USER_SETTINGS_CHANGE>
The user changed setting `Model Selection` from Gemini 3.5 Flash (High) to Gemini 3.1 Pro (High). No need to comment on this change if the user doesn't ask about it. If reporting what model you are, please use a human readable name instead of the exact string.
</USER_SETTINGS_CHANGE>