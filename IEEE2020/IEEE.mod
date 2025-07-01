#include IEEE.run
#set


set F;  #CS(charging station) include dummy CS
set D0; #start_depot
set Dσ; #end_depot
set D :=D0 union Dσ;
set V; #customers
set Vplun :=V union F; #include customers and CS 
set Vall :=D union V union F; #set of network nodes
set Vplun0 :=V union D0 union F; #include customers and start deopt and CS
set Vplunend :=V union Dσ union F; #include customers and end deopt and CS
set V0 :=D0 union V; #Set of the depot node {0} and the customer nodes C
set Vσ :=Dσ union V; #Set of the customer nodes C and the final depot {σ}


#parameter
param n in V;            #number of customers
param t{i in Vall, j in Vall}>=0; # travel time between node i and j
param d{i in Vall, j in Vall}>=0; # distance between node i and j
param Ct;                # travel cost of ECV
param Cf;                # fixed acquisition cost of an ECV
param Cs;     			 # battery swap cost(BSS)
param Cr;				 # charging cost
param r;                 # energy consumption rate per unit distance of ECV
param e{Vall};         # earliest service time of customer i 
param l{Vall};         # latest service time of customer i
param s{Vall}>=0;      # service time at customer i
param m{Vall};         #demend of customer i
param Q;                 # ECV battery capacity
param C;                 # maximum payload of an ECV
param g;     			 # the recharging rate of ECV 



#decision variable
var x{i in Vall, j in Vall: i != j} binary;      # Vehicle from i to j
var y{i in F} binary;           # ECV choose to battery swap station it will be 1
var z{i in F} binary;           # ECV choose to recharging station it will be 1
var v{Vall} >=0;                # remaining battery level of ECV at node i
var Y{i in F} >=0;              # remaining battery level of ECV from it depart at CS or BSS
var R{i in F}>=0;               # The recharging amount of ECV charged at CS node i
var u{Vall}>=0;            # remaining load on ECV at node i
var a{Vall}>=0;            # customer service start time by EV at node i



#the obj fun
minimize TotalCost: 
    Cf * sum{i in D0, j in Vplun} x[i,j] +          			     # ECV fixed cost
    Ct * sum{i in Vall, j in Vall: i != j} x[i,j] * t[i,j] +        # ECV distance cost
    Cr * sum{i in F} z[i] * R[i] +
    Cs * sum{i in F, j in Vplunend: i != j} y[i]* x[i,j]; # BSV distance cost


#subject to
subject to limit2{i in V}:sum{j in Vplunend:i<>j}x[i,j]=1;
subject to limit3{i in F}:sum{j in Vplunend:i<>j}x[i,j]<=1;
subject to limit4{j in Vplun}:sum{i in Vplun0:i<>j}x[i,j] = sum{i in Vplunend:i<>j}x[j,i];

subject to limit5{i in Vplun0,k in D0, j in Vplunend:i<>j}:
	a[i] + (t[i,j] + s[i])*x[i,j] -l[k]*(1 - x[i,j]) <= a[j];	
subject to limit6{i in F,k in D0, j in Vplunend:i<>j}:
	a[i] + t[i,j] * x[i,j] + g*R[i]*z[i] - (l[k] + g*Q)*(1 - x[i,j]) <= a[j];
subject to limit7{j in Vplunend}:e[j] <= a[j] <= l[j];
subject to limit8a{i in Vplun0, j in Vplunend:i<>j}:0 <= u[j];
subject to limit8b{i in Vplun0, j in Vplunend:i<>j}: 
    u[j] <= u[i] - m[i]*x[i,j] + C*(1 - x[i,j]);
subject to limit9{k in D0}:0 <= u[k] <= C;
#subject to limit10{i in V, j in Vplunend:i != j}:0 <= v[j] <= v[i] - r*d[i,j]*x[i,j] + Q*(1 - x[i,j]);
subject to limit10a{i in V0, j in Vplunend:i != j}:0 <= v[j];
subject to limit10b{i in V0, j in Vplunend:i != j}:
	v[j] <= v[i] - r*d[i,j]*x[i,j] + Q*(1 - x[i,j]);
#subject to limit11{i in F, j in Vplunend:i != j}:0 <= v[j] <= Y[i] - r*d[i,j]*x[i,j] + Q*(1 - x[i,j]);
subject to limit11a{i in F, j in Vplunend:i != j}:0 <= v[j];
subject to limit11b{i in F, j in Vplunend:i != j}:
	v[j] <= Y[i] - r*d[i,j]*x[i,j] + Q*(1 - x[i,j]);

subject to limit12{i in F}:Y[i] = z[i] * (v[i] + R[i]) + y[i]*Q;
subject to limit13{j in F}:y[j] + z[j] <= 1;
subject to limit14{i in F}:0 <= Y[i] <= Q;


subject to limit15{i in Vall}:0 <= v[i] <= Q;
#subject to limit16{k in D0}: v[k] = Q;


#我加的subject to limit15{i in Vall}:0 <= v[i] <= Q;
#我加的subject to limit10a{i in V0, j in Vplunend:i != j}:0 <= v[j];V---->V0