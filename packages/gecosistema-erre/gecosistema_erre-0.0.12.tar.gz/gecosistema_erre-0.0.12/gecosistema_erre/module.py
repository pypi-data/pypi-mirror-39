#-------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2019 Valerio for Gecosistema S.r.l.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        module.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:
#-------------------------------------------------------------------------------
import sys,os
import subprocess
import re,ast


def Rscript(command, env={}, envAsArgs=True, R_HOME="", R_LIBS_USER="",  verbose=False):
    """
    Rscript -  call  rscript interpreter
            -  we need to retun a JSON string from R script in the stdout
            -  (es: print {"success":"true","data":5}  )
    """

    command = """Rscript --no-save --no-restore --no-site-file --no-init-file "%s" """ % (command)
    environ = os.environ
    if not "R_HOME" in environ:
        environ['R_HOME'] = ""

    if not "R_LIBS_USER" in environ:
        environ['R_LIBS_USER'] =""

    environ['R_HOME'] = R_HOME if R_HOME else environ['R_HOME']
    environ['R_LIBS_USER'] = R_LIBS_USER if R_LIBS_USER else environ['R_LIBS_USER']

    if verbose:
        print("R_HOME=%s"%environ['R_HOME'] )
        print("R_LIBS_USER=%s" % environ['R_LIBS_USER'])

    #add the environ
    for key in env:
        env[key]="%s"%env[key]

    #add the enviton to the command line
    if envAsArgs:
        for key in env:
            command += ' "%s"'%(env[key])
    else:
        #put the environ in the os.environ
        environ.update(env)

    #debug
    if verbose:
        print(command)

    try:
        with open(os.devnull, 'w') as devnull:
            #outdata = subprocess.check_output(command, stderr=devnull).decode('utf-8')
            p = subprocess.Popen(command, env=environ, stdout=subprocess.PIPE)
            stdoutdata, stderrdata = p.communicate()
            stdoutdata = stdoutdata.decode("utf-8").strip("\r\n")
            #split output
            stdoutdata = stdoutdata.split("\r\n")
            if verbose:
                for line in stdoutdata:
                    print(line)
            #takes last line
            data = stdoutdata[-1]
            #remove index of line
            data = re.sub(r'^\[\d+\]\s*','',data)
            #parse into json
            if data!="":
                data = ast.literal_eval(data)
            else:
                data = ""
            return {"succes":True,"data":data}

    except subprocess.CalledProcessError as e:
        return {"success": False, "exception": "%s"% e.output, "returncode": e.returncode}


if __name__ == '__main__':
    print(os.getcwd())
    R_HOME = "d:\\Program Files\\R\\R-3.3.2\\bin"

    env={"date":"2015-06-01","tagname":"Tmed1"}

    scriptname = "D:\\Program Files (x86)\\SICURA\\apps\\iasmhyn\\lib\\R\\LST_krige.r"
    #scriptname= "test.R"
    res =Rscript(scriptname,env,verbose=True)
    print(res)
    #print(type(res))
