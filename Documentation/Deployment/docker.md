### Prerequisites

 - Docker

### Installation

Run either:

```sudo docker-compose -f docker-compose-dev.yml up```

to initiate the docker containers for development mode.  
It will only be available at the localhost environment and the mysql database can be accessed.  
The ports for the web server would be 81 and for the mysql server 3310.  
Both can be changed in the ```docker-compose-dev.yml``` file.

Or:

```sudo docker-compose -f docker-compose.yml up```

to initiate the docker container for production mode.  
The container will be open to the public on port 80.  
The port can be changed in the ```docker-compose.yml``` file.

In the next step the users plugin will be migrated and a new superadmin will be created.  
The following outputs the login data for the new superadmin.  
This should only be executed after the mysql database is fully loaded, however it can also be called another time to create a new superadmin.  
```docker exec scibib_scibib_1  /bin/sh -c "/var/www/SciBib/createlogin.sh"```  
This information should be saved by copying the console output or by pipeling the output.

## Troubleshooting

Nothing yet.
