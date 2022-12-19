import matplotlib.pyplot as plt
import numpy as np







energie_dichte = 4.24  #[Mj/kg]

dichte = 2320.0 #[kg/m^3]

waermemenge = 2.06  #[GWh]

wm_list = [312.06, 57.75, 20.68, 18.84, 7.64, 2.72]

wm_names = ["groß", "mittel mit ausgedehntem","mittel", "mittel kleink", "klein", "Landesgemeinde"]



leistung = [142560, 38880, 12960, 12960, 6480, 6480]

preis = 0.125  #[€/kg]

#menge = 0

silo = 475 #[€/m^3]

wirbelschicht_preis = 1000 #[€/kW]

lichtbogen_preis = 0.6 #[€/kg] #600 #[€/t]

transport_preis = 0.1 #[€/tkm]

strecke = 100 #[km]

luft_wasser_rippenrohr = 30 #[€/kw]

wasser_wasser_rohr = 10 #[€/kw]

abgas_wasser = 50 #[€/kw]

lebensdauer = 25  # Jahre

i = 2



"#####################CLASS########################"

class material:
    def __init__(self, energie, dichte, preis, name):
        self.energie = energie
        self.dichte = dichte
        self.preis = preis
        self.name = name



#"#####################################FUNCTIONS###################################"

#Berechnung material menge in [kg]

    def material_menge(self,wm):
        menge = (wm * 1000) / (self.energie / 3600)
        #print("menge in",menge, "[kg]")
        return menge


#Berechnung Material kosten in [€]

    def material_kosten(self, wm):
        kosten = (self.material_menge(wm) * self.preis)
        print("material kosten in", kosten, "[€]")
        return kosten


#Berechnung Silo kosten in [€]

    def silo_kosten(self, wm_list):
        silo_ko = (self.material_menge(wm_list) / self.dichte) * silo
        print("silo kosten", silo_ko, "[€]")
        return silo_ko


#Berechnet Wirbelschichtreaktor kosten in [€]

    def wirbel_kosten(self, leistung):
        wi_kosten = (leistung) * (wirbelschicht_preis)  # 4380 Winterstunden im Jahr (8760/2)
        #wi_wartungs_kosten = wi_kosten * 0.1 * lebensdauer # Wartungskosten 1%
        #wi_kosten = wi_kosten + wi_wartungs_kosten
        print("wirbelschichtreaktor kosten", wi_kosten, "[€]")
        return wi_kosten


#Berechnet Lichtbogen kosten in [€]

    def lichtbogen_kosten(self):
        li_kosten = self.material_menge() * lichtbogen_preis
        print("Lichtbogenofen kosten",li_kosten, "[€]")
        return li_kosten


#Berechnet transport kosten mit LKW in [€]

    def transport(self):

        transp_kosten = transport_preis * strecke * (self.material_menge()/1000)
        print(transp_kosten)
        return transp_kosten



    def tauscher_luft_wasser(self):

        tausher_preis = waermemenge * 1000000 * (luft_wasser_rippenrohr/4380)  # 4380 Winterstunden im Jahr (8760/2)
        print("yyyyyyy", tausher_preis)
        return tausher_preis



    def tauscher_wasser_wasser(self):

        tausher_preis = waermemenge * 1000000 * (wasser_wasser_rohr/4380)  # 4380 Winterstunden im Jahr (8760/2)

        return tausher_preis



    def tauscher_abgas_wasser(self):

        tausher_preis = waermemenge * 1000000 * (abgas_wasser/4380)  # 4380 Winterstunden im Jahr (8760/2)

        return tausher_preis


