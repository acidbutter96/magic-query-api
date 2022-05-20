from database.models.user import UserModel
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_model_is_right():
    user = UserModel(id=1, username='username',
        first_name='Jane', last_name='Doe',
        password='123')

    assert user.id == 1
    assert user.username == 'username'
    assert user.first_name == 'Jane'
    assert user.last_name == 'Doe'
    assert user.password == '123'

def test_id_model_is_not_right():
    user = UserModel(id='123', username='username',
        first_name='Jane', last_name='Doe',
        password='123')

    assert False
    ...
