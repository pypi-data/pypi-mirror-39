#-------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2013 Luzzi Valerio for Gecosistema S.r.l.
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
# Name:        specific db connector
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     30/10/2013
#-------------------------------------------------------------------------------
import sys,re
from gecosistema_core import *
from gecosistema_database import *
from gecosistema_spatial import *
from gecosistema_krige import *
from bilancio_idrologico import Calcola_infiltrato
from execution import *

def normalize(text,c=" "):
    """
    normalize - Remove all duplicate characters keeping just one
    """
    return re.sub(r'\s+', ' ', text)
#-------------------------------------------------------------------------------
#   stol - compressed string to list
#-------------------------------------------------------------------------------
def stol(text,sep =" "):
    res= []
    text = normalize(text,sep).replace("-"+sep,"-")
    items = text.split(sep)

    for item in items:
        if "-" in item:
            (a,b) = item.split("-")
            a = int(a.strip())
            b = int(b.strip())
            for j in range(a,b+1):
                res.append("%s"%j)
        else:
            res.append(item)
    return res

class FeFlowDB(SpatialDB):

    #FeFlowConst
    FeFloWConst ={
            "head_data":176,
            "vx_data":9996,
            "vy_data":9997,
            "vz_data":9998,
            "concentration_data":9995,
            "acceleration_data_flow":9994,
            "acceleration_data_mass":9993,
            "acceleration_data_flow":9992,
            "acceleration_data_heat":9991,
            "flow_cbc_data":9990,
            "mass_cbc_data":9989,
            "heat_cbc_data":9988
    }

    Vars = {
                "LIVELLO PIEZOMETRICO":0,
                "LIVELLO PIEZOMETRICO DA MODELLO":0,
                "THETA SUOLO 2":0,
                "THETA SUOLO 3":0,
                "THETA SUOLO 4":0,
                "DELTA THETA SUOLO 2":0,
                "DELTA THETA SUOLO 3":0,
                "DELTA THETA SUOLO 4":0,
                "CORRECT SWAT ET1 SUOLO 2":0,
                "CORRECT SWAT ET1 SUOLO 3":0,
                "CORRECT SWAT ET1 SUOLO 4":0,
                "ET0 HARGREAVES SAMANI":0,
                "RICARICA SUOLO 2":0,
                "RICARICA SUOLO 3":0,
                "RICARICA SUOLO 4":0,
                "TEMPERATURA MIN":0,
                "TEMPERATURA MED":0,
                "TEMPERATURA MAX":0,
                "PRECIPITAZIONE":0
           }

    location = {"Parametri Bilancio Idrologico":0,"P1":0,"P2":0,"P3":0,"P4":0,
    "P5":0,"P6":0,"P7":0,"P8":0,"P9":0,"P10":0,"N1":0,"N2":0,"N3":0,"N4":0,
    "N5":0,"N21":0,"N20":0,"P15":0,"N17":0,"P16":0,"P14":0,"N19":0,"N18":0,
    "N8":0,"N7":0,"N6":0,"I1":0,"I2":0,"N9":0,"N12":0}

    def __init__(self):
        """
        Constructor
        """
        print os.getcwd()
        print "-------"
        SpatialDB.__init__(self,"feflow.sqlite")
        #Load the functions
        self.conn.create_function("GetValueAt",3,GetValueAt)

        self.setup()

    def setup(self):

        self.execute("""
        CREATE TABLE IF NOT EXISTS [FeFlowData] (
          [Date] NUM,
          [location_id] INT,
          [type_id] INT,
          [value] REAL,
          CONSTRAINT [] PRIMARY KEY ([Date], [location_id], [type_id]));

        CREATE INDEX IF NOT EXISTS [idx_FeFlowData_Date] ON [FeFlowData] ([Date]);

        CREATE INDEX IF NOT EXISTS [idx_FeFlowData_location_id] ON [FeFlowData] ([location_id]);
        """)

        alias = self.attach("sicura.sqlite","sicura")
        self.attached=[alias]

        #RETRIEVE VARIABLES
        for varname in self.Vars.keys():
            self.Vars[varname] = self.execute("""
            SELECT ID FROM sicura.[type] WHERE tagname='{tagname}';
            """,{"tagname":varname},outputmode="scalar")

        for varname in self.location.keys():
            self.location[varname] = self.execute("""
            SELECT ID FROM sicura.[location] WHERE point ='{varname}';
            """,{"varname":varname},outputmode="scalar")


    def seasondate(self,date):
        if strftime("%m",date) in ("03","04","05"):
            return "1900-03-01"
        if strftime("%m",date) in ("06","07","08"):
            return "1900-06-01"
        if strftime("%m",date) in ("09","10","11"):
            return "1900-09-01"
        if strftime("%m",date) in ("12","01","02"):
            return "1900-12-01"


    def close(self,verbose=False):
        if verbose:
            print "detaching databases...."
        for databasename in self.attached:
            self.detach(databasename)
        SqliteDB.close(self,verbose)

    def log(self,text):
        filelog = "FeFlowSvc.log"
        text  = strftime("%H:%M:%S:   ",now())+text
        print text
        strtofile(text+"\n",filelog,True)

    def FeFlowType(self,type_id):
        if type_id==self.Vars["LIVELLO PIEZOMETRICO"]:
            return 8
        else:
            return type_id

    def importCOOR(self,filetpl):
        """
        Import the 2D (x,y) coordinates of a slice
        """
        start_acq = False
        xy =[]
        with open(filetpl,"rb") as stream:
            line = normalize(stream.readline().replace("\t"," "))
            while line:
                if line.upper().startswith("COOR"):
                    line = normalize(stream.readline().replace("\t"," "))
                    start_acq= True

                if start_acq and line.strip("\t\r\n ").replace("_","").isalnum() and not line.isdigit():
                        break

                if start_acq:
                    xy += line.split(",")

                line = normalize(stream.readline().replace("\t"," "))

        xy = [item.strip() for item in xy if len(item.strip())>0]
        x = xy[:len(xy)/2]
        y = xy[len(x):]
        xy = [(x[j],y[j]) for j in range(len(x))]
        return xy

    def importELEV(self,filetpl,np_2d):
        """
        importELEV of nodes
        """
        queue =""
        startacq=False
        values =[]
        slicen = 1
        env = {"tablename":juststem(filetpl)}
        counter =  0
        with open(filetpl,"r") as stream:
            line,queue = self.readFeFlowline(stream,queue)
            line = normalize(line.strip())
            while line:

                if line.startswith("ELEV_I"):
                    startacq=True
                elif startacq and line.startswith("STATELEV"):
                    break
                elif startacq:
                    if len(listify(line))==1 and isint(line):
                        slicen = int(line)
                    else:
                        value,line = line.split(" ",1)
                        nodes = stol(line," ")
                        values = [((slicen-1)*(np_2d) + int(id),value,slicen) for id in nodes]
                        #values = [(id,value,slicen) for id in nodes]
                        self.executeMany("""INSERT OR REPLACE INTO [{tablename}](ID,Z,slice) VALUES(?,?,?);""",env,values,commit=False)

                line,queue = self.readFeFlowline(stream,queue)
                line = normalize(line.strip())
        self.commit()


    def __toFLOW_I_BC__(self,Date,verbose= False):
        """
        Le condizioni al contorno sono quelle di Oggi
        che derivano dall'interpolazione delle misure odierne
        L'interpolazione rimane stabile fino alla seguente campagna di misure
        Per cui vado a prendere le condizioni al contorno nel giorno
        piu vicino ad oggi
        2.2.7 FLOW_I_BC
        The flow boundary conditions are stored in the following format:

        FLOW_I_BC
        for (bc_type = MIN_flow_bc_type; bc_type <= MAX_flow_bc_type; bc_type++) {
            if (boundary_conditions_with_this_bc_type_exist) {
                bc_type bc_value_list       bc_node_list
            }
        }
        """
        type_id= self.Vars["LIVELLO PIEZOMETRICO"]
        arguments ={
                        "type_id":type_id,
                        "Date":strftime("%Y-%m-%d",Date),
                        "Yesterday":strftime("%Y-%m-%d",yesterday(Date)),
                        "oneMonthAgo":strftime("%Y-%m-%d",yesterday(Date,30))}

