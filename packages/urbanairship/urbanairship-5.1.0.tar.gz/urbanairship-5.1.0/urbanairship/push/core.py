import json
import logging

from urbanairship import common


logger = logging.getLogger('urbanairship')


class Push(object):
    """A push notification. Set audience, message, etc, and send."""

    def __init__(self, airship):
        self._airship = airship
        self.audience = None
        self.notification = None
        self.device_types = None
        self.options = None
        self.campaigns = None
        self.message = None
        self.in_app = None

    @property
    def payload(self):
        data = {
            'audience': self.audience,
            'notification': self.notification,
            'device_types': self.device_types,
        }
        if self.options is not None:
            data['options'] = self.options
        if self.campaigns is not None:
            data['campaigns'] = self.campaigns
        if self.message is not None:
            data['message'] = self.message
        if self.in_app is not None:
            data['in_app'] = self.in_app
        return data

    def send(self):
        """Send the notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.
        :raises ValueError: Required keys missing or incorrect values included.
        """
        if 'email' in self.payload['notification']:
            if self.payload['device_types'] == 'all':
                raise ValueError(
                    'device_types cannot be all when including an email override'
                )
            if 'email' not in self.payload['device_types']:
                raise ValueError(
                    'email must be in device_types if email override is included'
                )
        if 'email' in self.payload['device_types'] \
                and 'email' not in self.payload['notification']:
            raise ValueError(
                'email override must be included when email is in device_types'
            )

        body = json.dumps(self.payload)
        response = self._airship._request(
            method='POST',
            body=body,
            url=common.PUSH_URL,
            content_type='application/json',
            version=3
        )

        data = response.json()
        logger.info('Push successful. push_ids: %s',
                    ', '.join(data.get('push_ids', []))
                    )

        return PushResponse(response)


class ScheduledPush(object):
    """A scheduled push notification. Set schedule, push, and send."""

    def __init__(self, airship):
        self._airship = airship
        self.schedule = None
        self.name = None
        self.push = None
        self.url = None

    @classmethod
    def from_url(cls, airship, url):
        """Load an existing scheduled push from its URL."""

        sched = cls(airship)
        response = sched._airship._request(
            method='GET',
            body=None,
            url=url,
            version=3
        )
        payload = response.json()
        sched.name = payload.get('name')
        sched.schedule = payload['schedule']
        sched.push = Push(airship)
        sched.push.audience = payload['push']['audience']
        sched.push.notification = payload['push']['notification']
        sched.push.device_types = payload['push']['device_types']
        if 'message' in payload['push']:
            sched.push.message = payload['push']['message']
        if 'options' in payload['push']:
            sched.push.options = payload['push']['options']
        sched.url = url
        return sched

    @classmethod
    def from_payload(cls, payload, id_key, airship):
        """Create based on results from a ScheduledList iterator."""
        obj = cls(airship)
        obj._schedule_id = payload[id_key]
        for key in payload:
            setattr(obj, key, payload[key])
        return obj

    @property
    def payload(self):
        if hasattr(self.push, 'merge_data'): # check if template
            data = self.push.payload
            data['schedule'] = self.schedule
        else:
            data = {
                'schedule': self.schedule,
                'push': self.push.payload,
            }

        if self.name is not None:
            data['name'] = self.name

        return data

    def send(self):
        """Schedule the notification

        :returns: :py:class:`PushResponse` object with ``schedule_url`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """
        body = json.dumps(self.payload)

        if hasattr(self.push, 'merge_data'):
            url = common.SCHEDULE_TEMPLATE_URL
        else:
            url = common.SCHEDULES_URL

        response = self._airship._request(
            method='POST',
            body=body,
            url=url,
            content_type='application/json',
            version=3
        )
        data = response.json()

        urls = data.get('schedule_urls', [])
        if urls:
            self.url = urls[0]
            logger.info('Scheduled push successful. schedule_urls: %s',
                        ', '.join(data.get('schedule_urls', [])))

        else:
            logger.info('Scheduled push resulted in zero messages scheduled.')


        return PushResponse(response)

    def cancel(self):
        """Cancel a previously scheduled notification."""
        if not self.url:
            raise ValueError('Cannot cancel ScheduledPush without url.')

        self._airship._request(
            method='DELETE',
            body=None,
            url=self.url,
            version=3
        )

    def update(self):
        if not self.url:
            raise ValueError(
                'Cannot update ScheduledPush without url.')
        body = json.dumps(self.payload)
        response = self._airship._request(
            method='PUT',
            body=body,
            url=self.url,
            content_type='application/json',
            version=3
        )

        data = response.json()
        logger.info('Scheduled push update successful. schedule_urls: %s',
                    ', '.join(data.get('schedule_urls', [])))

        return PushResponse(response)


class TemplatePush(object):
    """A personalized push notification. Set details and send."""

    def __init__(self, airship):
        self._airship = airship
        self.audience = None
        self.device_types = None
        self.merge_data = None

    @property
    def payload(self):
        data = {
            'audience': self.audience,
            'device_types': self.device_types,
            'merge_data': self.merge_data
        }

        return data

    def send(self):
        """Send the personalized notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """

        if not self.audience:
            raise ValueError('Must set audience for template push.')

        if not self.device_types:
            raise ValueError('Must set device_types for template push.')

        body = json.dumps(self.payload)
        response = self._airship._request(
            method='POST',
            body=body,
            url=common.TEMPLATES_URL + 'push',
            content_type='application/json',
            version=3
        )

        data = response.json()
        logger.info('Push successful. push_ids: %s',
                    ', '.join(data.get('push_ids', []))
                    )

        return PushResponse(response)


class PushResponse(object):
    """Response to a successful push notification send or schedule.

    Right now this is a fairly simple wrapper around the json payload response,
    but making it an object gives us some flexibility to add functionality
    later.

    """
    ok = None
    push_ids = None
    schedule_url = None
    operation_id = None
    payload = None

    def __init__(self, response):
        data = response.json()
        self.push_ids = data.get('push_ids')
        self.schedule_url = data.get('schedule_urls', [])
        self.operation_id = data.get('operation_id')
        self.ok = data.get('ok')
        self.payload = data

    def __str__(self):
        return 'Response Payload: {0}'.format(self.payload)
