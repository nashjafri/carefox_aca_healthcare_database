import psycopg2
import psycopg2.extras

from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_config import get_db_connection  

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages


# -- Directories --

STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia"
}


PLAN_TYPES = {
    1: "PPO",
    2: "HMO",
    3: "POS",
    4: "EPO",
    5: "Other"
}

PLAN_MARKETS = {
    1: "Only available on state/federal marketplace",
    2: "Only available off state/federal marketplace",
    3: "Available both on and off state/federal marketplace"
}

COPAY_CODES = {
    0: "No coverage for this benefit.",
    1: "No charge. This benefit requires no payment by the consumer.",
    2: "No charge after deductible.",
    3: "Copay always applies.",
    4: "Copay applies only after deductible.",
    5: "Copay applies only before deductible.",
    6: "Per-day copay (inpatient).",
    7: "Per-stay copay (inpatient).",
    8: "Per-day after deductible (inpatient).",
    9: "Per-day before deductible (inpatient).",
    10: "Per-stay after deductible (inpatient).",
    11: "Per-stay before deductible (inpatient).",
    99: "Cost-sharing is unknown."
}

BENEFIT_NAMES = {
    "AB": "Ambulance",
    "EY": "Child Eye Exam",
    "EW": "Child Eyewear",
    "DT": "Diagnostic Test",
    "DM": "Durable Medical Equipment",
    "ER": "Emergency Room",
    "GD": "Generic Drugs",
    "HA": "Habilitation Services",
    "HH": "Home Health Care",
    "HS": "Hospice Service",
    "IM": "Imaging",
    "IB": "Inpatient Birth",
    "IP": "Inpatient Facility",
    "IN": "Inpatient Mental Health",
    "IH": "Inpatient Physician",
    "IS": "Inpatient Substance Use",
    "ND": "Non-Preferred Brand Drugs",
    "OP": "Outpatient Facility",
    "OM": "Outpatient Mental Health",
    "OH": "Outpatient Physician",
    "OS": "Outpatient Substance Use",
    "PD": "Preferred Brand Drugs",
    "PN": "Prenatal/Postnatal Care",
    "PV": "Preventive Care",
    "PC": "Primary Care Physician",
    "RH": "Rehabilitation Services",
    "SN": "Skilled Nursing",
    "SP": "Specialist Visit",
    "SD": "Specialty Drugs",
    "UC": "Urgent Care"
}


# -------------------- Routes --------------------

# --- HOME ---
@app.route('/')
def home_page():
    return render_template('pages/home.html')

# --- BY ZIP  --- 
@app.route('/by-zip', methods=['GET', 'POST'])
def search_by_zip():
    conn = get_db_connection()
    cur = conn.cursor()

    # Get distinct states for dropdown
    cur.execute("SELECT DISTINCT ST FROM zip_fips ORDER BY ST;")
    state_codes = [row[0] for row in cur.fetchall()]
    states = [(st, STATE_NAMES.get(st, st)) for st in state_codes]

    selected_state = request.form.get('state')
    entered_zip = request.form.get('zip', '').strip()
    counties = []

    if selected_state:
        cur.execute("SELECT DISTINCT COUNTY FROM zip_fips WHERE ST = %s ORDER BY COUNTY;", (selected_state,))
        counties = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    if request.method == 'POST' and request.form.get('mode') == 'submit':
        zip_code = entered_zip
        county = request.form.get('county', '').strip()
        state = selected_state
        household = request.form.get('household', '').strip()

        if not zip_code and (not state or not county):
            flash("Please enter a ZIP code OR select a state and county.", "error")
            return render_template('pages/by_zip.html',
                states=states,
                selected_state=state,
                counties=counties,
                STATE_NAMES=STATE_NAMES
            )

        if not household:
            flash("Please select a household type.", "error")
            return render_template('pages/by_zip.html',
                states=states,
                selected_state=state,
                counties=counties,
                STATE_NAMES=STATE_NAMES
            )

        return redirect(url_for(
            'zip_results_page',
            zip=zip_code,
            state=state,
            county=county,
            household=household
        ))

    return render_template(
        'pages/by_zip.html',
        states=states,
        selected_state=selected_state,
        counties=counties,
        STATE_NAMES=STATE_NAMES
    )


# --- Helper to parse floats safely ---
def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

