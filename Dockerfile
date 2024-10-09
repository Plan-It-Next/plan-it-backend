# Use PostgreSQL 15
FROM postgres:15

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    postgresql-server-dev-15 \
    libreadline-dev \
    zlib1g-dev \
    flex \
    bison \
    libxml2-dev \
    libxslt-dev \
    libssl-dev \
    libxml2-utils \
    xsltproc \
    ccache

# Install Trunk
RUN curl https://get.trunk.io -fsSL | bash

# Clone and install AGE
RUN git clone https://github.com/apache/age.git && \
    cd age && \
    git checkout PG15 && \
    make && \
    make install

# Set environment variables
ENV POSTGRES_PASSWORD=mysecretpassword

# Create initialization script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL\n\
    CREATE EXTENSION age;\n\
    LOAD '\''age'\'';\n\
    SET search_path = ag_catalog, "$user", public;\n\
    SELECT * FROM create_graph('\''my_graph'\'');\n\
EOSQL' > /docker-entrypoint-initdb.d/init-age-db.sh

# Make the script executable
RUN chmod +x /docker-entrypoint-initdb.d/init-age-db.sh

# Expose the PostgreSQL port
EXPOSE 5432

# Use host network
CMD ["postgres", "-c", "shared_preload_libraries=age"]