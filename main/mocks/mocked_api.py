import json as json_module

def mocked_requests_post_login_view(url, json=None):
    """
    This function is a mock for the wired API user authentication endpoint.
    It mimmics the authentication behaviour of the api enpoint using dummy data.
    """
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

    if json['email_address'] == 'test@test.com' and json['password'] == 'test':
        
        responce_dict = {
            'token-key':'test-token',
            'user_id': 1,
            'email_address': 'test@test.com'
        }
       
        json_data = json_module.dumps(responce_dict).encode('utf-8')

        return MockResponse(json_data, 200)

    else:
        
        responce_dict = {
            'errors':{'dummy-error':'dummy error message'},
        }

        json_data = json_module.dumps(responce_dict).encode('utf-8')

        return MockResponse(json_data, 400)

def mocked_requests_post_register_view(url, json=None):
    """
    This function is a mock for the wired API create user endpoint.
    It mimmics the behaviours of the create user enpoint using dummy data to check if the email is unique.
    """
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

    if json['email_address'] != 'unique-email@test.com' and json['user_name'] != 'unique-user':
        
        responce_dict = {
            'user_data':{
                'first_name':'test', 
                'last_name':'test', 
                'user_name':'test', 
                'email_address':'test@test.com',
                'password': 'hashed-password'
                },
            'token-key': 'test-token'
            }
       
        json_data = json_module.dumps(responce_dict).encode('utf-8')

        return MockResponse(json_data, 201)

    else:
        
        responce_dict = {
            'errors':{'dummy-error':'dummy error message'},
        }

        json_data = json_module.dumps(responce_dict).encode('utf-8')

        return MockResponse(json_data, 400)
