import json
from test_api import app



# each def is a test unit
# all assertions need to be passed for the test to be considered 'passed'

# this is the first level, unit testing. you test each unit separately
# the second level is integration testing. you test a large part of the program that consists of multiple units
# the third level is end-to-end testing. you test the entire program like it's one unit

# end-to-end is a type of blackbox testing, while unit is similar to whitebox testing

def test_get_all_actors():
    response = app.test_client().get('/actors')
    res = json.loads(response.data).get("actors")
    
    assert response.status_code == 200
    assert type(res[0]) is dict
    assert type(res[1]) is dict
    assert type(res) is list

def test_get_one_actor():
    response = app.test_client().get('/actor?id=55')
    
    assert response.status_code == 200

def test_update_actor():
    response = app.test_client().post('/new', json={'first name': 'new first name', 'last name': 'new last name'})
    res = json.loads(response.data).get("actor")
    
    assert response.status_code == 200
    assert res['first name'] == 'new first name'

def test_delete_actor():
    response = app.test_client().get('/delete?id=208')
    
    assert response.status_code == 200