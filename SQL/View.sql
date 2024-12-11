CREATE VIEW CW2.TrailView AS
SELECT
    T.Trail_ID,
    T.Trail_Name,
    T.Description,
    T.DIstance,
    TL.Latitude,
    TL.Longtitude,
    U.Name AS CreatorName,
    T.Created_On
FROM
    CW2.Trail T
JOIN
    CW2.Users U ON T.User_ID = U.User_ID
LEFT JOIN
    CW2.TrailPoint TL ON T.Trail_ID = TL.Trail_ID
