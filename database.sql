CREATE DATABASE GPA_Calculator;
USE GPA_Calculator;


-- DROP database GPA_Calculator;

-- Create Programmes Table
CREATE TABLE Programmes (
    ProgrammeID INT PRIMARY KEY AUTO_INCREMENT,
    ProgrammeName VARCHAR(100),
    School VARCHAR(100)
);

-- Create Students Table
CREATE TABLE Students (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    StudentName VARCHAR(100),
    StudentEmail VARCHAR(100),
    School VARCHAR(100),
    ProgrammeID INT,
    FOREIGN KEY (ProgrammeID) REFERENCES Programmes(ProgrammeID)
);

-- Create Admins Table
CREATE TABLE Admins (
    AdminID INT PRIMARY KEY AUTO_INCREMENT,
    AdminName VARCHAR(100),
    AdminEmail VARCHAR(100)
);

-- Create ProgrammeDirectors Table
CREATE TABLE ProgrammeDirectors (
    ProgrammeDirectorID INT PRIMARY KEY AUTO_INCREMENT,
    ProgrammeDirectorName VARCHAR(100),
    ProgrammeDirectorEmail VARCHAR(100),
    ProgrammeID INT,
    FOREIGN KEY (ProgrammeID) REFERENCES Programmes(ProgrammeID)
);

-- Create Lecturers Table
CREATE TABLE Lecturers (
    LecturerID INT PRIMARY KEY AUTO_INCREMENT,
    LecturerName VARCHAR(100),
    LecturerEmail VARCHAR(100),
    School VARCHAR(100)
);

-- Create Modules Table
CREATE TABLE Modules (
    Module VARCHAR(100) PRIMARY KEY,
    NumberOfCredits INT
);

CREATE TABLE LetterGrades (
    LetterGrade VARCHAR(2) PRIMARY KEY,
    GradePoint DECIMAL(3, 2) NOT NULL
);
-- Create Grades Table
CREATE TABLE Grades (
    Module VARCHAR(100),
    Year INT,
    Semester INT,
    StudentID INT,
    LetterGrade VARCHAR(2),
    PRIMARY KEY (Module, Year, Semester, StudentID),
    FOREIGN KEY (Module) REFERENCES Modules(Module),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (LetterGrade) REFERENCES LetterGrades(LetterGrade)
);

-- Create LecturerModules Table
CREATE TABLE LecturerModules (
    LecturerID INT,
    Module VARCHAR(100),
    PRIMARY KEY (LecturerID, Module),
    FOREIGN KEY (LecturerID) REFERENCES Lecturers(LecturerID),
    FOREIGN KEY (Module) REFERENCES Modules(Module)
);
-- Create ProgrammeModules Table
CREATE TABLE ProgrammeModules (
    ProgrammeID INT,
    Module VARCHAR(100),
    PRIMARY KEY (ProgrammeID, Module),
    FOREIGN KEY (ProgrammeID) REFERENCES Programmes(ProgrammeID),
    FOREIGN KEY (Module) REFERENCES Modules(Module)
);
-- Create StudentUsers Table
CREATE TABLE StudentUsers (
    StudentID INT PRIMARY KEY,
    PasswordHash VARCHAR(255),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
);

-- Create AdminUsers Table
CREATE TABLE AdminUsers (
    AdminID INT PRIMARY KEY AUTO_INCREMENT,
    PasswordHash VARCHAR(255),
    FOREIGN KEY (AdminID) REFERENCES Admins(AdminID)
);

-- Create ProgrammeDirectorUsers Table
CREATE TABLE ProgrammeDirectorUsers (
    ProgrammeDirectorID INT PRIMARY KEY,
    PasswordHash VARCHAR(255),
    FOREIGN KEY (ProgrammeDirectorID) REFERENCES ProgrammeDirectors(ProgrammeDirectorID)
);

-- Create LecturerLogin Table
CREATE TABLE LecturerUsers (
    LecturerID INT PRIMARY KEY,
    PasswordHash VARCHAR(255),
    FOREIGN KEY (LecturerID) REFERENCES Lecturers(LecturerID)
);

