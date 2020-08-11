import random
import client
import os

print("Starting Benchmark...\n")
try:
    #print("A")
    os.remove("SIDs.txt")
except OSError:
    pass


save = 0
M = 16**4
with open("SIDs.txt", "a") as f:
   for i in range(100000):
      #print("2000:" + ":".join(("%x" % random.randint(0, M) for i in range(7))))
      a = "5000:" + ":".join(("%x" % random.randint(0, M) for i in range(7)))
      f.write(a+str("\n"))
   f.close()

print("Creation process...\n")

with open("SIDs.txt") as fp:
   SID_LINE = fp.readlines()
   #print("SID_LINE: "+str(SID_LINE))
   for SID in SID_LINE:
      #print("Line: {}".format(SID.strip()))
      client.run(SID.strip(), "CREATE")
      #print("Oi")
   fp.close()
exit()
print("Deletion process...\n")

with open("SIDs.txt") as fp:
   SID_LINE = fp.readlines()
   #print("SID_LINE: "+str(SID_LINE))
   for SID in SID_LINE:
      #print("Line: {}".format(SID.strip()))
      client.run(SID.strip(), "DELETE")
      #print("Oi")
   fp.close()

#print("SIDs.txt Removido")
#os.system("rm SIDs.txt")