#--- ZIP RESULTS ---
@app.route('/zip-results', methods=['GET'])
def zip_results_page():
    from psycopg2.extras import RealDictCursor
    from collections import defaultdict

    zip_code = request.args.get('zip', '').strip()
    state = request.args.get('state', '').strip()
    county = request.args.get('county', '').strip()
    household_type = request.args.get('household', '').strip()
    max_premium = parse_float(request.args.get('max_premium'))
    max_moop = parse_float(request.args.get('max_moop'))
    max_deductible = parse_float(request.args.get('max_deductible'))
    max_copay = parse_float(request.args.get('max_copay'))
    max_coinsurance = parse_float(request.args.get('max_coinsurance'))
    selected_benefits = request.args.getlist('benefits')
    carriers_selected = request.args.getlist('carrier')
    sort_by = request.args.get('sort_by', '')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    base_query = """
        SELECT pz.*, pr.PREMI21_BASE, moop.TOT_IN_IND_TIER1_AMOUNT AS moop,
               ded.TOT_IN_IND_TIER1_AMOUNT AS deductible
        FROM aca_individual_marketplace.plans_by_zip pz
        LEFT JOIN aca_individual_marketplace.premium pr
            ON pz.planid = pr.planid AND pz.area = pr.area
        LEFT JOIN aca_individual_marketplace.moop moop
            ON pz.planid = moop.planid AND pz.area = moop.area
        LEFT JOIN aca_individual_marketplace.deductibles ded
            ON pz.planid = ded.planid AND pz.area = ded.area
        WHERE {}
    """

    if zip_code:
        area_filter = "pz.zip = %s"
        area_params = [zip_code]
    elif state and county:
        area_filter = "pz.st = %s AND pz.county = %s"
        area_params = [state, county]
    else:
        flash("Please enter a ZIP code or select State + County.")
        return redirect(url_for('search_by_zip'))

    query_filters = [area_filter]
    query_params = area_params

    if carriers_selected:
        query_filters.append("pz.carrier = ANY(%s)")
        query_params.append(carriers_selected)

    if max_premium is not None:
        query_filters.append("pr.PREMI21_BASE <= %s")
        query_params.append(max_premium)
    if max_moop is not None:
        query_filters.append("moop.TOT_IN_IND_TIER1_AMOUNT <= %s")
        query_params.append(max_moop)
    if max_deductible is not None:
        query_filters.append("ded.TOT_IN_IND_TIER1_AMOUNT <= %s")
        query_params.append(max_deductible)

    final_query = base_query.format(" AND ".join(query_filters))
    cur.execute(final_query, query_params)
    plans = cur.fetchall()

    plan_keys = [(p['planid'], p['area']) for p in plans]
    if plan_keys:
        conditions = []
        params = []
        for planid, area in plan_keys:
            conditions.append("(planid = %s AND area = %s)")
            params.extend([planid, area])
        where_clause = " OR ".join(conditions)
        query = f"""
        SELECT planid, area, benefit_code, CopayInnTier1A AS copay, CoinsInnTier1A AS coins
        FROM aca_individual_marketplace.benefits
        WHERE {where_clause}
        """
        cur.execute(query, params)
        benefit_rows = cur.fetchall()
    else:
        benefit_rows = []

    plan_benefit_map = defaultdict(dict)
    for row in benefit_rows:
        key = (row['planid'], row['area'])
        plan_benefit_map[key][row['benefit_code']] = {
            'copay': row['copay'],
            'coins': row['coins']
        }

    def passes_all_checks(plan):
        key = (plan['planid'], plan['area'])
        benefits = plan_benefit_map.get(key, {})
        if selected_benefits:
            for code in selected_benefits:
                info = benefits.get(code)
                if not info:
                    return False
                if max_copay is not None and info['copay'] is not None and info['copay'] > max_copay:
                    return False
                if max_coinsurance is not None and info['coins'] is not None and info['coins'] > max_coinsurance:
                    return False
            return True
        if max_copay is not None:
            if not any(info['copay'] is not None and info['copay'] <= max_copay for info in benefits.values()):
                return False
        if max_coinsurance is not None:
            if not any(info['coins'] is not None and info['coins'] <= max_coinsurance for info in benefits.values()):
                return False
        return True

    plans = [plan for plan in plans if passes_all_checks(plan)]

    if sort_by == 'premium':
        plans.sort(key=lambda p: p.get('premi21_base') or float('inf'))
    elif sort_by == 'moop':
        plans.sort(key=lambda p: p.get('moop') or float('inf'))
    elif sort_by == 'deductible':
        plans.sort(key=lambda p: p.get('deductible') or float('inf'))

    grouped_plans = {}
    for plan in plans:
        carrier = plan['carrier']
        plan_data = {
            "id": plan['planid'],
            "area": plan['area'],
            "name": plan['planname'],
            "premium": plan.get('premi21_base'),
            "moop": plan.get('moop'),
            "deductible": plan.get('deductible'),
            "zip": plan['zip'],
            "st": plan['st'],
            "carrier": plan['carrier'],
            "metal": plan['metal'],
            "plantype": plan['plantype']
        }
        grouped_plans.setdefault(carrier, []).append(plan_data)

    cur.close()
    conn.close()

    return render_template(
        'pages/zip_results.html',
        grouped_plans=grouped_plans,
        household_type=household_type
    )