##        #Testo se esistono le condizioni al contorno in data Date
##        sql = """
##        SELECT COUNT(*)
##            FROM [FeFlowView] Fs
##        WHERE Date = '{Date}'
##        AND type_id={type_id}
##        AND BC
##        AND NOT value IS NULL
##        """

        #Numero delle misure reali nella campagna odierna
        sql = """
        SELECT count(*)
            FROM sicura.[Ts] Ts
		WHERE Date='{Date}'
    		AND Ts.type_id={type_id}
            AND Ts.location_id>1000000
            AND NOT Ts.value IS NULL;
        """
        R = self.execute(sql,arguments,outputmode="scalar")

        #Se non esistono prendo le condizioni al contorno del giorno piu' vicino ad oggi
        # ... ma vado indietro fino ad un mese altrimenti prendo i valori stagionali
        if R<20:
            sql = """
            SELECT Date FROM [FeFlowView] Fs
                WHERE BC AND  type_id = {type_id}
                AND Date BETWEEN '{oneMonthAgo}' AND '{Yesterday}'
                AND NOT value IS NULL
                GROUP BY Date HAVING Count(*) > 7000
                ORDER BY Date DESC LIMIT 1;
            """

            FindDate = self.execute(sql,arguments,verbose= verbose,outputmode="scalar")

            if FindDate:
                Date = strftime("%Y-%m-%d",FindDate)
            else:
                #Se non ci sono condizioni al contorno nell'intorno di un mese prendo quelle stagionali
                self.log("Se non ci sono condizioni al contorno nell'intorno di un mese prendo quelle stagionali")
                Date = self.seasondate(Date)

                #Ottenuta la data recupero le condizioni
                sql = """
                    SELECT type_id,value,location_id
                    FROM [FeFlowSeasonalAverage]
                    WHERE Date = '{Date}'
                    AND   type_id={type_id}
                    AND NOT value IS NULL
                    ORDER BY type_id,location_id;
                """

                arguments ={"type_id":type_id,"Date":Date}
                sql = sformat(sql,arguments)
                cur = self.execute(sql,arguments,verbose=verbose)
                return  self.__toFeFlowValues__(cur)

        #Ottenuta la data recupero le condizioni
        sql = """
            SELECT type_id,value,Fs.location_id
            FROM [FeFlowView] Fs
            WHERE BC AND type_id={type_id}
            AND Date = '{Date}'
            AND NOT value IS NULL
            ORDER BY type_id,location_id;
        """

        arguments ={"type_id":type_id,"Date":Date}
        sql  =sformat(sql,arguments)
        cur = self.execute(sql,arguments,verbose=verbose)
        res = self.__toFeFlowValues__(cur)
        return res

    def __toINIT_I_FLOW__(self,Date):
        """
        Le condizioni iniziali sono quelle di ieri
        che derivano dalla simulazione di ieri (.dac)
        2.2.8 INIT_I_FLOW
        INIT_I_FLOW
        LOOP_OF_head_ini_levels_FROM_MINIMUM_TO_MAXIMUM {

            head_ini_level node_list

        }
        """
        Date        =  strftime("%Y-%m-%d",Date)
        Yesterday   =   strftime("%Y-%m-%d",yesterday(Date))

        type_id= self.Vars["LIVELLO PIEZOMETRICO"]

        env = {"type_id":type_id,"Date":Yesterday}

        #Detect if there's a simulation ready for yesterday else we use seasonal data
        sql = """SELECT COUNT(*) FROM [FeFlowData] Fs WHERE Date = '{Date}' AND type_id = {type_id} AND NOT value IS NULL;"""
        if self.execute(sql,env,outputmode="scalar")>7000:
            sql = """
                SELECT value,location_id
                FROM [FeFlowView] Fs
                WHERE Date = '{Date}'
                AND type_id = {type_id}
                AND NOT value IS NULL
                ORDER BY location_id;
            """
        else:
            #Parto con condizioni iniziali nulle
            sql = """
                SELECT '0' as value,id as location_id
                FROM [FeFlowView]
                ORDER BY location_id;
            """
            #O Meglio parto dalle medie annuali salvate in AnnualAverage on date 1900-01-01
            sql = """
                SELECT value,location_id
                FROM [FeFlowAnnualAverage]
                ORDER BY location_id;
            """
        cur = self.execute(sql,env)
        res = self.__toFeFlowValues__(cur)
        return res

    def __toFeFlowValues__(self,cursor):
        """
        Generate a list type,value,nodelist
        """
        res=""
        for row in cursor:

            if len(row)==3:
                (type_id,value,node) = row
                res+="       %d  %21.14e\r\n\t\t   %s \r\n"%(self.FeFlowType(type_id),float(value),node)
            elif len(row)==2:
                (value,node) = row
                res+="  %21.14e\t%s \r\n"%(float(value),node)
            else:
                pass

        return res.rstrip("\r\n")

    def normalize(self,text,c=" "):
        """
        normalize - Remove all duplicate characters keeping just one
        """
        res = text.replace(c*2,c)
        while len(res)<len(text):
            text = res
            res = text.replace(c*2,c)
        return res.strip(c)

    def CreateTemplateFromFEM(self,filefem, filetpl=""):
        print "Acquiring..%s"%filefem
        filetpl = filetpl if filetpl else forceext(filefem,"tpl")
        copymode = True
        with open(filefem,"r") as stream:
            out = open(filetpl,"w")
            line = stream.readline()
            while line:
                if line.strip().upper().startswith("FLOW_I_BC"):
                    out.write(line)
                    out.write("$(FLOW_I_BC)\n")
                    copymode = False
                if line.strip().upper().startswith("INIT_I_FLOW"):
                    out.write(line)
                    out.write("$(INIT_I_FLOW)\n")
                    copymode = False
                elif line.strip().upper().startswith("MAT_I_FLOW"):
                    out.write(line)
                    copymode=True
                else:
                    if copymode:
                        out.write(line)
                line= stream.readline()
            out.close()
        return filetpl

    def GenerateFemFromTemplate(self,Date, workdir, filetpl, verbose= True):

        Date =  strftime("%Y-%m-%d",Date)


        #filetpl = "sicura36_ascii.tpl"

        mkdirs(workdir+"/femdata")
        filefem = workdir+"/femdata/%s.fem"%Date


        text = filetostr(filetpl)

        if verbose:
            self.log( "Retriving soil infiltration in meters")
        sql = """SELECT (value/1000) FROM sicura.[Ts] WHERE Date='{date}' AND type_id='{type_id}';"""
        SOIL2 = self.execute(sql,{"date":Date,"type_id":self.Vars["RICARICA SUOLO 2"]},outputmode="scalar")
        SOIL3 = self.execute(sql,{"date":Date,"type_id":self.Vars["RICARICA SUOLO 3"]},outputmode="scalar")
        SOIL4 = self.execute(sql,{"date":Date,"type_id":self.Vars["RICARICA SUOLO 4"]},outputmode="scalar")

        #Attenzione risolvi in caso di mancanza dati
        if (SOIL2,SOIL3,SOIL4) == (None,None,None):
             (SOIL2,SOIL3,SOIL4) = (0,0,0)

        text = text.replace("$(SOIL2)","%g"%SOIL2)
        text = text.replace("$(SOIL3)","%g"%SOIL3)
        text = text.replace("$(SOIL4)","%g"%SOIL4)

        self.log("FLOW_I_BC")
        FLOW_I_BC=self.__toFLOW_I_BC__(Date)
        if not FLOW_I_BC:
            self.log( "__toFLOW_I_BC__:Non ci sono le condizioni al contorno.")
            return False
        text = text.replace("$(FLOW_I_BC)",FLOW_I_BC)
        self.log("INIT_I_FLOW")
        INIT_I_FLOW = self.__toINIT_I_FLOW__(Date)
        if not INIT_I_FLOW:
            self.log( "__toINIT_I_FLOW__: Non ci sono le condizioni iniziali.")
            return False
        text = text.replace("$(INIT_I_FLOW)",INIT_I_FLOW)
        strtofile(text,filefem)
        return filefem

    def importMODEL(self,filefem, force = False, epsg = 3857):
        """
        importModel - import the tpl model into a database table
        """
        filetpl = "./template/%s"%(forceext(juststem(filefem),"tpl"))
        print os.getcwd()
        print filetpl
        mkdirs(justpath(filetpl))

        if isfile(filetpl) and not force:
            print("The file %s already exists so no change on existing FeFlowModel model."%filetpl)
        else:
            filetpl = self.CreateTemplateFromFEM(filefem,filetpl)
            modelname =juststem(filetpl)
            env ={
                "modelname":modelname,
                "epsg":epsg
            }

            sql = """
            DROP VIEW  IF EXISTS [FeFlowView];
            DROP TABLE IF EXISTS [{modelname}];
            CREATE TABLE IF NOT EXISTS [{modelname}](
              [ID] NUM PRIMARY KEY,
              [X] FLOAT,
              [Y] FLOAT,
              [Z] FLOAT,
              [slice] INTEGER,
              [BC] NUM DEFAULT 0,
              [F]  FLOAT DEFAULT 0,
              --[categoria] TEXT,
              [update]    TEXT);
            CREATE INDEX IF NOT EXISTS [idx_on_{modelname}_slice] ON [{modelname}] ([slice]);
            SELECT AddGeometryColumn('{modelname}','geometry',{epsg},'POINT',2);
            """
            self.execute(sql,env,verbose=False)

            np,ne,nbn= self.importDIMENS(filetpl)

            # Import all nodes ID and Z
            xy = self.importCOOR(filetpl)
            np_2d =len(xy)
            nslices = np/np_2d

            env["np_2d"] = np_2d
            self.importELEV(filetpl,np_2d)

            #update X,Y
            xyid = []
            for k in range(nslices):
                #print "slice# ",k
                for j in range(len(xy)):
                    xyid.append((xy[j][0],xy[j][1], k*np_2d+(j+1) ))  #1-based feflow id model

            self.executeMany("""UPDATE [{modelname}] SET X=?,Y=? WHERE ID=?;""",env,xyid)

            #Update the geometry
            self.execute("""UPDATE [{modelname}] SET [geometry] = MakePoint(X,Y,{epsg});""",env)

            #update BC
            self.updateBC(filefem,filetpl)

            #update m50
            #self.execute("""UPDATE [{modelname}] SET [categoria]='m50' WHERE SLICE=1 AND ID IN (SELECT a.ID FROM [{modelname}] a,[{modelname}] b WHERE a.slice=1 AND distance(a.[geometry],b.[geometry])<=50);""",env)

            #Update Kriging nodes / Fixed node
            self.updateFromShape(forceext(filefem,"shp"),"update")

            #Update the FelowModelView
            sql = """
            DROP VIEW IF EXISTS [FeFlowView];
            CREATE VIEW [FeFlowView] AS
            SELECT Fs.Date,Fs.location_id,Fs.type_id,Fs.value,L.BC,L.Slice,L.X,L.Y,[update]
            FROM [FeFlowData] Fs
            INNER JOIN [{modelname}] L On L.[id] = Fs.location_id;

            -- FeFlowModel View
            DROP VIEW IF EXISTS [FeFlowModel];
            CREATE VIEW [FeFlowModel] AS
            SELECT * FROM [{modelname}];
            """
            self.execute(sql,env)

            #export to shape
            #self.exportModelToShape(modelname,epsg)


    def importCLASS(self,filename):
        text = filetostr(filename)
        text = textbetween(text,"CLASS","DIMENS")
        text = text.replace("\r\n"," ").replace("\n"," ")
        text= normalize(text).split(" ")[2:-1]
        (ic1,ic2,proj,ndm,n_layers,ic0,save_fsize_rreal,save_fsize_creal,dontcare) = text[:9]
        res = [ic1,ic2,ndm,n_layers]
        res = [int(item) for item in res]
        return res

    def importDIMENS(self,filename):
        text = filetostr(filename)
        text = textbetween(text,"DIMENS","SCALE")
        text = text.replace("\r\n"," ").replace("\n"," ")
        text= normalize(text).split(" ")[1:-1]
        (np, ne ,nbn, numb_dt, icrank ,upwind ,obs ,optim, phreatic, nwca, np_cor,
        adaptive_mesh, special_fem_process_id, sorption_type ,reaction_type,dispersion_type) = text[:16]
        res = [np,ne,nbn]
        res = [int(item) for item in res]
        return res

    def importTIME(self,filename):
        text = filetostr(filename)
        text = textbetween(text,"\n","\$")
        text = text.replace("\r\n","").replace("\n","").rstrip("$")
        from dateutil import parser
        return parser.parse(text)

    def updateBC(self,filefem,filetpl):
        queue =""
        startacq=False
        env = {"modelname": juststem(filetpl)}
        with open(filefem,"r") as stream:
            line,queue = self.readFeFlowline(stream,queue)
            line = normalize(line.strip())
            NODES = []
            while line:

                if line.startswith("FLOW_I_BC"):
                    startacq=True
                elif startacq and line.strip("\t\r\n ").replace("_","").isalnum() and not line.isdigit():
                    break
                elif startacq:

                    type_id,value,line = line.split(" ",2)
                    nodes = stol(line," ")
                    nodes = [(int(node),) for node in nodes]
                    NODES += nodes

                line,queue = self.readFeFlowline(stream,queue)
                line = normalize(line.strip())

        self.executeMany("""UPDATE [{modelname}] SET BC=1 WHERE ID=?;""",env,NODES )


    def updateFromShape(self,fileshp,fieldname):
        """
        updateFromShape - read from shapefile
        """
        fileshp = forceext(fileshp,"shp")
        layername =str(juststem(fileshp))
        env ={"layername":layername,"fieldname":fieldname}
        #self.execute("""ALTER TABLE [{layername}] ADD COLUMN [{fieldname}] TEXT;""",env)
        dataset = ogr.OpenShared(fileshp)
        if dataset:
            layer = dataset.GetLayer(layername)
            for feature in layer:
                env["value"] =  feature.GetField(fieldname)
                env["NODE"]  =  feature.GetField("NODE")
                env["F"]     =  feature.GetField("F")
                if env["value"]:
                    sql = """UPDATE [{layername}] SET [{fieldname}] = '{value}',[F] = {F} WHERE [ID] = '{NODE}';"""
                    self.execute(sql,env,verbose= False)

        dataset = None

    def importINIT_I_FLOW(self,filename,Date,type_id):
        queue =""
        startacq=False
        tablename = juststem(filename)
        with open(filename,"r") as stream:
            line,queue = self.readFeFlowline(stream,queue)
            line = normalize(line.replace("\t"," ").replace("\n","").strip())
            while line:
                if line.startswith("INIT_I_FLOW"):
                    startacq=True
                elif startacq and line.strip("\t\r\n ").replace("_","").isalnum() and not line.isdigit():
                    break
                elif startacq:
                    value,line = line.split(" ",1)
                    nodes = stol(line," ")
                    env ={"tablename":tablename}
                    values = [(strftime("%Y-%m-%d",Date),node,type_id,value) for node in nodes]
                    self.executeMany("""INSERT OR REPLACE INTO [{tablename}](Date,location_id,type_id,value) VALUES(?,?,?,?);""",env,values,commit=False)

                line,queue = self.readFeFlowline(stream,queue)
                line = normalize(line.replace("\t"," ").replace("\n","").strip())
            self.commit()

    def readFeFlowline(self,stream,queue):

        if len(queue)>0:
            line = queue
        else:
            line = stream.readline()
        nextline = line
        lookahead = True
        while line and lookahead:
            line=stream.readline()
            if line.startswith("\t\t"):
                nextline+=line
            else:
                lookahead = False
                queue=line
        nextline= nextline.replace("\r\n","\n").replace("\n\t\t"," ")
        return (nextline,queue)

    def importOUTPUTTimeStep(self,Date,workdir):
        #3.2.4 Results data block format
        #3.2.4.1 General Structure of the data bloc
        res ={}

        Date= strftime("%Y-%m-%d",Date)
        filename = workdir+"/results/%s.dac"%Date

        ic1,ic2,ndm,n_layers = self.importCLASS(filename)
        np,ne,nbn = self.importDIMENS(filename)


        is_3D_problem = (ndm==3)
        is_mass_transport = (ic1==0)
        is_thermohaline_transport =(ic1==8)
        is_heat_transport = (ic1==5)
        is_unconfined = False
        is_slice1_free_movable =True
        exist_cbc_of_flow = (False)
        exist_cbc_of_mass = (False)
        exist_cbc_of_heat = (False)
        numb_slices = 0

        #Starts line with $ but ignore $ -1 and $  0
        text   = filetostr(filename)

        re_int   = r'\d+'
        re_float = r'([+-]?\d+(?:\.\d+)?(?:[eE][+-]\d+)?)'

        matches =  re.finditer(sformat('\$\s+{int},\s*{float}\n((\s*{float},?){12}\n*){{m}}',{"int":re_int,"float":re_float,"m":np/12}),text,re.MULTILINE|re.DOTALL)
        for match in matches:
            pass
        if match:
            text =  match.group(0)
            values = text.split(",")[1:-1]
            values  = [val(item.strip()) for item in values]
            res["LIVELLO PIEZOMETRICO"] = values
        else:
            return False

