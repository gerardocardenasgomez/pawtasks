# Pawtasks

This is the repo for the code.

## Running tests

Run `pytest` on the main directory and watch the tests complete.

## Running the app

Run `gunicorn app` on the main directory.

## Using the API

```
curl 127.0.0.1:8000/api/login -XPOST -d '{"username":"<username>", "password":"<password>"}' -H 'Content-type: application/json'
curl 127.0.0.1:8000/api/user -XPOST -H "Content-Type:application/json" -d '{"username":"<username>", "password":"<password>", "email":"<email>"}'
curl 127.0.0.1:8000/api/user -H 'Authentication-Token: <token>'
curl 127.0.0.1:8000/api/tasks -XPOST -H "Authentication-Token: <token>" -H 'Content-Type:application/json' -d '{"title":"<title>", "due_date":"<due_date>", "points":<points_int>, "difficulty":"<difficulty>"}'
curl 127.0.0.1:8000/api/tasks -H 'Authentication-Token: <token>'
```

## Using Docker

```
docker run --restart=always --name pawtaskspsql --net pawtasksdev -p 10.12.0.42:5432:5432 -d -e POSTGRES_PASSWORD=<password> postgres

docker run -it -d --env-file <filepath> -p 10.12.0.42:8000:8000 --net pawtasksdev <img>
```

## Building the Docker images

Run the build command from the parent directory so that the files can be copied into the Docker images.

```
docker build -f docker-app/Dockerfile .
```

## Using Terraform

Requires logging into DockerHub so that you can access the private images.

Create the `terraform.tfvars` files and add the required variables.

```
terraform plan
terraform apply
```
