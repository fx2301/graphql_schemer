# GraphQL Schemer

Derives the schema from a GraphQL endpoint given a curl statement.

# Setup

```bash
git clone git@github.com:fx2301/graphql_schemer.git
cd graphql_schemer
pip install -r requirements.txt
```

# Usage

```bash
python3 graphql_schemer.py --schema-file schema.graphql curl <curl options>
```

# How it works

Right now, all this does is make an introspection query. The idea is to accumulate a schema from valid queries, and perhaps also fuzz for schema discovery.