# multi-useraccount
Users can register as an admin and create an organisation, and add members into their organisations. These members can then login to the organisation.

## Database (Models.py)
| Tables | Description |
| :---:   | :---: | 
| User | Representation of a user with fields for email, name, organization (FK), and role |
| CustomUserManager | Contains method for user creation and permission assignment |
| Meta | Defines custom permissions such as add_members |
| Organisation | Represents an organization |
| CustomUserPermission | Associates permissions with a user |

## Roles
Roles are assigned with custom permissions upon creation.

| Roles | Permissions | Comments |
| :---:   | :---: | :---: |
| Admin | Able to add members into the organisation | First user of the organisation will take on this role |
| Co-Admin | Able to add members into the organisation | Members can be assigned this role to have the same permissions as an Admin |
| Member | Unable to add members into the organisation | Add button should be disabled when login |

### Dummy accounts to test
*They are all part of the same organisation - sianorg*

| Email | Password | Role |
| :---:   | :---: | :---: |
| sian@gmail.com | P@ssword123 | Admin
| sian2@gmail.com | P@ssword123 | Co-Admin |
| sianchild2@gmail.com | P@ssword123 | Member |

## Add members into an organisation
Unable to add members who are admins or members in other organisation, i.e. the email must not exist in the database.

## Session
Upon login, the user email is saved in session and remove upon logout.