-- TEST THE TRIGGER
EXEC CW2.InsertTrail
    @Trail_Name = 'New Trail',
    @Description = 'Sample Description',
    @Country_ID = 1,
    @State_ID = 1,
    @City_ID = 1,
    @Distance = 10.5,
    @Elevation_Gain = 500,
    @Estimated_Time = 3,
    @Route_Type = 'Loop',
    @User_ID = 1;