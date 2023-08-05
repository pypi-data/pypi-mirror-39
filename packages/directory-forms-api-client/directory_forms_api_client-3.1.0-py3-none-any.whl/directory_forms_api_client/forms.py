from django.forms import Form

from directory_forms_api_client import actions


class EmailActionMixin:
    action_class = actions.EmailAction

    def save(
        self, recipients, subject, reply_to, form_url=None, *args, **kwargs
    ):
        action = self.action_class(
            recipients=recipients,
            subject=subject,
            reply_to=reply_to,
            form_url=form_url,
        )
        return action.save(self.serialized_data)

    @property
    def serialized_data(self):
        return {
            'text_body': self.text_body,
            'html_body': self.html_body,
        }

    @property
    def text_body(self):
        raise NotImplementedError()

    @property
    def html_body(self):
        raise NotImplementedError()


class ZendeskActionMixin:
    action_class = actions.ZendeskAction

    def save(
        self, email_address, full_name, subject, service_name, subdomain=None,
        form_url=None, *args, **kwargs
    ):
        action = self.action_class(
            email_address=email_address,
            full_name=full_name,
            subject=subject,
            service_name=service_name,
            subdomain=subdomain,
            form_url=form_url,
        )
        return action.save(self.serialized_data)

    @property
    def serialized_data(self):
        return self.cleaned_data


class GovNotifyActionMixin:
    action_class = actions.GovNotifyAction

    def save(
        self, template_id, email_address, email_reply_to_id=None,
        form_url=None, *args, **kwargs
    ):
        action = self.action_class(
            template_id=template_id,
            email_address=email_address,
            email_reply_to_id=email_reply_to_id,
            form_url=form_url,
        )
        return action.save(self.serialized_data)

    @property
    def serialized_data(self):
        return self.cleaned_data


class PardotActionMixin:
    action_class = actions.PardotAction

    def save(self, pardot_url, form_url=None, *args, **kwargs):
        action = self.action_class(pardot_url=pardot_url, form_url=form_url)
        return action.save(self.serialized_data)

    @property
    def serialized_data(self):
        return self.cleaned_data


class EmailAPIForm(EmailActionMixin, Form):
    pass


class ZendeskAPIForm(ZendeskActionMixin, Form):
    pass


class GovNotifyAPIForm(GovNotifyActionMixin, Form):
    pass


class PardotAPIForm(PardotActionMixin, Form):
    pass
