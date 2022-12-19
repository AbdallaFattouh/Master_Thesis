import matplotlib.pyplot as plt
import numpy as np







energie_dichte = 4.24  #[Mj/kg]

dichte = 700.0 #[kg/m^3]

waermemenge = 7.64  #[GWh]

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

lebensdauer = 20  # Jahre

discount_rate = 0.02  # %

solarthermie_kosten = 5 #[€/kWh]

abwärme_kosten = 5 #[€/kWh]

anschluss_tcs = 750 #[€/kW]

wm_list = [312.06, 57.75, 20.68, 18.84, 7.64, 2.72]

wm_names = ["groß", "mittel mit ausgedehntem","mittel", "mittel kleink", "klein", "Landesgemeinde"]

leistung = [142560, 38880, 12960, 12960, 6480, 6480]


"#####################CLASS########################"

class material:
    def __init__(self, energie, dichte, preis, name):
        self.energie = energie
        self.dichte = dichte
        self.preis = preis
        self.name = name


#"#####################################FUNCTIONS###################################"

#'investitionskosten'

#Berechnung material menge in [kg]

    def material_menge(self):
        menge = (waermemenge * 1000) / (self.energie / 3600)
        #print("menge in",menge, "[kg]")
        return menge


#Berechnung Material kosten in [€]

    def material_kosten(self):
        kosten = (self.material_menge() * self.preis)
        print("material kosten in", kosten, "[€]")
        return kosten


#Berechnung Silo kosten in [€]

    def silo_kosten(self):
        silo_ko = (self.material_menge() / self.dichte) * silo
        #print("silo kosten", silo_ko, "[€]")
        return silo_ko


#Berechnet Wirbelschichtreaktor kosten in [€]

    def wirbel_kosten(self):
        wi_kosten = (waermemenge * 1000000) * (wirbelschicht_preis / 4380)  # 4380 Winterstunden im Jahr (8760/2)
        #wi_wartungs_kosten = wi_kosten * 0.1 * lebensdauer # Wartungskosten 1%
        #wi_kosten = wi_kosten + wi_wartungs_kosten
        #print("wirbelschichtreaktor kosten", wi_kosten, "[€]")
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

#Berechnet die Kosten der verschiedenen Wärmetauscher

    def tauscher_luft_wasser(self):

        tausher_preis = waermemenge * 1000000 * (luft_wasser_rippenrohr/2190)  # 4380 Winterstunden im Jahr (8760/2)
        print("yyyyyyy", tausher_preis)
        return tausher_preis



    def tauscher_wasser_wasser(self):

        tausher_preis = waermemenge * 1000000 * (wasser_wasser_rohr/4380)  # 4380 Winterstunden im Jahr (8760/2)

        return tausher_preis



    def tauscher_abgas_wasser(self):

        tausher_preis = waermemenge * 1000000 * (abgas_wasser/4380)  # 4380 Winterstunden im Jahr (8760/2)

        return tausher_preis


#Berechnet die Anschlusskosten

    def anschluss(self):

        anschluss_preis = (anschluss_tcs/2190) * (waermemenge * 1000000)

        return anschluss_preis


#Service Wartungskosten

    def wartung(self):

        om = ((self.wirbel_kosten()*0.01) + (self.silo_kosten()*0.02) + (self.anschluss() * 0.015))

        for i in range(1, lebensdauer + 1):
            wartungskosten = ((om) / (1 + discount_rate) ** i)

        return wartungskosten


############Maintanance###########



