# Multi-Domain Intelligence Platform

## Project Description
This project is a Multi-Domain Intelligence Platform built using Streamlit. It allows users to securely log in and manage information across multiple domains, including Cyber Security, Data Science, and IT Operations. The system combines structured data storage, interactive dashboards, and a simple AI assistant to help users analyse and understand their data more easily.

## Features

## Cyber Security Dashboard
The Cyber Security dashboard helps users manage and analyse security incidents. It includes:
- Total number of recorded security incidents
- Breakdown of incidents by severity (High, Medium, Low)
- Visualization of incidents by incident type
- Table view of incidents with key fields such as severity, status, and incident type
- Easy CRUD operations to add, update, and delete incidents



## Data Science Dashboard
The Data Science dashboard focuses on dataset management and overview analytics. It includes:
- Total number of datasets and overall dataset size
- Visualization showing datasets grouped by category
- Tabular view displaying all dataset metadata
- Ability to add, update, and remove dataset records
- Quick insights without needing manual data inspection



## IT Operations Dashboard
The IT Operations dashboard is designed to manage IT support tickets efficiently. It includes:
- Overview of total tickets and their current status
- Charts showing ticket distribution by priority level
- Ticket status tracking (Open, In Progress, Resolved, Closed)
- Category-based ticket analysis (Hardware, Software, Network, Security)
- Detailed table view of all IT tickets



## Security Features (Hashing and Encryption)
User security is a key part of this system. The following measures are implemented:
- User passwords are never stored in plain text
- Passwords are hashed using the bcrypt hashing algorithm
- A unique salt is generated for each password before hashing
- Even if the database is compromised, original passwords cannot be recovered
- Secure authentication process during login and registration



## How It Works
1. The user registers or logs into the system through the Streamlit interface.
2. Login credentials are securely hashed and verified using the database.
3. After authentication, the user can access different dashboards.
4. User actions (add, update, delete, view data) are handled by the service layer.
5. The service layer interacts with the SQLite database.
6. Results are sent back to the Streamlit interface as tables, charts, or AI responses.