INSERT INTO Programmes (ProgrammeID, ProgrammeName, School) VALUES
(1, 'Computer Science', 'School of Computing'),
(2, 'Business Administration', 'School of Business'),
(3, 'Mechanical Engineering', 'School of Engineering'),
(4, 'Electrical Engineering', 'School of Engineering'),
(5, 'Civil Engineering', 'School of Engineering'),
(6, 'Marketing', 'School of Business'),
(7, 'Finance', 'School of Business'),
(8, 'Biology', 'School of Science'),
(9, 'Chemistry', 'School of Science'),
(10, 'Physics', 'School of Science');

INSERT INTO Students (StudentID, StudentName, StudentEmail, School, ProgrammeID) VALUES
(1001, 'Damary Patterson', 'damaryp90@gmail.com', 'School of Computing', 1),
(1002, 'Bob Smith', 'bob.smith@gmail.com', 'School of Business', 2),
(1003, 'Charlie Brown', 'charlie.brown@gmail.com', 'School of Engineering', 3),
(1004, 'David Wilson', 'david.wilson@gmail.com', 'School of Engineering', 4),
(1005, 'Eva Green', 'eva.green@gmail.com', 'School of Engineering', 5),
(1006, 'Frank White', 'frank.white@gmail.com', 'School of Business', 6),
(1007, 'Grace Black', 'grace.black@gmail.com', 'School of Business', 7),
(1008, 'Hannah Blue', 'hannah.blue@gmail.com', 'School of Science', 8),
(1009, 'Ian Red', 'ian.red@gmail.com', 'School of Science', 9),
(1010, 'Jack Yellow', 'jack.yellow@gmail.com', 'School of Science', 10),
(1011, 'Karen Brown', 'karen.brown@gmail.com', 'School of Computing', 1),
(1012, 'Liam Smith', 'liam.smith@gmail.com', 'School of Business', 2),
(1013, 'Mia Johnson', 'mia.johnson@gmail.com', 'School of Engineering', 3),
(1014, 'Noah Wilson', 'noah.wilson@gmail.com', 'School of Engineering', 4),
(1015, 'Olivia Green', 'olivia.green@gmail.com', 'School of Engineering', 5),
(1016, 'Paul White', 'paul.white@gmail.com', 'School of Business', 6),
(1017, 'Quinn Black', 'quinn.black@gmail.com', 'School of Business', 7),
(1018, 'Rachel Blue', 'rachel.blue@gmail.com', 'School of Science', 8),
(1019, 'Sam Red', 'sam.red@gmail.com', 'School of Science', 9),
(1020, 'Tina Yellow', 'tina.yellow@gmail.com', 'School of Science', 10);

INSERT INTO Admins (AdminID, AdminName, AdminEmail) VALUES
(2001, 'Admin One', 'admin.one@gmail.com');

INSERT INTO ProgrammeDirectors (ProgrammeDirectorID, ProgrammeDirectorName, ProgrammeDirectorEmail, ProgrammeID) VALUES
(3001, 'Director One', 'director.one@gmail.com', 1),
(3002, 'Director Two', 'director.two@gmail.com', 2),
(3003, 'Director Three', 'director.three@gmail.com', 3);


INSERT INTO Modules (Module, NumberOfCredits) VALUES
('Introduction to Programming', 3),
('Data Structures', 3),
('Algorithms', 3),
('Database Systems', 3),
('Operating Systems', 3),
('Software Engineering', 3),
('Computer Networks', 3),
('Artificial Intelligence', 3),
('Machine Learning', 3),
('Web Development', 3),
('Business Management', 4),
('Marketing Principles', 4),
('Financial Accounting', 4),
('Corporate Finance', 4),
('Human Resource Management', 4),
('Thermodynamics', 3),
('Fluid Mechanics', 3),
('Circuit Analysis', 3),
('Digital Systems', 3),
('Structural Analysis', 3),
('Organic Chemistry', 3),
('Inorganic Chemistry', 3),
('Cell Biology', 3),
('Genetics', 3),
('Quantum Physics', 3);

INSERT INTO StudentUsers (StudentID, PasswordHash) VALUES
(1001, 'password1'),
(1002, 'password2'),
(1003, 'password3'),
(1004, 'password4'),
(1005, 'password5'),
(1006, 'password6'),
(1007, 'password7'),
(1008, 'password8'),
(1009, 'password9'),
(1010, 'password10'),
(1011, 'password11'),
(1012, 'password12'),
(1013, 'password13'),
(1014, 'password14'),
(1015, 'password15'),
(1016, 'password16'),
(1017, 'password17'),
(1018, 'password18'),
(1019, 'password19'),
(1020, 'password20');

