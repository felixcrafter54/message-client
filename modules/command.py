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