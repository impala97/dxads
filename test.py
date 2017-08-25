from user import user
data = user().getClientTableData()
#print data[0]
cdata = data[0]
for r in cdata:
    for c in range(0,len(r)-2):
        #print r[c]
        pass

for r in cdata:
   print r[0]