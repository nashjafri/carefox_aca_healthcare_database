<p align="center">
  <img src="image1.png" alt="App Screenshot" width="700">
</p>

SP25-BL-DSCI-D532  
**Applied Database Technologies**  
**Final Project**

# CareFox: ACA Plan Comparison App

**GitHub Repositories:**
- **Data Normalization and Cleaning:** [https://github.com/nashjafri/carefox_aca_healthcare_database](https://github.com/nashjafri/carefox_aca_healthcare_database)  
- **App Development using Flask:** [https://github.com/CareFox-ACA/carefox_app](https://github.com/CareFox-ACA/carefox_app)

---

## Purpose and Audience

The purpose of CareFox is to simplify the process of discovering, comparing, and estimating costs for Affordable Care Act (ACA) health insurance plans. Although the ACA was a major policy success in terms of expanding coverage, it has long suffered from limited transparency, narrow provider networks, and regionally fragmented access to plan details. Many users, especially those in rural or underserved areas, struggle to find plans that meet their needs due to limited network sizes and lack of centralized, user-friendly interfaces. This app is designed for individuals and families navigating the ACA marketplace who want a streamlined way to explore and compare health plans available in their region.

---

## App Functionalities

- **Homepage:**  
  Offers background on ACA, definitions of key insurance terms, Medicaid expansion info, and navigation to:
  - Explore plans
  - Estimate premiums
  - Compare selected plans

- **Find Plans by ZIP or County:**  
  - Users can enter a ZIP or select a State + County combination  
  - County dropdown is dynamically filtered by selected state  
  - User selects household type (Individual or Family) to personalize deductible/MOOP info

- **ZIP Results Page:**  
  - Displays all ACA plans for the region, grouped by **carrier**  
  - Sidebar filters:
    - Max deductible
    - Max out-of-pocket (MOOP)
    - Max copay and coinsurance
    - Desired benefits  
  - Each plan offers:
    - View details
    - Estimate monthly premium
    - Add to comparison cart

- **Plan Details Page:**
  - Shows:
    - Plan metadata (metal level, plan type, etc.)
    - Household-specific deductible & MOOP
    - Benefit-level cost-sharing:
      - In-network copay
      - In-network coinsurance
      - Out-of-network copay
      - Out-of-network coinsurance  
  - Smart filtering: Only displays relevant benefits based on user filters

- **Premium Estimator:**
  - User inputs: ZIP, state, age, carrier (optional: plan type, metal)
  - Calculates premium:  
    `Estimated Premium = Base Premium (age 21) × State Age Multiplier`  
  - Results:
    - Carrier, Metal Level, Age, Base Premium
    - Multiplier, Estimated Premium
    - Family premium examples
  - Options: Add to Cart, Try Another Estimate

- **Comparison Cart:**
  - Scrollable side-by-side plan comparison
  - Attributes displayed:
    - MOOP & Deductibles (in/out)
    - Base and Family Premiums
    - Copay & Coinsurance for up to 30 benefits
  - Delete individual plans or clear all

---

## Link/Hosting Status

The app currently runs **locally**.

-Attempts to host (e.g., on Render) failed due to PostgreSQL connection timeouts.  
-Free platforms were inadequate due to dataset size (~300MB+).  

Hosting will be reconsidered after optimizing data size and DB connections.

---

## Technical Development & Contributions

I was the **sole developer** on this project. My responsibilities included:

- Designing full relational schema (8 tables + 4 views)
- Cleaning & normalizing ACA plan data (723 → 192 columns)
- Creating dynamic filtering and performance-optimized views
- Implementing Flask routes and Jinja templates
- Writing backend logic for:
  - Premium estimation
  - Copay/coinsurance filtering
  - Comparison cart
- Frontend styling: HTML, CSS, FontAwesome
- Independent debugging, integration, and optimizations

---

## References

- [HIX Compare Dataset](https://www.hix-compare.org)  
- [CMS Age Curve Multipliers (State-wise)](https://www.cms.gov/CCIIO/Programs-and-Initiatives/Health-Insurance-Market-Reforms/Downloads/StateSpecAgeCrv053117.pdf)  
- [Kaggle ZIP-FIPS Crosswalk Dataset](https://www.kaggle.com/datasets/danofer/zipcodes-county-fips-crosswalk)  
- [Kaiser Family Foundation (KFF)](https://www.kff.org/status-of-state-medicaid-expansion-decisions/)  
- [Robert Wood Johnson Foundation (RWJF)](https://www.rwjf.org)  
- **IDEON** – Email consultation for field clarifications  
- **ChatGPT** – Helped debug:
  - Dynamic Jinja rendering
  - CSS button/table styling  
  _Note: All code/query logic was my own._

---

## Reflections & Learning

This project helped me grow in:

- Understanding U.S. healthcare policy and ACA plan structures
- Handling real-world data (723 cols × 85,000 rows)
- Schema normalization with composite keys (no unique ones!)
- Writing multi-table joins for ZIP-FIPS-County-State linkage
- End-to-end full stack web app development

**Challenges:**
- No simplification of messy data
- Lack of unique keys
- Legal limits on provider network integration
- Complex SQL without bloating schema
- First-ever solo full-stack app

---

## Future Improvements

- Add **exclusions/limitations** per benefit and visualize clearly
- Simplify views and route logic
- Integrate **provider-network** data when permitted
- Add sorting to comparison (e.g., by premium)
- User login/account features (though I liked hassle-free no-login)
- Deploy online after DB optimization
- Add interactive visuals (e.g., heatmaps, ratings)
- Include **small group marketplace** data (currently using individual market only)

---

## Developer

Nasheed Jafri
