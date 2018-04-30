# Omaha Mentor for Kids #

This respository consists of the code for Omaha Mentor for kids partnership. Using python the project was developed. 

The primary roles in this system are Admin, Employee and Mentor. 

## Admin ##
   * Has control over all the tables, rights to give access to employee and mentor.
    
## Employee ## 
   * He can search for any student using the search functionality on the home page.
   * He has the ability to create, edit, delete student and mentor profile. 
   * Can create a calendar invite for a mentor to meet the parents and discuss about the students performance.
   * Send SMS reminder to parents regarding the meeting.
    
## Mentor ##
   * Search for the student profile using the search facility
   * Can edit the student report and provide feedback.
   * View the student profile tagged under him.
    
 As part of this project we had the opportunity to implement 5 API's for various purposes.   The following are the list of APIs that we had used and their functionality.
 We have added and additional feature for the employee to make use of the Trello feature to manage tasks.
 
 * Social Auth - **Twitter sign up** for volunteers to enroll and contribute their efforts in monitoring the kids at OMK.
 * **PayPal** - This way donors can contribute funds to OMK, since its a Non-Profit-Organization
 * **GoogleMaps** - We have used the google maps feature thus helping the mentors and donors to locate the school address from their location
 * **Twilio** - Used this API to send text SMS to the regiestered parents number on the twilio site.
 * **Google Calendar** - This API helps the employee to create a invite for the mentor to meet the parents.
 * **Zendesk Chat** - This API helps the customer or user to chat with OMK support staff and get more required details
 
 After downloading the core and before running the project kindly do install the below requirements to run the code easily.
 
  o	Pip install social-auth-app-django  
  o	Pip install Django-paypal  
  o	Pip install geocoder  
  o	Pip install Django-sendsms  
  o	Pip install - -upgrade google-api-python-client  

 
