from .manage import User, Request, get_request_by_id


def handle_mentee_add_request(username, categories, details):
    print("Mentee added request:", username, categories, details)
    request = Request(username, categories, details)
    request.add()


def handle_mentee_signup_and_request(username, email, categories, details):
    print("Mentee signup and request:", username, email, categories, details)
    mentee = User(username, email, '', '', '')
    mentee.add()
    handle_mentee_add_request(username, categories, details)


def handle_mentee_reject_match(request_id):
    print("mentee rejected match:", request_id)
    request = get_request_by_id(request_id)
    request.state = "rejected"
    request.commit()


def handle_mentee_accept_match(request_id, current_user, matched_user):
    print("mentee accepted match:", request_id)
    request = get_request_by_id(request_id)
    request.state = "matched"
    request.commit()
    matched_user.add_mentor_match(current_user.name, request_id)


def handle_mentor_reject_match(request_id):
    print("mentor rejected match:", request_id)
    request = get_request_by_id(request_id)
    request.state = "rejected"
    request.commit()


def handle_mentor_accept_match(request_id):
    print("mentor accepted match:", request_id)
    request = get_request_by_id(request_id)
    request.state = "matched"
    request.commit()
