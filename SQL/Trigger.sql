-- IMPLEMENT THE TRIGGER
CREATE TRIGGER CW2.LogTrailAddition
ON CW2.Trail
AFTER INSERT
AS
BEGIN
    INSERT INTO CW2.TrailLog (Trail_ID, User_ID, Timestamp)
    SELECT i.Trail_ID, i.User_ID, GETDATE()
    FROM INSERTED I;
END;