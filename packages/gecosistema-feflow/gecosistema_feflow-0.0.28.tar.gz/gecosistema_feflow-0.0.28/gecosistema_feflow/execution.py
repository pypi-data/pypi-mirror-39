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
# Name:        execution.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:
#-------------------------------------------------------------------------------
import sys
from gecosistema_core import *


def findFeflow(tips="c:/Program Files/DHI,c:/Program Files/WASY,c:/Program Files (x86)/WASY"):
    """
    findFeflow - find the feflow executable
    """
    for root in listify(tips,sep=","):
        res = ls(root,".*\/feflow\d\d\w\.exe$",recursive=True)
        if res:
            return res[0]
    return []

def feflow62c(filefem,compressoutput=False,verbose=False):
    """
    feflow62c - run the feflow model
    """
    feflowexe = findFeflow()
    if not feflowexe:
        sys.stderr.write("feflowXXc.exe is not installed or not in PATH\n")
        return False
    workdir = justpath(filefem,2)
    filedac = workdir+"/results/"+forceext(justfname(filefem),"dac")
    env = {
        "feflow62c":findFeflow(),
        "n": cpu_count(),
        "workdir":workdir,
        "filefem":justfname(filefem),
        "filedac":justfname(filedac)
    }
    command = """"{feflow62c}" -threads {n} -ascii -work "{workdir}" -dac "{filedac}" "{filefem}" """
    if verbose:
        print sformat(command,env)
    res = Exec(command,env,precond=[filefem], postcond=[filedac],skipIfExists=True)
    if res:
        if compressoutput:
            return compress(filedac,removesrc=False)

        return filedac

    return False

if __name__ == "__main__":

    filefem = r"D:\Users\vlr20\Projects\GitHub\gecosistema_feflow\gecosistema_feflow\FeFlow\femdata\2015-08-01.fem"
    print feflow62c(filefem)