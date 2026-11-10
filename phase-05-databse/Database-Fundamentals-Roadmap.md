# Phase 5: Databases
## Database Fundamentals: Foundation Roadmap

**Status:** Foundation curriculum planned  
**Purpose:** Learn databases and SQL from the beginning before starting the Phase 5 backend data-layer project.

## Learning approach

We will learn one concept at a time.

For each lesson:

1. **Understand:** Define the concept and the problem it solves.
2. **Demonstrate:** Work through a small, clear example.
3. **Practise:** Write SQL and run it in PostgreSQL using DBeaver or `psql`.
4. **Check:** Explain the result and solve a short exercise.
5. **Advance:** Move forward when understanding is demonstrated.

New technical concepts, SQL syntax, PostgreSQL features, and Django APIs must be explained before the learner is asked to use them. Use official documentation for new topics.

**Important:** Do not begin the main application project while the learner is still acquiring the database foundations. Small exercises are allowed. Build the application after the foundation modules.

---

## Module 1: Database Fundamentals

**Goal:** Understand what databases are and how they fit into a backend application.

1. What is data?
2. What is a database?
3. What problem does a database solve?
4. What is a Database Management System (DBMS)?
5. What is a relational database?
6. What is SQL?
7. Database, table, row, column, and field.
8. How PostgreSQL stores and organizes data.
9. How a backend application communicates with a database.
10. PostgreSQL server, database, schema, and table.

**Practical understanding:** Explain the path from a client request, through a backend application, to a database query and back.

**Exit skills:** Explain the purpose of a database, DBMS, relational database, SQL, PostgreSQL, table, row, and column.

## Module 2: SQL Fundamentals and CRUD

**Goal:** Create and manipulate data directly with SQL.

1. Connecting to PostgreSQL and selecting a database.
2. Creating a database with `CREATE DATABASE`.
3. Creating tables with `CREATE TABLE`.
4. Data types: integers, decimal numbers, text, booleans, dates, and timestamps.
5. Inserting records with `INSERT`.
6. Reading records with `SELECT`.
7. Selecting particular columns.
8. Filtering records with `WHERE`.
9. Updating records with `UPDATE`.
10. Deleting records with `DELETE`.
11. Sorting with `ORDER BY`.
12. Limiting results with `LIMIT` and `OFFSET`.
13. Filtering with `IN`, `BETWEEN`, `IS NULL`, and comparison operators.
14. Pattern matching with `LIKE` and PostgreSQL `ILIKE`.

**Practice:** Create a small database, create tables, insert multiple records, retrieve them, update selected records, and delete selected records. Verify every change with `SELECT`.

**Safety habit:** Learn to inspect the target rows with `SELECT` before running an `UPDATE` or `DELETE`.

**Exit skills:** Independently perform basic create, read, update, and delete operations using SQL.

## Module 3: Table Design, Keys, and Constraints

**Goal:** Design tables that protect data correctness.

1. Choosing appropriate data types.
2. Primary keys.
3. Foreign keys.
4. `NOT NULL` constraints.
5. `UNIQUE` constraints.
6. `DEFAULT` values.
7. `CHECK` constraints.
8. Why constraints belong in the database as well as application validation.
9. One-to-one relationships.
10. One-to-many relationships.
11. Many-to-many relationships and junction tables.
12. Referential actions such as `ON DELETE` and `ON UPDATE`.
13. Database normalization: the problems caused by duplicated data and the basic purpose of 1NF, 2NF, and 3NF.

**Practice:** Design a small relational schema, identify its entities and relationships, create the tables, and test valid and invalid inserts.

**Exit skills:** Choose primary and foreign keys, explain common constraints, and design basic one-to-one, one-to-many, and many-to-many relationships.

## Module 4: Querying Related Data

**Goal:** Retrieve useful information stored across multiple tables.

1. Why related information is stored in separate tables.
2. Table aliases.
3. `INNER JOIN`.
4. `LEFT JOIN`.
5. `RIGHT JOIN` and when it is useful.
6. Joining more than two tables.
7. Aggregate functions: `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX`.
8. `GROUP BY`.
9. `HAVING`.
10. Subqueries.
11. Understanding `NULL` in query results and conditions.

**Practice:** Query related records across the schema created in Module 3. Produce grouped summaries and explain why rows appear or do not appear in each join.

**Exit skills:** Write basic joins, aggregate data, group results, and explain the difference between `WHERE` and `HAVING`.

## Module 5: Transactions and Data Correctness

**Goal:** Understand how databases keep a group of related operations consistent, including when something fails.

1. What is a database transaction?
2. Why multiple SQL statements sometimes belong to one transaction.
3. `BEGIN`, `COMMIT`, and `ROLLBACK`.
4. Atomicity: all operations in a transaction succeed together or are rolled back.
5. The ACID properties: Atomicity, Consistency, Isolation, and Durability.
6. What happens when an operation fails halfway through a multi-step change.
7. Basic isolation-level concepts.
8. What it means for transactions to overlap.
9. A conceptual introduction to conflicting reads and writes.
10. How transaction boundaries affect application correctness.

