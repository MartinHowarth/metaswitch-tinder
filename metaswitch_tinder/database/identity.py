from .manage import User, list_all_users


def handle_signup_submit(username, email, biography):
    print("Signup submitted:", username, email, biography)
    new_user = User(username, email, biography, '')
    new_user.add()


def handle_signin_submit(username):
    print("signin submitted:", username)
    all_users = list_all_users()
    all_usernames = [user.name for user in all_users]
    print("all users:", all_usernames)
    if username not in all_usernames:
        raise ValueError("User not found.")
