from django.test import SimpleTestCase, override_settings

from argus.incident.ticket.base import TicketPluginException
from argus_ticket_jira import JiraPlugin


class JiraTicketPluginTests(SimpleTestCase):
    @override_settings(
        TICKET_ENDPOINT="https://example.com/",
        TICKET_AUTHENTICATION_SECRET={"key": "value"},
        TICKET_INFORMATION={"project_key_or_id": "value"},
    )
    def test_import_settings_raises_error_if_token_is_missing_from_ticket_authentication_secret(
        self,
    ):
        jira_plugin = JiraPlugin()

        with self.assertRaises(TicketPluginException):
            jira_plugin.import_settings()

    @override_settings(
        TICKET_ENDPOINT="https://example.com/",
        TICKET_AUTHENTICATION_SECRET={"token": "value"},
        TICKET_INFORMATION={"key": "value"},
    )
    def test_import_settings_raises_error_if_project_key_or_id_is_missing_from_ticket_information(
        self,
    ):
        jira_plugin = JiraPlugin()

        with self.assertRaises(TicketPluginException):
            jira_plugin.import_settings()
