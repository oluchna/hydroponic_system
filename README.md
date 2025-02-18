## Requirements

- Python 3.12.*
- Docker

## Building image
**Building the application image**

    docker build -t hydroponicsystem .
    
## Application lifecycle
**Starting the application**

    docker-compose up -d
    
**Stopping the application**

    docker-compose down
**Accessing the Swagger documentation**
Swagger documentation can be accessed via below URL

	http://localhost:8000/swagger/