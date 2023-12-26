 <img src="Pics/folder.svg" width="50" height="50"> >> <img src="Pics/airflow.svg" width="50" height="50"> >> <img src="Pics/microsoft-azure.svg" width="70"  height="50"> >> <img src="Pics/power-bi.svg" width="50" height="50">

# Airflow Project: Data Pipeline with Cloud Azure Database

## Project Overview
Welcome to my Airflow project! This data pipeline project aims to extract, transform, and load data into a Cloud Azure Database. By leveraging the poIr of Airflow, I've automated the entire process, making it efficient and reliable.
<!--![Project Architecture](Pics/architecture.png)
The project architecture consists of three main components: data extraction, data transformation, and data loading. These components work together to ensure a smooth and streamlined data pipeline. -->

## Prepare the environment Apache Airflow in Windows 11 using a Linux VM
I. Ubuntu 22.04
  
-> From Windows Features checkbox Windows Subsystem for Linux

-> Search the store for "Ubuntu"

-> Install Ubuntu 22.04 (it is not necessary to sign in to the store)

-> Launch Ubuntu 22.04

-> Enter a username. This will create a local user account and you will be automatically logged in to Ubuntu 22.04 as this user

-> Enter a password for the user and enter a second time to confirm

-> Update all Ubuntu 22.04 software packages with "sudo apt update && sudo apt upgrade -y"

II. Visual Studio Code:

  Download Visual Studio Code: [here](https://code.visualstudio.com/download)
  
  Python3.10.12
  
-> Open Terminal (shift+`):

    > Ubuntu
    > sudo apt install python3-pip
    > nano ~/.bashrc 
    
-> Add this: AIRFLOW_HOME=/home/your_user_name/airflow then Ctrl+s Ctrl+x

-> Install and run airflow:

    > pip install apache-airflow
    > airflow db init
    > airflow user create -u admin -f admin -l admin -r Admin -e admin@admin.example.com
    > airflow scheduler
    > open another terminal and run "Ubuntu" then "airflow Ibsever"

    
-> To connect with Azure Cloud Database I need to install ODBC package:

     > sudo su 
     > curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
   > #Download appropriate package for the OS version

   > #Choose only ONE of the following, corresponding to your OS version
   > #Ubuntu 22.04

     > curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
     > exit
     > sudo apt-get update
     > sudo ACCEPT_EULA=Y apt-get install msodbcsql18
   > #optional: for bcp and sqlcmd

     > sudo ACCEPT_EULA=Y apt-get install mssql-tools
     > echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
     > echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
     > source ~/.bashrc
   > #optional: for unixODBC development

     > sudo apt-get install unixodbc-dev
    
Here is my dag file [LoadtoAzure.py](dags/LoadtoAzure.py)

## Data Extraction
In the data extraction phase, I retrieve data from various sources, including APIs, databases, and Local folder. I perform data preprocessing and cleansing to ensure high-quality data for further processing.

## Data Transformation
Using Airflow, I implement data transformation tasks that manipulate, filter, and aggregate the extracted data. I leverage custom Python code and Airflow operators to carry out these operations efficiently.

## Data Loading
Once the data is transformed, I load it into the Cloud Azure Database. I establish a secure connection to the database and optimize the loading process for maximum efficiency.

## File Naming Convention
To maintain data integrity, I follow a consistent file naming convention. Each CSV file is named in a way that aligns with its corresponding table in the Azure Database, making it easier to manage and track data.

## Results and Benefits
This project has brought several benefits, including:
- Improved data accessibility and availability
- Automated data pipeline, reducing manual effort
- Enhanced data quality and integrity
- Efficient and scalable data loading into the Cloud Azure Database

## Future Enhancements
Looking ahead, I have exciting plans for future enhancements, such as:
- Incorporating additional data sources for a more comprehensive dataset
- Implementing advanced analytics and visualization capabilities
- Scaling the data pipeline to handle larger volumes of data

## Conclusion
In conclusion, this Airflow project has successfully created a robust data pipeline for extracting, transforming, and loading data into a Cloud Azure Database. I would like to express my gratitude to the Airflow community and the various libraries and resources that supported this project.

## References and Acknowledgments
- Airflow Documentation: [airflow.apache.org](https://airflow.apache.org/)
- Cloud Azure Database Documentation: [docs.microsoft.com/en-us/azure/azure-sql/database](https://docs.microsoft.com/en-us/azure/azure-sql/database)
- Python Documentation: [docs.python.org](https://docs.python.org/)

Feel free to reach out if you have any questions or feedback. Happy exploring!
