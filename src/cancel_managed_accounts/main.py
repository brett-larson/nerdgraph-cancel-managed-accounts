# Imports
from pathlib import Path
from cancel_managed_accounts.utils import setup_logger
from cancel_managed_accounts.data import AccountListComparer, write_results_to_csv

# Create logger for the main module
logger = setup_logger(__name__)

def main():
    """
    Main function to execute the core logic of the application.
    :return: None
    """

    logger.info("Starting the application.")



    # Initialize the account comparer
    comparer = AccountListComparer()

    # Define file paths
    base_path = Path(__file__).parent
    data_path = base_path  / "data" / "csv"
    logger.info(f"Path to location of CSV files: {data_path}")

    # The file with the list of accounts to check
    main_file = data_path / "cancel_account_list_actual.csv"

    # The files to check against (which have the complex structure)
    comparison_files = [
        data_path / "active_accounts.csv",
        data_path / "canceled_accounts.csv"
    ]

    # Run comparison
    try:
        matches, not_found = comparer.compare_account_lists(
            str(main_file),
            [str(f) for f in comparison_files]
        )

        # Print summary
        print("\nComparison Results:")
        for file_name, account_list in matches.items():
            print(f"{file_name}: {len(account_list)} matching accounts")
        print(f"Accounts not found in any file: {len(not_found)}")

        # Write results to CSV files
        output_dir = data_path / "results"
        write_results_to_csv(matches, not_found, str(output_dir))
        print(f"\nResults written to {output_dir}")

    except Exception as e:
        logger.error(f"Error during comparison: {str(e)}")
        raise

    logger.info("Application complete.")


if __name__ == "__main__":
    main()