import subprocess

# execute command
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        if output == "":
            return "Command executed, no generated output"
        else:
            return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"
    
def execute_command_detached(command):
    try:
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Command started (detached): {command}"
    except Exception as e:
        return f"Error: {str(e)}"