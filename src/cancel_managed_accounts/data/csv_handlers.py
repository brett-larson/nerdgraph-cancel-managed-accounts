# Imports
from typing import List, Dict, Generator
import csv
import os
from get_managed_accounts.utils import setup_logger

# Create logger for the module
logger = setup_logger(__name__)

class CSVHandler:
    """
    Generic CSV handler class to process and write data in chunks
    """
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        self.csv_dir = os.path.join(os.path.dirname(__file__), 'csv')

        # Create the csv directory if it doesn't exist
        os.makedirs(self.csv_dir, exist_ok=True)

    def get_csv_path(self, filename: str) -> str:
        """
        Get the full path to a CSV file
        :param filename:
        :return: Full path to the CSV file
        """
        return os.path.join(self.csv_dir, filename)

    def process_in_chunks(self, data: List[Dict]) -> Generator[List[Dict], None, None]:
        """
        Process data in chunks.
        :param data: List of dictionaries
        :return: Generator of data chunks
        """
        for i in range(0, len(data), self.chunk_size):
            yield data[i:i + self.chunk_size]

    def write_chunked_data(self, filename: str, data: List[Dict]):
        """
        Write data to a CSV file in chunks
        :param filename: Name of the CSV file to write
        :param data: List of dictionaries to write
        :return: None
        """
        first_chunk = True

        with open(self.get_csv_path(filename), 'w', newline='') as f:
            for chunk in self.process_in_chunks(data):
                if not chunk:
                    continue

                writer = csv.DictWriter(f, fieldnames=chunk[0].keys())

                if first_chunk:
                    writer.writeheader()
                    first_chunk = False

                writer.writerows(chunk)


class NewRelicAccountsHandler(CSVHandler):
    """
    Handler class to process and write New Relic accounts data.
    """

    @staticmethod
    def flatten_accounts_response(response: Dict) -> List[Dict]:
        """
        Flatten the GraphQL response to get a list of accounts
        :param response: GraphQL response
        :return: List of accounts
        """

        try:
            logger.info("Parsing GraphQL response")
            return response['data']['actor']['organization']['accountManagement']['managedAccounts']
        except (KeyError, TypeError) as e:
            print(f"Error parsing GraphQL response: {e}")
            return []

    def write_accounts_to_csv(self, filename: str, response: Dict):
        """Process and write New Relic accounts data"""
        flattened_data = self.flatten_accounts_response(response)
        if flattened_data:
            self.write_chunked_data(filename, flattened_data)