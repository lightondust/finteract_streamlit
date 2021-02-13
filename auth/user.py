def user_table(user):
    return {
        'user1': 'password',
        'user2': 'password'
    }.get(user)


def check_user(user, password):
    if user_table(user) == password:
        return True
    else:
        return False
