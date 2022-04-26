create_table_dashboard = \
    """
CREATE TABLE IF NOT EXISTs general_dashboard (
    id SERIAL PRIMARY KEY,
    start_date TIMESTAMP WITHOUT TIME ZONE, 
    source TEXT, 
    sessions BIGINT,
    organic_searches BIGINT,
    users BIGINT, 
    transactions BIGINT,
    transaction_revenue FLOAT(53),
    item_quantity BIGINT,
    transactions_per_user FLOAT(53)
);
"""

create_table_publisher = \
    """
CREATE TABLE IF NOT EXISTS publisher (
    date_start TIMESTAMP WITHOUT TIME ZONE, 
    publisher_platform TEXT, 
    spend FLOAT(53)
);
"""

create_database = \
    """
    CREATE DATABASE company_x ;
    """

dashboard_count = \
    """
    SELECT COUNT(*)
    FROM general_dashboard ;
    """

publisher_count = \
    """
    SELECT COUNT(*)
    FROM publisher;
    """
