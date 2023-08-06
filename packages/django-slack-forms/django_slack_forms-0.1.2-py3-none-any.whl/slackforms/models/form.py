import dateparser
import re
import requests
import json
import os
import logging
from django.db import models
from django.contrib.postgres.fields import JSONField
from jsonschema import validate, exceptions
from ..utils import schema_to_form, slack, is_float
from ..conf import Settings

logger = logging.getLogger(__name__)


class Form(models.Model):
    """
    A form to be displayed on Slack and will send a validated input to a
    specific endpoint.
    """

    name = models.CharField(
        max_length=20,
        unique=True,
        help_text="The unique name of this form to serve as a unique key.",
    )

    endpoint = models.URLField(
        null=True,
        blank=True,
        help_text="A URL to hit with the processed and validated form data.",
    )

    token = models.ForeignKey(
        "slackforms.Token",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="A token to send with the endpoint.",
    )

    json_schema = JSONField(
        help_text="A schema for the form data. See docs."
    )
    ui_schema = JSONField(
        null=True,
        blank=True,
        help_text="A schema for the form inputs. See docs."
    )
    data_source = models.URLField(
        blank=True,
        help_text="""
The source of data if an Id is supplied. Variable is passed through to
this template. Use "{id}" to crate the template.
""",
    )

    slash_command = models.CharField(
        max_length=40,
        unique=True,
        blank=True,
        null=True,
        help_text="The slash command for this form (don't include the slash).",
    )

    def __str__(self):
        return self.name

    def get_resonse_url(self):
        """
        Get the proper response_url callback for webhook request data.
        """
        return os.path.join(Settings.ROOT_URL, "callback/")

    def get_prop_attr(self, prop, attr):
        """
        Get a particular attribute of a particular form property.
        """
        return (
            self.json_schema.get("properties", {}).get(prop, {}).get(attr, "")
        )

    def is_prop_number(self, prop):
        """
        Get whether a property is of a number type.
        """
        return self.get_prop_attr(prop, "type") in ["number", "integer"]

    def post_ephemeral(self, text, meta):
        username = meta.get("user", {}).get("id", "")
        channel = meta.get("channel", {}).get("id", "")
        slack("chat.postEphemeral", user=username, channel=channel, text=text)

    def get_form_data(self, id, meta):
        """
        Get starting data from the form's data_source given a particular id.
        """
        if not self.data_source == "" and not id == "":
            url = self.data_source.format(id=id)
            r = requests.get(url=url)
            try:
                return r.json()
            except json.decoder.JSONDecodeError:
                self.post_ephemeral(r.text, meta)
                return False
        else:
            return {}

    def process(self, content):
        """
        Process data from a Slack form.
        """
        output = {}
        for prop, value in content.items():
            if value is not None:
                if self.is_prop_number(prop) and is_float(value):
                    output[prop] = int(value)
                elif isinstance(value, float):
                    output[prop] = float(value)
                elif self.get_prop_attr(prop, "type") == "boolean":
                    output[prop] = bool(value)
                elif self.get_prop_attr(prop, "format") == "date-time":
                    try:
                        date = dateparser.parse(value).isoformat()
                    except AttributeError:
                        date = ""
                    output[prop] = date
                else:
                    output[prop] = value

        return output

    def validate(self, content):
        """
        Validate form data based on a form's json schema and return errors
        in a Slack-friendly structure.
        """
        try:
            validate(content, self.json_schema)
        except exceptions.ValidationError as e:
            errorObj = {"name": "".join(e.path), "error": e.message}
            if errorObj["name"] == "":
                m = re.search("'(.*)' is a required property", e.message)
                errorObj["name"] = m.group(1)
            return errorObj

        return True

    def create_slack_form(self, data, data_id):
        """
        Create a Slack form dictionary from the record's json and ui schemas.
        """
        form = schema_to_form(
            self.name, self.json_schema, self.ui_schema, data
        )
        if data_id and not data_id == "":
            form["state"] = data_id

        return form

    def trigger(self, trigger_id, method="POST", **kwargs):
        """
        Trigger a form action. Either a new form or a DELETE request to the
        form's webhook.
        """
        if method == "POST" or method == "PUT":
            self.post_to_slack(trigger_id, **kwargs)
        if method == "DELETE":
            self.post_to_webhook({}, method, **kwargs)

    def post_to_slack(
        self, trigger_id, data_id="", data={}, meta={}, **kwargs
    ):
        """
        Given starting data and/or an Id to get data from a data_source,
        trigger a new form to open in Slack.
        """
        source_data = self.get_form_data(data_id, meta)

        if source_data is False:
            return

        form_data = {**source_data, **data}  # noqa: E999
        form = self.create_slack_form(form_data, data_id=data_id)
        resp = slack("dialog.open", dialog=form, trigger_id=trigger_id)

        if resp.get("ok", False) is True:
            logger.info(resp)
        else:
            logger.error(resp)

    def post_to_webhook(self, processed_content, method, meta={}, **kwargs):
        """
        Send processed form data (along with some metadata) to the form's
        designated webhook.
        """
        if self.endpoint is None:
            return

        data = processed_content
        meta_data = meta
        meta_data["response_url"] = self.get_resonse_url()
        meta_data["form"] = self.name
        meta_data["token"] = self.token.token if self.token is not None else None
        data["slackform_meta_data"] = json.dumps(meta_data)

        if method == "PUT":
            return requests.put(url=self.endpoint, data=data)
        elif method == "DELETE":
            return requests.delete(url=self.endpoint, data=data)
        else:
            return requests.post(url=self.endpoint, data=data)
