from daos.user_dao import UserDAO
from daos.user_dao_mongo import UserMongoDAO
from models.user import User
import time

# dao = UserDAO()

dao = UserMongoDAO()

def test_user_select():
    # insert some users to ensure there are at least 3
    user1 = User(None, 'User One', 'userone@example.com')
    user2 = User(None, 'User Two', 'usertwo@example.com')
    user3 = User(None, 'User Three', 'userthree@example.com')
    dao.insert(user1)
    dao.insert(user2)
    dao.insert(user3)
    user_list = dao.select_all()
    assert len(user_list) >= 3

def test_user_insert():
    user = User(None, 'Joanne Test', 'joannetest@example.com')
    dao.insert(user)
    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert user.email in emails

def test_user_update():
    user = User(None, 'Joe Test', 'testttt@example.com')
    assigned_id = dao.insert(user)

    corrected_email = 'joetest@example.com'
    user.id = assigned_id
    user.email = corrected_email
    dao.update(user)

    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert corrected_email in emails

    # cleanup
    dao.delete(assigned_id)

def test_user_delete():
    test_email = 'joetest@example.com'
    # Clean up any existing users with the test email before the test
    for u in dao.select_all():
        if u.email == test_email:
            dao.delete(u.id)

    user = User(None, 'Joe Test', test_email)
    assigned_id = dao.insert(user)
    dao.delete(assigned_id)

    # Clean up any users with the test email after the test (in case of failure)
    for u in dao.select_all():
        if u.email == test_email:
            dao.delete(u.id)

    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert user.email not in emails