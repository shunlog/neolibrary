# Install 

## Pip pagkages
```
pip3 install -r requirements.txt
```

Install the latest py2neo release:
```
pip install git+https://github.com/technige/py2neo.git#egg=py2neo
```

# Run

## Neo4j

Use ongdb-enterprise:

1. Make sure the database directory is in ONGDB/data/
2. Check out if it's the one used in ONGDB/conf/neo4j.conf 
3. Start neo4j with `ONGDB/bin/neo4j start`

## Web app

Start with
```
python3 app.py
```

# Backup

## Backup

Check the variables in the script, then execute:
```
./backup
```

## Restore

Check the variables in the script, then execute:
```
./restore
```

