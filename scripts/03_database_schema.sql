-- Plans Table --

CREATE TABLE aca_individual_marketplace.plans (
    PLANID TEXT,
    AREA TEXT,
    ST TEXT,
    CARRIER TEXT,
    PLANNAME TEXT,
    METAL TEXT,
    PLANTYPE INTEGER,
    CSR BOOLEAN,
    PLANMARKET INTEGER,
    CHILDONLY BOOLEAN,
    NETWORKID TEXT,
    ACTIVELY_MARKETED BOOLEAN,
    MULTITIERED BOOLEAN,
    PRIMARY KEY (PLANID, AREA)
);

SELECT * FROM aca_individual_marketplace.plans;

-- Benefits Table --

DROP TABLE IF EXISTS aca_individual_marketplace.benefits;

CREATE TABLE aca_individual_marketplace.benefits (
    PLANID TEXT,
    AREA TEXT,
	
    LIMITED INTEGER,
	
    CopayInn_TIERS INTEGER,
    CopayInnTier1Complex INTEGER,
    CopayInnTier1 INTEGER,
	CopayInnTier1A NUMERIC,
    
    CopayInnTier2Complex INTEGER,
    CopayInnTier2 INTEGER,
	CopayInnTier2A NUMERIC,
    
    CoinsInn_TIERS INTEGER,
    CoinsInnTier1Complex INTEGER,
    CoinsInnTier1 INTEGER,
    CoinsInnTier1A NUMERIC,
    
    CoinsInnTier2Complex INTEGER,
    CoinsInnTier2 INTEGER,
    CoinsInnTier2A NUMERIC,
    
    CopayOutofNetComplex INTEGER,
    CopayOutofNet INTEGER,
    CopayOutofNetA NUMERIC,
    
    CoinsOutofNetComplex INTEGER,
    CoinsOutofNet INTEGER,
    CoinsOutofNetA NUMERIC,

    benefit_code TEXT,

    PRIMARY KEY (PLANID, AREA, benefit_code)
);


SELECT * FROM aca_individual_marketplace.benefits;

-- Premium Table --

CREATE TABLE aca_individual_marketplace.premium (
    PLANID TEXT,
    AREA TEXT,
    ST TEXT,
    PREMI21_BASE NUMERIC,
    PREMI2C30 NUMERIC,
    PREMC2C30 NUMERIC,
    PRIMARY KEY (PLANID, AREA)
);

SELECT * FROM aca_individual_marketplace.premium;

-- State Age Curve Table --

CREATE TABLE aca_individual_marketplace.age_multiplier (
    AGE INTEGER PRIMARY KEY,
    "DEFAULT" NUMERIC,
    "AL" NUMERIC,
    "DC" NUMERIC,
    "MA" NUMERIC,
    "MN" NUMERIC,
    "MS" NUMERIC,
    "OR" NUMERIC,
    "UT" NUMERIC
);

SELECT * FROM aca_individual_marketplace.age_multiplier;

-- ZIP to FIPS Mapping Table --

CREATE TABLE aca_individual_marketplace.zip_fips (
    ZIP INTEGER,
    COUNTY TEXT,
    ST TEXT,
    FIPS INTEGER,
	PRIMARY KEY (ZIP, COUNTY)
);

SELECT * FROM aca_individual_marketplace.zip_fips;

-- COUNTY to RATING AREA Mapping Table --

CREATE TABLE aca_individual_marketplace.county_area (
    FIPS INTEGER,
    COUNTY TEXT,
    AREA_COUNT INTEGER,
    AREA TEXT,
	PRIMARY KEY (AREA, COUNTY)
);

SELECT * FROM aca_individual_marketplace.county_area;

-- Deductibles Table --