**Practice:** Perform a multi-step change inside a transaction, deliberately cause a failure, roll it back, and verify the database state. Then commit a successful transaction.

**Scope boundary:** Learn what overlapping transactions and isolation mean, but do not go deeply into race-condition reproduction, row locking, `SELECT FOR UPDATE`, or concurrency-control implementation here. Those are part of the next Concurrency phase.

**Exit skills:** Explain ACID, use basic transactions, and identify which related operations should succeed or fail together.

## Module 6: Working with PostgreSQL

**Goal:** Operate a PostgreSQL database safely at a basic backend-engineering level.

1. PostgreSQL server and client.
2. PostgreSQL cluster, database, schema, and table.
3. Roles and users.
4. Database privileges and least privilege.
5. Connecting with `psql`.
6. Basic `psql` meta-commands.
7. Working with databases and query results in DBeaver.
8. Connection details: host, port, database, username, and password.
9. Basic backup and restore concepts.
10. Common connection and permission errors.

**Practice:** Inspect roles and databases, connect using an application role, inspect permissions, and practise a basic backup/restore workflow in a safe local environment.

**Exit skills:** Connect to PostgreSQL, inspect its structure, distinguish server/client tools, and explain basic database permissions.

## Module 7: Indexes and Query Performance

**Goal:** Understand common causes of slow queries and how to investigate them.

1. What makes a query slow?
2. How PostgreSQL finds matching rows.
3. What an index is and what problem it solves.
4. Common B-tree index use cases.
5. Columns that may benefit from indexes.
6. Why indexes are not free: storage and write overhead.
7. Why adding indexes to every column is not good practice.
8. Reading a basic query plan with `EXPLAIN`.
9. Understanding the purpose of `EXPLAIN ANALYZE`.
10. A basic approach to investigating a slow query.

**Practice:** Compare a query plan before and after adding a suitable index on a practice table. Observe the plan rather than assuming an index must always be used.

**Exit skills:** Explain what an index does, identify sensible candidates, and read basic query-plan output.

## Module 8: Connecting PostgreSQL to Django

**Goal:** Understand how Django models and the ORM interact with the relational database.

1. Django model fields and database column types.
2. How models map to database tables.
3. Migrations: `makemigrations` and `migrate`.
4. How Django creates and changes database schema.
5. Django ORM create, retrieve, update, and delete operations.
6. Model relationships: `OneToOneField`, `ForeignKey`, and `ManyToManyField`.
7. How ORM relationships map to database keys.
8. QuerySets and when queries are executed.
9. `select_related()`.
10. `prefetch_related()`.
11. Aggregation and annotation.
12. Understanding and detecting N+1 queries.
13. Database transactions with `transaction.atomic()`.
14. Inspecting and optimizing ORM-generated SQL.

**Practice:** Use a small Django exercise app connected to PostgreSQL. Compare ORM operations with the SQL concepts already learned.

**Exit skills:** Explain how Django models, migrations, relationships, QuerySets, and transactions map to database behavior.

---

## Foundation completion project

Only after completing the foundation modules, build a small database-backed application from scratch.

The project should require the learner to:

- Identify the data entities and their relationships.
- Design tables, primary keys, foreign keys, and constraints.
- Create and modify tables using migrations or SQL where appropriate.
- Implement CRUD operations.
- Query related data with joins.
- Handle a multi-step write with a transaction.
- Add an index only when there is a reason.
- Inspect a query plan.
- Connect the database to Django and explain what the ORM does.

The project is a learning exercise, not a substitute for understanding the modules.

## Return to the original Backend Engineering Phase 5

After the foundation curriculum and completion project, return to the original Phase 5 objectives:

- PostgreSQL fundamentals for backend engineers.
- Advanced Django ORM: `select_related`, `prefetch_related`, annotations, and query optimization.
- Indexes and query plans at a conceptual level.
- Transactions, atomicity, and isolation levels.
- Refactor the existing API data layer: fix N+1 queries, wrap a multi-step write in a transaction, and add indexes where they matter.

**Original Phase 5 skill target:** Read a slow query, improve it, and reason about transaction boundaries.

**Not yet:** Deep concurrency and locking. Those remain in Phase 6: Concurrency.

---

## Learning progress

Mark a module complete only after the learner has demonstrated the stated exit skills.

- [x] Module 1: Database Fundamentals
- [x] Module 2: SQL Fundamentals and CRUD
- [x] Module 3: Table Design, Keys, and Constraints
- [x] Module 4: Querying Related Data
- [x] Module 5: Transactions and Data Correctness
- [x] Module 6: Working with PostgreSQL
- [x] Module 7: Indexes and Query Performance
- [x] Module 8: Connecting PostgreSQL to Django
- [x] Foundation completion project
- [x] Original Backend Engineering Phase 5 objectives
