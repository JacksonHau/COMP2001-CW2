-- CREATE SCHEMA CW2 
CREATE SCHEMA CW2;
GO

-- RECREATE USER TABLE FOR CW2
CREATE TABLE CW2.Users 
(
    User_ID INT PRIMARY KEY,
    Username NVARCHAR(100) UNIQUE NOT NULL,
    Name NVARCHAR(100),
    Created_On DATE NOT NULL
);

-- RECREATE TRAIL TABLE FOR CW2
CREATE TABLE CW2.Trail 
(
    Trail_ID INT PRIMARY KEY,
    Trail_Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Country_ID INT,
    State_ID INT,
    City_ID INT,
    Distance FLOAT NOT NULL CHECK (Distance > 0),
    Created_On DATE NOT NULL,
    Elevation_Gain INT CHECK (Elevation_Gain >= 0),
    Estimated_Time INT CHECK (Estimated_Time > 0),
    Route_Type VARCHAR(50) CHECK (Route_Type IN ('Loop', 'Out & Back', 'Point to Point')),
    User_ID INT NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES CW2.Users(User_ID)
);

-- RECREATE TRAIL POINT TABLE FOR CW2
CREATE TABLE CW2.TrailPoint
(
    Point_ID INT PRIMARY KEY,
    Trail_ID INT NOT NULL,
    Latitude DECIMAL(9, 6) NOT NULL CHECK (Latitude BETWEEN -90 AND 90),
    Longtitude DECIMAL(9, 6) NOT NULL CHECK (Longtitude BETWEEN -180 AND 180),
    Position INT NOT NULL CHECK (Position > 0),
    FOREIGN KEY (Trail_ID) REFERENCES CW2.Trail(Trail_ID)
);

-- INSERT SAMPLE DATA INTO USERS TABLE IN CW2 THIS TIME WITH 5 DATA
INSERT INTO CW2.Users (User_ID, Username, Name, Created_On) VALUES
(1, 'John Doe', 'johnd', '2024-01-15'),
(2, 'Jane Doe', 'janed', '2024-02-20'),
(3, 'alexs', 'Alex Smith', '2024-03-10'),
(4, 'emilyr', 'Emily Rose', '2024-04-05'),
(5, 'mikew', 'Mike Watson', '2024-05-15');

-- INSERT SAMPLE DATA INTO TRAIL TABLE IN CW2 THIS TIME WITH 5 DATA
INSERT INTO CW2.Trail (Trail_ID, Trail_Name, Description, Country_ID, State_ID, City_ID, Distance, Created_On, Elevation_Gain, Estimated_Time, Route_Type, User_ID) VALUES
(1, 'Mountain Trail', 'A scenic trail up the mountain.', 101, 201, 301, 5.2, '2024-03-01', 4, 120, 'Loop', 1),
(2, 'Lakeside Walk', 'A peaceful walk by the lake.', 102, 202, 302, 3.0, '2024-03-05', 5, 60, 'Loop', 2),
(3, 'Forest Path', 'A tranquil path through the forest.', 103, 204, 303, 3.8, '2024-04-10', 90, 45, 'Out & Back', 1),
(4, 'Desert Trek', 'An adventurous trek through the desert.', 104, 205, 304, 8.0, '2024-05-15', 250, 120, 'Point to Point', 2),
(5, 'Coastal Route', 'A scenic walk along the coast.', 105, 206, 305, 6.5, '2024-06-20', 150, 90, 'Loop', 1);

-- INSERT SAMPLE DATA INTO TRAILS POINTS TABLE 
INSERT INTO CW2.TrailPoint (Point_ID, Trail_ID, Latitude, Longtitude, Position) VALUES
(1, 1, 40.712776, -74.005974, 1),
(2, 1, 40.713776, -74.006974, 2),
(3, 2, 34.052235, -118.243683, 1),
(4, 2, 34.053235, -118.244683, 2),
(5, 3, 37.774929, -122.419416, 1),
(6, 3, 37.775000, -122.419500, 2),
(7, 4, 36.778259, -119.417931, 1),
(8, 4, 36.778500, -119.418000, 2),
(9, 5, 34.019454, -118.491191, 1),
(10, 5, 34.020000, -118.491300, 2);