#"#####################PLOTTING######################"


    def plot_mwh(self):
        width = 0.25
        sum_list = []
        ax = []
        grid = ()
        x = self.name
        y1 = self.material_kosten() / (waermemenge * 1000)
        y2 = self.silo_kosten() / (waermemenge * 1000)
        y3 = self.wirbel_kosten() / (waermemenge * 1000)

        #adding list y1 and y2
        #for (y1, y2) in zip(y1, y2):
            #sum_list.append(y1 + y2)

        #plotting stacked bar
        plt.bar(x, y1, color='g', width=width, zorder=3)
        plt.bar(x, y2, bottom=y1, color='y', width=width, zorder=3)
        plt.bar(x, y3, bottom=y1+y2, color='b', width=width, zorder=3)


        #plotting axes and legend

        plt.ylabel("Kosten [€/MWh]")

        colors = {'Material': 'green', 'Silo': 'yellow', 'Wirbelstoffreaktor' : 'blue' }
        labels = list(colors.keys())
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)

        plt.grid(color='k', which='both', linestyle='-', linewidth=1, alpha=0.5, zorder=0, axis='y')
        #plt.show()


    def rechnung(self, leistung, wm_list):
        x = self.name
        y1 = self.material_kosten(wm_list)
        y2 = self.silo_kosten(wm_list)
        y3 = self.wirbel_kosten(leistung)

        return x,y1,y2,y3


    def plot(self,leistung, wm_list, wm_names):
        width = 0.25
        sum_list = []
        ax = []
        grid = ()
        x = wm_names
        y1 = self.material_kosten(wm_list)
        y2 = self.silo_kosten(wm_list)
        y3 = self.wirbel_kosten(leistung)

        #adding list y1 and y2
        #for (y1, y2) in zip(y1, y2):
            #sum_list.append(y1 + y2)

        #plotting stacked bar
        plt.bar(x, y1, color='g', width=width, zorder=3)
        plt.bar(x, y2, bottom=y1, color='y', width=width, zorder=3)
        plt.bar(x, y3, bottom=y1+y2, color='b', width=width, zorder=3)


        #plotting axes and legend

        plt.ylabel("Kosten [€]")

        colors = {'Material': 'green', 'Silo': 'yellow', 'Wirbelstoffreaktor' : 'blue' }
        labels = list(colors.keys())
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)

        plt.grid(color='k', which='both', linestyle='-', linewidth=1, alpha=0.5, zorder=0, axis='y')
        #plt.show()


#"################Definition Materialien(energie, dichte, preis, name)###########################"

#Hydrate
Mgcl2 = material(4.24, 2320.0, 0.125, "Mgcl2")
Mgso4 = material(3.61, 1670, 0.15, "Mgso4")

#Zeolith
Zeolith13x = material(0.65, 700.0, 1.28, "Zeolith13x")
Zeolith4a = material(0.86, 750, 1.28, "Zeolith4a")

#Oxide
Sio2 = material(32.43, 2500, 0.5, "Sio2")
Mgo = material(24.75, 3580, 0.15, "Mgo")


for i in range(len(wm_list)):
    Zeolith13x.plot(leistung[i], wm_list[i], wm_names[i])
    #if i == 5:
       # plt.show()

plt.show()

#Zeolith13x.plot(leistung[1],wm_list[1])
#Zeolith13x.plot(leistung[2],wm_list[2])
#Zeolith13x.plot(leistung[3],wm_list[3])
#Zeolith13x.plot(leistung[4],wm_list[4])
#Zeolith13x.plot(leistung[5],wm_list[5])
#Zeolith13x.plot(leistung[0],wm_list[0])



#Zeolith13x.plot(leistung, wm)



#Mgo.plot_mwh()
#Mgso4.plot_mwh()
#Zeolith4a.plot_mwh()
#Zeolith13x.plot()
#Sio2.plot_mwh()

#plt.show()
#Berechnung der Menge an benötigtem Material

#Zeolith13x.plot()
#Mgso4.plot()


#plt.show()


Mgo.tauscher_luft_wasser()



def material_menge(energie_dichte,waermemenge):
    menge = (waermemenge*1000)/(energie_dichte/3600)
    print(menge, "[kg]")
    return menge


#Berechnung der materialkosten
def material_kosten(menge, preis):

    kosten = menge * preis
    print(kosten, "[€]")
    return kosten

#Berechnung der silo kosten
def silo_kosten(menge, dichte, silo):
    silo_ko = (menge/dichte) * silo
    print(silo_ko, "[€]")
    return silo_ko

def wirbel_kosten(waermemenge, wirbelschicht_preis):
    wi_kosten = (waermemenge*1000000) * (wirbelschicht_preis/4380)  #4380 Winterstunden im Jahr (8760/2)
    print(wi_kosten, "[€]")
    return wi_kosten


def lichtbogen_kosten(lichtbogen_preis, menge):
    li_kosten = menge * lichtbogen_preis
    print(li_kosten, "[€]")
    return li_kosten



#silo_kosten(material_menge(energie_dichte, waermemenge), dichte, silo)
#wirbel_kosten(waermemenge, wirbelschicht_preis)
#lichtbogen_kosten(lichtbogen_preis, material_menge(energie_dichte, waermemenge))




