import math
import itertools as it

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
    def __init__(self,quota,weights=None,parties=None):
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
        
        self.N=len(self.weights)
        self.banzhaf=None
        self.shapley_shubik=None
    def __len__(self):
        return len(self.parties)
    def __str__(self):
        return "The game consists of %s parties, the threshold is %s"%(len(self.parties),self.quota)

    """
        This function launches calculation of all implemented indeces
    """
    def calc(self):
        self.calc_banzhaf()
        self.calc_shapley_shubik()

    """
        Computes Banzhaf power index using generating function approach.
    """
    def calc_banzhaf(self):
        coeffs=self._coeffs_of_general_GF("Banzhaf")
        pows=[sum(self._coeffs_of_player_GF(coeffs,weight,"Banzhaf")[(self.quota-weight):self.quota]) for weight in self.weights]
        s_pows=float(sum(pows))
        self.banzhaf=map(lambda x: x/s_pows,pows)
        
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
        #pl_coeffs=[self._coeffs_of_player_GF(coeffs,weight,"ShapleyShubik")[(self.quota-weight):self.quota][0:(self.N)] for weight in self.weights]
        #pows=map(lambda x: sum(*x),pl_coeffs)
        #pows=[sum(lambda x: sum(x),self._coeffs_of_player_GF(coeffs,weight,"ShapleyShubik")[(self.quota-weight):self.quota][0:(self.N)])) for weight in self.weights]
        s_pows=float(sum(pows))
        self.shapley_shubik=map(lambda x: x/s_pows,pows)
        
    """
        Computes coefficients of the generating function of the game.
    """
    def _coeffs_of_general_GF(self,index):
        if index=="Banzhaf":
            return self._coeffs_of_general_GF_bf()
        elif index=="ShapleyShubik":
            return self._coeffs_of_general_GF_sh()
    
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
                
    def GF_coeffs(self,N,q,index):
        if index=="ShapleyShubik":
            coeffs=[[[1]+[0 for y in range(1,q+1)]] for j in range(N+1)]# a[j][0][0]=1
            #coeffs[0]=[[0 for k in range(N+1)] for y in range(q+1)]# a[0][k][y]=0
            coeffs[0]=[[0 for y in range(q+1)] for k in range(N+1)]# a[0][k][y]=0
            coeffs[0][0][0]=1
            return coeffs
        elif index=="Banzhaf":
            coeffs=[[1] for i in xrange(N+1)] # makes a[j][0]=1
            coeffs[0]=[0 for i in xrange(q+1)]# makes a[0][k]=0
            coeffs[0][0]=1
            return coeffs

    def _coeffs_of_player_GF(self,coeffs,w,index):
        if index=="Banzhaf":
            return self._coeffs_of_player_GF_bf(coeffs,w)
        elif index=="ShapleyShubik":
            return self._coeffs_of_player_GF_sh(coeffs,w)

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

    def pie_chart(self):
        indices={}
        if self.shapley_shubik is not None:
            indices["Shapley-Shubik Power Index"]=self.shapley_shubik
        if self.banzhaf is not None:
            indices["Banzhaf Power Index"]=self.banzhaf
        
        try:
            import matplotlib.pyplot as plt
            from matplotlib.gridspec import GridSpec
            from matplotlib.colors import ColorConverter
            CC=ColorConverter()
        except ImportError as ex:
            print "plot() function requires matplotlib library which is not installed on your computer"
            raise ex
        
        #colors_cycle=it.cycle('bgrmcyk')# blue, green, red, ...
        #colors=[colors_cycle.next() for weight in self.weights]
        gray_scales=[i/100.0 for i in sorted(range(50,100,10),reverse=True)]
        
        colors_cycle=it.cycle(gray_scales)# blue, green, red, ...
        colors_raw=[colors_cycle.next() for weight in self.weights]
        if colors_raw[0]==colors_raw[-1]:
            colors_raw[-1]-=0.1
        colors=[CC.to_rgb(str(color)) for color in colors_raw]
        
        I=len(indices)
        the_grid = GridSpec(1, I)
        i=0
        labels=[player.name for player in self.parties]
        for name in indices:
            ax=plt.subplot(the_grid[0, i], aspect=1)
            try:
                plt.pie(indices[name], labels=labels, colors=colors ,autopct='%1.1f%%',startangle=90)
            except TypeError:
                pass
            ax.set_title(name,bbox={'facecolor':'0.8', 'pad':5},fontweight='bold')
            i+=1
        
        plt.show()

    def hist():
        # to do
        n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
