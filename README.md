# Sales Dashboard

Sales Dashboard is a web application designed to provide insightful analytics on sales data. It includes a backend service, a frontend interface, and a CLI for seeding sample data.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/) for managing multi-container applications.

### Installation & Execution

To start the application, run the following command:

```sh
docker compose up
```

To run the application in detached mode (without logs):

```sh
docker compose up -d
```

### Seeding Sample Data

To populate the database with sample data, follow these steps:

1. Access the backend container:

   ```sh
   docker compose exec -it backend bash
   ```

2. Run the CLI command to generate sample data:

   ```sh
   python cli.py --categories 10 --products 20 --orders 70
   ```

This command will create:

- 10 categories
- 20 products
- 70 orders

### Frontend Access

The frontend runs on port `80`. Open your browser and visit:

```
http://localhost
```
