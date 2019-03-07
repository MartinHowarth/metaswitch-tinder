"""Handle generating matches and handling match requests from mentors and mentees."""
from metaswitch_tinder import tinder_email
from metaswitch_tinder.components.session import get_current_user
from metaswitch_tinder.database import Request, User


def handle_mentee_reject_match(matched_user: User, request: Request):
    print("mentee rejected match:", matched_user, request)
    request.handle_mentee_reject_mentor(matched_user)


def handle_mentee_accept_match(matched_user: User, request: Request):
    print("mentee accepted match:", matched_user, request)
    request.handle_mentee_accept_mentor(matched_user)


def handle_mentor_reject_match(matched_user: User, request: Request):
    print("mentor rejected match:", matched_user, request)
    request.handle_mentor_reject_mentee(get_current_user())


def handle_mentor_accept_match(matched_user: User, request: Request):
    print("mentor accepted match:", matched_user, request)
    mentor = get_current_user()
    mentee = matched_user
    request.handle_mentor_accept_mentee(mentor)

    email_text = "You're a match!"
    email_text += "\n\n"
    email_text += request.comment

    tinder_email.send_match_email([mentor.email, mentee.email], email_text)
