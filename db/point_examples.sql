INSERT INTO Reports(Report_Origin_Location,
Subject_Location, Passability)
VALUES(POINT(25.7786222, -80.1956483),POINT(10, 32.3),57);

SELECT ST_X(Subject_Location) AS Latitude, ST_Y(Subject_Location) AS Longitude FROM Reports