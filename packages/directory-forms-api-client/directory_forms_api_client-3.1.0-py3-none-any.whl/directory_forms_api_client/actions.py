import abc

from directory_forms_api_client.client import forms_api_client


class AbstractAction(abc.ABC):

    def __init__(self, form_url, client=forms_api_client, *args, **kwargs):
        self.form_url = form_url
        self.client = client

    @property
    @abc.abstractmethod
    def name(self):
        return ''

    def serialize_data(self, data):
        return {
            'data': data,
            'meta': self.serialize_meta()
        }

    def serialize_meta(self):
        return {
            'action_name': self.name,
            'form_url': self.form_url,
            **self.meta,
        }

    def save(self, data):
        serialized_data = self.serialize_data(data)
        return self.client.submit_generic(serialized_data)


class EmailAction(AbstractAction):
    name = 'email'

    def __init__(self, recipients, subject, reply_to, *args, **kwargs):
        self.meta = {
            'recipients': recipients,
            'subject': subject,
            'reply_to': reply_to,
        }
        super().__init__(*args, **kwargs)


class ZendeskAction(AbstractAction):
    name = 'zendesk'

    def __init__(
        self, subject, full_name, email_address, service_name, subdomain=None,
        *args, **kwargs
    ):
        self.meta = {
            'full_name': full_name,
            'email_address': email_address,
            'subject': subject,
            'service_name': service_name,
        }
        # if empty Forms API will use the default configured zendesk subdomain
        if subdomain:
            self.meta['subdomain'] = subdomain
        super().__init__(*args, **kwargs)


class GovNotifyAction(AbstractAction):
    name = 'gov-notify'

    def __init__(
        self, template_id, email_address, email_reply_to_id=None,
        *args, **kwargs
    ):
        self.meta = {
            'template_id': template_id,
            'email_address': email_address,
        }
        if email_reply_to_id:
            self.meta['email_reply_to_id'] = email_reply_to_id
        super().__init__(*args, **kwargs)


class PardotAction(AbstractAction):
    name = 'pardot'

    def __init__(self, pardot_url, *args, **kwargs):
        self.meta = {
            'pardot_url': pardot_url,
        }
        super().__init__(*args, **kwargs)
