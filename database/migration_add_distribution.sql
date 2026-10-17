USE phytovault;

-- Adds the separate "Distribution" field used by the Add / Edit Plant pages.
ALTER TABLE plants
    ADD COLUMN distribution VARCHAR(255) NULL AFTER origin;
