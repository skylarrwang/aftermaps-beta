#AfterMaps - SQL Connector Template
#Import necessary connector packages/libraries
from db.SQLconnector import query_all, query_none, query_one
from werkzeug.security import generate_password_hash

def login_query(username):
    """Pulls user's ID and pwd"""
    query_getusername = '''SELECT ID, Password FROM users WHERE Username = %s'''
    return query_one(query_getusername, username)

def register_user(username, password):
    """Inserts new user + hashed pwd"""
    
    query_register = '''INSERT INTO users(Username, Password) VALUES(%s, %s)''' 
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=2)
    query_none(query_register, username, hashed_password)
    return

def increment_reports(userid):
    """Increments the report count for a user after submission"""
    query_updatecount = '''UPDATE users
    SET ReportQuantity = (ReportQuantity + 1)
    WHERE ID = %s'''
    query_none(query_updatecount, userid)
    return

def report_count(userid):
    """Gets the number of reports a user has submitted"""
    
    query_reportcount = '''SELECT ReportQuantity FROM users WHERE ID = %s'''
    row = query_one(query_reportcount, userid)
    return int(row[0])

def new_user_map(userid, oLong, oLat, sLong, sLat, distance, passability):
    """Adds a report for a new user, report cred default 0.5"""
    
    query_nuReport = '''INSERT INTO Reports(User_ID,
    Report_Origin_Location, Subject_Location,
    Origin_Subj_Distance,Passability)
    VALUES(%s,POINT(%s, %s),POINT(%s, %s),%s,%s)'''
    query_none(query_nuReport, userid, oLong, oLat,
               sLong,sLat,distance,passability)
    return

def new_user_report(userid, segid, oLong, oLat, sLong, sLat, distance, passability):
    """Adds a report for a new user, report cred default 0.5"""
    
    query_nuReport = '''INSERT INTO Reports(User_ID, Seg_ID,
    Report_Origin_Location, Subject_Location,
    Origin_Subj_Distance,Passability)
    VALUES(%s,%s,POINT(%s, %s),POINT(%s, %s),%s,%s)'''
    query_none(query_nuReport, userid, segid, oLong, oLat,
               sLong,sLat,distance,passability)
    return

def cred_user_report(userid, cred, segid, oLong, oLat, sLong, sLat, distance, passability):
    """Adds a report for a "credible" user, report cred calculated w/ user model"""
    
    query_cuReport = '''INSERT INTO Reports(User_ID, Report_Cred, Seg_ID,
    Report_Origin_Location, Subject_Location,
    Origin_Subj_Distance,Passability)
    VALUES(%s,%s,%s,POINT(%s, %s),POINT(%s, %s),%s,%s)'''
    query_none(query_cuReport, userid, cred, segid, oLong, oLat,
               sLong,sLat,distance,passability)
    return

def check_road(street, zip):
    """Checks if the given road exists in DB"""
    query_checkRoad = '''SELECT Road_ID FROM Road_Seg WHERE Street=%s AND Zipcode=%s'''
    return query_one(query_checkRoad, street, zip)

def create_road(street, zip):
    """Creates a new road entr and returns its id"""
    query_newRoad = '''INSERT INTO Road_Seg(Street, Zipcode)
                    VALUES (%s, %s)'''
    query_none(query_newRoad, street, zip)
    return

def cred_input(userid):
    """Queries for Distance and Ground Truth"""
    query_credInput = '''SELECT Reports.Origin_Subj_Distance, Road_Seg.Ground_Truth
                        FROM Reports
                        INNER JOIN Road_Seg ON Reports.Seg_ID = Road_Seg.Road_ID
                        WHERE User_ID = %s;'''
    return query_all(query_credInput, userid)

def get_cred(userid):
    """Gets the user credibility"""
    query_getCred = '''SELECT Credibility FROM users WHERE ID = %s'''
    return query_one(query_getCred, userid)

def update_cred(userid, newCred):
    """Updates the user credibility and records in log table"""
    oldCred = get_cred(userid)[0]

    #Log the update
    query_logCredUpdate = '''INSERT INTO User_Cred_Log(User_ID, Old_Cred, New_Cred)
                        VALUES(%s, %s, %s)'''
    query_none(query_logCredUpdate, userid, oldCred, newCred)
    
    #Change user table
    query_changeUserCred = '''UPDATE users
                            SET Credibility = %s
                            WHERE ID=%s'''
    query_none(query_changeUserCred,newCred,userid)
    return

def update_passability(segID, oldPassability, newPassability, userid):
    """Updates the road table, pass_log"""
    
    #Log the update
    query_logPassUpdate = '''INSERT INTO Pass_Log(Segment_ID, Previous_Pass, Curr_Pass, Last_User)
                            VALUES(%s, %s, %s, %s)'''
    query_none(query_logPassUpdate, segID,oldPassability,newPassability,userid)
    
    #Change road table
    query_changePass = '''UPDATE Road_Seg 
                        SET Avg_Passability = %s,
                        Report_Quantity = Report_Quantity + 1 
                        WHERE Road_ID = %s'''
    query_none(query_changePass, newPassability, segID)
    
def get_passability(segID):
    """Gets the average passability of a road"""
    query_getPassability = '''SELECT Avg_Passability FROM Road_Seg 
                            WHERE Road_ID = %s'''
    return query_one(query_getPassability,segID)

def blockage_input(segID):
    """Queries for credibilities and corresponding passabilities"""
    query_blockageInput = '''SELECT Report_Cred, Passability 
                            FROM Reports 
                            WHERE Seg_ID = %s'''
    return query_all(query_blockageInput, segID)

def map_input(userID, oLat, oLong):
    query_mapInput = '''INSERT INTO Reports(User_ID, Report_Origin_Location) VALUES(%s,POINT(%s, %s))'''
    return query_none(query_mapInput, userID, oLat, oLong)

def road_info(increment):
    query_roadInfo = '''SELECT ST_AsGeoJSON(Location) AS Location_GeoJSON, Avg_Passability
            FROM Road_Seg
            LIMIT 1 OFFSET %s'''
    query_roadInfo = query_roadInfo % (increment)
    return query_one(query_roadInfo)

def road_count():
    query_roadCount = '''SELECT COUNT(*) FROM Road_Seg'''
    return query_one(query_roadCount)

def all_roads():
    query_allRoads = '''SELECT ST_AsGeoJSON(Location) AS Location_GeoJSON, Avg_Passability FROM Road_Seg WHERE Report_Quantity > 0'''
    return query_all(query_allRoads)

## geojson is long, lat
def closest_road(long, lat):
    query_closestRoad = '''SELECT Road_ID, ST_Distance(Location, 
    ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [%s, %s]}'), 'kilometre') as distance FROM Road_Seg
    ORDER BY distance LIMIT 1'''
    query_closestRoad = query_closestRoad % (long, lat)
    return query_one(query_closestRoad)


def printd(message):
    """
    prints message
    """
    with open('logfile.txt', 'a') as f:
        f.write(str(message))
