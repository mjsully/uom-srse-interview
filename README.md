# Repository contents

## Coding task
This directory holds several subdirectories, outlined below:
```
go/ - holds the source code for a query API written in Go.
python/api - holds the source code for a query API written in Python.
python/library - holds the source code for a Python library. 
```
Each directory is packaged into a docker container, also outlined below:
```
ghcr.io/mjsully/ontologies-api:python
ghcr.io/mjsully/ontologies-api:go
ghcr.io/mjsully/ontologies-library:python
```
Docker compose files for each piece of code are included in the relevant subdirectories. 
## Running and querying the API
To run and query either the Python or Go APIs, do the following:
```
cd coding-task/python/api
docker compose up
```
If all is well, the docker image will be pulled from the registry and run according to the compose file. To query, try the following:
```
curl localhost:8000/ontologies/<onto>
```
If you are running the Go API, replace port 8000 with port 8080. Replace `<onto>` with an ontology ID, e.g. 'addicto'. Both APIs will return JSON formatted data. The Python library also has a simple UI, which can be found by running the container and then going to [http://localhost:8000/docs](http://localhost:8000/docs).
## Using the library
A container has been provided to allow one to test the library. You can do this as follows:
```
docker run -it ghcr.io/mjsully/ontologies-library:python python3 ontologies.py --onto <onto>
```
Here, replace `<onto>` with an ontology ID, such as 'addicto'. To use the library in your code, first make sure all dependencies are installed with `pip3 install -r requirements.txt`. Then, import the `ontologies` library into your code, and query the ontology information as follows:
```
ontology_data = ontologies.get_ontology_info(<onto>)
```
Once more, replace `<onto>` with an ontology ID. 
