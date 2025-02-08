# Flight Management Web App

## Overview
This project is a web application designed to manage and optimize flight data for a flight simulator game. The client, a game developer from Spain, aims to create a simulator that realistically replicates real-life flight paths for pilot training. The application processes large-scale flight data from CSV files, allowing for efficient search, retrieval, and modification of flight records.

## Project Goals
The primary objective is to create a web-based flight management system that allows users to:
- Load, search, and modify large-scale flight data efficiently.
- Display flight information accurately to enhance the simulator experience.
- Provide an advanced search function capable of handling partial flight details.
- Ensure secure access control with login and logout functionality.
- Maintain a user-friendly interface for seamless data management.

## Technical Considerations
- **Programming Language:** Python
- **Framework:** Flask (for rapid development and deployment)
- **Data Handling:** CSV file processing for flight information (~7.5 million records from Kaggle’s American Airlines dataset)
- **Security:** User authentication via source code-defined credentials

## Features
### 1. User Authentication
- Secure login/logout system.
- Restricted access to unauthorized users.
- Users must be added manually through the source code.

### 2. Flight Management
- **Search Flights:** Users can search flights based on partial or complete data.
- **Add Flights:** Interface to add new flights to the dataset.
- **Delete Flights:** Functionality to remove unwanted flight records.
- **Cancelled Flights View:** Dedicated section to display cancelled flights.

### 3. Optimized Search Algorithm
- Designed to handle large-scale datasets efficiently.
- Allows keyword-based searches for flight details without requiring full data.
- Improves data retrieval speed compared to traditional methods.

## Implementation Steps
1. Develop and deploy a local web application using Flask.
2. Implement user authentication for secure access.
3. Design and develop HTML/CSS templates for search, add, and delete functions.
4. Implement backend logic for handling large-scale CSV files.
5. Optimize the search algorithm to enhance efficiency.
6. Create a separate interface for cancelled flights.
7. Test and validate the system before deployment.

## Success Criteria
- Web application runs locally and can be transferred to a production server.
- Secure login/logout mechanism implemented.
- Restricted access without authentication.
- Fully functional add, delete, and search features.
- Efficient search functionality for partial flight information.
- Dedicated section for cancelled flights.

## Conclusion
This project delivers a secure and optimized web application that enhances flight data management for a professional flight simulator. By leveraging Python and Flask, the system provides an efficient solution for handling large-scale flight data while maintaining an intuitive and user-friendly interface.

