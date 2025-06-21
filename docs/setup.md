### Database
Create a postgres cluster
```bash
pg_ctl initdb -D ../db/llm_stock_db
```

Connect to it and create a database and a user
```bash
psql -p 5432 -h 127.0.0.1 -d postgres    
psql (14.15 (Homebrew))
Type "help" for help.
```

```sql
postgres=# CREATE DATABASE llm_stock_db;
CREATE DATABASE
postgres=# CREATE USER write WITH PASSWORD 'Abcd1234';
CREATE ROLE
postgres=# GRANT CONNECT ON DATABASE llm_stock_db TO write;
GRANT
postgres=# GRANT USAGE ON SCHEMA public TO write;
GRANT
postgres=# GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO write;
GRANT
postgres=# ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO write
;
ALTER DEFAULT PRIVILEGES
postgres=# 
```