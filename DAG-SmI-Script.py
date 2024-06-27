import subprocess
import os

def execute_script(filename, script_type, input_data=None):

  if script_type == "python":
    try:
      if input_data:
        with open(os.devnull, 'w') as devnull: 
          process = subprocess.Popen(["python3", filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          output, err = process.communicate(input=input_data.encode())
          return_code = process.wait()
      else:
        process = subprocess.Popen(["python3", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()
        return_code = process.wait()
      if err:
        raise RuntimeError(f"Error running Python script: {err.decode()}")
      return return_code, output
    except FileNotFoundError:
      print(f"Error: Python interpreter not found. Please ensure Python is installed and accessible.")
      return None, None

  elif script_type == "cpp":
    executable_name = os.path.splitext(filename)[0]
    try:
      subprocess.run(["g++", "-o", executable_name, filename])
    except FileNotFoundError:
      print(f"Error: C++ compiler (g++) not found. Please ensure a C++ compiler is installed.")
      return None, None

    if input_data:
      process = subprocess.Popen(["./"+executable_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      output, err = process.communicate(input=input_data.encode())
      return_code = process.wait()
    else:
      process = subprocess.Popen(["./"+executable_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      output, err = process.communicate()
      return_code = process.wait()

    os.remove(executable_name)

    if err:
      raise RuntimeError(f"Error running C++ script: {err.decode()}")
    return return_code, output
  else:
    print("Error: Unsupported script type. Please specify 'python' or 'cpp'.")
    return None, None

python_file = "SMI-Matrix-Generate.py"
cpp_file = "DAG-SmI.cpp"

file_input = input("Please write the dataset path: ")

inp_name = input("Result prefixes: ")

try:
  input_string = f"{file_input}\nLinear\nSMI-Matrix/{inp_name}.mat"
  return_code, output = execute_script(python_file, "python", input_string)
  if return_code == 0:
    print("Python script execution successful!")
    if output:
      print("Python script output:", output.decode())
  else:
    print(f"Python script execution failed with return code: {return_code}")


  input_data = f"SMI-Matrix/{inp_name}.mat\nResults/Graph{inp_name}.txt" 
  return_code, output = execute_script(cpp_file, "cpp", input_data)
  if return_code == 0:
    print("C++ script execution successful!")
    if output:
      print("C++ script output:", output.decode())
  else:
    print(f"C++ script execution failed with return code: {return_code}")

  python_file = "drawGraph.py"

  input_string = f"Results/Graph{inp_name}.txt\nResults/Graph{inp_name}.png"
  return_code, output = execute_script(python_file, "python", input_string)

  if return_code == 0:
    print("Python script execution successful!")
    if output:
      print("Python script output:", output.decode())
  else:
    print(f"Python script execution failed with return code: {return_code}")

except RuntimeError as e:
  print(f"Error: {e}")