#"#####################PLOTTING######################"


    def plot_mwh(self):
        width = 0.25
        sum_list = []
        ax = []
        grid = ()
        x = self.name
        y1 = (self.material_kosten() / (waermemenge * 1000))/lebensdauer
        y2 = (self.silo_kosten() / (waermemenge * 1000))/lebensdauer
        y3 = (self.wirbel_kosten() / (waermemenge * 1000))/lebensdauer
        y4 = (self.tauscher_luft_wasser() / (waermemenge * 1000))/lebensdauer
        y5 = (self.anschluss() / (waermemenge * 1000))/lebensdauer
        y6 = ((self.wartung()) / (waermemenge * 1000))

        #adding list y1 and y2
        #for (y1, y2) in zip(y1, y2):
            #sum_list.append(y1 + y2)

        #plotting stacked bar
        plt.bar(x, y1, color='g', width=width, zorder=3)
        plt.bar(x, y2, bottom=y1, color='y', width=width, zorder=3)
        plt.bar(x, y3, bottom=y1+y2, color='b', width=width, zorder=3)
        plt.bar(x, 2*y4, bottom=y1+y2+y3, color='r', width=width, zorder=3)      # 2*y4, weil zwei Luft/wasser Wärmetauscher benötigt werden
        plt.bar(x, y5, bottom=y1+y2+y3+y4, color='k', width=width, zorder=3)
        plt.bar(x, y6, bottom=y1+y2+y3+y4+y5, color='c', width=width, zorder=3)



        #plotting axes and legend

        plt.ylabel("Kosten [€/MWh]")

        colors = {'Material': 'green', 'Silo': 'yellow', 'Wirbelstoffreaktor': 'blue', 'Wärmetauscher': 'red', 'Anschlusskosten': 'black', 'Wartung': 'c'}
        labels = list(colors.keys())
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)

        plt.grid(color='k', which='both', linestyle='-', linewidth=1, alpha=0.5, zorder=0, axis='y')
        #plt.show()



    def plot(self):
        width = 0.25
        sum_list = []
        ax = []
        grid = ()
        x = self.name
        y1 = self.material_kosten()
        y2 = self.silo_kosten()
        y3 = self.wirbel_kosten()
        y4 = self.tauscher_luft_wasser()
        y5 = self.anschluss()
        y6 = self.wartung()

        #adding list y1 and y2
        #for (y1, y2) in zip(y1, y2):
            #sum_list.append(y1 + y2)

        #plotting stacked bar
        plt.bar(x, y1, color='g', width=width, zorder=3)
        plt.bar(x, y2, bottom=y1, color='y', width=width, zorder=3)
        plt.bar(x, y3, bottom=y1+y2, color='b', width=width, zorder=3)
        plt.bar(x, 2*y4, bottom=y1+y2+y3, color='r', width=width, zorder=3)
        plt.bar(x, y5, bottom=y1+y2+y3+y4, color='k', width=width, zorder=3)
        plt.bar(x, y6, bottom=y1+y2+y3+y4+y5, color='c', width=width, zorder=3)

        #plotting axes and legend

        plt.ylabel("Kosten [€]")

        colors = {'Material': 'green', 'Silo': 'yellow', 'Wirbelstoffreaktor' : 'blue', 'Wärmetauscher': 'red', 'Anschlusskosten': 'black', 'Wartung': 'c' }
        labels = list(colors.keys())
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)

        plt.grid(color='k', which='both', linestyle='-', linewidth=1, alpha=0.5, zorder=0, axis='y')
        #plt.show()

    def plot_lcos(self):
        width = 0.25
        sum_list = []
        ax = []
        grid = ()
        x = self.name
        y1 = self.lcos_cap_sz1()
        y2 = self.lcos_om_sz1()
        # y3 = self.wirbel_kosten()

        # adding list y1 and y2
        # for (y1, y2) in zip(y1, y2):
        # sum_list.append(y1 + y2)

        # plotting stacked bar
        plt.bar(x, y1, color='g', width=width, zorder=3)
        plt.bar(x, y2, bottom=y1, color='y', width=width, zorder=3)
        # plt.bar(x, y3, bottom=y1+y2, color='b', width=width, zorder=3)

        # plotting axes and legend

        plt.ylabel("Kosten [€/kWh]")

        colors = {'Kapital': 'green', 'OM': 'yellow'}
        labels = list(colors.keys())
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)

        plt.grid(color='k', which='both', linestyle='-', linewidth=1, alpha=0.5, zorder=0, axis='y')
        # plt.show()










#"################Definition Materialien(energie, dichte, preis, name)###########################"

#Hydrate
Mgcl2 = material(4.24, 2320.0, 0.125, "Mgcl2")

Mgso4 = material(3.61, 1670, 0.15, "Mgso4")

#Zeolith
Zeolith13x = material(0.86, 700.0, 0.96, "Zeolith13x")
Zeolith4a = material(0.65, 750, 1.28, "Zeolith4a")

#Oxide
Sio2 = material(32.43, 2500, 0.5, "Sio2")
Mgo = material(24.75, 3580, 0.15, "Mgo")






Mgso4.plot_mwh()
Mgcl2.plot_mwh()
Zeolith4a.plot_mwh()

Zeolith13x.plot_mwh()


plt.show()


print("Material Menge Zeolith",Zeolith13x.material_menge())





#Mgso4.plot_mwh()
#Zeolith13x.plot_mwh()
#plt.show()
Mgso4.plot()
Mgcl2.plot()
Zeolith4a.plot()
Zeolith13x.plot()

plt.show()