# --- PLAN DETAILS ----
@app.route('/plans/<planid>/<area>')
def plan_detail(planid, area):
    # Parse query parameters
    selected_benefits = request.args.getlist('benefits')
    max_copay = request.args.get('max_copay', type=float)
    max_coinsurance = request.args.get('max_coinsurance', type=float)

    # Determine household type
    household_raw = request.args.get('household', 'Individual')
    household_type = 'IND' if household_raw.lower() == 'individual' else 'FAM'


    # Connect to DB
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Plan metadata
    cur.execute("""
        SELECT * FROM aca_individual_marketplace.plans
        WHERE planid = %s AND area = %s
    """, (planid, area))
    plan = cur.fetchone()

    # Deductibles based on household type
    deductible_fields = {
        'med_in': f'med_in_{household_type.lower()}_tier1_amount',
        'drug_in': f'drug_in_{household_type.lower()}_tier1_amount',
        'tot_in': f'tot_in_{household_type.lower()}_tier1_amount',
        'med_out': f'med_out_{household_type.lower()}_amount',
        'drug_out': f'drug_out_{household_type.lower()}_amount',
        'tot_out': f'tot_out_{household_type.lower()}_amount'
    }
    cur.execute(f"""
        SELECT {', '.join(deductible_fields.values())}
        FROM aca_individual_marketplace.deductibles
        WHERE planid = %s AND area = %s
    """, (planid, area))
    raw_deductibles = cur.fetchone()
    deductibles = dict(zip(deductible_fields.keys(), raw_deductibles.values())) if raw_deductibles else {}

    # MOOP based on household type — FIXED!
    moop_fields = {
        'med_in': f'med_in_{household_type.lower()}_tier1_amount',
        'drug_in': f'drug_in_{household_type.lower()}_tier1_amount',
        'tot_in': f'tot_in_{household_type.lower()}_tier1_amount',
        'med_out': f'med_out_{household_type.lower()}_amount',
        'drug_out': f'drug_out_{household_type.lower()}_amount',
        'tot_out': f'tot_out_{household_type.lower()}_amount'
    }
    cur.execute(f"""
        SELECT {', '.join(moop_fields.values())}
        FROM aca_individual_marketplace.moop
        WHERE planid = %s AND area = %s
    """, (planid, area))
    raw_moop = cur.fetchone()
    moop = dict(zip(moop_fields.keys(), raw_moop.values())) if raw_moop else {}

    # Benefits logic
    if selected_benefits:
        cur.execute("""
            SELECT * FROM aca_individual_marketplace.benefits
            WHERE planid = %s AND area = %s AND benefit_code = ANY(%s)
        """, (planid, area, selected_benefits))
        benefits = cur.fetchall()

    elif max_copay is not None or max_coinsurance is not None:
        cur.execute("""
            SELECT * FROM aca_individual_marketplace.benefits
            WHERE planid = %s AND area = %s
        """, (planid, area))
        all_benefits = cur.fetchall()
        benefits = [
            b for b in all_benefits if (
                (max_copay is None or (b['copayinntier1a'] is not None and b['copayinntier1a'] <= max_copay)) or
                (max_coinsurance is None or (b['coinsinntier1a'] is not None and b['coinsinntier1a'] <= max_coinsurance))
            )
        ]
    else:
        cur.execute("""
            SELECT * FROM aca_individual_marketplace.benefits
            WHERE planid = %s AND area = %s
        """, (planid, area))
        benefits = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        'pages/plan_detail.html',
        plan=plan,
        planid=planid,
        area=area,
        deductibles=deductibles,
        moop=moop,
        benefits=benefits,
        household_type=household_type,
        plan_types=PLAN_TYPES,
        plan_markets=PLAN_MARKETS,
        copay_codes=COPAY_CODES,
        benefit_names=BENEFIT_NAMES
    )


