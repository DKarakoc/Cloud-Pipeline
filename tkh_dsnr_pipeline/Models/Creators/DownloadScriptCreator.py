import os
import sys
import platform
import re


class DownloadScriptCreator:

    def createDownloadScript(self):
        # TODO: check if the download script already exists.
        python_loc = sys.executable  # location of the python interpreter

        if platform.system() == 'Windows':
            self.createScriptWindows(python_loc)
        elif platform.system() == 'Linux':
            self.createScriptLinux(python_loc)
        else:
            raise RuntimeError("System platform not recognized as Windows or Linux")

    def createScriptWindows(self, python_loc):
        """
        Creates a windows shell script which runs the python download client with a given argument.
        :param python_loc:
        :return:
        """
        script_string = '"' + python_loc + '"' + " " + '"' + os.getcwd() + "/DownloadClient2.py" + '"' + " " + "%*"
        with open(os.getcwd() + "/downloadScript.bat", 'w') as file:
            file.write(script_string)
            file.close()

    def createScriptLinux(self, python_loc):
        """
        Creates a linux shell script which runs the python download client with a given argument.
        :param: python_loc - file path to python
        :return:
        """
        script_string = "#!/bin/bash\n" + python_loc

        linux_script = ""

        print(os.getcwd())

        with open(os.getcwd() + '/downloadScript.sh', 'w') as rsh:
            rsh.write(script_string)
            rsh.write(" ")

        for each in re.split('/', os.getcwd() + "/DownloadClient2.py"):
            if each == '':
                continue
            elif ' ' in each:
                linux_script += "/" + "\"" + each + "\""
            else:
                linux_script += "/" + each

        with open(os.getcwd() + '/downloadScript.sh', 'a') as rsh:
            rsh.write(linux_script)
            rsh.write(" " + '"$@"')
        os.chmod('downloadScript.sh', 0o777)
        rsh.close()
