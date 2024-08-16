import db.SQLscripts as SQLscripts
from helpers.usercred_helper import init_uc, update_uc, convert_nplist
from helpers.blockage_helper import blockage_nplist, run_bm

def report_controller(userID, road_id, curr_long, curr_lat,add_long, add_lat, distance, passability):
    """Handles report processing:
    (1) Updates user report count
    (2) Checks street against roads table
    (3) Adds report
    (4) Updates user credibility
    (5) Calculate road passability
    (6) Update road passability"""

    ## Step 1: update user report count
    SQLscripts.increment_reports(userID)

    ## Step 2: add report to table
    ## Check user report count to determine new/old user
    report_count = SQLscripts.report_count(userID)

    ## New user
    if report_count < 6:
        SQLscripts.new_user_report(userID, road_id, curr_long, curr_lat,
                                    add_long, add_lat, distance, passability)

    ## First credit user (6th submission)
    elif report_count == 6:
        rows = SQLscripts.cred_input(userID)
        uf_distance, uf_groundtruths = convert_nplist(rows)
        userCred = init_uc(uf_distance,uf_groundtruths)
        SQLscripts.cred_user_report(userID, userCred, road_id, curr_long, curr_lat,
                                    add_long, add_lat, distance, passability)
        ## Step 4: Update user credibility
        SQLscripts.update_cred(userID,userCred)

    ## Old user (6+ submissions)
    else:
        rows = SQLscripts.cred_input(userID)
        uf_distance, uf_groundtruths = convert_nplist(rows)
        oldCred = SQLscripts.get_cred(userID)[0]
        userCred = update_uc(uf_distance,uf_groundtruths, oldCred)
        SQLscripts.cred_user_report(userID, userCred, road_id, curr_long, curr_lat,
                                    add_long, add_lat, distance, passability)

        ## Step 4: Update user credibility
        SQLscripts.update_cred(userID,userCred)

    ## Step 5: Calculate road passability
    b_rows = SQLscripts.blockage_input(road_id)
    uf_cred, uf_sev = blockage_nplist(b_rows)
    blockage_prob = run_bm(uf_cred, uf_sev)

    ## Step 6: Update blockages
    oldPass = SQLscripts.get_passability(road_id)[0]
    SQLscripts.update_passability(road_id, oldPass, blockage_prob, userID)

