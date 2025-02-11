# Imports
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Set
import logging

logger = logging.getLogger(__name__)


class AccountListComparer:
    """
    A class to handle CSV-based account list comparisons.
    """

    def __init__(self):
        """
        Initialize the comparer with known column structures.
        """
        # Define expected column names for different file types
        self.complex_columns = ['id', 'isCanceled', 'name', 'regionCode']
        self.account_id_column = 'id'  # The specific column we want to compare

    def read_account_list(self, file_path: str) -> Set[str]:
        """
        Read account IDs from a CSV file into a set, handling different file structures.

        Args:
            file_path (str): Path to the CSV file

        Returns:
            Set[str]: Set of account IDs from the file
        """
        try:
            df = pd.read_csv(file_path)

            # Check if this is a complex CSV (with multiple columns)
            if all(col in df.columns for col in self.complex_columns):
                account_ids = df[self.account_id_column]
            else:
                # Assume it's a simple CSV with just account IDs
                # Use the first column regardless of name
                account_ids = df.iloc[:, 0]

            # Convert to strings and remove any leading/trailing whitespace
            return set(account_ids.astype(str).str.strip())

        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise

    def compare_account_lists(self, main_file: str, comparison_files: List[str]) -> Tuple[
        Dict[str, List[str]], List[str]]:
        """
        Compare account IDs between a main CSV file and multiple comparison CSV files.

        Args:
            main_file (str): Path to the main CSV file containing account IDs to check
            comparison_files (list): List of paths to CSV files to compare against

        Returns:
            tuple: (matches_dict, not_found)
                - matches_dict: Dictionary with filename keys and lists of matching account IDs
                - not_found: List of account IDs not found in any comparison file
        """
        # Read the main account list
        main_accounts = self.read_account_list(main_file)

        # Initialize results
        matches_dict: Dict[str, List[str]] = {}
        all_matches: Set[str] = set()

        # Compare with each comparison file
        for comp_file in comparison_files:
            try:
                comp_accounts = self.read_account_list(comp_file)

                # Find matches for this file
                matches = main_accounts.intersection(comp_accounts)

                if matches:
                    matches_dict[Path(comp_file).name] = sorted(list(matches))
                    all_matches.update(matches)

            except Exception as e:
                logger.warning(f"Error processing {comp_file}: {str(e)}")
                continue

        # Find accounts that don't appear in any comparison file
        not_found = sorted(list(main_accounts - all_matches))

        return matches_dict, not_found


def write_results_to_csv(matches_dict: Dict[str, List[str]], not_found: List[str], output_dir: str) -> None:
    """
    Write comparison results to CSV files.

    Args:
        matches_dict (Dict[str, List[str]]): Dictionary of matches per file
        not_found (List[str]): List of accounts not found in any comparison file
        output_dir (str): Directory to write output files
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Write matches for each file
    for filename, accounts in matches_dict.items():
        output_file = output_path / f"matches_{filename}"
        pd.DataFrame(accounts, columns=['id']).to_csv(output_file, index=False)

    # Write not found accounts
    if not_found:
        not_found_file = output_path / "not_found_accounts.csv"
        pd.DataFrame(not_found, columns=['id']).to_csv(not_found_file, index=False)