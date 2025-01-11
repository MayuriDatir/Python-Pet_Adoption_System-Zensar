--step 1: Create Database
CREATE DATABASE IF NOT EXISTS pet_adoption;
USE pet_adoption;

-- Step 2: Create Tables

-- Table: Pets
CREATE TABLE Pets (
    PetID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Species VARCHAR(30),
    Breed VARCHAR(50),
    Age INT,
    Status VARCHAR(20) DEFAULT 'Available'
);

-- Table: Adopters
CREATE TABLE Adopters (
    AdopterID INT PRIMARY KEY AUTO_INCREMENT,
    FullName VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(100),
    Address VARCHAR(255)
);

-- Table: Adoptions
CREATE TABLE Adoptions (
    AdoptionID INT PRIMARY KEY AUTO_INCREMENT,
    PetID INT NOT NULL,
    AdopterID INT NOT NULL,
    AdoptionDate DATE DEFAULT CURRENT_DATE,
    Status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (PetID) REFERENCES Pets(PetID) ON DELETE CASCADE,
    FOREIGN KEY (AdopterID) REFERENCES Adopters(AdopterID) ON DELETE CASCADE
);

-- Step 3: Insert Sample Data

-- Insert Sample Pets
INSERT INTO Pets (Name, Species, Breed, Age, Status)
VALUES 
    ('Bella', 'Dog', 'Labrador', 3, 'Available'),
    ('Max', 'Cat', 'Siamese', 2, 'Available'),
    ('Charlie', 'Dog', 'Beagle', 4, 'Available'),
    ('Luna', 'Cat', 'Persian', 1, 'Available'),
    ('Rocky', 'Dog', 'Bulldog', 5, 'Available'),
    ('Daisy', 'Dog', 'Poodle', 2, 'Available'),
    ('Simba', 'Cat', 'Maine Coon', 3, 'Available'),
    ('Buddy', 'Dog', 'Golden Retriever', 4, 'Available'),
    ('Nala', 'Cat', 'Bengal', 2, 'Available'),
    ('Oscar', 'Dog', 'German Shepherd', 5, 'Available'),
    ('Milo', 'Cat', 'Ragdoll', 1, 'Available'),
    ('Zoe', 'Dog', 'Husky', 3, 'Available');

-- Insert Sample Adopters
INSERT INTO Adopters (FullName, ContactInfo, Address)
VALUES 
    ('John Doe', 'john@example.com', '123 Main St'),
    ('Jane Smith', 'jane@example.com', '456 Oak Ave'),
    ('Emily Clark', 'emily@example.com', '789 Pine Rd'),
    ('Michael Brown', 'michael@example.com', '321 Birch Blvd'),
    ('Sarah Davis', 'sarah@example.com', '654 Maple Ln'),
    ('Chris Johnson', 'chris@example.com', '321 Elm St'),
    ('Laura White', 'laura@example.com', '741 Cedar St'),
    ('Robert Green', 'robert@example.com', '852 Birch Rd'),
    ('Linda Black', 'linda@example.com', '963 Maple Ave'),
    ('Kevin Gray', 'kevin@example.com', '147 Pine St'),
    ('Anna Blue', 'anna@example.com', '258 Oak Rd'),
    ('Sophia Gold', 'sophia@example.com', '369 Willow Ln');

-- Insert Sample Adoptions
INSERT INTO Adoptions (PetID, AdopterID, AdoptionDate, Status)
VALUES 
    (1, 1, '2023-12-01', 'Pending'),
    (2, 2, '2023-12-02', 'Pending'),
    (3, 3, '2023-12-03', 'Pending'),
    (4, 4, '2023-12-04', 'Pending'),
    (5, 5, '2023-12-05', 'Pending'),
    (6, 6, '2023-12-06', 'Pending'),
    (7, 7, '2023-12-07', 'Pending'),
    (8, 8, '2023-12-08', 'Pending'),
    (9, 9, '2023-12-09', 'Pending'),
    (10, 10, '2023-12-10', 'Pending'),
    (11, 11, '2023-12-11', 'Pending'),
    (12, 12, '2023-12-12', 'Pending');

SELECT * FROM Adoptions WHERE AdoptionID = 1;
SELECT * FROM Pets WHERE PetID = (SELECT PetID FROM Adoptions WHERE AdoptionID = 1);