# ---- ESTIMATE PREMIUM FORM ----
@app.route('/estimate', methods=['GET', 'POST'])
def estimate_premium():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # STEP 1: Get metal properly depending on method
    if request.method == 'POST':
        zip_code = request.form.get('zip', '').strip()
        selected_state = request.form.get('state', '').strip()
        carrier = request.form.get('carrier', '').strip()
        age = request.form.get('age', '').strip()
        raw_metal = request.form.get('metal')
        plan_type_str = request.form.get('plantype')
    else:
        zip_code = request.args.get('zip', '').strip()
        selected_state = request.args.get('state', '').strip()
        carrier = request.args.get('carrier', '').strip()
        age = request.args.get('age', '').strip()
        raw_metal = request.args.get('metal')
        plan_type_str = request.args.get('plantype')

    # STEP 2: Normalize metal
    metal = raw_metal.replace('_', ' ').title() if raw_metal else ''
    print("RAW METAL:", raw_metal)
    print("FINAL METAL:", metal)

    # STEP 3: Map plan type
    plantype_mapping = {
        'PPO': 1,
        'HMO': 2,
        'POS': 3,
        'EPO': 4,
        'Other': 5
    }
    plan_type = plantype_mapping.get(plan_type_str) if plan_type_str else None

    # STEP 4: Get state list for dropdown
    cur.execute("SELECT DISTINCT ST FROM aca_individual_marketplace.zip_fips ORDER BY ST;")
    state_codes = [row['st'] for row in cur.fetchall()]
    states = [(st, STATE_NAMES.get(st, st)) for st in state_codes]

    # STEP 5: Get carriers ONLY for selected state if available
    if selected_state:
        cur.execute("""
            SELECT DISTINCT carrier 
            FROM aca_individual_marketplace.plans 
            WHERE st = %s 
            ORDER BY carrier
        """, (selected_state,))
    else:
        cur.execute("SELECT DISTINCT carrier FROM aca_individual_marketplace.plans ORDER BY carrier;")
    carriers = [row['carrier'] for row in cur.fetchall()]


    # STEP 6: On POST, return results
    if request.method == 'POST' and zip_code and selected_state and carrier and age:
        query = """
            SELECT DISTINCT planid, area, planname, carrier, metal
            FROM aca_individual_marketplace.plans_by_zip
            WHERE zip = %s AND st = %s AND carrier = %s
        """

        params = [zip_code, selected_state, carrier]

        if plan_type:
            query += " AND plantype = %s"
            params.append(plan_type)
        if metal:
            query += " AND metal = %s"
            params.append(metal.replace(' ', '_'))  # convert back for DB match

        cur.execute(query, params)
        plans = cur.fetchall()

        cur.close()
        conn.close()

        from collections import defaultdict

        # Group plans by metal level
        grouped_plans = defaultdict(list)
        for plan in plans:
            metal_level = plan['metal'].title() if plan['metal'] else 'Other'
            grouped_plans[metal_level].append(plan)

        # Sort keys manually for desired display order
        sorted_metals = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Catastrophic', 'Other']
        grouped_plans_ordered = {metal: grouped_plans[metal] for metal in sorted_metals if metal in grouped_plans}

        return render_template(
            'pages/estimate_results.html',
            plans_by_metal=grouped_plans_ordered,
            age=int(age),
            state=selected_state
        )


    # STEP 7: Return form page
    cur.close()
    conn.close()

    return render_template(
        'pages/estimate_form.html',
        states=states,
        selected_state=selected_state,
        zip=zip_code,
        carrier=carrier,
        age=age,
        plantype=plan_type_str,
        metal=metal,
        carriers=carriers
    )


# --- PREMIUM CALCULATOR ---

@app.route('/estimate-calc')
def estimate_calc():
    planid = request.args.get('planid')
    area = request.args.get('area')
    age = request.args.get('age', type=int)
    state = request.args.get('state')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Get base premium and metadata
    cur.execute("""
        SELECT pp.planname, pp.carrier, pp.metal, pp.premi21_base, pp.premi2c30, pp.premc2c30
        FROM aca_individual_marketplace.plan_with_premium pp
        WHERE pp.planid = %s AND pp.area = %s
    """, (planid, area))
    plan = cur.fetchone()

    # Get rate multiplier from age_multiplier
    cur.execute("""
        SELECT * FROM aca_individual_marketplace.age_multiplier
        WHERE age = %s
    """, (age,))
    rate_row = cur.fetchone()
    multiplier = rate_row.get(state) if state in rate_row and rate_row.get(state) else rate_row.get("DEFAULT")

    # Final premium
    user_premium = round(plan['premi21_base'] * multiplier, 2) if plan and multiplier else None

    cur.close()
    conn.close()

    return render_template("pages/premium_result.html", plan=plan, multiplier=multiplier,
                           age=age, user_premium=user_premium)


