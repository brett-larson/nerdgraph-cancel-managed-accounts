# Imports
from dotenv import load_dotenv
from get_managed_accounts.api import execute_query, RateLimiter
from get_managed_accounts.api.queries import GET_MANAGED_ACCOUNTS as get
from get_managed_accounts.data import NewRelicAccountsHandler
from get_managed_accounts.utils import setup_logger


# Create logger for the main module
logger = setup_logger(__name__)

def main():
    """
    Main function to execute the core logic of the application.
    :return: None
    """

    logger.info("Starting the application.")

    # Load environment variables
    load_dotenv()

    # Initialize variables
    account_list_result = None
    get_active_account_variables = {"isCanceled": False}
    get_canceled_account_variables = {"isCanceled": True}
    csv_active_filename = 'active_accounts.csv'
    csv_canceled_filename = 'canceled_accounts.csv'


    # Initialize handlers
    accounts_handler = NewRelicAccountsHandler(chunk_size=1000)

    # Rate Limiter function for when required.
    # rate_limiter = RateLimiter(calls_per_minute=2000)
    # rate_limiter.wait_if_needed()


    try:
        logger.info("Executing GraphQL query to get active accounts.")
        account_list_result = execute_query(query=get, variables=get_active_account_variables)
    except Exception as e:
        logger.error(f"Error: {e}")

    try:
        logger.info("Writing active accounts to CSV.")
        accounts_handler.write_accounts_to_csv(csv_active_filename, account_list_result)
    except Exception as e:
        logger.error(f"Error: {e}")


    try:
        logger.info("Executing GraphQL query to get canceled accounts.")
        account_list_result = execute_query(query=get, variables=get_canceled_account_variables)
    except Exception as e:
        logger.error(f"Error: {e}")

    try:
        logger.info("Writing canceled accounts to CSV.")
        accounts_handler.write_accounts_to_csv(csv_canceled_filename, account_list_result)
    except Exception as e:
        logger.error(f"Error: {e}")

    logger.info("Application finished.")

if __name__ == "__main__":
    main()