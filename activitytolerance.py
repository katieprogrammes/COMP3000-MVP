from models import InitialActivity


def get_activity_recommendations(user_id):
    #Fetching Activity level from model
    initial = InitialActivity.query.filter_by(user_id=user_id).first()

    if not initial:
        return {
            "do": ["resting"],
            "careful": [],
            "avoid": [],
            "not_applicable": []
        }

    ratings = {
        "Showering": initial.shower,
        "Cooking": initial.cooking,
        "Laundry": initial.laundry,
        "Vacuuming": initial.vacuuming,
        "Cleaning": initial.cleaning,
        "Grocery Shopping": initial.groceries,
        "Walking": initial.walking,
        "Driving": initial.driving,
        "Exercise": initial.exercise,
        "Studying": initial.studying,
        "Socialising": initial.socialising,
        "Going Out": initial.outing
    }

    #Categorising based on difficulty
    do_list = []
    careful_list = []
    avoid_list = []
    not_applicable = []

    for activity, rating in ratings.items():
        if rating == 0:
            not_applicable.append(activity)
        elif rating <= 3:
            do_list.append(activity)
        elif rating <= 7:
            careful_list.append(activity)
        else:
            avoid_list.append(activity)

    #Resting always allowed
    do_list.append("Resting")

    return {
        "do": do_list,
        "careful": careful_list,
        "avoid": avoid_list,
        "not_applicable": not_applicable
    }
