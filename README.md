# Instructions

## Pip pagkages
```
pip3 install -r requirements.txt
```

## Neo4j

Verify the database in `conf/neo4j.conf`

Run neo4j

``` sh
bin/neo4j start
```

## Flask app

Configure environment variables in .env and .flaskenv

Set a different `SECRET_KEY`

Start with
```
flask run
```
