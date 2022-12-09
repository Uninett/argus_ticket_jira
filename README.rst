argus_ticket_jira
=================

This is a plugin to create tickets in Jira from
`Argus <https://github.com/Uninett/argus-server>`_

Settings
--------

* ``TICKET_ENDPOINT``: ``"https://jira.atlassian.net"`` or link to self-hosted instance, absolute URL
* ``TICKET_AUTHENTICATION_SECRET``: create an `API token <https://id.atlassian.com/manage-profile/security/api-tokens>`_

  ::

    {
        "token": token,
    }

  If you're using a cloud-hosted instance, also add your email address:

  ::

    {
        "token": token,
        "email": email address,
    }

* ``TICKET_INFORMATION``:

  To know which project to create the ticket in the Jira API needs to know
  the project key or id of it. To figure out the project key visit the section
  ``Project Key`` of the `Jira ticket documentation <https://support.atlassian.com/jira-software-cloud/docs/what-is-an-issue/>`_.
  To figure out the project id visit this `guide on how to get the project id <https://confluence.atlassian.com/jirakb/how-to-get-project-id-from-the-jira-user-interface-827341414.html/>`_.

  ::

    {
       "project_key_or_id": project_key_or_id,
    }

  If the tickets should have a different type than ``Task``, optionally add a 
  type.

  ::

    {
       "project_key_or_id": project_key_or_id,
       "type": "Epic"|"Story"|"Task"|"Bug"|"Subtask"|any other ticket type,
    }