CREATE TABLE aca_individual_marketplace.deductibles (
    PLANID TEXT,
    AREA TEXT,

    MED_IN_IND_CODE INTEGER,
    MED_IN_IND_TIERS INTEGER,
    MED_IN_IND_TIER1_AMOUNT NUMERIC,
    MED_IN_IND_TIER2_AMOUNT NUMERIC,

    DRUG_IN_IND_CODE INTEGER,
    DRUG_IN_IND_TIERS INTEGER,
    DRUG_IN_IND_TIER1_AMOUNT NUMERIC,
    DRUG_IN_IND_TIER2_AMOUNT NUMERIC,

    TOT_IN_IND_CODE INTEGER,
    TOT_IN_IND_TIERS INTEGER,
    TOT_IN_IND_TIER1_AMOUNT NUMERIC,
    TOT_IN_IND_TIER2_AMOUNT NUMERIC,

    MED_OUT_IND_CODE INTEGER,
    DRUG_OUT_IND_CODE INTEGER,
    TOT_OUT_IND_CODE INTEGER,

    MED_OUT_IND_AMOUNT NUMERIC,
    DRUG_OUT_IND_AMOUNT NUMERIC,
    TOT_OUT_IND_AMOUNT NUMERIC,

    MED_IN_FAM_CODE INTEGER,
    MED_IN_FAM_TIERS INTEGER,
    MED_IN_FAM_TIER1_AMOUNT NUMERIC,
    MED_IN_FAM_TIER2_AMOUNT NUMERIC,

    DRUG_IN_FAM_CODE INTEGER,
    DRUG_IN_FAM_TIERS INTEGER,
    DRUG_IN_FAM_TIER1_AMOUNT NUMERIC,
    DRUG_IN_FAM_TIER2_AMOUNT NUMERIC,

    TOT_IN_FAM_CODE INTEGER,
    TOT_IN_FAM_TIERS INTEGER,
    TOT_IN_FAM_TIER1_AMOUNT NUMERIC,
    TOT_IN_FAM_TIER2_AMOUNT NUMERIC,

    MED_OUT_FAM_CODE INTEGER,
    DRUG_OUT_FAM_CODE INTEGER,
    TOT_OUT_FAM_CODE INTEGER,

    MED_OUT_FAM_AMOUNT NUMERIC,
    DRUG_OUT_FAM_AMOUNT NUMERIC,
    TOT_OUT_FAM_AMOUNT NUMERIC,

    PRIMARY KEY (PLANID, AREA)
);

SELECT * FROM aca_individual_marketplace.deductibles;

-- Maximum Out Of Pocket Table --

CREATE TABLE aca_individual_marketplace.moop (
    PLANID TEXT,
    AREA TEXT,

    MED_IN_IND_CODE INTEGER,
    MED_IN_IND_TIERS INTEGER,
    MED_IN_IND_TIER1_AMOUNT NUMERIC,
    MED_IN_IND_TIER2_AMOUNT NUMERIC,

    DRUG_IN_IND_CODE INTEGER,
    DRUG_IN_IND_TIERS INTEGER,
    DRUG_IN_IND_TIER1_AMOUNT NUMERIC,
    DRUG_IN_IND_TIER2_AMOUNT NUMERIC,

    TOT_IN_IND_CODE INTEGER,
    TOT_IN_IND_TIERS INTEGER,
    TOT_IN_IND_TIER1_AMOUNT NUMERIC,
    TOT_IN_IND_TIER2_AMOUNT NUMERIC,

    MED_OUT_IND_CODE INTEGER,
    DRUG_OUT_IND_CODE INTEGER,
    TOT_OUT_IND_CODE INTEGER,

    MED_OUT_IND_AMOUNT NUMERIC,
    DRUG_OUT_IND_AMOUNT NUMERIC,
    TOT_OUT_IND_AMOUNT NUMERIC,

    MED_IN_FAM_CODE INTEGER,
    MED_IN_FAM_TIERS INTEGER,
    MED_IN_FAM_TIER1_AMOUNT NUMERIC,
    MED_IN_FAM_TIER2_AMOUNT NUMERIC,

    DRUG_IN_FAM_CODE INTEGER,
    DRUG_IN_FAM_TIERS INTEGER,
    DRUG_IN_FAM_TIER1_AMOUNT NUMERIC,
    DRUG_IN_FAM_TIER2_AMOUNT NUMERIC,

    TOT_IN_FAM_CODE INTEGER,
    TOT_IN_FAM_TIERS INTEGER,
    TOT_IN_FAM_TIER1_AMOUNT NUMERIC,
    TOT_IN_FAM_TIER2_AMOUNT NUMERIC,

    MED_OUT_FAM_CODE INTEGER,
    DRUG_OUT_FAM_CODE INTEGER,
    TOT_OUT_FAM_CODE INTEGER,

    MED_OUT_FAM_AMOUNT NUMERIC,
    DRUG_OUT_FAM_AMOUNT NUMERIC,
    TOT_OUT_FAM_AMOUNT NUMERIC,

    PRIMARY KEY (PLANID, AREA)
);

