CREATE TABLE User (
    ID_user INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    phone_num VARCHAR(20),
    role ENUM('caregiver', 'veterinarian', 'volunteer'),

    -- volunteer specific
    verified BOOLEAN,
    ID_caregiver INT NULL,

    PRIMARY KEY (ID_user),
    FOREIGN KEY (ID_caregiver) REFERENCES User(ID_user)
);

CREATE TABLE Animal (
    ID_animal INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    species VARCHAR(255) NOT NULL,
    breed VARCHAR(255),
    birth_year YEAR,
    photo BLOB,
    admission_date DATE,
    size ENUM('small', 'medium', 'large'),
    caregivers_description TEXT,
    ID_caregiver INT NOT NULL,

    PRIMARY KEY (ID_animal),
    FOREIGN KEY (ID_caregiver) REFERENCES User(ID_user)
);

CREATE TABLE Feed (
    ID_feed INT NOT NULL AUTO_INCREMENT,
    typ VARCHAR(255),

    PRIMARY KEY (ID_feed)
);

CREATE TABLE Consume (
    ID_feed INT NOT NULL,
    ID_animal INT NOT NULL,
    amount DECIMAL(5,2) NOT NULL,
    per_day INT NOT NULL,

    PRIMARY KEY (ID_feed, ID_animal),
    FOREIGN KEY (ID_feed) REFERENCES Feed(ID_feed),
    FOREIGN KEY (ID_animal) REFERENCES Animal(ID_animal)

);

CREATE TABLE Examination_request (
    ID_request INT NOT NULL AUTO_INCREMENT,
    caregivers_description TEXT,
    ID_animal INT NOT NULL,
    ID_caregiver INT NOT NULL,

    -- if ID_veterinarian is NULL, the request is not yet handled
    ID_veterinarian INT NULL,

    PRIMARY KEY (ID_request, ID_animal),
    FOREIGN KEY (ID_animal) REFERENCES Animal(ID_animal),
    FOREIGN KEY (ID_caregiver) REFERENCES User(ID_user),
    FOREIGN KEY (ID_veterinarian) REFERENCES User(ID_user)
);

CREATE TABLE Medical_record (
    ID_record INT NOT NULL AUTO_INCREMENT,
    date DATE,
    weight DECIMAL(5,2),
    vaccination BOOLEAN,
    vaccination_type VARCHAR(255) NULL,
    vet_description TEXT,
    ID_animal INT NOT NULL,
    ID_veterinarian INT NOT NULL,

    PRIMARY KEY (ID_record, ID_animal),
    FOREIGN KEY (ID_animal) REFERENCES Animal(ID_animal),
    FOREIGN KEY (ID_veterinarian) REFERENCES User(ID_user)
);

CREATE TABLE Animal_borrow (
    ID_borrow INT NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL,
    time TIME NOT NULL,
    borrowed BOOLEAN,
    returned BOOLEAN,
    ID_animal INT NOT NULL,

    PRIMARY KEY (ID_borrow),
    FOREIGN KEY (ID_animal) REFERENCES Animal(ID_animal)
);

CREATE TABLE Reservation (
    ID_reservation INT NOT NULL AUTO_INCREMENT,
    approved BOOLEAN,
    ID_borrow INT NOT NULL,
    ID_volunteer INT NOT NULL,

    PRIMARY KEY (ID_reservation),
    FOREIGN KEY (ID_borrow) REFERENCES Animal_borrow(ID_borrow),
    FOREIGN KEY (ID_volunteer) REFERENCES User(ID_user)
);
