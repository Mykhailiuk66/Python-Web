import pytest
from app import create_app, db  
from flask_login import current_user
from datetime import timezone, datetime
from app.tasks.models import Priority

@pytest.fixture
def app():
    app = create_app(config_name='test')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        

@pytest.fixture    
def client(app):
    return app.test_client()


@pytest.fixture
def register_user(client):
    with client:
        client.post('/register', data={'username': 'test_name', 'email': 'test1234@gmail.com',  'password': 'Qwerty1234', "confirm_password": 'Qwerty1234'},
                    follow_redirects=True)
    

@pytest.fixture
def login_user(client):
    with client:
        client.post('/login', data={'email': 'test1234@gmail.com',  'password': 'Qwerty1234', 'remember': True}, 
                    follow_redirects=True)
        
    
@pytest.fixture
def add_category(client, register_user, login_user):
    client.post('/category/create', data={'name': 'work'}, follow_redirects=True)
    
    
@pytest.fixture
def add_task(client, register_user, login_user, add_category):
    data = {
        'title': 'Test Task',  
        'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting', 
        'priority': '1',
        'category_id': '1',
    }
    response = client.post('/task/create', data=data, follow_redirects=True)


def test_client(client):
    assert client is not None
    
    
def test_index(client):
    response = client.get('/')
    
    assert response.status_code == 200
    assert b'Portfolio' in response.data
    

def test_about(client):
    response = client.get('/about')
    
    assert response.status_code == 200
    assert b'About Me' in response.data


def test_reg_log_logout(client):
    with client:
        response = client.post('/register', data={'username': 'test_name', 'email': 'test1234@gmail.com',  'password': 'Qwerty1234', "confirm_password": 'Qwerty1234'}, 
            follow_redirects=True)

        assert response.status_code == 200
        assert b'Login' in response.data
        
        response = client.post('/login', data={'email': 'test1234@gmail.com',  'password': 'Qwerty1234', 'remember': True}, 
                        follow_redirects=True)
        assert response.status_code == 200
        assert current_user.username == "test_name"
        
        response = client.get('/logout', follow_redirects=True)
    
        assert response.status_code == 200
        assert current_user.is_anonymous  
            
        
def test_add_task(client, add_category):
    data = {
        'title': 'Test Task',  
        'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting', 
        'priority': '1',
        'category_id': '1',
    }
    response = client.post('/task/create', data=data, follow_redirects=True)
    
    assert b'Task added' in response.data


def test_tasks(client, add_task):
    response = client.get('/tasks', follow_redirects=True)
    assert b'Lorem Ipsum is simply dummy text of the printing and typesetting' in response.data
    

def test_task(client, add_task):
    response = client.get('/task/1', follow_redirects=True)
    
    assert b'Lorem Ipsum is simply dummy text of the printing and typesetting' in response.data
    assert b'Comments' in response.data
    assert b'Assigned users' in response.data


def test_task_update(client, add_task):
    data = {
        'title': 'Test Task (ch)',  
        'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting', 
        'priority': '3',
        'category': '1',
    }
    response = client.post('/task/1/update', data=data, follow_redirects=True)
    
    assert b'Test Task (ch)' in response.data
    assert b'High' in response.data


def test_task_delete(client, add_task):
    response = client.get('/task/1/delete', follow_redirects=True)
    
    assert b"Task deleted" in response.data
