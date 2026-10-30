-- EYEWHERE? Database Schema for MariaDB / MySQL

CREATE DATABASE IF NOT EXISTS eyewhere_db;
USE eyewhere_db;

CREATE TABLE IF NOT EXISTS travel_intelligence_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    current_loc VARCHAR(255),
    target_loc VARCHAR(255),
    distance_km FLOAT,
    weather VARCHAR(255),
    environment VARCHAR(255),
    safety_guidelines TEXT,
    timestamp VARCHAR(50)
);

