import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from sql_queries import create_database, create_table_dashboard, dashboard_count, publisher_count, \
    create_table_publisher


def establish_connection(host, port, db, user, password):
    """

    :param host: postgres  host
    :param port: postgres host, default is 5432
    :param db: postgres db
    :param user:
    :param password:
    :return: cur, engine
    """

    # connection for pandas
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()
    cur = None
    # connection for psycopg2 to postgres
    try:
        conn = psycopg2.connect(host=host, database=db, user=user, password=password)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        print("connected to postgres database")
    except psycopg2.Error as e:
        print("error creating connection")
        print(e)

    return cur, engine


def run_sql_query(cur, query):
    """

    :param cur:
    :param query:
    :return:
    """
    try:
        cur.execute(query)
        print(f"query: \n{query} executed successfully")
    except psycopg2.Error as e:
        print(f"Error running: {query}")
        print(e)


def quality_check(cur, query):
    """

    :param cur:
    :param query:
    :return:
    """
    try:
        cur.execute(query)
        result = cur.fetchone()
        print(f"The table {query.split(' ')[-6]} has {result[0]} rows")

    except psycopg2.Error as e:
        print(f"Error running: select from {query.split('')[-5]}")
        print(e)


def process_ga_daily(file, engine):
    """

    :param file:
    :param engine:
    :return:
    """
    # read csv file
    df_ga = pd.read_csv(file, index_col=False)

    # separate the sourceMedium column, to extract the source
    df_ga[["source", "medium"]] = df_ga["ga:sourceMedium"].str.split("/", expand=True)

    # select the needed columns
    columns = ["start_date", "source", "ga:sessions", "ga:organicSearches", "ga:users", "ga:transactions",
               "ga:transactionRevenue", "ga:itemQuantity", "ga:transactionsPerUser"]

    df_dashboard = df_ga[columns]

    # give the columns a more consistent name
    columns_rename = ["start_date", "source", "sessions", "organic_searches", "users", "transactions",
                      "transaction_revenue", "item_quantity", "transactions_per_user"]

    df_dashboard.columns = columns_rename

    # convert string to datetime object
    pd.options.mode.chained_assignment = None  # default='warn'
    df_dashboard["start_date"] = df_dashboard.start_date.astype('datetime64[ns]')

    # insert data into the general_dashboard table
    df_dashboard.to_sql(name="general_dashboard", con=engine, if_exists="append", index=False)


def process_daily_publish(file, engine):
    """

    :param file:
    :param engine:
    :return:
    """
    # read csv file
    df2 = pd.read_csv(file, index_col=False)

    # select the needed the columns
    df_publisher = df2[["date_start", "publisher_platform", "spend"]]

    # convert string to datetime object
    df_publisher["date_start"] = df_publisher.date_start.astype('datetime64[ns]')

    # insert data into the publisher table
    df_publisher.to_sql(name="publisher", con=engine, if_exists="append", index=False)


def main():
    ga_file = "./data/ga_daily.csv"
    publisher_file = "./data/fb_daily_publisher_platform.csv"

    # connect to postgres database
    cur, engine = establish_connection(host="pgdatabase", port="5432", db="postgres", user="root", password="root")

    #### SQL queries #####

    # create_database
    run_sql_query(cur=cur, query=create_database)

    # re-establish_connection to new database company_x
    cur, engine = establish_connection(host="pgdatabase", port="5432", db="company_x", user="root", password="root")

    # create general_dashboard table
    run_sql_query(cur=cur, query=create_table_dashboard)

    # create publisher table
    run_sql_query(cur=cur, query=create_table_publisher)

    #### process and insert data #####

    # process and insert Google Analytics data
    process_ga_daily(file=ga_file, engine=engine)

    # process and insert facebook data
    process_daily_publish(file=publisher_file, engine=engine)

    #### Run data quality check ####

    quality_check(cur=cur, query=dashboard_count)

    quality_check(cur=cur, query=publisher_count)


if __name__ == "__main__":
    main()

# postgresql://root:root@host.docker.internal/company_x
