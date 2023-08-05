# RBX Platform

The **RBX Platform** is the core service powering the **Rig**.
Its purpose is to house the business logic for planning and distributing campaigns,
and provide a web interface to manipulating its data, via a JSON-RPC API.

## Domain Design

The Platform is composed of 3 domains:

- the public-facing interfaces (Public APIs),
- the business domain,
- and the technical domain.

When adding functionality, keep this domain split in mind.
The following diagram describes how these domains interact:

```
   Public APIs   |     Business     |       Technical
-----------------|------------------|----------------------
                 |                  |
     ------      |    ----------    |
    | HTTP |-------->|          |   |    ---------------
     ------      |   | Platform |------>|  Third-Party  |
   ----------    |   |   API    |   |   |   Libraries   |
  | JSON-RPC |------>|          |   |   |               |
   ----------    |    ----------    |   |    --------   |
                 |         |        |   |   | Django |  |
                 |    -----^----    |   |   | Models |  |
                 |   | Entities |------>|    --------   |
                 |    ----------    |    ---------------
                 |                  |
  rbx.api        |  rbx.iponweb     |  rbx.ext
                 |  rbx.platform    |

```

> The **Platform API** is the _Internal Public Interface_ to access the business domain entities.
> The **Public APIs** should only interact with this interface, and never with the entities
> directly.

#### Files Structure

The files are laid out according to the domains they implement:

```
rbx/
    api/               JSON-RPC API
    ext/               External packages (including REST API via the Django REST Framework)
    helpers.py         Shared helpers
    iponweb/           IPONWEB Integration
    platform/          Platform core and business logic
        _utils.py      Platform utilities
        _helpers.py    Platform helpers
        core.py        Internal Public Interface
        types.py       Platform types
        ...
    utils/             Shared utilities
    ...
```

Some modules to note are the Platform types and utilities modules.
These modules should be imported via their package.

e.g.:

```python
from rbx.platform import State
from rbx.utils import datetime_to_timestamp
```

## Platform Formats

The JSON-formatted Ad Unit and Creative **Formats** definitions are available at the following URLs:

```
/fixtures/ad-formats.json
/fixtures/creative-formats.json
```

## Platform Permissions

**Platform Permissions** define **actions** a user can perform.

An action represents a particular feature in the Rig.
For instance, _"Create a Campaign"_, _"Update a Strategy"_, or _"Access the Custom Report"_.

These permissions are represented as strings in the Platform.
For instance, the permissions representing the _"Create a Campaign"_ action is `create_campaign`.

They are implemented on top of the Django's simple permissions system.

> The full list of Permissions is defined in the `rbx.platform.types.permission` module.
>
> Note that these permissions are never assigned to users.
> Instead, **Roles** (Django Groups) are created and given specific sets of permissions.
> These Roles are then assigned to users.

Access to these actions is implemented in the **Public APIs**.

> The **Platform API** controls access to individual Campaigns.

## Public APIs

The Public APIs are used exclusively by the Rig UIs.

- The REST API is the legacy API and is being deprecated.
- The JSON-RPC API is the main public entrypoint.
  See the full [API Reference](./docs/api/README.md) for details.

## Platform API

The **Platform API** is a Python API whose purpose is to host the domain's business logic.
See the [getting started guide](./docs/platform/README.md) for a primer.

> When referring to **API**, we usually refer to the JSON-RPC API.

## PyPI

The project is also used as the root PyPI namespace `rbx` for the public index.
It is distributed as an empty distribution, in order to reserve the name.

