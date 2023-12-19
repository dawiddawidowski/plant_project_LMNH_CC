-- -- Use database
-- USE my_database;
-- GO

-- Ensure starting with an empty schema (dependent tables first)
DROP TABLE IF EXISTS s_gamma.reading;
DROP TABLE IF EXISTS s_gamma.plant;
DROP TABLE IF EXISTS s_gamma.image;
DROP TABLE IF EXISTS s_gamma.license;
DROP TABLE IF EXISTS s_gamma.botanist;
DROP TABLE IF EXISTS s_gamma.origin;
GO

-- Create tables

-- Latitude/longitude precision matching API response.
CREATE TABLE IF NOT EXISTS origin (
    origin_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    time_zone_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    latitude DECIMAL(7,5) NOT NULL,
    longitude DECIMAL(8,5) NOT NULL,
);


CREATE TABLE IF NOT EXISTS botanist (
    botanist_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(25),
    email VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS license (
    license_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    number SMALLINT NOT NULL,
);


CREATE TABLE IF NOT EXISTS image (
    image_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    medium_url TEXT NOT NULL,
    regular_url TEXT NOT NULL,
    original_url TEXT NOT NULL,
    small_url TEXT NOT NULL,
    thumbnail_url TEXT NOT NULL,
    license_id INT NOT NULL,
    CONSTRAINT fk_license_id FOREIGN KEY (license_id) REFERENCES s_gamma.license (license_id)
);


CREATE TABLE IF NOT EXISTS plant (
    plant_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    plant_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(100) NOT NULL,
    origin_id INT NOT NULL,
    image_id INT NOT NULL,
    CONSTRAINT fk_origin_id FOREIGN KEY (origin_id) REFERENCES s_gamma.origin (origin_id),
    CONSTRAINT fk_image_id FOREIGN KEY (image_id) REFERENCES s_gamma.image (image_id)
);


CREATE TABLE IF NOT EXISTS reading (
    reading_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    plant_id INT NOT NULL,
    botanist_id INT NOT NULL,
    soil_moisture DECIMAL(4,1) NOT NULL,
    temperature DECIMAL(3,1) NOT NULL,
    last_watered TIMESTAMPTZ NOT NULL,
    recording_taken TIMESTAMPTZ NOT NULL,
    CONSTRAINT fk_plant_id FOREIGN KEY (plant_id) REFERENCES s_gamma.plant (plant_id),
    CONSTRAINT fk_botanist_id FOREIGN KEY (botanist_id) REFERENCES s_gamma.botanist(botanist_id)

);