SELECT * FROM aca_individual_marketplace.moop;


SELECT 
    p.planname, 
    p.carrier, 
    m.TOT_OUT_IND_AMOUNT, 
    m.MED_OUT_IND_AMOUNT, 
    m.DRUG_OUT_IND_AMOUNT
FROM aca_individual_marketplace.moop m
JOIN aca_individual_marketplace.plans p 
    ON m.planid = p.planid AND m.area = p.area
WHERE m.TOT_OUT_IND_AMOUNT IS NOT NULL
  AND m.area LIKE 'IN%';


-- Connecting the Tables --

ALTER TABLE aca_individual_marketplace.benefits
ADD FOREIGN KEY (PLANID, AREA)
REFERENCES aca_individual_marketplace.plans (PLANID, AREA);

ALTER TABLE aca_individual_marketplace.deductibles
ADD FOREIGN KEY (PLANID, AREA)
REFERENCES aca_individual_marketplace.plans (PLANID, AREA);

ALTER TABLE aca_individual_marketplace.moop
ADD FOREIGN KEY (PLANID, AREA)
REFERENCES aca_individual_marketplace.plans (PLANID, AREA);

ALTER TABLE aca_individual_marketplace.premium
ADD FOREIGN KEY (PLANID, AREA)
REFERENCES aca_individual_marketplace.plans (PLANID, AREA);

-- Test queries --

-- Get the Plan ID, the Area it's offered in, and the benefit code associated with it.
SELECT p.PLANID, p.AREA, b.benefit_code
FROM aca_individual_marketplace.plans p
JOIN aca_individual_marketplace.benefits b ON p.PLANID = b.PLANID AND p.AREA = b.AREA
LIMIT 5;

-- WRONG: Joining on COUNTY name causes incorrect matches 
-- when multiple states have counties with the same name 
-- e.g. "Barbour County" exists in both AL and WV
SELECT DISTINCT z.ZIP, z.COUNTY, c.AREA
FROM aca_individual_marketplace.zip_fips z
JOIN aca_individual_marketplace.county_area c
  ON z.COUNTY = c.COUNTY
WHERE z.ZIP = '36053';

--CORRECT: Joining on FIPS ensures accurate matching, since FIPS uniquely identifies each county
SELECT DISTINCT z.ZIP, z.COUNTY, c.AREA
FROM aca_individual_marketplace.zip_fips z
JOIN aca_individual_marketplace.county_area c
  ON z.FIPS = c.FIPS
WHERE z.ZIP = '36053';

--CORRECT: Joining on FIPS ensures accurate matching, since FIPS uniquely identifies each county
SELECT DISTINCT z.ZIP, z.COUNTY, c.AREA
FROM aca_individual_marketplace.zip_fips z
JOIN aca_individual_marketplace.county_area c
  ON z.FIPS = c.FIPS
WHERE z.COUNTY = 'Barbour County';

-- Create indices for common user queries

CREATE INDEX idx_zip_fips_zip ON aca_individual_marketplace.zip_fips (ZIP);
CREATE INDEX idx_county_area_county ON aca_individual_marketplace.county_area (COUNTY);
CREATE INDEX idx_plans_area ON aca_individual_marketplace.plans (AREA);
CREATE INDEX idx_benefits_code ON aca_individual_marketplace.benefits (benefit_code);
CREATE INDEX idx_planid ON aca_individual_marketplace.plans (PLANID);
CREATE INDEX idx_age ON aca_individual_marketplace.age_multiplier (AGE);

-- Get all plans for a user ZIP code
SELECT DISTINCT p.*
FROM aca_individual_marketplace.zip_fips z
JOIN aca_individual_marketplace.county_area c ON z.FIPS = c.FIPS
JOIN aca_individual_marketplace.plans p ON c.AREA = p.AREA
WHERE z.ZIP = 36053;

-- Create a view for plan info by ZIP code
CREATE OR REPLACE VIEW aca_individual_marketplace.plans_by_zip AS
SELECT DISTINCT z.ZIP, z.COUNTY, p.*
FROM aca_individual_marketplace.zip_fips z
JOIN aca_individual_marketplace.county_area c ON z.FIPS = c.FIPS
JOIN aca_individual_marketplace.plans p ON c.AREA = p.AREA
WHERE p.planid NOT SIMILAR TO '%-(04|05|06)';  --Removing the last codes -04,-05,-06 for plans with same id and area


