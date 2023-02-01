# argus_ticket_jira

This is a plugin to create tickets in Jira from [Argus](https://github.com/Uninett/argus-server)

## Settings

* `TICKET_ENDPOINT`: `"https://jira.atlassian.net"` or link to self-hosted instance, absolute URL
* `TICKET_AUTHENTICATION_SECRET`: Create an [API token](https://id.atlassian.com/manage-profile/security/api-tokens)

    ```
    {
        "token": token,
    }
    ```

    If you're using a cloud-hosted instance, also add your email address:

    ```
    {
        "token": token,
        "email": email address,
    }
    ```

* `TICKET_INFORMATION`: 
    Projekt key or id (obligatory)

    To know which project to create the ticket in the Jira API needs to know
    the project key or id of it. To figure out the project key visit the
    section `Project Key` of the
    [Jira ticket documentation](https://support.atlassian.com/jira-software-cloud/docs/what-is-an-issue/).

    To figure out the project id visit this [guide on how to get the project id](https://confluence.atlassian.com/jirakb/how-to-get-project-id-from-the-jira-user-interface-827341414.html/)


    ```
    {
        "project_key_or_id": project_key_or_id,
    }
    ```

    Task type (optional)

    If the tickets should have a different type than `Task` this need to be declared.

    ```
    {
        "type": "Epic"|"Story"|"Task"|"Bug"|"Subtask"|any other ticket type,
    }
    ```

    Custom fields (optional)

    There are two ways of automatically filling custom fields:
    
    1. Custom fields that are always the same, independent of the incident. 
    These will be set in `custom_fields_set` with the name of the custom field as key and the fixed value as value.

  
        ```
        {
            "custom_fields_set" : {
                "name_of_custom_field": set_value,
            }
        }
        ```

    2. Custom fields that are filled by attributes of the Argus incident. These are set in `custom_fields_mapping` with the name of the custom field as key and the name of the attribute as it is returned by the API  as value (e.g. `start_time`). If the information can be found in the tags the value consists of a dictionary with `tag` as the key and the name of the tag as the value (e.g. {"tag": "host"}).

        ```
        {
            "custom_fields_mapping" : {
                "name_of_custom_field": attribute_of_incident,
                "name_of_custom_field": {"tag": name_of_tag},
            }
        }
        ```

    A completely filled `TICKET_INFORMATION` could look like this:

        ```
        {
            "project_key_or_id": "AT",
            "type": "Bug",
            "custom_fields_set" : {
                "source": "Argus",
            },
            {
            "custom_fields_mapping" : {
                    "start": "start_time",
                    "host": {"tag": "host"},
                }
            }

        }
        ```
