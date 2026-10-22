-- =====================================================================
-- PhytoVault: research-level schema migration
-- Additive only: nothing is dropped, renamed or emptied.
-- Safe to run on the existing database. If you prefer an idempotent
-- runner (skips columns/tables that already exist), use:
--     python migrate_research_schema.py
-- =====================================================================
USE phytovault;

-- 1. Taxonomy + occurrence tier on plants
ALTER TABLE plants
    ADD COLUMN kingdom         VARCHAR(100) NULL DEFAULT 'Plantae' AFTER species,
    ADD COLUMN phylum          VARCHAR(100) NULL AFTER kingdom,
    ADD COLUMN class_name      VARCHAR(100) NULL AFTER phylum,
    ADD COLUMN order_name      VARCHAR(100) NULL AFTER class_name,
    ADD COLUMN occurrence_tier ENUM('A','B','C','R') NULL AFTER category,
    ADD KEY idx_distribution (distribution),
    ADD KEY idx_occurrence_tier (occurrence_tier);

-- 2. Medicinal uses: which part + how it is prepared (per plant)
ALTER TABLE plant_uses
    ADD COLUMN plant_part  VARCHAR(150) NULL AFTER use_id,
    ADD COLUMN preparation TEXT NULL AFTER plant_part;

-- 3. Phytochemicals: compound class
ALTER TABLE phytochemicals
    ADD COLUMN compound_class VARCHAR(150) NULL AFTER compound_name,
    ADD KEY idx_compound_class (compound_class);

-- 4. Bioactivity (many per plant)
CREATE TABLE IF NOT EXISTS plant_bioactivities (
    bioactivity_id INT NOT NULL AUTO_INCREMENT,
    plant_id       INT NOT NULL,
    activity_name  VARCHAR(150) NOT NULL,
    PRIMARY KEY (bioactivity_id),
    KEY idx_bio_plant (plant_id),
    KEY idx_bio_name (activity_name),
    CONSTRAINT fk_bio_plant FOREIGN KEY (plant_id)
        REFERENCES plants (plant_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. ADMET (one row per plant)
CREATE TABLE IF NOT EXISTS plant_admet (
    admet_id     INT NOT NULL AUTO_INCREMENT,
    plant_id     INT NOT NULL,
    absorption   TEXT NULL,
    distribution TEXT NULL,
    metabolism   TEXT NULL,
    excretion    TEXT NULL,
    toxicity     TEXT NULL,
    PRIMARY KEY (admet_id),
    UNIQUE KEY uq_admet_plant (plant_id),
    CONSTRAINT fk_admet_plant FOREIGN KEY (plant_id)
        REFERENCES plants (plant_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. References: reuses your existing research_papers + paper_plants tables
--    (authors, title, journal, publication_year, doi, paper_url already exist).