SELECT * FROM aca_individual_marketplace.plans_by_zip
WHERE ST = 'IN' AND COUNTY = 'Monroe County' AND ZIP = 47408;

			
-- Create a view for plan info with premium
CREATE VIEW aca_individual_marketplace.plan_with_premium AS
SELECT p.PLANID, p.AREA, p.CARRIER, p.PLANNAME, p.METAL, pr.PREMI21_BASE, pr.PREMI2C30, pr.PREMC2C30
FROM aca_individual_marketplace.plans p
JOIN aca_individual_marketplace.premium pr
  ON p.PLANID = pr.PLANID AND p.AREA = pr.AREA;

-- Show all Gold plans in Alabama with base premium under $400
SELECT *
FROM aca_individual_marketplace.plan_with_premium
WHERE METAL = 'Gold' 
  AND PREMI21_BASE < 500
  AND AREA LIKE 'AL%';

-- Create a view for plan info with In-Network Tier 1 deductible and MOOP individual amounts
CREATE VIEW aca_individual_marketplace.plan_with_moop_deductibles AS
SELECT 
    p.PLANID, p.AREA, p.CARRIER, p.PLANNAME, p.METAL,
    d.MED_IN_IND_TIER1_AMOUNT AS in_network_deductible_medical,
    d.DRUG_IN_IND_TIER1_AMOUNT AS in_network_deductible_drug,
	d.TOT_IN_IND_TIER1_AMOUNT AS in_network_deductible_total,
    m.MED_IN_IND_TIER1_AMOUNT AS in_network_moop_medical,
    m.DRUG_IN_IND_TIER1_AMOUNT AS in_network_moop_drug,
	m.TOT_IN_IND_TIER1_AMOUNT AS in_network_moop_total
FROM aca_individual_marketplace.plans p
JOIN aca_individual_marketplace.deductibles d
  ON p.PLANID = d.PLANID AND p.AREA = d.AREA
JOIN aca_individual_marketplace.moop m
  ON p.PLANID = m.PLANID AND p.AREA = m.AREA;

-- Find all Silver plans where the in-network total MOOP is under $1000
SELECT *
FROM aca_individual_marketplace.plan_with_moop_deductibles
WHERE METAL = 'Silver'
  AND in_network_moop_total < 1000

-- Create a view for plan info by benefit
CREATE VIEW aca_individual_marketplace.plans_by_benefit AS
SELECT 
    p.PLANID,
    p.AREA,
    p.CARRIER,
    p.PLANNAME,
    p.METAL,
    b.benefit_code,
    b.CopayInnTier1A AS in_network_copay_amount,
    b.CoinsInnTier1A AS in_network_coinsurance_percentage,
	b.CopayOutofNetA AS out_of_network_copay_amount,
	b.CoinsOutofNetA AS out_of_network_coinsurance_percentage
FROM aca_individual_marketplace.plans p
JOIN aca_individual_marketplace.benefits b
  ON p.PLANID = b.PLANID AND p.AREA = b.AREA;

-- Find all plans in ZIP 36053 that cover Emergency Room (ER) benefits with an in-network copay under $1000
SELECT pb.*
FROM aca_individual_marketplace.plans_by_benefit pb
JOIN aca_individual_marketplace.county_area ca ON ca.AREA = pb.AREA
JOIN aca_individual_marketplace.zip_fips z ON z.FIPS = ca.FIPS 
WHERE z.ZIP = 36053
  AND pb.benefit_code = 'ER'
  AND pb.in_network_copay_amount < 1000;


-- Max/Min Base Premium for slider range
SELECT MIN(PREMI21_BASE), MAX(PREMI21_BASE) FROM aca_individual_marketplace.premium;

-- Max/Min MOOP
SELECT MIN(TOT_IN_IND_TIER1_AMOUNT), MAX(TOT_IN_IND_TIER1_AMOUNT) FROM aca_individual_marketplace.moop;

-- Max/Min Deductible
SELECT MIN(TOT_IN_IND_TIER1_AMOUNT), MAX(TOT_IN_IND_TIER1_AMOUNT) FROM aca_individual_marketplace.deductibles;

-- Max/Min Copay
SELECT MIN(CopayInnTier1A), MAX(CopayInnTier1A) FROM aca_individual_marketplace.benefits;

-- Max/Min Coinsurance
SELECT MIN(CoinsInnTier1A), MAX(CoinsInnTier1A) FROM aca_individual_marketplace.benefits;