INSERT INTO AdminUsers (AdminID, PasswordHash) VALUES
(2001, 'adminpass1');

INSERT INTO ProgrammeDirectorUsers (ProgrammeDirectorID, PasswordHash) VALUES
(3001, 'directorpass1'),
(3002, 'directorpass2'),
(3003, 'directorpass3');

INSERT INTO Lecturers (LecturerID, LecturerName, LecturerEmail, School) VALUES
(4001, 'Prof. David Blue', 'david.blue@gmail.com', 'School of Computing'),
(4002, 'Prof. Linda Red', 'linda.red@gmail.com', 'School of Business'),
(4003, 'Prof. Michael Yellow', 'michael.yellow@gmail.com', 'School of Engineering');

INSERT INTO LecturerUsers (LecturerID, PasswordHash) VALUES
(4001, 'lecturerpass1'),
(4002, 'lecturerpass2'),
(4003, 'lecturerpass3');

INSERT INTO Grades (Module, Year, Semester, StudentID, LetterGrade) VALUES
('Introduction to Programming', 2024, 1, 1001, 'A-'),
('Data Structures', 2024, 1, 1001, 'C'),
('Algorithms', 2024, 1, 1001, 'B+'),
('Database Systems', 2024, 1, 1001, 'C+'),
('Operating Systems', 2024, 1, 1001, 'D+'),
('Software Engineering', 2024, 1, 1001, 'B'),
('Computer Networks', 2024, 1, 1001, 'A'),
('Artificial Intelligence', 2024, 2, 1001, 'A-'),
('Machine Learning', 2024, 2, 1001, 'C'),
('Web Development', 2024, 2, 1001, 'B+'),
('Business Management', 2024, 1, 1002, 'C+'),
('Marketing Principles', 2024, 1, 1002, 'D+'),
('Financial Accounting', 2024, 1, 1002, 'B'),
('Corporate Finance', 2024, 1, 1002, 'A'),
('Human Resource Management', 2024, 1, 1002, 'A-'),
('Thermodynamics', 2024, 1, 1003, 'C'),
('Fluid Mechanics', 2024, 1, 1003, 'B+'),
('Circuit Analysis', 2024, 1, 1003, 'C+'),
('Digital Systems', 2024, 1, 1003, 'D+'),
('Structural Analysis', 2024, 1, 1003, 'B'),
('Organic Chemistry', 2024, 1, 1004, 'A'),
('Inorganic Chemistry', 2024, 1, 1004, 'A-'),
('Cell Biology', 2024, 1, 1004, 'C'),
('Genetics', 2024, 1, 1004, 'B+'),
('Quantum Physics', 2024, 1, 1004, 'C+'),
('Introduction to Programming', 2024, 2, 1005, 'D+'),
('Data Structures', 2024, 2, 1005, 'B'),
('Algorithms', 2024, 2, 1005, 'A'),
('Database Systems', 2024, 2, 1005, 'A-'),
('Operating Systems', 2024, 2, 1005, 'C'),
('Software Engineering', 2024, 2, 1005, 'B+'),
('Computer Networks', 2024, 2, 1005, 'C+'),
('Artificial Intelligence', 2024, 2, 1006, 'D+'),
('Machine Learning', 2024, 2, 1006, 'B'),
('Web Development', 2024, 2, 1006, 'A'),
('Business Management', 2024, 2, 1006, 'A-'),
('Marketing Principles', 2024, 2, 1006, 'C'),
('Financial Accounting', 2024, 2, 1006, 'B+'),
('Corporate Finance', 2024, 2, 1006, 'C+');

INSERT INTO LetterGrades (LetterGrade, GradePoint) VALUES
('A', 4.0),
('A-', 3.7),
('B+', 3.3),
('B', 3.0),
('B-', 2.7),
('C+', 2.3),
('C', 2.0),
('C-', 1.7),
('D+', 1.3),
('D', 1.0),
('F', 0.0);

INSERT INTO LecturerModules (LecturerID, Module) VALUES
(4001, 'Introduction to Programming'),
(4001, 'Data Structures'),
(4001, 'Algorithms'),
(4002, 'Business Management'),
(4002, 'Marketing Principles'),
(4002, 'Financial Accounting'),
(4003, 'Thermodynamics'),
(4003, 'Fluid Mechanics'),
(4003, 'Circuit Analysis'),
(4003, 'Digital Systems');



select * from lecturermodules;