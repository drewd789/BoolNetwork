# Mammalian immune response to B. bronchiseptica infection

from test import BoolNetwork, random_state

rules = [
lambda n: n[0] and not n[33],                                       #Bb
lambda n: n[0] and not (n[5] or n[8]),                              #TTSSI
lambda n: n[1],                                                     #TTSSII
lambda n: n[0],                                                     #Oag
lambda n: n[0],                                                     #EC
lambda n: n[9] or n[5],                                             #Cab
lambda n: (n[0] and not n[3]) or (n[7] and n[5]),                   #C
lambda n: n[0] and (n[8] or n[5]),                                  #AgAb
lambda n: n[9] or n[8],                                             #Oab
lambda n: n[29],                                                    #BC
lambda n: n[4] or n[20] or n[23] and not n[15],                     #PIC
lambda n: (n[32] and n[24] and not n[14]),                          #IL12I
lambda n: (n[32] and n[24] and not n[14]),                          #IL12II
lambda n: (n[32] and n[24]) and not n[12],                          #IL4I
lambda n: (n[32] and n[24]) and not n[12],                          #IL4II
lambda n: (n[26] or n[30] or (n[21] and n[1])) and not n[11],       #IL10I
lambda n: (n[26] or n[30] or (n[21] and n[1])) and not n[11],       #IL10II
lambda n: (n[28] or n[21]) and not (n[15] or n[13]),                #IFNgI
lambda n: (n[28] or n[21]) and not (n[15] or n[13]),                #IFNgII
lambda n: n[10],                                                    #RP
lambda n: n[19] and n[1],                                           #DP
lambda n: (n[10] or n[17]) and not n[15],                           #MPI
lambda n: n[21],                                                    #MPII
lambda n: n[0] and (n[19] or n[21]) and ((n[6] and n[5]) or n[7]),  #AP
lambda n: n[32],                                                    #T0
lambda n: n[32] and n[24] and n[2],                                 #TrII
lambda n: n[25],                                                    #TrI
lambda n: n[32] and n[24] and n[12],                                #Th1II
lambda n: n[27],                                                    #Th1I
lambda n: n[32] and n[24] and not n[12],                            #Th2II
lambda n: n[29],                                                    #Th2I
lambda n: n[17] or n[10] or n[0],                                   #DCI
lambda n: n[31],                                                    #DCII
lambda n: n[23] and n[0]                                            #PH
]

b = BoolNetwork(34, rules)
b.state = random_state(b.num_nodes)
for _ in xrange(20):
    print b.get_state()
    b.next()
