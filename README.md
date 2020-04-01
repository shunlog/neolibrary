### Pip pagkages
```
pip3 install -r requirements.txt
```

Install the latest py2neo release:
```
pip install git+https://github.com/technige/py2neo.git#egg=py2neo
```

### Backup

Cd to ~/.config/Neo4j\ Desktop/Application/neo4jDatabases/.../inst../bin

Backup with:
```
./neo4j-admin backup --backup-dir=/home/awh/backups/library_db --database=neo4j --pagecache=4G
```

Restore:
```
./neo4j-admin restore --from=/home/awh/backups/library_db/neo4j --database=neo4j --force
```

