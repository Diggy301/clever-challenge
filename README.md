# Clever Challenge

## Overview
The Clever Challenge is a technical project that aims to extract data from various Excel files, process the data, and store it in a SQLite database. The project utilizes Docker for containerization, ensuring a consistent environment across different systems.

## Features
- Downloads Zip files containing Excel data.
- Extracts and processes data from the specified sheets of each Excel file.
- Stores the processed data in a SQLite database.
- Easily deployable using Docker.

## How to Run
To build and run the Docker container, use the following commands:

```bash
docker build -t clever -f docker/Dockerfile .
docker run -v $(pwd)/docker/volumes/db_data:/clever/db -it clever
```

## Prerequisities
- Docker installed on your machine.

## Directory Structure
```bash
.
├── docker
│   ├── Dockerfile
│   ├── requirements.txt
│   └── volumes
│       └── db_data
├── main.py
└── README.md
```