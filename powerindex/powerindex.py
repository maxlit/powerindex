import math
import itertools as it
import argparse
import sys

class Party:
    def __init__(self,weight,name):
        self.weight=weight
        self.name=name
    def __eq__(self,other):
        if self.name==other.name:
            return True
        else:
            return False
    def __ne__(self,other):
        return not (self==other)
    def __str__(self):
        return "Party %s with weight %s"%(self.name,self.weight)
    
    def __repr__(self):
        return self.__str__()

class Game:
    def __init__(self,quota,weights=None,parties=None, absolute=False):
        if parties is None:
            if weights is None:
                raise TypeError("You need to put weights or parties as parameter while initializing the game")
            else:
                self.weights=weights
                self.parties=[Party(weights[i],i) for i in range(len(weights))]
        else:
            self.parties=parties
            self.weights=[party.weight for party in parties]
            
        self.quota=quota
        # divide by GCD to speed up the calculation
        gcd = math.gcd(self.quota, *self.weights)
        if gcd > 1:
            self.quota = self.quota // gcd
            self.weights = [w // gcd for w in self.weights]
        # keep the original values for weights and quota for whatever reaon
        self.original_quota=quota
        self.original_weights=weights
        self.N=len(self.weights)
        self.banzhaf=None
        self.shapley_shubik=None
        self.s_weights=float(sum(self.weights))
        self.nominal=[weight/self.s_weights for weight in self.weights]
        self.absolute = absolute
        
    def __len__(self):
        return len(self.parties)
    def __str__(self):
        return "The game consists of %s parties, the threshold is %s"%(len(self.parties),self.quota)

    """
        This function launches calculation of all implemented indeces
    """
    def calc(self):
        # find if there's a party with seats greater or equal to quota
        ge_quota = list(map(lambda x: 1 if x >= self.quota else 0, self.weights))
        num_ge_quota = sum(ge_quota)
        if num_ge_quota == 0: # if not calculate according to algos
            self.calc_banzhaf()
            self.calc_shapley_shubik()
            self.calc_contested_garment()
        else: # if yes manually assign all power to the party (parties)
            self.banzhaf = list(map(lambda x: x / float(num_ge_quota), ge_quota))
            self.shapley_shubik = list(map(lambda x: x / float(num_ge_quota), ge_quota))
            self.contested_garment = list(map(lambda x: x / float(num_ge_quota), ge_quota))


    """
        Computes Banzhaf power index using generating function approach.
    """
    def calc_banzhaf(self):
        coeffs=self._coeffs_of_general_GF("Banzhaf")
        pows=[sum(self._coeffs_of_player_GF(coeffs,weight,"Banzhaf")[(self.quota-weight):self.quota]) for weight in self.weights]
        self.banzhaf = list(map(lambda x: x/float(sum(pows)), pows))
        if self.absolute:
            self.banzhaf = list(map(lambda x: x*self.original_quota, self.banzhaf))
        
    def calc_shapley_shubik(self):
        coeffs=self._coeffs_of_general_GF("ShapleyShubik")
        pows=[0 for n in range(self.N)]
        i=0
        n_fac=float(math.factorial(self.N))
        for weight in self.weights:
            c=self._coeffs_of_player_GF(coeffs,weight,"ShapleyShubik")
            for z in range(self.N):
                relevant=c[z][(self.quota-weight):self.quota]
                binomial_coefficient=math.factorial(z)*math.factorial(self.N-z-1)/n_fac
                if len(relevant)>0:
                    pows[i]+=sum(relevant)*binomial_coefficient
            i+=1
        self.shapley_shubik = list(map(lambda x: x/float(sum(pows)), pows))
        if self.absolute:
            self.shapley_shubik = list(map(lambda x: x*self.original_quota, self.shapley_shubik))

    def calc_contested_garment(self):
        pows = self._coeffs_of_general_GF("ContestedGarment")
        #pows  = self._coeffs_of_player_GF(limits, self.quota, "ContestedGarment")
        self.contested_garment = list(map(lambda x: x/float(sum(pows)), pows))
        # restore the permutation
        permutation, _  = zip(*sorted(enumerate(self.weights), key  = lambda x: x[1]))
        self.contested_garment = [self.contested_garment[permutation.index(i)] for i in range(self.N)]
        if self.absolute:
            self.contested_garment = list(map(lambda x: x*self.original_quota, self.contested_garment))
        
    """
        Computes coefficients of the generating function of the game.
    """
    def GF_coeffs(self,N,q,index):
        if index=="ShapleyShubik":
            coeffs=[[[1]+[0 for y in range(1,q+1)]] for j in range(N+1)]# a[j][0][0]=1
            #coeffs[0]=[[0 for k in range(N+1)] for y in range(q+1)]# a[0][k][y]=0
            coeffs[0]=[[0 for y in range(q+1)] for k in range(N+1)]# a[0][k][y]=0
            coeffs[0][0][0]=1
        elif index=="Banzhaf":
            coeffs=[[1] for i in range(N+1)] # makes a[j][0]=1
            coeffs[0]=[0 for i in range(q+1)]# makes a[0][k]=0
            coeffs[0][0]=1
        elif index == "ContestedGarment":
            coeffs=[0 for i in range(N)]
            sorted_weights = sorted(self.weights)
            s = 0
            for i in range(N):
                coeffs[i] = s + sorted_weights[i]*(N-i)/2
                s += sorted_weights[i]/2
        return coeffs

    def _coeffs_of_general_GF(self,index):
        if index=="Banzhaf":
            return self._coeffs_of_general_GF_bf()
        elif index=="ShapleyShubik":
            return self._coeffs_of_general_GF_sh()
        elif index == "ContestedGarment":
            return self._coeffs_of_general_GF_cg()
    
    def _coeffs_of_general_GF_bf(self):
        N=len(self.weights)
        W=sum(self.weights)
        
        coeffs=self.GF_coeffs(N,W,"Banzhaf")
        
        for j in range(1,N+1):
            for k in range(1,W+1):
                if k<self.weights[j-1]:
                    coeffs[j].append(coeffs[j-1][k])
                else:
                    coeffs[j].append(coeffs[j-1][k]+coeffs[j-1][k-self.weights[j-1]])
            if j>2:
                coeffs[j-2]=None # free memory
        return coeffs[-1]
    
    def _coeffs_of_general_GF_sh(self):
        N=len(self.weights)
        W=sum(self.weights)
        q=self.quota

        coeffs=self.GF_coeffs(N,q,"ShapleyShubik")
        
        for i in range(1,N+1):
            for k in range(1,i+1):
                coeffs[i].append([])
                for y in range(0,q):
                    if y<self.weights[i-1]:
                        if k==i:
                            coeffs[i][k].append(0)
                        else:
                            coeffs[i][k].append(coeffs[i-1][k][y])
                    else:
                        if k==i:
                            coeffs[i][k].append(coeffs[i-1][k-1][y-self.weights[i-1]])
                        else:
                            coeffs[i][k].append(coeffs[i-1][k][y]+coeffs[i-1][k-1][y-self.weights[i-1]])
                if k>2:
                    pass#coeffs[i][k-2]=None # free memory
            if i>2:
                pass#coeffs[i-2]=None # free memory
        return coeffs[-1]
    
    def tmp_coeffs_of_player_GF_cg(self, q, sorted_weights, limits):
        N = len(sorted_weights)
        c = [w/2 for w in sorted_weights]
        i = 0
        while limits[i] < q:
            i += 1
        if i == 0:
            c = [q/float(N) for w in sorted_weights]
        else:
            for j in range(i, N):
                c[j] = c[i-1] + (q - limits[i-1])/(N-i)
        return c

    def _coeffs_of_general_GF_cg(self):
        sorted_weights = sorted(self.weights)
        N = len(sorted_weights)
        W = sum(self.weights)
        limits = self.GF_coeffs(self.N, W, "ContestedGarment")
        q = self.quota
        if q <= W/2:
            c = self.tmp_coeffs_of_player_GF_cg(q, sorted_weights, limits)
        else:
            c = self.tmp_coeffs_of_player_GF_cg(W - q, sorted_weights, limits)
            for r in range(N):
                c[r] = sorted_weights[r] - c[r]
        return c

    def _coeffs_of_player_GF(self,coeffs,w,index):
        if index=="Banzhaf":
            return self._coeffs_of_player_GF_bf(coeffs,w)
        elif index=="ShapleyShubik":
            return self._coeffs_of_player_GF_sh(coeffs,w)
        elif index == "ContestedGarment":
            return self._coeffs_of_player_GF_cg(coeffs,w)

    def _coeffs_of_player_GF_bf(self,coeffs,w):
        W=len(coeffs)-1
        c=[0 for i in range(W)]
        for k in range(0,W):
            if k<w:
                c[k]=coeffs[k]
            else:
                c[k]=coeffs[k]-c[k-w]
        return c

    def _coeffs_of_player_GF_sh(self,coeffs,w):
        c=[[] for i in range(self.N)]
        c[0]=[0 for i in range(self.quota)]
        c[0][0]=1
        for n in range(1,self.N):
            for k in range(0,self.quota):
                if k<w:
                    c[n].append(coeffs[n][k])
                else:
                    c[n].append(coeffs[n][k]-c[n-1][k-w])
        return c
    
    def _coeffs_of_player_GF_cg(self, sorted_weights, q):
        sorted_weights = sorted(self.weights)
        W = sum(self.weights)
        limits = self.GF_coeffs(self.N, W, "ContestedGarment")
        #q = self.quota
        if q <= W/2:
            c = self.tmp_coeffs_of_player_GF_cg(q, sorted_weights, limits)
        else:
            c = self.tmp_coeffs_of_player_GF_cg(W - q, sorted_weights, limits)
            for r in range(N):
                c[r] = sorted_weights[r] - c[r]
        return c

    def pie_chart(self,indices=["banzhaf","shapley"],fname=None,show=True):
        hashed_parties=zip(range(self.N),self.parties) # assign a number to each parties in order to match their power indices later on
        ordered_hashed_parties=sorted(hashed_parties,key=lambda x: x[1].weight)
        #median=ordered_hashed_parties[self.N/2][1].weight
        #ordered_hashed_parties=sorted(ordered_hashed_parties,key=lambda x: abs(x[1].weight-median)) # mix big and small parties

        if self.N>3:# receipt from http://nxn.se/post/46440196846/making-nicer-looking-pie-charts-with-matplotlib
            large = ordered_hashed_parties[:int(self.N / 2)]
            small = ordered_hashed_parties[int(self.N / 2):]
            reordered_hashed_parties = large[::2] + small[::2] + large[1::2] + small[1::2]
            angle = 310
        else:
            reordered_hashed_parties=ordered_hashed_parties
            angle=90

        reordered_parties=[el[1] for el in reordered_hashed_parties]
        pow_indices={}
        if "shapley" in indices and self.shapley_shubik is not None:
            pow_indices["Shapley-Shubik Power Index"]=[self.shapley_shubik[el[0]] for el in reordered_hashed_parties]
        if "banzhaf" in indices and self.banzhaf is not None:
            pow_indices["Banzhaf Power Index"]=[self.banzhaf[el[0]] for el in reordered_hashed_parties]
        if "nominal" in indices and self.nominal is not None:
            pow_indices["% of seats"]=[self.nominal[el[0]] for el in reordered_hashed_parties]
        
        try:
            import matplotlib.pyplot as plt
            plt.rcParams['figure.figsize']=12,9
            plt.rcParams['font.size']=16
            plt.rcParams['axes.titlesize']=24
            plt.rcParams['font.family']='fantasy'
            plt.rcParams['font.weight']='semibold'
            #plt.rcParams['savefig.dpi']=200
            from matplotlib.gridspec import GridSpec
            from matplotlib.colors import ColorConverter
            CC=ColorConverter()
        except ImportError as ex:
            print("plot() function requires matplotlib library which is not installed on your computer")
            raise ex
        
        # make a pie chart look nices as described here: http://nxn.se/post/46440196846/making-nicer-looking-pie-charts-with-matplotlib
        
        
        #colors_cycle=it.cycle('bgrmcyk')# blue, green, red, ...
        #colors=[colors_cycle.next() for weight in self.weights]
        gray_scales=[i/100.0 for i in sorted(range(50,100,10),reverse=True)]

        rgb_colors={
            "Maroon":"#800000",  #(128,0,0),
            "Olive":"#808000",   #(128,128,0),
            "Pale Green":"#98FB98",   #(152,251,152),
            "Teal":"#008080", #(0,128,128),
            "Peru": "#CD853F",#(205,133,63),
            "Steel Blue":"#4682B4",   #(70,130,180),
            "Slate Blue":"#6A5ACD",   #(106,90,205),
            "Pale Violet Red":"#DB7093",  #(219,112,147),
            "Khaki":"#F0E68C",    #(240,230,140),
            "Thistle":"#D8BFD8" #(216,191,216)
            }
        
        design="color"
        
        if design=="gray":
            colors_cycle=it.cycle(gray_scales)# blue, green, red, ...
            colors_raw=[next(colors_cycle) for weight in self.weights]
            if colors_raw[0]==colors_raw[-1]:
                colors_raw[-1]-=0.1
            colors=[CC.to_rgb(str(color)) for color in colors_raw]
        else:
            colors_cycle=it.cycle(rgb_colors.values())# blue, green, red, ...
            colors_raw=[next(colors_cycle) for weight in self.weights]
            colors=colors_raw
        
        I=len(pow_indices)
        the_grid = GridSpec(1, I)
        i=0
        labels=[player.name for player in reordered_parties]
        
        labels_raw=[str(player.name) for player in reordered_parties]
        
        labels=[]
        for label in labels_raw:# if the name of the party is too long split it in two lines
            if len(label)>24:
                spl=label.split(' ')
                L=len(spl)
                if L>1: # if 2 words or more than split in 2 lines
                    label="%s\n    %s"%(' '.join(spl[:3*L/4]),' '.join(spl[3*L/4:]))
            labels.append(label)
        
        
        for name in pow_indices:
            #labels=["%s (%s)"%(reordered_parties[i].name,round(pow_indices[name][i]*100,1)) for i in range(self.N)]
            ax=plt.subplot(the_grid[0, i], aspect=1)
            try:
                plt.pie(pow_indices[name], labels=labels, labeldistance=1.1
                        , colors=colors ,autopct='%1.1f%%',startangle=angle,
                        pctdistance=0.8)
            except TypeError:
                pass
            ax.set_title(name,bbox={'facecolor':'0.8', 'pad':5},fontweight='bold')
            i+=1
        if fname is not None:
            plt.savefig(fname)
            plt.close()
        if show:
            plt.show()

    def save_as_csv(self,full_filename,indices=["banzhaf","shapley","nominal"]):
        pow_indices={}
        if "shapley" in indices and self.shapley_shubik is not None:
            pow_indices["Shapley-Shubik Power Index"]=self.shapley_shubik
        if "banzhaf" in indices and self.banzhaf is not None:
            pow_indices["Banzhaf Power Index"]=self.banzhaf
        if "nominal" in indices and self.nominal is not None:
            pow_indices["% of seats"]=self.nominal

        output="Party;Seats;"+";".join(pow_indices.keys())+"\n"
        c=0
        for party in parties:
            output+="%s;%s"%(party.name,party.weight)
            for name in pow_indices:
                output+=";%s"%str(pow_indices[name][c])
            output+="\n"
            c+=1

        f=open(full_filename,'w')
        f.write(output)
        f.close()

    def hist():
        # to do
        n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
        print("not implemented yet")


def calculate_power_index(weights, quota, index_type, absolute=False):
    # Your power index calculation logic goes here
    game=Game(quota, weights, absolute=absolute)
    if index_type=="ss":
        game.calc_shapley_shubik()
        return game.shapley_shubik
    elif index_type=="b" or index_type=="bz":
        game.calc_banzhaf()
        return game.banzhaf
    if index_type=="cg":
        game.calc_contested_garment()
        return game.contested_garment
    else:
        raise ValueError("Unknown power index type: %s, only 'ss' (Shapley-Shubik) and 'b' (Banzhaf) are accepted" % index_type)

def main():
    parser = argparse.ArgumentParser(prog='px', description='Calculate power index')
    parser.add_argument('-i', '--index', metavar='INDEX', choices=['ss', 'b', 'bz', 'cg'], default='ss', help='Power index type: ss - Shapley-Shubik, bz - Banzhaf, cg - Contested Garment (default: ss)')
    parser.add_argument('-q', '--quota', metavar='QUOTA', type=int, required=False, help='Quota value (default: half of the sum of weights)')
    parser.add_argument('-w', '--weights', metavar='WEIGHT', type=int, nargs='+', required=True, help='integer weights (or votes integers)')
    parser.add_argument('-a', '--absolute', action='store_true', help='Calculate a power index in absolute values (weights times quote - makes sense rather for contested garment)')

    args = parser.parse_args()
    index_type = args.index
    quota = args.quota
    weights = list(args.weights)  # Convert to a Python list
    absolute = args.absolute
    if args.quota is None:
        quota = math.ceil(sum(weights) / 2)
    else:
        quota = args.quota
        
    power_index = calculate_power_index(weights, quota, index_type, absolute)
    # Remove whitespaces, brackets, and then print
    formatted_output = str(power_index)[1:-1].replace(" ", "")
    print(formatted_output)
    sys.stdout.flush()
    # Print or use the power index as needed

if __name__ == '__main__':
    main()

