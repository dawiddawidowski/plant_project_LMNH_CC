-- -- Use database
-- USE my_database;
-- GO

-- Ensure starting with an empty schema
DROP TABLE IF EXISTS s_gamma.origin;
GO
DROP TABLE IF EXISTS s_gamma.botanist;
GO
DROP TABLE IF EXISTS s_gamma.license;
GO
DROP TABLE IF EXISTS s_gamma.image;
GO
DROP TABLE IF EXISTS s_gamma.plant;
GO
DROP TABLE IF EXISTS s_gamma.reading;
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
    number smallint NOT NULL,
);


CREATE TABLE IF NOT EXISTS image (
    image_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    word TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS plant (
    plant_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    medium_url TEXT NOT NULL,
    regular_url TEXT NOT NULL,
    original_url TEXT NOT NULL,
    small_url TEXT NOT NULL,
    thumbnail_url TEXT NOT NULL,
    CONSTRAINT fk_license_id FOREIGN KEY (license_id) REFERENCES s_gamma.license (license_id)
    license_id INT NOT NULL REFERENCES s_gamma.license(license_id)
);


CREATE TABLE IF NOT EXISTS reading (
    reading_id INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    word TEXT NOT NULL
);