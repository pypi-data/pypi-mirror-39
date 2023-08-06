#



## Installation

```
pip install dj-healthchecks
```

## Usage

### Add to a project

In `urls.py`:

```
from django.conf.urls import url, include

from rest_framework import routers
from healthchecks.api import HealthViewSet

router = routers.DefaultRouter()
router.register(r'health', HealthViewSet, basename='health')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
```

**You define your healthchecks in `settings.py`**

```python
HEALTH_CHECKS = [
    'healthchecks.checks.im_ok',
    'healthchecks.checks.connect_to_db',
    'healthchecks.checks.connect_to_queue',
    'healthchecks.checks.connect_to_redis',
    'healthchecks.checks.ping_upstream_urls',
    ...
]
```

This library provides some utility healthchecks, but you can also easily write your own.

Provided healthchecks are in `healthchecks/checks.py`

**Specifying your own healthcheck:**

```python
HEALTH_CHECKS = [
    ...
    'myapp.myodule.my_health_check',
]
```


**Now you have:**

```
GET /health/ # run all health checks in settings.py
GET /health/some-health-check/ # run a specific healthcheck
```

**Note:** for a specific healthcheck, you `-` will be replaced with `.`


## Run project:

```
docker-compose up
```

## Run tests:

```
docker-compose run --rm web python manage.py test
```

Profit.

## Updating

Bump the version:

```
bumpversion manjor|minor|patch
```

Push to master