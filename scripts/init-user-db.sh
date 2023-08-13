#!/bin/bash
set -e
set -u

function create_user_and_database() {
	local database=$1
    local user=$2
    local password=$3

	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	    CREATE USER $user WITH PASSWORD '$password';
	    CREATE DATABASE $database OWNER $user;
	    GRANT ALL PRIVILEGES ON DATABASE $database TO $user;
EOSQL
}

create_user_and_database $BACKEND_DB $BACKEND_USER $BACKEND_PASSWORD
create_user_and_database $ADMIN_DB $ADMIN_USER $ADMIN_PASSWORD
