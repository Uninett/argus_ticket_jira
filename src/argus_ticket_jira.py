"Allow argus-server to create tickets in Jira"

import logging

from jira import JIRA
from markdownify import markdownify

from argus.incident.ticket.base import (
    TicketClientException,
    TicketCreationException,
    TicketPlugin,
    TicketPluginException,
    TicketSettingsException,
)

LOG = logging.getLogger(__name__)


__version__ = "1.0"
__all__ = [
    "JiraPlugin",
]


class JiraPlugin(TicketPlugin):
    @classmethod
    def import_settings(cls):
        try:
            endpoint, authentication, ticket_information = super().import_settings()
        except TicketSettingsException as e:
            LOG.exception(e)
            raise TicketSettingsException(f"Jira: {e}")

        if "token" not in authentication.keys():
            authentication_error = "Jira: No token can be found in the authentication information. Please update the setting 'TICKET_AUTHENTICATION_SECRET'."
            LOG.error(authentication_error)
            raise TicketSettingsException(authentication_error)

        if "project_key_or_id" not in ticket_information.keys():
            project_key_id_error = "Jira: No project key or id can be found in the ticket information. Please update the setting 'TICKET_INFORMATION'."
            LOG.error(project_key_id_error)
            raise TicketSettingsException(project_key_id_error)

        return endpoint, authentication, ticket_information

    @staticmethod
    def convert_tags_to_dict(tag_dict: dict) -> dict:
        incident_tags_list = [entry["tag"].split("=") for entry in tag_dict]
        return {key: value for key, value in incident_tags_list}

    @staticmethod
    def get_custom_fields(
        ticket_information: dict, serialized_incident: dict, map: dict
    ) -> dict:
        incident_tags = JiraPlugin.convert_tags_to_dict(serialized_incident["tags"])
        custom_fields = {}
        if "custom_fields_set" in ticket_information.keys():
            for key, value in ticket_information["custom_fields_set"].items():
                field_id = map.get(key, None)
                if field_id:
                    custom_fields[field_id] = value

        custom_fields_mapping = ticket_information.get("custom_fields_mapping", {})
        for key, value in custom_fields_mapping.items():
            field_id = map.get(key, None)
            if field_id:
                if type(value) is dict:
                    # Information can be found in tags
                    custom_fields[field_id] = incident_tags[value["tag"]]
                else:
                    # Infinity means that the incident is still open
                    if serialized_incident[value] == "infinity":
                        continue
                    custom_fields[field_id] = serialized_incident[value]

        return custom_fields

    @staticmethod
    def create_client(endpoint, authentication):
        """Creates and returns a Jira client"""
        # different between self hosted and cloud hosted
        # cloud: needs email & api token
        # self: only api token

        try:
            if "email" in authentication.keys():
                client = JIRA(
                    server=endpoint,
                    basic_auth=(authentication["email"], authentication["token"]),
                )
            else:
                client = JIRA(
                    server=endpoint,
                    token_auth=authentication["token"],
                )
        except Exception as e:
            client_error = "Jira: Client could not be created."
            LOG.exception(client_error)
            raise TicketClientException(client_error)
        else:
            return client

    @classmethod
    def create_ticket(cls, serialized_incident: dict):
        """
        Creates a Jira ticket with the incident as template and returns the
        ticket url
        """
        endpoint, authentication, ticket_information = cls.import_settings()

        client = cls.create_client(endpoint, authentication)

        ticket_type = (
            ticket_information["type"]
            if "type" in ticket_information.keys()
            else "Task"
        )

        html_body = cls.create_html_body(serialized_incident=serialized_incident)
        markdown_body = markdownify(html=html_body)

        custom_fields_map = {field["name"]: field["id"] for field in client.fields()}
        custom_fields = cls.get_custom_fields(
            ticket_information=ticket_information,
            serialized_incident=serialized_incident,
            map=custom_fields_map,
        )

        fields = {
            "project": ticket_information["project_key_or_id"],
            "summary": serialized_incident["description"],
            "description": markdown_body,
            "issuetype": ticket_type,
        }
        fields.update(custom_fields)

        try:
            ticket = client.create_issue(fields=fields)
        except Exception as e:
            ticket_error = "Jira: Ticket could not be created."
            LOG.exception(ticket_error)
            raise TicketPluginException(f"{ticket_error} {e}")
        else:
            return ticket.permalink()
