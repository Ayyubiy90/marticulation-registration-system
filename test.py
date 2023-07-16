import requests

# Testing the Registration Endpoint
registration_url = 'http://localhost:5001/register'
registration_data = {
    'name': 'John Doe',
    'date_of_birth': '2000-01-01',
    'program_enrolled': 'Computer Science',
    'registration_number': 'CS123'
}

try:
    registration_response = requests.post(
        registration_url, json=registration_data)
    # Raise an exception if the request was unsuccessful
    registration_response.raise_for_status()
    print('Registration successful')
except requests.exceptions.RequestException as e:
    print(f'Registration failed: {e}')

# Testing the Search Endpoint
search_url = 'http://localhost:5001/search'
search_params = {'term': 'John'}

try:
    search_response = requests.get(search_url, params=search_params)
    # Raise an exception if the request was unsuccessful
    search_response.raise_for_status()
    search_results = search_response.json()
    print('Search Results:', search_results)
except requests.exceptions.RequestException as e:
    print(f'Search failed: {e}')
