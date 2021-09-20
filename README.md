# Doctor's Assistant
#### Video Demo: https://youtu.be/wAkkCh9gr38
#### Description:

This is a web application built with Flask, SQLite, Bootstrap, and JavaScript. It is designed for medical workers and allows them to create, update and share patients' data.
Apart from storing general information about a person like their gender, age, race, the application keeps track of diseases, allergies, surgical operations, immunizations,
and medical tests that a patient had in the past, as well as medications that were used for the treatment of illnesses. A user can also make virtual records of encounters
with a patient describing their complaints and professional assessment of the claims. All of this constitutes a patient's medical history which can be accessed and, if necessary,
updated by any user of the application.

Application.py stores the code which runs on the server: different routes that process data passed through the forms. The deletion, edition, and insertion of data into a database also happens here.
Helpers.py contains two additional functions which are run on the server if certain conditions are met. The "apology" function displays a template with an error message if a user does something that
is not allowed, like sending the form with empty fields. Function "login_required" checks that a user is logged in before displaying a particular route.
Requirements.txt file specifies what python packages are required to run the project.
Medical_history.db is a file that stores the database.

"Templates" folder keeps HTML templates for various routes that a user can visit. For example, the "patient.html" template will be displayed if a user visits a page of a particular patient. It contains
several tables, each representing a specific section of a patient's medical history: allergies, diseases, etc. There are also separate templates for routes where you can search for a patient or a doctor.
The "layout.html" template contains a navigation bar and a footer which can be seen in every route. Some templates, like "diseases.html", "allergies.html", and "immunization_history", also have scripts
that send AJAX requests to a server without refreshing the whole page upon form data submission. They are used for adding medications which a patient took to treat their illnesses.

"Static" folder contains images for a landing page and several other files that are necessary for styling. Different browsers have different default stylesheets where fonts, margins, and other properties
are set. Reset.css erases all these default settings. This is necessary for the application to look the same in all browsers. Styles.css contains some custom styles that I wrote for HTML elements:
headers, buttons, tables, etc. Finally, scripts.js stores functions that check that forms input fields are correctly filled in by a user. If a field is empty or has data in the wrong format, the message
with a warning will appear, and a user won't be able to proceed. My application uses double form validation: first on the client-side when validation functions are run in the browser, and then on the
server-side when the data is already sent to a server. The validation on the server side is necessary because a user can bypass browser validation by switching off scripts attached to a page.

Another essential thing to note is that users can see patients' data even if other users made the records of these patients, but they can not delete or edit such entries.
The deletion or edition is only allowed for the encounters that the user made.




