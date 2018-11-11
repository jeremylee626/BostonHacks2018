# BostonHacks18
Boston Hacks 2018


To run service, first run "python __init__.py"
Then type in "localhost:5000" into web browser.

Background of this app, currently police get texts about warnings, but they
have one screen that the texts come up on.
They are assigned in order of them coming in, and the only way to get location
is to open the text and read it. This causes the police to sort through
the data mentally/manually, and is time consuming.

On the civilian side, the people might not necessarilly save the police number.
They also might not have the time to get their exact location. Our mobile application
automatically sends a text message and geotags the location.

The message is sent to twilio, which then sends the message to the web application.
The web application determines an address from the geo coordinates of the text.
The application then puts the data on a dashboard with the text, and will
determine priority for the police (example, if multiple tips come in for location A
but only two come in for location B, then location A would be prioritized over location B)

This would allow for more efficient police deployment, and more safety for the public.

Web app located in __init__.py
mobile app in BostonHacks2018