##        idx1   = text.index("FBCCEND\n$     0")
##        text   = text[idx1+len("FBCCEND\n"):]
##        text   = textbetween(text,"FBCCEND\n$","       8").replace("\r\n","\n")
##        text   = text.split("\n")
##        text   = [item for item in text if len(item.split(","))>=12]
##        text   = "".join(text).strip(",")
##        text   = text.split(",")
##        values  = [val(item.strip()) for item in text]



##        #3.2.4 Results data block format
##        #3.2.4.1 General Structure of the data bloc
##        res ={}

##        j=0
##        res["LIVELLO PIEZOMETRICO"] = values[j*np:(j+1)*np]
##        j+=1
##        res["vx_data"] = values[j*np:(j+1)*np]
##        j+=1
##        res["vy_data"] = values[j*np:(j+1)*np]
##        j+=1
##        if (is_3D_problem):
##            res["vz_data"] = values[j*np:(j+1)*np]
##            j+=1
##        if (is_mass_transport or is_thermohaline_transport):
##            res["concentration_data"] = values[j*np:(j+1)*np]
##            j+=1
##        elif (is_heat_transport):
##            res["temperature_data"] = values[j*np:(j+1)*np]
##            j+=1
##        if (is_thermohaline_transport):
##            res["temperature_data"] = values[j*np:(j+1)*np]
##            j+=1
##        if (is_3D_problem and is_unconfined and is_slice1_free_movable):
##            #   This part has to be performed!!
##            #for slc in range(numb_slices):
##            #   if (slicetype[slc] == UNSPECIFIED or slicetype[slc] == MOVABLE)
##            #      res["slice_elevation_data"] = values[j*np:(j+1)*np]
##            #      j+=1
##            pass
##        if (ic2 != 2):
##            res["acceleration_data_mass"] = values[j*np:(j+1)*np]
##            j+=1
##            if (ic1 != 2):
##                if (ic2 == 1):
##                    res["acceleration_data_flow"] = values[j*np:(j+1)*np]
##                    j+=1
##                if (ic1 == 8):
##                    res["acceleration_data_heat"] = values[j*np:(j+1)*np]
##                    j+=1
##        if (exist_cbc_of_flow):
##            res["flow_cbc_data"] = values[j*np:(j+1)*np]
##            j+=1
##        if (exist_cbc_of_mass):
##            res["mass_cbc_data"] = values[j*np:(j+1)*np]
##            j+=1
##        if (exist_cbc_of_heat):
##            res["heat_cbc_data"] = values[j*np:(j+1)*np]
##            j+=1

        #INSERT INTO DB
        #for keyname in res.keys():
        #for keyname in ["head_data"]:
        #Livello PIEZOMETRICO:
        varname  ="LIVELLO PIEZOMETRICO"
        values = [(Date,(1+j),self.Vars[varname],res[varname][j]) for j in range(len(res[varname]))]
        self.log( """INSERT OR REPLACE INTO [FeFlowData] VALUES %s"""%len(values))
        self.executeMany("""INSERT OR REPLACE INTO [FeFlowData](Date,location_id,type_id,value)  VALUES(?,?,?,?);""",{},values)
        self.log("COMMITTED.")
        return True

    def importOBSERVATION_POINTS(self,Date,workdir):

        OBSERVATION_POINTS= {"P1":1,"P2":2,"P3":3,"P4":4,"P5":5,"P6":6,"P7":7,"P8":8,"P9":9,
        "P10":10,"N1":11,"N2":12,"N3":13,"N4":14,"N5":15,"N21":16,"N20":17,"P15":18,
        "N17":19,"P16":20,"P14":21,"N19":22,"N18":23,"N8":24,"N7":25,
        "N6":26,"I1":27,"I2":28,"N9":29,"N12":291}

        Date=  strftime("%Y-%m-%d",Date)
        filename = workdir+"/results/%s.dac"%Date
        text   = filetostr(filename)
        if not text:
            return None

        re_int   = r'\d+'
        re_float = r'([+-]?\d+(?:\.\d+)?(?:[eE][+-]\d+)?)'
        env ={"int":re_int,"float":re_float}

        re_target = r'(?<=DIAGRAMS\n)(?P<N_WIND>{int}),(?P<obs_pnts>{int}),(?P<numb_wells>{int}),(?P<cdiagnum>{int}),(?P<ntime>{int})\n(.*\n){3}'
        re_target = sformat(re_target,env)
        match =  re.search(re_target,text,re.MULTILINE)
        ntime  =  match.group("ntime")
        ntime_minus1 = val(ntime)-1
        env["ntime"] = ntime
        env["ntime_minus1"]= ntime_minus1
        re_target = r"""((DIAGRAMS\n(.*\n){4}(\s*{float},){{ntime}}))"""    #(\n1\n((\s*{float},){{ntime}}))"""
        re_target = sformat(re_target,env)

        match =  re.search(re_target,text,re.MULTILINE)
        text  = text[match.end():]

        for k in OBSERVATION_POINTS:
            env["observation_point"] = OBSERVATION_POINTS[k]
            re_target = r"""\n{observation_point}\n({float},\s*){{ntime_minus1}}(?P<data>{float})"""
            re_target = sformat(re_target,env)
            match =  re.search(re_target,text,re.MULTILINE)

            if match:
                data =  match.group("data")
                res =  {"date":Date,"value":val(data),"type_id":self.Vars["LIVELLO PIEZOMETRICO DA MODELLO"],"location_id":self.location[k],"dateupd": strftime("%Y-%m-%d",None),"src_id":3}
                sql = """INSERT OR REPLACE INTO Ts(Date,location_id,type_id,value,dateupd,src_id) VALUES('{date}',{location_id},{type_id},{value},'{dateupd}',{src_id});"""
                self.execute(sql,res,verbose= False)

        return None

    def exportModelToShape(self, modelname, epsg=3857):
        """
        exportModelToShape
        """
        modelname = juststem(modelname)
        fileshp = forceext(modelname,"shp")
        env = {"modelname":modelname}
        self.toShp("""SELECT AsBinary(geometry) as geometry, X,Y,Z,SLICE,BC FROM [{modelname}];""",env,fileshp,epsg)
        return fileshp

    def exportToRaster(self,bdate,workdir,edate=None,method="IDW2",pixelsize=50,contour=True):
        """
        Legge le piezometrie dal database
        genera lo shape dei punti del modello
        e krigga per ottenere un raster
        """

        sql = """
        SELECT
            AsBinary(MakePoint(X,Y)) as geometry,
            AVG(value) AS VALUE
		FROM [FeFlowView] Fs
		WHERE type_id={type_id}
        AND SLICE = 1
        AND Date BETWEEN '{bdate}' AND '{edate}'
             GROUP BY location_id;
        """
        bdate =  strftime("%Y-%m-%d",bdate)
        edate =  strftime("%Y-%m-%d",edate) if edate else bdate
        env = {
            "bdate":bdate,
            "edate":edate,
            "date":bdate if bdate==edate else "%s_%s"%(bdate,edate),
            "tagname":"LIVELLO PIEZOMETRICO",
            "type_id":self.Vars["LIVELLO PIEZOMETRICO"],
            "workdir": workdir
        }

        fileshp   = sformat("{workdir}/falda/AVG_{tagname}_{date}/AVG_{tagname}_{date}.shp",env)

        self.toShp(sql,env,fileshp)
        #filetif     = qkrige(fileshp,method,pixelsize,RemoveNegativeValues=True) True??? why???
        filetif  = Kriging(fileshp,method=method,pixelsize=pixelsize,RemoveNegativeValues=False)

