class User:
    def __init__(self, username: str, user_email: str):
        self._username = username
        self._user_email = user_email
        self._is_active = True

    def get_username(self):
        return self._username

    def get_user_email(self):
        return self._user_email

    def set_email(self, new_email: str):
        if "@" in new_email:
            self._user_email = new_email
        else:
            raise ValueError("Invalid email address")

    def deactivate(self):
        """Deactivate the user (used by external code as user.deactivate())."""
        self._is_active = False

    def get_is_active(self):
        """Return whether the user is active (used by UserStore)."""
        return self._is_active


class UserStore:
    """
    Manages a collection of User objects, adhering to the Single Responsibility Principle.
    """

    def __init__(self):
        """
        Initializes the private dictionary to store User objects.
        """
        # Key: username (str), Value: User object
        self._users = {}

    def add_user(self, user_obj: User):
        """
        Adds a User object to the store, using the username as the key.
        """
        username = user_obj.get_username()
        if username in self._users:
            print(f"⚠️ User '{username}' already exists in the store.")
        else:
            self._users[username] = user_obj
            print(f"➕ User '{username}' added to the store.")

    def get_user(self, username: str) -> User | None:
        """
        Retrieves a user object by username or returns None if not found.
        """
        return self._users.get(username)

    def list_active_users(self) -> list[str]:
        """
        Returns a list of usernames for all currently active users using a list comprehension.
        """
        active_usernames = [
            username
            for username, user_obj in self._users.items()
            if user_obj.get_is_active()  # Calls the getter method
        ]
        return active_usernames


if __name__ == "__main__":
    print("--- Task C: Execution and Testing ---")

    # Prepare test users
    user1 = User("alice_k", "alice@company.com")
    user2 = User("bob_s", "bob@company.org")
    invalid_user = User("no_at", "no_at")  # intentionally missing '@' in email

    # Test Setter Method
    print("\n--- Testing Setter ---")
    user1.set_email("new.alice@company.net")  # Should succeed
    try:
        user1.set_email("justabasicstring")  # Should fail
    except ValueError as e:
        print(f"Invalid email provided: {e}")

    # 2. Create a UserStore object
    store = UserStore()

    # 3. Add users to the store
    print("\n--- Adding Users ---")
    store.add_user(user1)
    store.add_user(user2)
    store.add_user(invalid_user)

    # 4. Deactivate a user
    print("\n--- Deactivating User ---")
    user1.deactivate()

    # 5. List active users and print the result
    print("\n--- Listing Active Users ---")
    active_users = store.list_active_users()
    print(f"List of Active Usernames: {active_users}")

    # Expected Result: ['bob_s', 'no_at'] (since 'alice_k' was deactivated)
