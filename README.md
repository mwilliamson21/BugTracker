Write a bug tracker application that:

requires logging in, but people who aren't logged in cannot create accounts (don't want any random person to see bugs in your application! Also, don't worry about custom user models. Just use the built-in one.)
has a homepage that shows all tickets, sorted by current status
allows filing tickets
has a ticket detail page
allows assigning tickets to yourself
allows editing tickets
has a page where you can see the current tickets assigned to each user, which tickets that user has filed, and which tickets that user completed
Each ticket should have the following fields:

Title
Time / Date filed
Description
Name of user who filed ticket
Status of ticket (New / In Progress / Done / Invalid)
Name of user assigned to ticket
Name of user who completed the ticket
When a ticket is created, it should have the following settings:

Status: New
User Assigned: None
User who Completed: None
User who filed: Person who's logged in
When a ticket is assigned, these change as follows:

Status: In Progress
User Assigned: person the ticket now belongs to
User who Completed: None
When a ticket is Done, these change as follows:

Status: Done
User Assigned: None
User who Completed: person who the ticket used to belong to
When a ticket is marked as Invalid, these change as follows:

 Status: Invalid
User Assigned: None
User who Completed: None

Run following commands in Terminal:
pipenv install --python=3.8.0
pipenv shell
pipenv install django


python manage.py runserver  