##        if (contour):
##            filecontour = sformat("{workdir}/ISO_AVG_{tagname}_{date}/ISO_AVG_{tagname}_{date}.shp",env)
##            gdal_contour(filetif,filecontour,step =0.1,verbose=False)

        return filetif


    def UpdateBoundaryConditions(self,date,workdir):
        """
        In corrispondenza di ogni campagna di misura le condizioni al contorno
        vengono riportate alla misure reali affinche' il modello non vada alla
        deriva. Le misure reali sono interpolate con un ordinary kriging su una
        zona limitata. (buffer di 200m sull'estensione generata dai piezometri)
        Medie stagionali sul resto dei nodi.


        """
        #Numero potenziale dei piezometri
        type_id = self.Vars["LIVELLO PIEZOMETRICO"]
        date =  strftime("%Y-%m-%d",date)
        env ={"MeasurementCampaignDate":date,"date":date,"type_id":type_id}

        sql = """SELECT count(*)
        FROM sicura.[location] L
        WHERE id>=1000000
        AND (point LIKE 'P%' OR point LIKE 'N%')
        AND NOT X IS NULL;
        """
        N = self.execute(sql,outputmode="scalar")

        #Numero delle misure reali nella campagna odierna
        sql = """
        SELECT count(*)
            FROM sicura.[Ts] Ts
		INNER JOIN sicura.[location] L ON L.id=Ts.location_id
		WHERE Date='{MeasurementCampaignDate}'
    		AND Ts.type_id='{type_id}'
            AND Ts.location_id>1000000
            AND NOT L.X IS NULL
            AND NOT Ts.value IS NULL;
        """
        R = self.execute(sql,env,outputmode="scalar")

        if  R/float(N) < 0.5 :
            #print "In data %s ci sono solo %d misure su %d piezometri potenziali"%(date,R,N)
            #print "Pertanto non aggiorno le condizioni al contorno"
            return False

        #Creazione shape con le misure
        #Tutti i valori piezometrici misurati
        sql = """SELECT AsBinary(MakePoint(L.X,L.Y)) as geometry,
                        Ts.VALUE as VALUE
                        FROM sicura.[Ts] Ts
            		INNER JOIN sicura.[location] L ON L.id=Ts.location_id
            		WHERE Date='{MeasurementCampaignDate}'
                		AND Ts.type_id='{type_id}'
                        AND Ts.location_id>1000000
                        AND NOT L.X IS NULL
                        AND NOT Ts.value IS NULL
                        AND NOT L.point IN ('I1','I2');"""

        fileprj = "%s/template/sicura2018v2_002_ascii.prj"%(workdir)
        fileshp = "%s/results/%s"%(workdir,tempname("okrige-","-"+date,ext="shp"))
        self.toShp(sql,env,fileshp,epsg = fileprj)

        #Ordinary kriging
        filetif = Kriging(fileshp, method="AUTO", pixelsize=10, RemoveNegativeValues=False, verbose=False)

        #remove([fileshp, forceext(fileshp,"dbf"),forceext(fileshp,"shx"),forceext(fileshp,"prj")])

        #nodi al contorno soggetti a kriging
        sql = """
        INSERT OR REPLACE INTO [FeFlowData](Date,location_id,type_id,value)
            SELECT '{MeasurementCampaignDate}',id,{type_id},GetValueAt(X,Y,'{filetif}')
            FROM [FeFlowModel] WHERE BC AND LOWER([update])='kriging';
        CREATE TABLE IF NOT EXISTS [GetValueAtXY] AS
            SELECT '{MeasurementCampaignDate}',id,{type_id},GetValueAt(X,Y,'{filetif}')
            FROM [FeFlowModel] WHERE BC AND LOWER([update])='kriging';
        """

        env["filetif"] = filetif
        self.execute(sql,env,verbose= True)

        #nodi al contorno markati come FIxed
        sql = """INSERT OR REPLACE INTO [FeFlowData](Date,location_id,type_id,value)
                     SELECT '{MeasurementCampaignDate}',id,{type_id},F
                     FROM [FeFlowModel] WHERE BC AND LOWER([update])='fixed';"""

        self.execute(sql,env,verbose= False)

