----------------------------------
----------CRUD PROCEDURE----------
----------------------------------

-- CREATE PROCEDURE 
CREATE PROCEDURE CW2.InsertTrail
    @Trail_Name NVARCHAR(100),
    @Description NVARCHAR(255),
    @Country_ID INT,
    @State_ID INT,
    @City_ID INT,
    @Distance DECIMAL(10, 2),
    @Elevation_Gain INT,
    @Estimated_Time INT,
    @Route_Type NVARCHAR(50),
    @User_ID INT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM CW2.Users WHERE User_ID = @User_ID)
    BEGIN
        RAISERROR ('User_ID does not exist in Users table.', 16, 1);
        RETURN;
    END;

    DECLARE @NewTrailID INT;
    SELECT @NewTrailID = ISNULL(MAX(Trail_ID), 0) + 1 FROM CW2.Trail;

    INSERT INTO CW2.Trail 
        (Trail_ID, Trail_Name, Description, Country_ID, State_ID, City_ID, Distance, Elevation_Gain, Estimated_Time, Route_Type, User_ID, Created_On)
    VALUES
        (@NewTrailID, @Trail_Name, @Description, @Country_ID, @State_ID, @City_ID, @Distance, @Elevation_Gain, @Estimated_Time, @Route_Type, @User_ID, GETDATE());
END;
GO

-- READ PROCEDURE
CREATE PROCEDURE CW2.ReadTrail
    @Trail_ID INT = NULL,
    @Trail_Name NVARCHAR(100) = NULL,
    @User_ID INT = NULL
AS
BEGIN
    SELECT
        Trail_ID,
        Trail_Name,
        Description,
        Country_ID,
        State_ID,
        City_ID,
        Distance,
        Elevation_Gain,
        Estimated_Time,
        Route_Type,
        User_ID,
        Created_On
    FROM CW2.Trail
    WHERE 
        (@Trail_ID IS NULL OR Trail_ID = @Trail_ID) AND
        (@Trail_Name IS NULL OR Trail_Name LIKE '%' + @Trail_Name + '%') AND
        (@User_ID IS NULL OR User_ID = @User_ID);
END;
GO

-- UPDATE PROCEDURE
CREATE PROCEDURE CW2.UpdateTrail
    @Trail_ID INT,
    @Trail_Name NVARCHAR(100) = NULL,
    @Description NVARCHAR(255) = NULL,
    @Country_ID INT = NULL,
    @State_ID INT = NULL,
    @City_ID INT = NULL,
    @Distance DECIMAL(10, 2) = NULL,
    @Elevation_Gain INT = NULL,
    @Estimated_Time NVARCHAR(50) = NULL,
    @Route_Type NVARCHAR(50) = NULL,
    @User_ID INT = NULL
AS
BEGIN
    IF EXISTS (SELECT 1 FROM CW2.Trail WHERE Trail_ID = @Trail_ID)
    BEGIN
        UPDATE CW2.Trail
        SET
            Trail_Name = COALESCE(@Trail_Name, Trail_Name),
            Description = COALESCE(@Description, Description),
            Country_ID = COALESCE(@Country_ID, Country_ID),
            State_ID = COALESCE(@State_ID, State_ID),
            City_ID = COALESCE(@City_ID, City_ID),
            Distance = COALESCE(@Distance, Distance),
            Elevation_Gain = COALESCE(@Elevation_Gain, Elevation_Gain),
            Estimated_Time = COALESCE(@Estimated_Time, Estimated_Time),
            Route_Type = COALESCE(@Route_Type, Route_Type),
            User_ID = COALESCE(@User_ID, User_ID)
        WHERE
            Trail_ID = @Trail_ID;
    END
    ELSE
    BEGIN
        PRINT 'No trail found with the specified Trail_ID';
    END
END;
GO

-- DELETE PROCEDURE
CREATE PROCEDURE CW2.DeleteTrail
    @Trail_ID INT
AS
BEGIN
    -- TO CHECK IF THE TRAIL EXISTS BEFORE ATTEMPTING TO DELETE
    IF EXISTS (SELECT 1 FROM CW2.Trail WHERE Trail_ID = @Trail_ID)
    BEGIN
        DELETE FROM CW2.Trail
        WHERE Trail_ID = @Trail_ID;
        PRINT 'Trail deleted successfully.';
    END
    ELSE
    BEGIN
        PRINT 'No trail found with the specified Trail_ID';
    END
END;
GO