-- -- Use database
USE plants;
GO

-- Ensure starting with an empty schema (dependent tables first)
DROP TABLE s_gamma.reading;
GO
DROP TABLE s_gamma.plant;
GO
DROP TABLE s_gamma.image;
GO
DROP TABLE s_gamma.license;
GO
DROP TABLE s_gamma.botanist;
GO
DROP TABLE s_gamma.origin;
GO


-- Create tables

-- Latitude/longitude precision matching API response.
CREATE TABLE s_gamma.origin (
    origin_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    time_zone_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    latitude DECIMAL(7,5) NOT NULL,
    longitude DECIMAL(8,5) NOT NULL,
);
GO

CREATE TABLE s_gamma.botanist (
    botanist_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(25),
    email VARCHAR(50)
);
GO

CREATE TABLE s_gamma.license (
    license_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    name VARCHAR(100),
    url TEXT,
    number SMALLINT,
);
GO

CREATE TABLE s_gamma.image (
    image_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    medium_url TEXT,
    regular_url TEXT,
    original_url TEXT,
    small_url TEXT,
    thumbnail_url TEXT,
    license_id INT,
    CONSTRAINT fk_license_id FOREIGN KEY (license_id) REFERENCES s_gamma.license (license_id)
);
GO

CREATE TABLE s_gamma.plant (
    plant_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    plant_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(100),
    origin_id INT NOT NULL,
    image_id INT,
    CONSTRAINT fk_origin_id FOREIGN KEY (origin_id) REFERENCES s_gamma.origin (origin_id),
    CONSTRAINT fk_image_id FOREIGN KEY (image_id) REFERENCES s_gamma.image (image_id)
);
GO

CREATE TABLE s_gamma.reading (
    reading_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    plant_id INT NOT NULL,
    botanist_id INT NOT NULL,
    soil_moisture DECIMAL(4,2) NOT NULL,
    temperature DECIMAL(3,2) NOT NULL,
    last_watered TIMESTAMP NOT NULL,
    recording_taken DATETIME2(6) NOT NULL,
    CONSTRAINT fk_plant_id FOREIGN KEY (plant_id) REFERENCES s_gamma.plant (plant_id),
    CONSTRAINT fk_botanist_id FOREIGN KEY (botanist_id) REFERENCES s_gamma.botanist(botanist_id)

);
GO

-- Sample inserts so other parts of pipeline can be tested
INSERT INTO s_gamma.botanist VALUES ('Carl Linnaeus', '(146)994-1635x35992', 'carl.linnaeus@lnhm.co.uk') -- plant 0
INSERT INTO s_gamma.botanist VALUES ('Gertrude Jekyll', '001-481-273-3691x127', 'gertrude.jekyll@lnhm.co.uk') -- plant 1
INSERT INTO s_gamma.botanist VALUES ('Eliza Andrews', '(846)669-6651x75948', 'eliza.andrews@lnhm.co.uk') -- plant 3
-- plant 2 has same botanist as plant 0

INSERT INTO s_gamma.plant VALUES ('Epipremnum Aureum', 'Epipremnum aureum', 1, 1 ); -- plant 0
INSERT INTO s_gamma.plant VALUES ('Venus flytrap', NULL, 2, NULL ); -- plant 1
INSERT INTO s_gamma.plant VALUES ('Corpse flower', NULL, 3, NULL ); -- plant 2
INSERT INTO s_gamma.plant VALUES ('Rafflesia arnoldii', NULL, 1, NULL); -- plant 3

INSERT INTO s_gamma.plant VALUES ()