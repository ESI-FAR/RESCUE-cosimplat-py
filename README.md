# CoSimPlat - Python Version

This README file provides instructions for installing and running the *CoSimPlat - Python Version* software on your local machine. It also includes steps for creating the necessary MySQL database and table. You can use this cosimulation in conjunction to the [CoSimPlat Web Application](https://github.com/ESI-FAR/RESCUE-cosimplat/tree/main) which is there to help you visualize your co-simulation status during a game. 

### How It Works

The *CoSimPlat - Python Version* is a co-simulation framework which uses the so called Long Polling paradigme to enable Event-Based real-time communication among the players exploiting MySQL database​. The whole mechanism is made possible thanks to the standardization of the Payload, ​i.e. a  JSON template containing Meta and Packets. Precisely, the Payload is the total amount of information that is shared between the players at every step, while the Packets are intended as the customizable part of the Payload which has to be agreed a priori by all the players of the cosimulation. 


<img src="https://github.com/user-attachments/assets/c176426c-28df-4abe-bd50-42e9458ece84" alt="Screenshot 2024-11-27 141809" width="40%">

The logic behing this cosimulation platform is simple: the co-simulation leader (always identified with id = 1 in the code) makes the first move (Step 0) and waits until everyone reaches the current step, then proceeds to the next. And so on...



![cosimplat](https://github.com/user-attachments/assets/818d5e87-173c-4f42-944b-224ccd17dda1)


## Prerequisites

Before you begin, ensure you have the following software installed:

## Installation Steps

### 1. Set Up the MySQL Database (on a cloud server or on a local)

Create a database named `cosimplat`.

### 2. Create the `simcrono` Table 

1. With the `cosimplat` database selected, enter the following SQL code to create the `simcrono` table:

    ```sql
    CREATE TABLE simcrono (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simgame_id INT NOT NULL,
    submodel_id INT NOT NULL,
    sim_step INT,  
    payload LONGTEXT NOT NULL,
    state_history LONGTEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

    ```


### 3. Download the CoSimPlat-py Codebase

To download the CoSimPlat-py codebase, follow the steps below:

1. Clone the repository using Git:
   ```bash
   git clone https://github.com/ESI-FAR/RESCUE-cosimplat-py.git


### 4. Setup your co-simulation 

1. Agree on the JSON packet structure with other players: which information would you like to share at every step? 
2. Setup the details: Game Leader (ID = 1) , simulation steps, Your unique ID, MySQL connection details
3. Create an extractor function to retreive the information you need from the JSON payload
4. Fill the *your_simulation()* function with your actual programmatic simulation loop


### 5. Run the Application

Run the main.py and proceed with your co-simulation.

## Troubleshooting

- If you encounter any issues with database connections, ensure that your MySQL service is running ;).


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
