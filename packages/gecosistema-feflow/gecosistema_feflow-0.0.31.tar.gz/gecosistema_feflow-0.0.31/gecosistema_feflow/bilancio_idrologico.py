#-------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2013 Valerio for Gecosistema S.r.l.
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
# Name:        bilancio_idrologico
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     19/02/2016
#-------------------------------------------------------------------------------
import sys

from gecosistema_core import *
from gecosistema_database import *
import numpy


def sun_NR(doy,lat):
    """
    Function to calculate the maximum sunshine duration N and incoming radiation
    at the top of the atmosphere from day of year and latitude.

    NOTE: Only valid for latitudes between 0 and 67 degrees (tropics and
    temperate zone)

    Input:
        - doy: (array of) day of year
        - lat: latitude in degrees, negative for southern hemisphere

    Output:
        - N: (array of) maximum sunshine hours [h]
        - Rext: (array of) extraterrestrial radiation [J/day]
    """

    # Set solar constant [W/m2]
    S = 1367.0 # [W/m2]
    # Convert latitude [degrees] to radians
    latrad = lat * math.pi / 180.0
    # Determine length of doy array
    #l = scipy.size(doy)
    # Check if we have a single value or an array
    #if l < 2:   # Dealing with single value...
        # calculate solar declination dt [radians]
    dt = 0.409 * math.sin(2 * math.pi / 365 * doy - 1.39)
    # calculate sunset hour angle [radians]
    ws = math.acos(-math.tan(latrad) * math.tan(dt))
    # Calculate sunshine duration N [h]
    N = 24 / math.pi * ws
    # Calculate day angle j [radians]
    j = 2 * math.pi / 365.25 * doy
    # Calculate relative distance to sun
    dr = 1.0 + 0.03344 * math.cos(j - 0.048869)
    # Calculate Rext
    Rext = S * 86400 / math.pi * dr * (ws * math.sin(latrad) * math.sin(dt) + math.sin(ws) * math.cos(latrad) * math.cos(dt))
    return Rext

def ET0_HargreavesSamani (lam, kRs, Pow,  date, lat, Tmax, Tmin):

    if (Tmax is None or Tmin is None):
        return None
    # lam=2.45 # [MJ/kg]
    # kRs=0.16 #0.16 internal and 0.19 coastal
    julianday=float(strftime("%j",date))
    Ra=sun_NR(julianday,lat)/1000000
    #ET0 =  0.0135*kRs*(Ra/lam)*numpy.sqrt(Tmax-Tmin)*(Tmed+17.8)
    #ET0 =  0.0135*kRs*(Ra/lam)*numpy.sqrt(Tmax-Tmin)*((Tmax+Tmin)/2+17.8)

    #ET0 = 0.0135*kRs*(Ra/lam)*numpy.power((Tmax-Tmin),0.6 )*((Tmax+Tmin)/2+17.8)
    ET0  = 0.0135*kRs*(Ra/lam)*numpy.power(abs(Tmax-Tmin),Pow )*((Tmax+Tmin)/2+17.8)
    return ET0