The PyPI package is available at [pypi.python.org/pypi/rbx](https://pypi.python.org/pypi/rbx/).

To publish a new release:

```
python setup.py sdist
pip install twine
twine upload [--repository-url https://test.pypi.org/legacy/] dist/*
```

## Available Scripts

The repository also provides some helper scripts.

Install them with pip:

```
pip install rbx
```

### Generate Geo Files

City-level targeting requires a series of JSON files to be generated using a format the Rig can use.
The database used is a CSV dump from MaxMind. So does Geocode targeting.

First, copy the database files to a versioned folder (e.g.: `data/geo/db/<VERSION>/`).
Where `<VERSION>` is the database version.
This can be a timestamp (e.g.: `20180619`), or a string (e.g.: `latest`).

> The files can be downloaded from MaxMind (https://www.maxmind.com/en/accounts/current/geoip/downloads).
> There should be 2 files: `GeoIP2-Country.csv` and `GeoIP2-City.csv`.

Download them using our MaxMind Licence Key:

```
mkdir -p data/geo/db/<VERSION>
wget -O data/geo/db/<VERSION>/GeoIP2-Country.csv \
  "https://download.maxmind.com/app/geoip_download?edition_id=GeoIP2-Country-CSV&license_key=<KEY>&suffix=zip"
wget -O data/geo/db/<VERSION>/GeoIP2-City.csv \
  "https://download.maxmind.com/app/geoip_download?edition_id=GeoIP2-City-CSV&license_key=<KEY>&suffix=zip"
```

Upload the database files to S3 so Jenkins can access them:

```
aws s3 sync ./data/geo/db/<VERSION> s3://474071279654-eu-west-1-jenkins/fixtures/geo/<VERSION>
```

Run the script to generate the files:

```
unpack -d ./data/geo/output ./data/geo/db/<VERSION>/
```

This will create the output files in the `data/geo/output/<VERSION>` folder.

And finally upload these files to the AWS S3 buckets for all environments:

e.g.:

```
aws s3 sync ./data/geo/output/latest s3://474071279654-eu-west-1-assets/rig/geo/latest
```

#### Fixing Discrepancies

Sometimes the location/country pair found in the MaxMind database clashes with the results returned
by the Google Maps API. In these cases, we will get a Geocode lookup failure.

The Platform provides a command to lookup locations:

```
geocode "location" --key <MAPS-API-KEY> [--country <iso-2-country-code>]
```

The result can then be manually set in the database via the Admin UI, setting the `location_type`
to `MANUAL`.

For country-wide boundaries, the closest we've found to an answer is on this website:

    https://www.worldatlas.com

From there, locate the "Where is 'Country'" page, which will display the boundaries in the
**Quick facts** section.

> The minimum lat/lng is the South West, and the maximum the North East.

## IPONWEB Publishing

Real-time bidding (RTB) is the process by which the decision about which ad to serve to a user
browsing a site happens in real time, by means of a bidding process where the highest bidder wins.
Without going into detail about what that process entails, our interface to the RTB world is via
a platform developed by our partner IPONWEB.

Our "API" to the IPONWEB platform consists of uploading an XML file that contains the whole set of
live campaigns that participate in bidding.

### XML Feed

The XML feed sent to the IPONWEB SFTP server is generated on the fly.
An endpoint is available to display it in its entirety when troubleshooting,
and is accessible at the following URL:

```
/iponweb/rtb_data.xml
```

### SFTP Server

Access to the IPONWEB SFTP server is granted via the private RSA key
`iponweb-publishing.pem`. This key is not included in this repository, so you
must grab it from the [Configurations](https://github.com/rockabox/configuration)
repository, and place it at the root of the project.

> All IPONWEB-related documentation can be found on their
> [Confluence Wiki](https://confluence.iponweb.net/display/UPLATFORMKB/u-Platform+Knowledge+Base).

### U-Slicer

The **Media Cost**, a.k.a. _Spend_, is queried via IPONWEB's u-Slicer API.

A client implementation is available in the `rbx.iponweb` package.

e.g.:

```python
from rbx.iponweb.client import Client
>>> client = Client(slicer_name='Traffic', project_name='rockabox', token='eyJhbGciO...')
>>> client.actual_pub_payout(start_date='2017-08-10',
...                          end_date='2017-08-25',
...                          strategies=[1073745495, 1073745496])

{1073745496: 988.07, 1073745495: 1369.36}
```

> The `token` is a permanent API token, generated via the IPONWEB UI: https://uauth.iponweb.com/

### Automated Delivery Control

The Platform always ensures that Campaigns don't over-deliver. The controlling factor is spend,
which we get from the bidder (IPONWEB) via their u-Slicer API.

Once the total spend for a Strategy has reached its budget, the Strategy is flagged as `FINISHED`.

These Strategies will resume when more budget is assigned to them.

> There are no restrictions on the budget users can allocate, apart from it being within the
> Campaign budget.
> It is therefore up to the user to make sure enough budget is added.

The bidder doesn't support overall impression or spend cap. It does, however, support daily spend
capping. Using the total spend for LIVE Strategies, and the total budget assigned to them, we can
regularly adjust the daily capping to ensure that they never overspend.

The data processing latency of the u-Slicer API is ~3h. Therefore the schedule for this regular
adjustment check runs every 3 hours.

> Although we do store the spend figure for this feature, we do not expose it to the UI.

#### Notifications

Ad Operations (`opsuk@scoota.com`) and all users assigned to the affected Strategies with the
`CREATE_CAMPAIGN` permission are notified via email:

- When a daily cap is automatically adjusted.
- When a Strategy is flagged as having reached its total budget.

## Deployment

Deploying the Platform to any environment is performed in the same way:

- Install DevOps requirements:

```
pip install -r requirements/dev.txt
```

- Build and upload a Docker image:

```
`aws ecr get-login --no-include-email`
invoke image.build --name platform --version redqa5b84810
invoke image.upload --name platform --version redqa5b84810
```

- Ensure the host instance's SSH service is setup to accept the `VERSION` environment:

```
# /etc/ssh/sshd_config
AcceptEnv VERSION
```

- Set environment variables:

```
export FABRIC_ENVIRONMENT=redqa
export FABRIC_KEY_FILENAME=~/.ssh/development
export FABRIC_HOST=10.2.111.54
export FABRIC_USER=ec2-user
export FABRIC_VERSION=redqa5b84810
```

- Run the deployment script:

```
fab deploy
```

- Reset the Pub/Sub Emulator on QA:

```
fab setup-pubsub-emulator
```

## Development & Local Testing

This service is deployed as a Docker image. As such, working on it should also be done in a
Docker container.

The `docker/yml/develop.yml` configuration is to be used for development.
It mounts local folders inside the running container.

> See comments in `docker/yml/develop.yml` for usage.

To make it easier to work on an image, you can enter a running container
of the image:

```
/> docker-compose -f docker/yml/develop.yml run --rm platform /bin/bash
root@(container):/opt# ./tests/test_runner.sh -f|--failfast -c|--with-coverage [/path/to/test.py]
```

This will run the test run from within the container.

### Running a Service Locally

In order to run a local version of the service, use the configuration in `docker/yml/local.yml`.

Make sure you run the `docker/yml/local-setup.yml` once to set things up.
i.e.: migrate databases and collect static files.

> You might have to run the setup twice, as the first run might fail
> when static files are extracted to fact, before the postgres engine is ready.

The service (group `docker` [999]) will also need access to your aws credentials
stored in `~/.aws/credentials`, which will be mounted into the platform docker
container.

The local Pub/Sub topic must also be created:

- Enter the running container, and run the `create_topic.py` script:

```
/> docker exec -it yml_platform_1 /bin/bash
root@(container):/opt# python config/create_topic.py
```

### JSON-RPC Methods

The JSON-RPC backend is implemented with the [json-rpc](http://json-rpc.readthedocs.io/en/latest/)
library, exposed in the `rbx.api.backend` package.

Example:

```python
from rbx.api.backend import api

@api.dispatcher.add_method
def do_something(request, **kwargs):
    return {}
```

### Permissions

The JSON-RPC backend provides a decorator to protect access to methods.
The decorator will protect any decorated method so that:

- only authenticated users may access it;
- only users with specific permissions may access it;

The decorator will also inject an instance of the `Platform` object, which will automatically
instantiate with a valid `Campaign` if the `campaign_id` parameter is provided, and the user
has access to that campaign.

For instance:

```python
from rbx.api.backend import api

@api.dispatcher.add_method
@api.protect_method(permissions=['edit_campaign'])
def my_protected_method(request, platform):
    assert platform.campaign is not None
```

#### Testing Authentication & Permissions

The `tests.test` module provides a suite of `TestCase` implementions to write integration tests.

##### `IntegrationTestCase`

The class provides helpers to manage all areas of the Platform, particularly background workers.

##### `APITestCase`

The class provides helpers to manage users and permissions.
It also provide a helper to post a JSON-RPC 2.0 request.

```python
from tests.test import APITestCase

class MyTestCase(APITestCase):
    permissions = ['some_permission']

    def my_test(self):
        """The user object will be available as an instance attribute."""
        user = self.user
```

> This class provides a much more complete option set.
> See the class docstring for more details.

### Asynchronous Jobs

For long-running or resource-consuming job, the `rbx.ext.task` application provides an API
to run these jobs in the background.

The implementation is based on [Python RQ](http://python-rq.org/), and uses a Redis cluster
as the underlying queue.

To send a job to the background, use the `deferred.defer` method:

```python
from rbx.ext.task import deferred

def my_function(*arg, **kwargs):
    ...

deferred.defer(my_function, *arg, **kwargs)
```

You can check which jobs are in the queue with:

```python
from rbx.ext.task import deferred

print(deferred.queue.jobs)
```

When a job fails for any reason, it is moved to the failed queue.
You can list all failed jobs using:

```python
from rbx.ext.task import deferred

print(deferred.failed_queue.jobs)
```

The task package also provides a decorator to retry failed jobs a certain amount of tries
before giving up and moving it to the failed queue:

```python
from rbx.ext.task import deferred
from rbx.ext.task.decorators import retry

@retry(max_retries=3)
def my_function(*arg, **kwargs):
    ...

deferred.defer(my_function, *arg, **kwargs)
```

### Scheduled Jobs

Scheduled jobs, or recurring jobs, are managed by the Scheduler in `rbx.ext.task.scheduler`.
They are defined and scheduled using the standard CRON expression syntax.

> This tool is useful to check CRON expressions: https://crontab.guru/

To schedule any Python function, simply add it to the `JOBS_SCHEDULE` in the base settings.

_e.g._:

```python
JOBS_SCHEDULE = {
    'recurring_task_name': {
        'task': 'rbx.<app>.<module>.<function>',
        'schedule': '* * * * *',  # CRON expression
    },
    ...
}
```

To list all scheduled jobs:

```
from rbx.ext.task.scheduler import Scheduler

scheduler = Scheduler()
print(scheduler.get_jobs()))
```

### Shared File System

The Platform uses AWS **Elastic File System** to share binary files between the web processes and the
scheduled and asynchronous job processes. This is to allow the Web Server and the Worker to live in
separate virtual instances on AWS.

AWS EFS can be setup on a new instance by following the steps below:

```
cd /home/ec2-user
mkdir efs
sudo bash -c "echo '<EFS DNS name>:/ /home/ec2-user/efs nfs nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 0 0' >> /etc/fstab"
sudo mount -a
sudo chown ec2-user: efs
chmod 777 efs
```

Where `<EFS DNS name>` is the full EFS DNS name of the file system.
e.g.: `fs-514a8698.efs.eu-west-1.amazonaws.com`

The EFS folder may now be mounted inside a running Docker container by adding a volume to
the `docker-compose.yml` file:

```
volumes:
    - /home/ec2-user/efs:/data/efs
```

### Google Cloud Platform

Access to the **Google Cloud Platform** is granted via a JSON credentials file.
The testing and development setup uses the **Pub/Sub Publisher** service account to
access the Google APIs.

> This service account already exists.
> See the [GCP API Manager](https://console.cloud.google.com/apis/credentials).

#### Master Data Management Notifications

MDM notifications are published to the `platform-notifications` Pub/Sub topic.

> This topic must exist.
> Check the [GCP Console](https://console.cloud.google.com/cloudpubsub/topicList).

The MDM is notified about:

 - New Campaigns.
 - Campaign updates.
 - New Strategies (when they become `READY`).
 - Strategy updates (`READY` and above only).
 - New Ad Units (when they become `READY`).
 - Ad Unit updates (`READY` only).
 - Creatives and Components (when the Creatives are released).
 - New Placements (when they become `READY`).

### CI Test

Jenkins will use the `docker/yml/ci.yml` configuration, which will test
against the final image.

> See `docker/yml/ci.yml` for usage.

The runner will generate Cobertura XML report in `coverage.xml`.

> If the CI test is run locally, make sure the `coverage.xml` file
> is not added to the commit.
> The file must be a dummy empty file, to ensure it inherits the correct
> file permissions.

### Database Queries Profiling

If not careful, the Django ORM will generate millions of queries. Throughout the code, we make sure
the caching and prefetching features of the ORM are being used, so as to optimize the number of
queries generated.

There is no automated way of doing this. In the future, we should consider adding query performance
as part of the test suite using a library like [this](https://github.com/YPlan/django-perf-rec).

Until then, the [Silk Django profiler](https://github.com/jazzband/django-silk) can be used.

> Django Silk is not installed, so it needs to be installed and set up manually when needed.
