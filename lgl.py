# T-cell large granular lymphocyte leukemia model

from test import PropensityNetwork, TanhNetwork, random_state
import numpy as np

rules = [
lambda n: n[47] and not (n[3] or n[36])                                                 #0: TCR
lambda n: n[22] and not n[36]                                                           #1: Fyn
lambda n: n[1] and not n[36]                                                            #2: Migration
lambda n: n[0] and not n[36]                                                            #3: CTLA4
lambda n: (n[0] or n[22] or CD45) and not (n[7] or n[36])                               #4: LCK
lambda n: n[6] and not n[36]                                                            #5: PLC
lambda n: n[4] and not n[36]                                                            #6: GRB2
lambda n: n[0] and not n[36]                                                            #7: CSK
lambda n: (n[38] and n[26]) and not n[36]                                               #8: Ceramide
lambda n: n[43] and not n[36]                                                           #9: STAT3
lambda n: n[20] and not n[36]                                                           #10: TBET
lambda n: not (n[9] or n[36])                                                           #11: PIAS
lambda n: n[9] and not (n[36] or n[15])                                                 #12: C-Myc
lambda n: n[5] and not n[36]                                                            #13: NFAT
lambda n: n[12] and not n[36]                                                           #14: Proliferation
lambda n: (n[32] and not n[16]) and not n[36]                                           #15: SMAD
lambda n: n[15] and not n[36]                                                           #16: SMAD7
lambda n: (n[18] or (n[46] and n[19])) and not (n[8] or n[24] or n[36])                 #17: Flip
lambda n: ((n[23] or n[37]) or (n[17] and n[35] and n[39])) and not (n[36] or n[11])    #18: NFKB
lambda n: ((n[24] or n[47]) and n[20]) and not (n[36] or n[15])                         #19: IFN
lambda n: n[43] and not n[36]                                                           #20: IFNT
lambda n: (n[24] and n[9]) and not (n[21] or n[36])                                     #21: IL2R
lambda n: (n[24] and n[33]) and not n[36]                                               #22: IL2RL
lambda n: n[34] and not n[36]                                                           #23: TPL2
lambda n: (n[18] or n[12] or n[13]) and not (n[15] or n[10] or n[36])                   #24: IL2
lambda n: (n[6] or n[5]) and not (n[42] or n[36])                                       #25: Ras
lambda n: (n[12] or n[18] or n[13] or n[33]) and not n[36]                              #26: FasL
lambda n: n[18] or n[27] and not n[36]                                                  #27: FasT
lambda n: ((n[27] and n[8]) or (n[27] and n[26] and not n[29])) and not n[36]           #28: Fas
lambda n: n[29]                                                                         #29: sFas
lambda n: (n[23] or n[25]) and not n[36]                                                #30: MEK
lambda n: n[28] and not (n[17] or n[39] or n[36])                                       #31: Caspase
lambda n: (n[15] or n[33]) and not (n[34] or n[45] or n[36])                            #32: TGF
lambda n: n[30] and not (n[36] or n[19])                                                #33: Erk
lambda n: (n[18] and n[37]) and not n[36]                                               #34: TNF
lambda n: n[34] and not (n[39] or n[36])                                                #35: TRADD
lambda n: n[31] or n[36]                                                                #36: Apoptosis
lambda n: n[25] and not n[36]                                                           #37: PI3K
lambda n: (n[31] or n[45]) and not (n[40] or n[48] or n[36])                            #38: BID
lambda n: n[18] and not n[36]                                                           #39: IAP
lambda n: (n[18] and n[9]) and not (n[38] or (n[25] and n[20]) or n[24] or n[36])       #40: BclxL
lambda n: n[43] and not (n[36] or n[24] or IL15)                                        #41: SOCS
lambda n: n[25] and not (IL15 or n[24] or n[36])                                        #42: GAP
lambda n: (n[43] or n[22]) and not (n[41] or CD45 or n[36])                             #43: JAK
lambda n: n[18] and not n[36]                                                           #44: RANTES
lambda n: (n[46] or n[10] or n[45]) and not n[36]                                       #45: GZMB
lambda n: (n[33] and n[19]) and not n[36]                                               #46: CREB
lambda n: n[47]                                                                         #47: Stimuli
lambda n: (n[9] and n[18] and n[33]) and not ((n[28] and n[24]) or n[36])               #48: Mcl1
]

b = PropensityNetwork(len(rules), rules, [(.9,.9)]*34)
t = TanhNetwork(len(rules))
for _ in xrange(5000):
    b.state = random_state(b.num_nodes)
    t.set_state(b.get_state())
    b.next()
    t.next()
    t.train(b.get_state())

for i, row in enumerate(t.weights):
    arow = np.abs(row[:-1])
    print i, '<-', np.nonzero(arow > np.mean(arow) + np.std(arow))[0]
