CREATE TABLE Animals (
    AnimalID INT AUTO_INCREMENT PRIMARY KEY,
    ShelterCode VARCHAR(255) NOT NULL UNIQUE,
    IdentichipNumber VARCHAR(255) UNIQUE,
    AnimalName VARCHAR(255) NOT NULL,
    SpeciesName VARCHAR(255) NOT NULL,
    BaseColour VARCHAR(255),
    AnimalAge VARCHAR(255),
    SexName VARCHAR(50),
    CONSTRAINT UC_Animal UNIQUE (ShelterCode, IdentichipNumber)
);

CREATE TABLE Species (
    SpeciesID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) UNIQUE NOT NULL
);


CREATE TABLE Breeds (
    BreedID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
	SpeciesID INT NOT NULL,
    FOREIGN KEY (SpeciesID) REFERENCES Species(SpeciesID)
);


CREATE TABLE Intakes (
    IntakeID INT AUTO_INCREMENT PRIMARY KEY,
    AnimalID INT,
    IntakeDate DATE NOT NULL,
    IntakeReason VARCHAR(255),
    IsTransfer BOOLEAN,
    FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID)
);


CREATE TABLE Movements (
    MovementID INT AUTO_INCREMENT PRIMARY KEY,
    AnimalID INT,
    MovementDate DATE NOT NULL,
    MovementType VARCHAR(255) NOT NULL,
    IsTrial BOOLEAN,
    ReturnDate DATE,
    ReturnedReason VARCHAR(255),
    FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID)
);


CREATE TABLE Deceased (
    DeceasedID INT AUTO_INCREMENT PRIMARY KEY,
    AnimalID INT,
    DeceasedDate DATE,
    DeceasedReason VARCHAR(255),
    DiedOffShelter BOOLEAN,
    PutToSleep BOOLEAN,
    IsDOA BOOLEAN,
    FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID)
);


CREATE TABLE Locations (
    AnimalID INT,
    Description VARCHAR(255) NOT NULL,
	FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID)

);
DROP TABLE locations;
