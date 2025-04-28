# CareFox  
*ACA-Compliant (Individual) Healthcare Plan Comparison & Analytics Platform*  

<table>
<tr>
<td width="150">
<img src="images/image1.png" alt="CareFox Logo" width="140">
</td>
<td>
Project for the Spring 2025 course DSCI-D532 – Applied Database Technologies at Indiana University, Bloomington. <br>
Developer: <a href="https://github.com/nashjafri" target="_blank">Nasheed Jafri</a>
</td>
</tr>
</table>

## Overview

Choosing the right healthcare plan can be overwhelming due to the vast number of options, varying benefit coverages, network limitations, and cost structures. **CareFox** is a web-based platform designed to help users easily **compare ACA-compliant individual health insurance plans in the US market** based on key factors like coverage, cost, provider networks, and location accessibility.  

---

## Data Sources

- **Primary:** [HIX Compare Dataset](https://hix-compare.org) — plan-level information for nearly all ACA-compliant individual and small group health insurance markets.
- **Additional/External Sources:**  
  - [Medicare Inpatient Hospitals Data (CMS)](https://data.cms.gov/provider-summary-by-type-of-service/medicare-inpatient-hospitals)  
  - [Healthcare.gov Plan Information](https://www.healthcare.gov/health-plan-information/)  
  - [CMS Provider Data](https://data.cms.gov/provider-data/)  
  - [AHD.com Hospital Data](https://www.ahd.com/data_services.html) *(data requested)*  

---

## Technology Stack

- **Database:** SQL (relational queries), MongoDB (if needed)
- **Backend:** Python (Flask or Django)
- **Frontend:** React.js or basic HTML/CSS/JavaScript
- **Data Processing:** Pandas, NumPy, SQL
- **Visualization:** Plotly, Leaflet.js (interactive maps), Matplotlib
- **Hosting:** GitHub Pages (for static) or Cloud services like Heroku, AWS, or Firebase (for dynamic backend)

---

## Key Features

- **Plan Comparison Tool**
  - Compare plans based on premiums, deductibles, benefit coverage, and more.
  - Filter by budget, location (ZIP code), and preferences.

- **Geospatial Insights**
  - Interactive maps showing in-network hospitals and doctors nearby.
  - Visualize provider coverage areas.

- **Predictive Analytics**
  - Estimate procedure costs based on historical plan data.
  - Suggest best-fit plans based on user preferences and basic health history.

- **User Interaction**
  - Search, filter, and save preferred plans.
  - Manage provider preferences.

- **Data Visualization**
  - Cost trends, premium changes, and plan popularity graphs.
  - Regional comparisons of coverage and healthcare access.