# --- ADD TO CART ---
@app.route('/add-to-cart')
def add_to_cart():
    planid = request.args.get('planid')
    area = request.args.get('area')
    redirect_url = request.args.get('redirect', request.referrer)

    if not planid or not area:
        flash("Missing plan information.")
        return redirect(redirect_url)

    cart = session.get('comparison_cart', [])
    key = [planid, area]

    if key not in cart:
        cart.append(key)
        session['comparison_cart'] = cart
        flash("Plan added to comparison cart!")
    else:
        flash("Plan is already in your cart.")

    return redirect(redirect_url)





# --- REMOVE FROM CART ---
@app.route('/remove-from-cart')
def remove_from_cart():
    planid = request.args.get('planid')
    area = request.args.get('area')

    if not planid or not area:
        flash("Invalid plan removal request.")
        return redirect(url_for('comparison_cart'))

    cart = session.get('comparison_cart', [])
    
    # Normalize to tuple strings for comparison (safe even if cart has list/tuple mix)
    updated_cart = [
        item for item in cart
        if not (str(item[0]) == planid and str(item[1]) == area)
    ]

    session['comparison_cart'] = updated_cart
    flash("Plan removed from comparison cart.")
    return redirect(url_for('comparison_cart'))




# --- EMPTY CART ---

@app.route('/empty-cart')
def empty_cart():
    session['comparison_cart'] = []
    flash("Comparison cart emptied.")
    return redirect(url_for('comparison_cart'))



# ---- COMPARISON CART PAGE -----
@app.route('/comparison-cart')
def comparison_cart():
    from psycopg2.extras import RealDictCursor
    cart = session.get('comparison_cart', [])

    clean_cart = [
        (item[0], item[1])
        for item in cart
        if isinstance(item, list) and len(item) == 2
    ]

    if not clean_cart:
        return render_template('pages/comparison_cart.html', plans=[])

    conditions = []
    params = []
    for planid, area in clean_cart:
        conditions.append("(pz.planid = %s AND pz.area = %s)")
        params.extend([planid, area])
    where_clause = " OR ".join(conditions)

    query = f"""
        SELECT *
        FROM (
            SELECT DISTINCT ON (pz.planid, pz.area)
                pz.planid, pz.area, pz.planname, pz.carrier, pz.metal, pz.plantype,
                pr.premi21_base, pr.premi2c30, pr.premc2c30,
                moop.tot_in_ind_tier1_amount AS moop_in,
                moop.tot_out_ind_amount AS moop_out,
                ded.tot_in_ind_tier1_amount AS ded_in,
                ded.tot_out_ind_amount AS ded_out
            FROM aca_individual_marketplace.plans_by_zip pz
            LEFT JOIN aca_individual_marketplace.premium pr 
                ON pr.planid = pz.planid AND pr.area = pz.area
            LEFT JOIN aca_individual_marketplace.moop moop 
                ON moop.planid = pz.planid AND moop.area = pz.area
            LEFT JOIN aca_individual_marketplace.deductibles ded 
                ON ded.planid = pz.planid AND ded.area = pz.area
            WHERE {where_clause}
            ORDER BY pz.planid, pz.area
        ) AS unique_plans
    """

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, params)
    plans = cur.fetchall()

    # === Fetch Copay and Coinsurance ===
    plan_keys = [(plan['planid'], plan['area']) for plan in plans]
    benefit_conditions = []
    benefit_params = []
    for planid, area in plan_keys:
        benefit_conditions.append("(planid = %s AND area = %s)")
        benefit_params.extend([planid, area])

    benefit_where_clause = " OR ".join(benefit_conditions)
    benefit_query = f"""
        SELECT planid, area, benefit_code, CopayInnTier1A AS copay, CoinsInnTier1A AS coins
        FROM aca_individual_marketplace.benefits
        WHERE {benefit_where_clause}
    """
    cur.execute(benefit_query, benefit_params)
    benefit_rows = cur.fetchall()

    # Split copay and coinsurance into separate maps
    copay_data = {}
    coins_data = {}
    for row in benefit_rows:
        key = (row['planid'], row['area'], row['benefit_code'])
        copay_data[key] = row['copay']
        coins_data[key] = row['coins']

    cur.close()
    conn.close()

    return render_template(
        'pages/comparison_cart.html',
        plans=plans,
        benefit_names=BENEFIT_NAMES,
        copay_data=copay_data,
        coins_data=coins_data
    )



# -------------------- Run App --------------------

if __name__ == '__main__':
    app.run(debug=True)
