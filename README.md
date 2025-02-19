## Requirements

- Python 3.12.*
- Docker
- Git

## Clone Githhub repository
**- Create new folder, where you will store the project.**

	 git clone https://github.com/oluchna/hydroponic_system.git

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

