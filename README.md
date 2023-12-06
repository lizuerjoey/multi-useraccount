# multi-useraccount
Users can register as an admin and create an organisation, and add members into their organisations. These members can then login to the organisation.

## Database (Models.py)
| Roles | Permissions | Remarks |
| :---:   | :---: | :---: |
| Admin | Able to add members into the organisation | First user of the organisation will take on this role |
| Co-Admin | Able to add members into the organisation | Members can be assigned this role to have the same permissions as an Admin |
| Member | Unable to add members into the organisation | Add button is disabled when login |

## Roles
Roles are assigned with custom permissions upon creation.

| Roles | Permissions | Remarks |
| :---:   | :---: | :---: |
| Admin | Able to add members into the organisation | First user of the organisation will take on this role |
| Co-Admin | Able to add members into the organisation | Members can be assigned this role to have the same permissions as an Admin |
| Member | Unable to add members into the organisation | Add button is disabled when login |

## Add members into an organisation
Unable to add members who are admins or members in other organisation, i.e. the email must not exist in the database

## Session
Upon login, the user email is save in session and remove upon logout.