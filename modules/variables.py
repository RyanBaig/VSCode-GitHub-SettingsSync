class Variables:
    """
    Base class for Environment Variable-related actions.
    """
    def get_var(self, var_name: str) -> str:
        """
        Get the value of a variable from the `.env` file.
        """
        with open(".env", "r") as env_file:
            for line in env_file:
                if var_name.upper() + "=" in line:
                    value = line.split('=')[1].strip()
                    return value

    def put_var(self, var_name: str, var_value: str) -> str:
        """
        Put a variable inside the .env` file.
        """
        with open(".env", "w") as env_file:
            env_file.write(f"{var_name.upper()}={var_value}\n")
