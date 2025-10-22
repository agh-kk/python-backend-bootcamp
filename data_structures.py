import time
import random
import string
from typing import List, Set, Any, Dict, Union

# --- Task 1 Constants ---
DATA_SIZE = 1_000_000
TARGET_STRING = "NON_EXISTENT_UNIQUE_STRING_TO_SEARCH_FOR_42"

# --- Task 2 Data ---
# Raw website traffic data including user IDs and domains
RAW_DATA = [
    {"user_id": 101, "domain": "example.com"},
    {"user_id": 205, "domain": "api-service.net"},
    {"user_id": 101, "domain": "example.com"},  # Duplicate user
    {"user_id": 312, "domain": "internal-app.org"},
    {"user_id": 205, "domain": "example.com"},
    {"user_id": 404, "domain": "api-service.net"},
    {"user_id": 312, "domain": "internal-app.org"},
]


class PerformanceTester:
    """
    A class designed to encapsulate the logic for generating data and
    testing the performance difference between List (O(n)) and Set (O(1))
    membership checks (Task 1).
    """

    def __init__(self, data_size: int, target: str):
        """Initializes the tester with data size and the target string."""
        self.data_size = data_size
        self.target = target
        self.random_list: List[str] = []
        self.random_set: Set[str] = set()
        self.results = {}

    def _generate_data(self, length: int = 10):
        """Private method to generate the list and set."""
        print(f"Generating {self.data_size:,} random strings...")

        self.random_list = [
            "".join(random.choices(string.ascii_letters + string.digits, k=length))
            for _ in range(self.data_size)
        ]
        self.random_set = set(self.random_list)

    @staticmethod
    def _test_membership(items: Any, target: str) -> float:
        """Static method to time a membership check operation."""
        start_time = time.perf_counter()
        _ = target in items
        end_time = time.perf_counter()
        return end_time - start_time

    def run_tests(self):
        """Executes both the List and Set performance tests."""
        self._generate_data()

        # Test 1: List O(n)
        print("\n--- Task 1: List Performance Test (O(n)) ---")
        list_duration = self._test_membership(self.random_list, self.target)
        self.results["list_duration"] = list_duration
        print(f"List Search Time: {list_duration:.6f} seconds")

        # Test 2: Set O(1)
        print("\n--- Task 1: Set Performance Test (O(1)) ---")
        set_duration = self._test_membership(self.random_set, self.target)
        self.results["set_duration"] = set_duration
        print(f"Set Search Time: {set_duration:.9f} seconds")

    def display_report(self):
        """Presents the final comparison report for Task 1."""
        list_duration = self.results.get("list_duration", 0)
        set_duration = self.results.get("set_duration", 0)

        print("\n--- Task 1: Final Performance Report ---")

        if set_duration > 0 and list_duration > 0:
            speed_ratio = list_duration / set_duration
            print(f"List (O(n)) Time: {list_duration:.6f} s")
            print(f"Set (O(1)) Time: {set_duration:.9f} s")
            print("-" * 30)
            print(
                f"Conclusion: Set lookup was approx. {speed_ratio:,.0f} times faster."
            )
        else:
            print("Task 1 tests did not run or returned zero time.")


# --- Task 2 Function ---


def aggregate_traffic(raw_data: List[Dict[str, Union[int, str]]]) -> Dict[str, int]:
    """
    Aggregates raw traffic data to count the total number of unique users
    for each domain.

    This leverages a dictionary (mapping domain -> set of user IDs) for
    O(1) lookups and set's inherent uniqueness property.
    """

    # Structure: { "domain_name": {user_id_1, user_id_2, ...} }
    # Using a dictionary where the values are sets ensures that duplicate user_ids
    # for the same domain are automatically handled.
    unique_users_per_domain: Dict[str, Set[int]] = {}

    for record in raw_data:
        domain = record["domain"]
        user_id = record["user_id"]

        # Initialize a set for the domain if it doesn't exist
        if domain not in unique_users_per_domain:
            unique_users_per_domain[domain] = set()

        # Add the user ID to the set. Sets only store unique items.
        unique_users_per_domain[domain].add(user_id)

    # Final aggregation: count the size of each set
    result: Dict[str, int] = {
        domain: len(users_set) for domain, users_set in unique_users_per_domain.items()
    }

    return result


if __name__ == "__main__":
    # --- Execute Task 1 (Performance Testing) ---
    tester = PerformanceTester(data_size=DATA_SIZE, target=TARGET_STRING)
    tester.run_tests()
    tester.display_report()

    # --- Execute Task 2 (Data Cleaning and Aggregation) ---
    print("\n" + "=" * 40)
    print("--- Task 2: Data Cleaning and Aggregation ---")

    aggregated_results = aggregate_traffic(RAW_DATA)

    print("\nRaw Data Snippet:")
    for record in RAW_DATA:
        print(f"  - {record}")

    print("\nAggregated Unique User Counts:")
    for domain, count in aggregated_results.items():
        print(f"  {domain:<20}: {count} unique users")

    print("=" * 40)
