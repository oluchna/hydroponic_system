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

## Testing API
1. Go to ```http://localhost:8000/admin/```

2. Log in with credentials:
- username: admin
- password: SuperAdmin

3. Go to Users section and create new user. 
4. Go to ```http://localhost:8000/swagger/```
5. Log in in /POST/login/ endpoint
![image](https://github.com/user-attachments/assets/4331971b-f7db-48f6-9295-7d8f52fdfb52)