def Calcola_infiltrato(db, date):
    #Rain,Tmin,Tmax,Tmean,
    #theta_of_yesterday,delta_theta_of_yesterday,correct_SWAT_ET1_of_yesterday
    #db = SqliteDB("sicura.sqlite")
    #Per ogni suolo
    for soiltype in (2,3,4,):

        params = {
            "date":strftime("%Y-%m-%d",date),
            "yesterday":strftime("%Y-%m-%d",yesterday(date)),
            "soiltype":soiltype,
            "location_id":0,

            "THETA SUOLO %s"%soiltype:None,
            "DELTA THETA SUOLO %s"%soiltype:None,
            "CORRECT SWAT ET1 SUOLO %s"%soiltype:None,
            "RICARICA SUOLO %s"%soiltype:None,
            "ET0 HARGREAVES SAMANI":None

        }#end params


        Tmin               = db.execute("""SELECT value FROM TsView WHERE tagname ='TEMPERATURA MIN' AND Date <='{date}'  ORDER BY Date Desc LIMIT 1;""",params,outputmode="scalar",verbose =False)
        Tmax               = db.execute("""SELECT value FROM TsView WHERE tagname ='TEMPERATURA MAX' AND Date <='{date}'  ORDER BY Date Desc LIMIT 1;""",params,outputmode="scalar",verbose =False)
        Rain               = db.execute("""SELECT value FROM TsView WHERE tagname ='PRECIPITAZIONE'  AND Date ='{date}'   ORDER BY Date Desc LIMIT 1;""",params,outputmode="scalar",verbose =False)
        theta_of_yesterday = db.execute("""SELECT value FROM TsView WHERE tagname ='THETA SUOLO {soiltype}' AND Date <='{yesterday}'   ORDER BY Date Desc LIMIT 1;""",params,outputmode="scalar",verbose =False)
        delta_theta_of_yesterday      = db.execute("""SELECT value FROM TsView WHERE tagname ='DELTA THETA SUOLO {soiltype}' AND Date <='{yesterday}'   ORDER BY Date Desc LIMIT 1;""",params,outputmode="scalar",verbose =False)
        correct_SWAT_ET1_of_yesterday = db.execute("""SELECT value FROM TsView WHERE tagname ='CORRECT SWAT ET1 SUOLO {soiltype}' AND Date <='{yesterday}'   ORDER BY Date Desc LIMIT 1;""",params,outputmode="scalar",verbose =False)


        if Rain ==None:
            Rain = 0.0

        if (Tmin == None or Tmax==None ):
            return False


        lam=2.45 # [MJ/kg]
        kRs=0.16 #0.16 internal and 0.19 coastal
        lat=42.0 #latitude

        #soil parameters arrays
        soil_typeID = [1,2,3,4,5]
        theta_r_a   = [0.025,0.01,0.01,0.01,0.01]
        theta_s_a   = [0.403,0.439,0.43,0.52,0.614]
        n_a         = [1.3774,1.1804,1.2539,1.1012,1.1033]
        FC_a        = [0.294,0.379,0.406,0.472,0.567]
        WP_a        = [0.059,0.151,0.133,0.279,0.335]
        K_sat_a     = [6.94E-06,1.4E-06,2.63E-07,2.87E-06,1.74E-06]
        alpha_a     = [3.83,3.14,0.83,3.67,2.65]

        init_ab=10.0 # [mm]
        tortuosity=0.5
        Z=1.0 #[m] soil thickness
        theta_init_sat=0.1 #[%]

        #Soil Parametrers
        K_sat=K_sat_a[soiltype-1]
        alpha =alpha_a[soiltype-1]
        n=n_a[soiltype-1]
        theta_s=theta_s_a[soiltype-1]
        theta_r=theta_r_a[soiltype-1]
        FC=FC_a[soiltype-1]
        WP=WP_a[soiltype-1]

        #print Date,Rain,Tmin,Tmax,
        #Arguments
        Rain,Tmin,Tmax = float(Rain) if Rain else 0,float(Tmin),float(Tmax)

        ET0=ET0_HargreavesSamani (lam, kRs,0.5, date, lat, Tmax, Tmin)

        #first day
        if theta_of_yesterday==None:
            print "RESET"
            theta=theta_r
            ET1=min(ET0,(theta-theta_r)*1000*Z)
        #Other days
        else:

            theta= min(max(theta_of_yesterday+delta_theta_of_yesterday,theta_r),theta_s)
            ET1  = min(ET0,(theta_of_yesterday-theta_r)*1000*Z)*correct_SWAT_ET1_of_yesterday

        sat_soil=(theta-theta_r)/(theta_s-theta_r)

        a=math.pow(sat_soil,(n/(n-1)))
        b=math.pow(1-a,(1-1/n))
        c=math.pow(1-b,2)
        K=K_sat*math.pow(sat_soil,0.5)*c
        inf_excess=max(0,Rain-math.sqrt(K_sat*K)*86400*1000-init_ab)

        if theta<FC:
            delta_water=min((theta_s-theta)*Z*1000,max(Rain-inf_excess-ET1-(K*1000*86400),Z*1000*(theta_r-theta)))
        else:
            delta_water=min((theta_s-theta)*Z*1000,max(Rain-inf_excess-ET1-min((theta-FC)*Z*1000,K*1000*86400),Z*1000*(theta_r-theta)))

        delta_theta=delta_water/(Z*1000)
        sat_excess=max(0,Rain-inf_excess-ET1-delta_water-(K*1000*86400))
        runoff=sat_excess+inf_excess
        soil_wv=theta*Z*1000
        infilt=max(0.0,Rain-ET1-runoff-delta_water)

        #print date, Rain,ET1,runoff,delta_water

        correct_SWAT_ET1=math.exp(2.5*(theta-FC)/(FC-WP)) if theta<FC else 1

        params ={
            "date":strftime("%Y-%m-%d",date),
            "location_id":1000064,
            "type_id":None,
            "value":None,

            "THETA SUOLO %s"%soiltype:theta,
            "DELTA THETA SUOLO %s"%soiltype:delta_theta,
            "CORRECT SWAT ET1 SUOLO %s"%soiltype:correct_SWAT_ET1,
            "RICARICA SUOLO %s"%soiltype:infilt,
            "ET0 HARGREAVES SAMANI":ET0
        }

        for varname in params:
            #env = {"date":res["date"],"location_id":0,"value":res[varname]}
            #location_id = 1000064
            type_id = db.execute("""SELECT id FROM [type] WHERE tagname='{tagname}';""",{"tagname":varname},outputmode="scalar")
            if type_id:
                params["type_id"]=type_id
                params["value"] = params[varname]
                sql = """INSERT OR REPLACE INTO Ts(Date,location_id,type_id,value,dateupd,src_id) VALUES('{date}',{location_id},{type_id},{value},date(),3);"""
                #print varname, params["value"]
                db.execute(sql,params,verbose=False)

    return True

if __name__ == '__main__':
    print os.getcwd()

    bdate = '2015-08-01'
    edate = '2016-08-31'

    date = ctod(bdate)
    while date <=ctod(edate):
        print date
        Calcola_infiltrato(date)
        date = tomorrow(date)