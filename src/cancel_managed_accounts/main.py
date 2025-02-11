# Imports
from get_managed_accounts.api import execute_query, RateLimiter
from get_managed_accounts.api.queries import GET_MANAGED_ACCOUNTS as get
from get_managed_accounts.data import NewRelicAccountsHandler
from get_managed_accounts.utils import setup_logger
from pathlib import Path
from get_managed_accounts.csv_handlers import AccountListComparer, write_results_to_csv




def main():
    # Initialize the account comparer
    comparer = AccountListComparer()

    # Define file paths
    base_path = Path(__file__).parent
    data_path = base_path / "cancel_managed_accounts" / "data" / "csv"

    # The file with the list of accounts to check
    main_file = data_path / "pantheon_cancel_account_list.csv"

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
        logging.error(f"Error during comparison: {str(e)}")
        raise


if __name__ == "__main__":
    main()