from activitytolerance import get_activity_recommendations
from flarerisk import get_flarerisk_for_user

def apply_flare_weighting(activity_lists, risk_level):
    do_list = activity_lists["do"][:]
    careful_list = activity_lists["careful"][:]
    avoid_list = activity_lists["avoid"][:]
    not_applicable = activity_lists["not_applicable"][:]


    #Resting is a permanent do activity
    always_do = ["Resting"]

    if risk_level == "Low":
        return {
            "do": do_list + always_do,
            "careful": careful_list,
            "avoid": avoid_list,
            "not_applicable": not_applicable
        }

    if risk_level == "Medium":
        #Shift do to careful
        careful_list = careful_list + do_list
        do_list = always_do

        return {
            "do": do_list,
            "careful": careful_list,
            "avoid": avoid_list,
            "not_applicable": not_applicable
        }

    if risk_level == "High":
        #Shift up one again
        avoid_list = avoid_list + careful_list
        careful_list = do_list
        do_list = always_do

    #Remove resting from other lists
    final_careful = [a for a in careful_list if a != "Resting"]
    final_avoid = [a for a in avoid_list  if a != "Resting"]
    return {
        "do": do_list,
        "careful": final_careful,
        "avoid": final_avoid,
        "not_applicable": not_applicable
    }
