def get_var(var_name: str):
   with open(".env", "r") as env_file:
       for line in env_file:
           if var_name.upper() + "=" in line:
               value = line.split('=')[1].strip()
               
               return value

def put_var(var_name: str, var_value: str):
    with open(".env", "w") as env_file:
       env_file.write(f"{var_name.upper()}={var_value}\n")
