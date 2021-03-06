"""
IP Tracker [Python3]

This is a tool which serves the feature of fetching out information about any IP address (i.e., any computer device that is publically connected to the internet, and we just need the address of it). The tool is written in Python3. This is the CLI version of the tool, and the original version too which is mostly maintained between regular intervals.

Usage :
1. First clone the repository from github mirror of it, using the command 'git clone https://github.com/rdofficial/ip-tracker-py/' [Type these commands in the terminal].
2. Run the script using these commands - 'python3 main.py'

Author : Rishav Das (https://github.com/rdofficial/)
Created on : May 9, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : May 22, 2021

Changes made in last modification:
1. Adding the feature for the users to enter the --no-history argument in order to avoid saving the history to a local file.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the requird functions and modules
try:
    from os.path import dirname
    from sys import argv, platform
    from json import loads, dumps
    from urllib import request
    from datetime import datetime
    import ArgumentParser
except Exception as e:
    # If there are any errors encountered during the importing of the modules, then we display the error on the console screen

    input(f'{red_rev}[ Error : {e} ]{defcol}\nPress enter key to continue...')
    exit()

# Defining the ANSII color codes for colored output
if 'linux' in platform:
    # If the current operating system is linux, then we continue to define the color codes

    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    red_rev = '\033[07;91m'
    yellow_rev = '\033[07;92m'
    defcol = '\033[00m'
else:
    red = ''
    green = ''
    yellow = ''
    blue = ''
    red_rev = ''
    yellow_rev = ''
    defcol = ''

# Declaring some variables that hold the properties of the tool
# ----
# 1. This section includes the declaration of the variables like session_history, etc.
# ----
session_history = []
# ----

def fetchIp(ip = '', save = False):
    """ This function fetches the details of the user provided IP address, also the IP address provided should be of a public server, computer / network system, otherwise the tracking results will be resulting in failure (HTTP:404). The function fetches the information of the user specified IP address from an external API (http://ipinfo.io/). The function takes 1 argument : ip, save. The ip argument is to specify the IP address. The argument 'save' is a flag used to determine whether to save the fetched results to a file on local machine or not. The function prints the fetched data to the console screen and then proceeds with either saving the data or not. """

    # Validating the user specified IP address
    if len(ip) == 0:
        # If the user specified IP address string is empty, then we raise an error

        raise ValueError('The specified IP address value is an empty string.')
    else:
        # If the user specfied IP address is not empty, then we continue the task

        # Sending the HTTP GET request
        response = request.urlopen(f'http://ipinfo.io/{ip}')

        # Checking the response HTTP code
        if response.status == 200:
            # If the response from the API server states no error, then we continue

            # Parsing the contents of the response from JSON format
            response = response.read().decode()
            response = loads(response)

            # Printing the fetched information on the console screen in a more organised form
            for item in response:
                print(f'[{green}#{defcol}] %-25s    :    {yellow}%-25s{defcol}' %(item.upper(), response[item]))

            # Checking if the save flag is specified or not
            if save == False:
                # If the user did not specified (left default as false), then we skip the process

                pass
            else:
                # If the user specifed save flag is not by default, then we continue to execute the task

                # Saving the fetched information to the user specifeid file on the local machine
                response["timestamp"] = datetime.now().timestamp()
                open(save, 'w+').write(dumps(response))

            # Saving into session history
            session_history.append({
                "ip" : ip,
                "timestamp" : datetime.now().timestamp(),
                })
        else:
            # If the response from the API server states any form of error, then we raise the error

            raise SystemError(f'{loads(response.read().decode())["error"]["message"]}')

def main():
    # Displaying some warnings before proceeding to the task
    print(f'[{green}!{defcol}]-----------------{yellow}Note{defcol}-----------------[{green}!{defcol}]\n[{red}1{defcol}] Make sure you are connected to internet.\n[{red}2{defcol}] Make sure the IP address you are looking is a public IP.\n[{red}3{defcol}] If you want to stop the script in the middle, then press CTRL+C key combo.\n')

    # Getting the user entered values from the arguments
    arguments = ArgumentParser.parse(arguments = argv, parameters = ['-i', '--save'], flags = ['--no-history'])

    # Executing the task as per user specified arguments
    if '-i' in arguments:
        # If the user entered IP address via the arguments, then we continue to complete the task

        # Checking for the --save argument
        if '--save' in arguments:
            # If the user mentioned the --save argument, then we continue with the user mentioned file location

            if len(arguments["--save"]) == 0:
                # If the user entered --save argument value is an empty string, then we raise an error

                raise ValueError('Please mention a proper filename to save the output of the fetching. Else, do not use the --save argument.')
            else:
                # If the user entered --save argument value is not an empty string, then we continue the process

                fetchIp(ip = arguments["-i"], save = arguments["--save"])
        else:
            # If the user did not entered the IP address via the arguments, then we continue without saving the fetched details

            fetchIp(ip = arguments["-i"])
    else:
        # If the user did not entered the IP address via the arguments, then we raise an error with a custom message

        raise ValueError('Please properly specify IP address. Check out the "--doc help" argument for more information.')

    # After completing every process, we will save the current session history to the overall history
    if arguments["--no-history"] == False:
        # If the --no-history is not mentioned in the arguments, then only we continue to save the history

        try:
            data = loads(open(f'{dirname(__file__)}/data.json', 'r').read())
        except FileNotFoundError:
            # If the file is not found on the current working directory, then we continue using a blank list as default

            data = {"history" : []}
        finally:
            try:
                # Saving each items from the current session history
                for item in session_history:
                    data["history"].append(item)
                open(f'{dirname(__file__)}/data.json', 'w+').write(dumps(data))
            except:
                # If there are any errors encountered in the process, then we pass it

                pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # If the user presses CTRL+C key combo, then we exit

        exit()
    except Exception as e:
        # If we encounter any error during the process, then we display the error on the console screen

        input(f'{red_rev}[ Error : {e} ]{defcol}\nPress enter key to continue...')
        exit()