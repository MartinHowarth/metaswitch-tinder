def handle_mentee_added_request(username, email, categories, details):
    print("Mentee submitted:", username, email, categories, details)
    # TODO this should actually put it in the database somehow


def handle_mentee_reject_match(matched_user):
    print("mentee rejected match:", matched_user)
    # TODO


def handle_mentee_accept_match(matched_user):
    print("mentee accepted match:", matched_user)
    # TODO


def handle_mentor_reject_match(matched_user):
    print("mentor rejected match:", matched_user)
    # TODO


def handle_mentor_accept_match(matched_user):
    print("mentor accepted match:", matched_user)
    # TODO