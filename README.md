# CoSimPlat - Python Version

This README file provides instructions for installing and running the *CoSimPlat - Python Version* software on your local machine. It also includes steps for creating the necessary MySQL database and table. You can use this cosimulation in conjunction to the [CoSimPlat Web Application](https://github.com/ESI-FAR/RESCUE-cosimplat/tree/main) which is there to help you visualize your co-simulation status during a game. 

### How It Works

The *CoSimPlat - Python Version* is a co-simulation framework which uses the so called Long Polling paradigme to enable Event-Based real-time communication among the players exploiting SQL database​. The whole mechanism is made possible thanks to the standardization of the Payload, ​i.e. a  JSON template containing Meta and Packets. Precisely, the Payload is the total amount of information that is shared between the players at every step, while the Packets are intended as the customizable part of the Payload which has to be agreed a priori by all the players of the cosimulation. 


<img src="https://github.com/user-attachments/assets/c176426c-28df-4abe-bd50-42e9458ece84" alt="Screenshot 2024-11-27 141809" width="40%">

The logic behing this cosimulation platform is simple: the co-simulation leader (always identified with id = 1 in the code) makes the first move (Step 0) and waits until everyone reaches the current step, then proceeds to the next. And so on...



![cosimplat](https://github.com/user-attachments/assets/818d5e87-173c-4f42-944b-224ccd17dda1)


## Prerequisites

Before you begin, ensure you have the following software installed:

## Installation Steps

### 1. Set Up the MySQL Database (on a cloud server or on a local)

Create a database named `cosimplat`. You can use also PostgreSQL or similar.
You can do that by exploiting Docker.

Starting a MySQL instance:

```shell
docker run --name some-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=cosimplat -d mysql:9.2
```

When you are done use `docker rm -f some-mysql` to stop the container.

Alternative spinning up local sql sesrver you can spin one up using the the devcontainer from  https://github.com/ESI-FAR/RESCUE-cosimplat
.

### 2. Create the `simcrono` Table

0. In mysql console

    ```shell
    docker exec -it some-mysql mysql -p cosimplat
    # Use the password my-secret-pw
    ```

    If you are using the devcontainer you can connect to the db with
    ```shell
    docker exec -it rescue-cosimplat_devcontainer-mariadb-1 mariadb -u user -p cosimplat
    # use userpassword as password
    ```

1. With the `cosimplat` database selected, enter the following SQL code to create the `simcrono` table:

    ```sql
    CREATE TABLE IF NOT EXISTS simcrono (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simgame_id INT NOT NULL,
    submodel_id INT NOT NULL,
    sim_step INT,  
    payload LONGTEXT NOT NULL,
    state_history LONGTEXT,
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

In 3 shells run

<details>
<summary>
python3 main.py 1
</summary>

```shell
Starting long-polling with simulation...
Co-simulation started at step 0 by submodel_id 1.
Running simulation step: 1
Waiting for all players to share data for step 1.
Running simulation step: 1
Waiting for all players to share data for step 1.
Running simulation step: 1
All players have shared data for step 1.
Running simulation step: 2
Waiting for all players to share data for step 2.
Running simulation step: 2
Waiting for all players to share data for step 2.
Running simulation step: 2
All players have shared data for step 2.
Running simulation step: 3
Waiting for all players to share data for step 3.
Running simulation step: 3
Waiting for all players to share data for step 3.
Running simulation step: 3
All players have shared data for step 3.
Running simulation step: 4
Waiting for all players to share data for step 4.
Running simulation step: 4
Waiting for all players to share data for step 4.
Running simulation step: 4
All players have shared data for step 4.
Running simulation step: 5
Waiting for all players to share data for step 5.
Running simulation step: 5
Waiting for all players to share data for step 5.
Running simulation step: 5
All players have shared data for step 5.
Running simulation step: 6
Waiting for all players to share data for step 6.
Running simulation step: 6
Waiting for all players to share data for step 6.
Running simulation step: 6
All players have shared data for step 6.
Running simulation step: 7
Waiting for all players to share data for step 7.
Running simulation step: 7
Waiting for all players to share data for step 7.
Running simulation step: 7
All players have shared data for step 7.
Running simulation step: 8
Waiting for all players to share data for step 8.
Running simulation step: 8
Waiting for all players to share data for step 8.
Running simulation step: 8
All players have shared data for step 8.
Running simulation step: 9
Waiting for all players to share data for step 9.
Running simulation step: 9
Waiting for all players to share data for step 9.
Running simulation step: 9
All players have shared data for step 9.
Running simulation step: 10
Waiting for all players to share data for step 10.
Running simulation step: 10
Waiting for all players to share data for step 10.
Running simulation step: 10
All players have shared data for step 10.
Running simulation step: 11
Waiting for all players to share data for step 11.
Running simulation step: 11
Waiting for all players to share data for step 11.
Running simulation step: 11
All players have shared data for step 11.
Running simulation step: 12
Waiting for all players to share data for step 12.
Running simulation step: 12
Waiting for all players to share data for step 12.
Running simulation step: 12
All players have shared data for step 12.
Running simulation step: 13
Waiting for all players to share data for step 13.
Running simulation step: 13
Waiting for all players to share data for step 13.
Running simulation step: 13
All players have shared data for step 13.
Running simulation step: 14
Waiting for all players to share data for step 14.
Running simulation step: 14
Waiting for all players to share data for step 14.
Running simulation step: 14
All players have shared data for step 14.
Running simulation step: 15
Waiting for all players to share data for step 15.
Running simulation step: 15
Waiting for all players to share data for step 15.
Running simulation step: 15
All players have shared data for step 15.
Running simulation step: 16
Waiting for all players to share data for step 16.
Running simulation step: 16
Waiting for all players to share data for step 16.
Running simulation step: 16
All players have shared data for step 16.
Running simulation step: 17
Waiting for all players to share data for step 17.
Running simulation step: 17
Waiting for all players to share data for step 17.
Running simulation step: 17
All players have shared data for step 17.
Running simulation step: 18
Waiting for all players to share data for step 18.
Running simulation step: 18
Waiting for all players to share data for step 18.
Running simulation step: 18
All players have shared data for step 18.
Running simulation step: 19
Waiting for all players to share data for step 19.
Running simulation step: 19
Waiting for all players to share data for step 19.
Running simulation step: 19
All players have shared data for step 19.
Running simulation step: 20
Waiting for all players to share data for step 20.
Running simulation step: 20
Waiting for all players to share data for step 20.
Running simulation step: 20
All players have shared data for step 20.
Running simulation step: 21
Waiting for all players to share data for step 21.
Running simulation step: 21
Waiting for all players to share data for step 21.
Running simulation step: 21
All players have shared data for step 21.
Running simulation step: 22
Waiting for all players to share data for step 22.
Running simulation step: 22
Waiting for all players to share data for step 22.
Running simulation step: 22
All players have shared data for step 22.
Running simulation step: 23
Waiting for all players to share data for step 23.
Running simulation step: 23
Waiting for all players to share data for step 23.
Running simulation step: 23
All players have shared data for step 23.
Running simulation step: 24
Waiting for all players to share data for step 24.
Running simulation step: 24
Waiting for all players to share data for step 24.
Running simulation step: 24
All players have shared data for step 24.
Running simulation step: 25
Waiting for all players to share data for step 25.
Running simulation step: 25
Waiting for all players to share data for step 25.
Running simulation step: 25
All players have shared data for step 25.
Running simulation step: 26
Waiting for all players to share data for step 26.
Running simulation step: 26
Waiting for all players to share data for step 26.
Running simulation step: 26
All players have shared data for step 26.
Running simulation step: 27
Waiting for all players to share data for step 27.
Running simulation step: 27
Waiting for all players to share data for step 27.
Running simulation step: 27
All players have shared data for step 27.
Running simulation step: 28
Waiting for all players to share data for step 28.
Running simulation step: 28
Waiting for all players to share data for step 28.
Running simulation step: 28
All players have shared data for step 28.
Running simulation step: 29
Waiting for all players to share data for step 29.
Running simulation step: 29
Waiting for all players to share data for step 29.
Running simulation step: 29
All players have shared data for step 29.
```
</details>

<details>
<summary>
python3 main.py 2
</summary>

```shell
Starting long-polling with simulation...
Co-simulation started at step 0 by submodel_id 2.
SQL Error: 1364 (HY000): Field 'state_history' doesn't have a default value
^CTraceback (most recent call last):
  File "/home/stefanv/git/esi-far/RESCUE-cosimplat-py/main.py", line 259, in <module>
    long_poll_with_simulation(steps)
  File "/home/stefanv/git/esi-far/RESCUE-cosimplat-py/main.py", line 126, in long_poll_with_simulation
    time.sleep(polling_interval)
KeyboardInterrupt

(venv) stefanv@ID14300:~/git/esi-far/RESCUE-cosimplat-py$ python3 main.py 2
Starting long-polling with simulation...
Running simulation step: 0
Waiting for all players to share data for step 0.
Co-simulation started at step 0 by submodel_id 2.
Running simulation step: 1
Waiting for all players to share data for step 1.
Running simulation step: 1
Waiting for all players to share data for step 1.
Running simulation step: 1
All players have shared data for step 1.
Running simulation step: 2
Waiting for all players to share data for step 2.
Running simulation step: 2
Waiting for all players to share data for step 2.
Running simulation step: 2
All players have shared data for step 2.
Running simulation step: 3
Waiting for all players to share data for step 3.
Running simulation step: 3
Waiting for all players to share data for step 3.
Running simulation step: 3
All players have shared data for step 3.
Running simulation step: 4
Waiting for all players to share data for step 4.
Running simulation step: 4
Waiting for all players to share data for step 4.
Running simulation step: 4
All players have shared data for step 4.
Running simulation step: 5
Waiting for all players to share data for step 5.
Running simulation step: 5
Waiting for all players to share data for step 5.
Running simulation step: 5
All players have shared data for step 5.
Running simulation step: 6
Waiting for all players to share data for step 6.
Running simulation step: 6
Waiting for all players to share data for step 6.
Running simulation step: 6
All players have shared data for step 6.
Running simulation step: 7
Waiting for all players to share data for step 7.
Running simulation step: 7
Waiting for all players to share data for step 7.
Running simulation step: 7
All players have shared data for step 7.
Running simulation step: 8
Waiting for all players to share data for step 8.
Running simulation step: 8
Waiting for all players to share data for step 8.
Running simulation step: 8
All players have shared data for step 8.
Running simulation step: 9
Waiting for all players to share data for step 9.
Running simulation step: 9
Waiting for all players to share data for step 9.
Running simulation step: 9
All players have shared data for step 9.
Running simulation step: 10
Waiting for all players to share data for step 10.
Running simulation step: 10
Waiting for all players to share data for step 10.
Running simulation step: 10
All players have shared data for step 10.
Running simulation step: 11
Waiting for all players to share data for step 11.
Running simulation step: 11
Waiting for all players to share data for step 11.
Running simulation step: 11
All players have shared data for step 11.
Running simulation step: 12
Waiting for all players to share data for step 12.
Running simulation step: 12
Waiting for all players to share data for step 12.
Running simulation step: 12
All players have shared data for step 12.
Running simulation step: 13
Waiting for all players to share data for step 13.
Running simulation step: 13
Waiting for all players to share data for step 13.
Running simulation step: 13
All players have shared data for step 13.
Running simulation step: 14
Waiting for all players to share data for step 14.
Running simulation step: 14
Waiting for all players to share data for step 14.
Running simulation step: 14
All players have shared data for step 14.
Running simulation step: 15
Waiting for all players to share data for step 15.
Running simulation step: 15
Waiting for all players to share data for step 15.
Running simulation step: 15
All players have shared data for step 15.
Running simulation step: 16
Waiting for all players to share data for step 16.
Running simulation step: 16
Waiting for all players to share data for step 16.
Running simulation step: 16
All players have shared data for step 16.
Running simulation step: 17
Waiting for all players to share data for step 17.
Running simulation step: 17
Waiting for all players to share data for step 17.
Running simulation step: 17
All players have shared data for step 17.
Running simulation step: 18
Waiting for all players to share data for step 18.
Running simulation step: 18
Waiting for all players to share data for step 18.
Running simulation step: 18
All players have shared data for step 18.
Running simulation step: 19
Waiting for all players to share data for step 19.
Running simulation step: 19
Waiting for all players to share data for step 19.
Running simulation step: 19
All players have shared data for step 19.
Running simulation step: 20
Waiting for all players to share data for step 20.
Running simulation step: 20
Waiting for all players to share data for step 20.
Running simulation step: 20
All players have shared data for step 20.
Running simulation step: 21
Waiting for all players to share data for step 21.
Running simulation step: 21
Waiting for all players to share data for step 21.
Running simulation step: 21
All players have shared data for step 21.
Running simulation step: 22
Waiting for all players to share data for step 22.
Running simulation step: 22
Waiting for all players to share data for step 22.
Running simulation step: 22
All players have shared data for step 22.
Running simulation step: 23
Waiting for all players to share data for step 23.
Running simulation step: 23
Waiting for all players to share data for step 23.
Running simulation step: 23
All players have shared data for step 23.
Running simulation step: 24
Waiting for all players to share data for step 24.
Running simulation step: 24
Waiting for all players to share data for step 24.
Running simulation step: 24
All players have shared data for step 24.
Running simulation step: 25
Waiting for all players to share data for step 25.
Running simulation step: 25
Waiting for all players to share data for step 25.
Running simulation step: 25
All players have shared data for step 25.
Running simulation step: 26
Waiting for all players to share data for step 26.
Running simulation step: 26
Waiting for all players to share data for step 26.
Running simulation step: 26
All players have shared data for step 26.
Running simulation step: 27
Waiting for all players to share data for step 27.
Running simulation step: 27
Waiting for all players to share data for step 27.
Running simulation step: 27
All players have shared data for step 27.
Running simulation step: 28
Waiting for all players to share data for step 28.
Running simulation step: 28
Waiting for all players to share data for step 28.
Running simulation step: 28
All players have shared data for step 28.
Running simulation step: 29
Waiting for all players to share data for step 29.
Running simulation step: 29
Waiting for all players to share data for step 29.
Running simulation step: 29
All players have shared data for step 29.
```
</details>

<details>
<summary>
python3 main.py 3
</summary>

```shell
Starting long-polling with simulation...
Running simulation step: 0
Waiting for all players to share data for step 0.
Running simulation step: 0
All players have shared data for step 0.
Running simulation step: 1
Waiting for all players to share data for step 1.
Running simulation step: 1
Waiting for all players to share data for step 1.
Running simulation step: 1
All players have shared data for step 1.
Running simulation step: 2
Waiting for all players to share data for step 2.
Running simulation step: 2
Waiting for all players to share data for step 2.
Running simulation step: 2
All players have shared data for step 2.
Running simulation step: 3
Waiting for all players to share data for step 3.
Running simulation step: 3
Waiting for all players to share data for step 3.
Running simulation step: 3
All players have shared data for step 3.
Running simulation step: 4
Waiting for all players to share data for step 4.
Running simulation step: 4
Waiting for all players to share data for step 4.
Running simulation step: 4
All players have shared data for step 4.
Running simulation step: 5
Waiting for all players to share data for step 5.
Running simulation step: 5
Waiting for all players to share data for step 5.
Running simulation step: 5
All players have shared data for step 5.
Running simulation step: 6
Waiting for all players to share data for step 6.
Running simulation step: 6
Waiting for all players to share data for step 6.
Running simulation step: 6
All players have shared data for step 6.
Running simulation step: 7
Waiting for all players to share data for step 7.
Running simulation step: 7
Waiting for all players to share data for step 7.
Running simulation step: 7
All players have shared data for step 7.
Running simulation step: 8
Waiting for all players to share data for step 8.
Running simulation step: 8
Waiting for all players to share data for step 8.
Running simulation step: 8
All players have shared data for step 8.
Running simulation step: 9
Waiting for all players to share data for step 9.
Running simulation step: 9
Waiting for all players to share data for step 9.
Running simulation step: 9
All players have shared data for step 9.
Running simulation step: 10
Waiting for all players to share data for step 10.
Running simulation step: 10
Waiting for all players to share data for step 10.
Running simulation step: 10
All players have shared data for step 10.
Running simulation step: 11
Waiting for all players to share data for step 11.
Running simulation step: 11
Waiting for all players to share data for step 11.
Running simulation step: 11
All players have shared data for step 11.
Running simulation step: 12
Waiting for all players to share data for step 12.
Running simulation step: 12
Waiting for all players to share data for step 12.
Running simulation step: 12
All players have shared data for step 12.
Running simulation step: 13
Waiting for all players to share data for step 13.
Running simulation step: 13
Waiting for all players to share data for step 13.
Running simulation step: 13
All players have shared data for step 13.
Running simulation step: 14
Waiting for all players to share data for step 14.
Running simulation step: 14
Waiting for all players to share data for step 14.
Running simulation step: 14
All players have shared data for step 14.
Running simulation step: 15
Waiting for all players to share data for step 15.
Running simulation step: 15
Waiting for all players to share data for step 15.
Running simulation step: 15
All players have shared data for step 15.
Running simulation step: 16
Waiting for all players to share data for step 16.
Running simulation step: 16
Waiting for all players to share data for step 16.
Running simulation step: 16
All players have shared data for step 16.
Running simulation step: 17
Waiting for all players to share data for step 17.
Running simulation step: 17
Waiting for all players to share data for step 17.
Running simulation step: 17
All players have shared data for step 17.
Running simulation step: 18
Waiting for all players to share data for step 18.
Running simulation step: 18
Waiting for all players to share data for step 18.
Running simulation step: 18
All players have shared data for step 18.
Running simulation step: 19
Waiting for all players to share data for step 19.
Running simulation step: 19
Waiting for all players to share data for step 19.
Running simulation step: 19
All players have shared data for step 19.
Running simulation step: 20
Waiting for all players to share data for step 20.
Running simulation step: 20
Waiting for all players to share data for step 20.
Running simulation step: 20
All players have shared data for step 20.
Running simulation step: 21
Waiting for all players to share data for step 21.
Running simulation step: 21
Waiting for all players to share data for step 21.
Running simulation step: 21
All players have shared data for step 21.
Running simulation step: 22
Waiting for all players to share data for step 22.
Running simulation step: 22
Waiting for all players to share data for step 22.
Running simulation step: 22
All players have shared data for step 22.
Running simulation step: 23
Waiting for all players to share data for step 23.
Running simulation step: 23
Waiting for all players to share data for step 23.
Running simulation step: 23
All players have shared data for step 23.
Running simulation step: 24
Waiting for all players to share data for step 24.
Running simulation step: 24
Waiting for all players to share data for step 24.
Running simulation step: 24
All players have shared data for step 24.
Running simulation step: 25
Waiting for all players to share data for step 25.
Running simulation step: 25
Waiting for all players to share data for step 25.
Running simulation step: 25
All players have shared data for step 25.
Running simulation step: 26
Waiting for all players to share data for step 26.
Running simulation step: 26
Waiting for all players to share data for step 26.
Running simulation step: 26
All players have shared data for step 26.
Running simulation step: 27
Waiting for all players to share data for step 27.
Running simulation step: 27
Waiting for all players to share data for step 27.
Running simulation step: 27
All players have shared data for step 27.
Running simulation step: 28
Waiting for all players to share data for step 28.
Running simulation step: 28
Waiting for all players to share data for step 28.
Running simulation step: 28
All players have shared data for step 28.
Running simulation step: 29
Waiting for all players to share data for step 29.
Running simulation step: 29
Waiting for all players to share data for step 29.
Running simulation step: 29
All players have shared data for step 29.
```
</details>

## Troubleshooting

- If you encounter any issues with database connections, ensure that your MySQL service is running ;).


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
