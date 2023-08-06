<img src="http://i.imgur.com/YF8yAJS.png" width="80">

# Django Slack OAuth [![Build Status](https://travis-ci.org/izdi/django-slack-oauth.svg?branch=master)](https://travis-ci.org/izdi/django-slack-oauth)

A lightweight module for integrating your Django application with Slack.

## Requirements

- Django >= 1.8

To use Slack OAuth in your Django app, you'll need your `SLACK_CLIENT_ID` and `SLACK_CLIENT_SECRET` which can be found when you [Create a New Slack Application](https://api.slack.com/applications).


## Instructions

1. Install using pip:

    ```
    $ pip install django-slack-oauth
    ```

2. Add `django_slack_oauth` to `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = (
        ...
        'django_slack_oauth',
    )
    ```

3. Run initial migrations:

    ```
    $ python manage.py migrate
    ```

4. Add Slack OAuth base url to your project's `urls.py`:

    ```python
    urlpatterns = [
        ...
        url(r'^slack/', include('django_slack_oauth.urls')),
        ...
    ]
    ```

5. Specify your Slack credentials and OAuth Scope in `settings.py`:

    ```python
    SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
    SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')
    SLACK_SCOPE = 'admin,bot'
    ```
    If you aren't sure what your scope should be, read more about [Slack OAuth Scopes](https://api.slack.com/docs/oauth-scopes).

## Example

Add a link to Slack OAuth in one of your templates:

```
<a href='{% url 'slack_auth' %}'>Get slacked</a>
```

After clicking it, you will be redirected to Slack for the OAuth process. If successful, you will be redirected to a view showing a success message. You can change this view by setting `SLACK_SUCCESS_REDIRECT_URL` in `settings.py`.

You can then view the successful request and API data in the Admin under Slack OAuth Requests.


## Advanced Usage

### Pipelines

Pipelines allow you to create actions after a successful OAuth authentication. Some use cases may be:

- Register an account for the user
- Capture returned API data from Slack after authentication (Default Behaviour)
- Send Slack messages to the user's Slack team after authentication

They are simply a list of functions, which get called in order. They must accept and return two parameters: `request` and `api_data`, containing the initial request and returned API data respectively.

Pipelines are defined as a list of callables in `settings.py`:

```python
SLACK_PIPELINES = [
    'path.to.function1',
    'path.to.function2',
    ...
]
```


- **Example 1:** Show returned data from the OAuth request

    *settings.py*

    ```python
    ...
    SLACK_PIPELINES = [
        'my_app.pipelines.debug_oauth_request',
    ]
    ```

    *my_app/pipelines.py*

    ```python
    def debug_oauth_request(request, api_data):
        print(api_data)
        return request, api_data
    ```

- **Example 2:** Register User and send an email

    *settings.py*

    ```python
    ...
    SLACK_PIPELINES = [
        'my_app.pipelines.register_user',
        'my_app.pipelines.send_email',
    ]
    ```

    *my_app/pipelines.py*

    ```python
    from django.contrib.auth.models import User

    from django_slack_oauth.models import SlackUser


    def register_user(request, api_data):
        if api_data['ok']:
            user, created = User.objects.get_or_create(
                username=api_data['team_id']+':'+api_data['user_id']
            )

            if user.is_active:
                slacker, _ = SlackUser.objects.get_or_create(slacker=user)
                slacker.access_token = api_data.pop('access_token')
                slacker.extras = api_data
                slacker.save()

            if created:
                request.created_user = user

        return request, api_data


    def notify(request, api_data):
        if hasattr(request, 'created_user'):
            notify_admins("New user with id {} has been created.".format(request.created_user))
            notify_user(request.created_user)

        return request, api_data
    ```

_Thanks to_ [Daniel van Flymen](https://github.com/dvf)

### Slack Endpoints

The following parameters may be overriden, in the (rare) case that Slack changes their endpoints:

```python
SLACK_AUTHORIZATION_URL = 'https://slack.com/oauth/authorize'
SLACK_OAUTH_ACCESS_URL = 'https://slack.com/api/oauth.access'
```

### Forgery Attacks

To avoid forgery attacks we pass the `state` parameter in the initial authorization request. This state is stored in the session, which requires the [session middleware to be enabled](https://docs.djangoproject.com/en/2.1/topics/http/sessions/#enabling-sessions) (on by default).