##      ##----------------------------------------------------------------------------------------------------------
##    	##		Assegnamento dei valori stagionali ai nodi al contorno restanti
##    	##  	In base alla data determinare la stagione (o meglio marcati con "S")
##    	##      -Reperire i valori stagionali
##    	##      Es:select distinct Date  from Ts where substr(Date,6) in ("03-21","06-21","09-23","12-23")
##
##        ## Determinazione della data sotto alla quale sono salvati
##        season_date= self.seasondate(env["MeasurementCampaignDate"])
##        env["season_date"] = season_date
##        #Inserimento nel db
##        sql = """
##        INSERT OR REPLACE INTO [FeFlowData](Date,location_id,type_id,value)
##		SELECT '{MeasurementCampaignDate}',Fe.[location_id],Fe.[type_id],Fe.[value]
##            FROM [FeFlowSeasonalAverage] Fe
##    		INNER JOIN [FeFlowModel] L ON Fe.location_id = L.id
##            WHERE Fe.Date='{season_date}'
##    		  AND type_id={type_id} AND BC AND [update]='S';"""
##        self.execute(sql,env,verbose= False)
        return True

    def FeFlowCycle(self,environ):

        filetpl =sformat("""{workdir}/template/{filetpl}""",environ)
        if not isfile(filetpl):
            print "%s not exits!"%filetpl
            return

        workdir = environ["workdir"]
        bdate = ctod(environ["bdate"])
        edate = ctod(environ["edate"]) if environ.has_key("edate") else bdate
        date  = bdate

        while date <= edate:
            success=False
            while not success:

                    self.log("FeFlowCycle on date:%s"%date)
                    filedac = "%s/results/%s.dac"%(workdir,date)
                    #remove(filedac)
                    #Assicurasi che hai acquisito i dati meteo + piezometrie
                    #Todo...

                    #Fai Girare il bilancio idrologico
                    self.log("Calcola_infiltrato on date %s"%(date))
                    Calcola_infiltrato(self, date)


                    #Fai il krige se c'e' una nuova campagna di misure
                    self.log("UpdateBoundaryConditions on date %s"%(date))
                    self.UpdateBoundaryConditions(date,workdir)


                    self.log("GenerateFemFromTemplate on date %s"%(date))
                    filefem = self.GenerateFemFromTemplate(date, workdir, filetpl)


                    if not file(filedac):
                        self.log("Running FeFlow")
                        filedac = feflow62c(filefem,compressoutput=False)


                    #Acquisisci piezometrie
                    self.log("importOUTPUTTimeStep on date %s"%(date))
                    self.importOUTPUTTimeStep(date,workdir)
                    self.importOBSERVATION_POINTS(date,workdir)

                    #Crea il raster delle piezometrie
                    self.log("CREATE the raster on date %s"%(date))
                    print self.exportToRaster(date, workdir=workdir)
                    self.log("------------------------------------------------")

                    sys.exit()
                    #clean
                    success =True



            date = tomorrow(date)

if __name__ =="__main__":


    db = FeFlowDB()
    env ={
        "workdir":Desktop()+"/FeFlow",
        "filetpl": "sicura2018v2_002_ascii.tpl",
        "bdate" : "2015-08-01",
        "edate" : "2015-08-01"
    }

    chdir(env["workdir"])
    print os.getcwd()

    remove("./template/sicura2018v2_002_ascii.tpl")
    db.importMODEL("./template/sicura2018v2_002_ascii.fem")



    db.FeFlowCycle(env)
    db.close()



