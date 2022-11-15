import json as json_module

class MockResponse:
    """
    This class defines the mock responce object.
    """
    def __init__(self, json_data, status_code):
        self.content = json_data
        self.status_code = status_code

    def content(self):
        return self.content

    def status_code(self):
        return self.status_code

def mocked_requests_post_login_view(url, json=None):
    """
    This function is a mock for the wired API user authentication endpoint.
    It mimmics the authentication behaviour of the api enpoint using dummy data.
    """
    responce_dict = {
        'user_data':{
            'user_id': 1,
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'email_address':'test@test.com',
            'bio': 'this is a bio',
            'display_pic': None
            },
        'token_key': 'test-token'
        }

    responce_error_dict = {
        'errors':{'dummy-error':'dummy error message'},
    }

    json_data = json_module.dumps(responce_dict).encode('utf-8')
    json_error_data = json_module.dumps(responce_error_dict).encode('utf-8')

    if json['email_address'] == 'test@test.com' and json['password'] == 'test':
        
        return MockResponse(json_data, 200)

    else:
        return MockResponse(json_error_data, 400)

def mocked_requests_post_register_view(url, json=None):
    """
    This function is a mock for the wired API create user endpoint.
    It mimmics the behaviours of the create user enpoint using dummy data to check if the email and username is unique.
    """
    responce_dict = {
        'user_data':{
            'user_id': 1,
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'email_address':'test@test.com',
            'bio': 'this is a bio',
            'display_pic': None
            },
        'token_key': 'test-token'
    }

    responce_error_dict = {
        'errors':{'dummy-error':'dummy error message'},
    }

    json_data = json_module.dumps(responce_dict).encode('utf-8')
    json_error_data = json_module.dumps(responce_error_dict).encode('utf-8')

    if json['email_address'] != 'unique-email@test.com' and json['user_name'] != 'unique-user':
        
        return MockResponse(json_data, 201)

    else:
        return MockResponse(json_error_data, 400)

def mocked_requests_patch_edit_profile_view(url, data=None, files=None, headers=None):
    """
    This function is a mock for the wired API update user endpoint.
    It mimmics the behaviours of the update user enpoint using dummy data to check if the username is unique and the user id is one.
    It also mimmics the behaviour of the enpoints and checks if there is an authorization header with a token.
    """ 
    user_id = url.partition('users/')[2]
    user_name = data.get('user_name')

    responce_dict = {
        'user_data':{
            'user_id': 1,
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'email_address':'test@test.com',
            'bio': 'this is a bio',
            'display_pic': None
            },
        'token_key': 'test-token'
    }

    responce_errors_dict = {
        'errors':{'dummy-error':'dummy error message'},
    }

    json_data = json_module.dumps(responce_dict).encode('utf-8')     
    json_error_data = json_module.dumps(responce_errors_dict).encode('utf-8')

    if headers['Authorization'] == 'token test-token':    
        
        if user_id == '1':

            if user_name and user_name != 'unique-user':
                
                return MockResponse(json_data, 200)

            elif not user_name:
                
                return MockResponse(json_data, 200)
                
            else:
                return MockResponse(json_error_data, 400)

        else:
            return MockResponse(json_error_data, 401)

    else: 
        return MockResponse(json_error_data, 401)