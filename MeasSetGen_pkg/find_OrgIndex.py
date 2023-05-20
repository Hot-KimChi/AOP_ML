
## find freq index
def fn_findOrgIdx(self):

    orgindex = []

    for mode, subidx in zip(self.df['MODE'], self.df['SUBMODEINDEX']):
        if mode == 'B' and subidx == 0:
            orgindex.append(0)
        elif mode == 'B' and subidx == 1:
            orgindex.append(1)
        elif mode == 'Cb' and subidx == 0:
            orgindex.append(5)
        elif mode == 'D' and subidx == 0:
            orgindex.append(10)
        elif mode == 'M' and subidx == 0:
            orgindex.append(15)
        elif mode == 'M' and subidx == 1:
            orgindex.append(20)

    self.df['OrgBeamstyleIdx'] = orgindex