# Django Epsilon

[Epsilon.com](https://us.epsilon.com/home) API integration for Django applications

#### Installation
```python
pip install django-epsilon
```

#### Usage
```python
from epsilon.models import Epsilon

profile = {
    'first_name': 'John',
    'last_name': 'Smith',
    'date_of_birth': '1990-01-01',
    'zip_code': '12345',
    'email': 'john.smith@example.com'
}

promotion_id = Epsilon.addProfile(profile, add_survey=True)
```

#### Configuration
Add these variables to your Django settings
```python
from os import getenv

# If set to False, API will never be called
EPSILON_ON = getenv('EPSILON_ON', True)
# Enables django signals
EPSILON_AUTO_PUSH = getenv('EPSILON_AUTO_PUSH', False)

# Epsilon.com client settings
EPSILON_CLIENT_ID = ''
EPSILON_CLIENT_SECRET = ''
EPSILON_API_ENDPOINT = 'https://your_url.epsilon.com/CPGWebServices'
EPSILON_CAMPAIGN_CONTROL_ID = ''
EPSILON_QUESTION_ANSWER_ID = ''

# Epsilon.com campaign settings
EPSILON_TRACKING_INFO_DOMAIN_HASH = ''
EPSILON_TRACKING_INFO_TIMESTAMP = ''
EPSILON_TRACKING_UTM_SOURCE = ''
EPSILON_TRACKING_UTM_MEDIUM = ''
EPSILON_TRACKING_UTM_TERM = ''
EPSILON_TRACKING_UTM_CONTENT = ''
EPSILON_TRACKING_UTM_CAMPAIGN = ''
```
