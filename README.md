**Car-Go: Vehicle Rental Management System**

**Overview**
Car-Go is a streamlined, efficient vehicle rental management system designed to simplify the entire process of vehicle rental operations. From managing reservations to processing payments and insurance, Car-Go offers an automated and user-friendly platform for vehicle rental businesses. This system minimizes paperwork, enhances operational efficiency, and provides insightful data for decision-making, ensuring a seamless customer experience and enabling business growth.

**Features**
-Customer Profiles: Manage customer details including rental history and preferences.
-Reservation Management: Easy tracking of vehicle availability, booking, and reservation management.
-Vehicle Management: Keep track of vehicle types, models, and availability.
-Insurance and Payments: Select insurance options and process payments securely.
-Admin Dashboard: Admin users can monitor vehicle status, manage customers, and handle reservations.
-User Interface: End users can easily select rental locations, vehicle types, insurance, and proceed with the payment and booking process.

**System Architecture**
The system is built using a MySQL database for storing customer and reservation data, which is integrated with a Streamlit app for the user interface. The app features:

-Login Page: Directs to two types of users: admin users and end users.
-Admin Interface: Allows admins to interact with the database and manage customer details and reservations.
-Customer Interface: Enables customers to select rental locations, car types, models, insurance options, and make payments.

**Database Design**
The database for Car-Go was designed using an Entity-Relationship Diagram (ERD). Entities and their relationships were identified to ensure proper data flow and integration within the system:

Entities: Customers, Vehicles, Reservations, Insurance, Payments
Attributes: Customer Name, Vehicle Type, Reservation Date, Payment Amount, etc.
The database was implemented in MySQL, ensuring the following:

Efficient storage and retrieval of rental and customer data.
Real-time updates of vehicle availability and reservation status.
