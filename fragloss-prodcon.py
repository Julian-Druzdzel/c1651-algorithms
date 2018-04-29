import random as rand

class FragProdCon:

  def __init__(self, siz):
    self.iter = 1
    self.size = siz
    self.buff = [0] * self.size
    self.writes = [0] * self.size
    self.sent = []
    self.head = 0
    self.tail = 0
    self.stride = 0

  def naive_send(self, num):
    print("Sending", num, "entries")
    sent=[]
    tosend = [i for i in self.buff if i != 0]
    cuck = False
    while len(sent) != num:
      if len(tosend) == 0:
        print("No more packets to send after", len(sent))
        cuck = True
        break
      if self.buff[self.tail] == min(tosend):
        sent.append(self.buff[self.tail])
        self.sent.append(self.buff[self.tail])
        tosend.remove(self.buff[self.tail])
        self.buff[self.tail] = 0
      
      self.tail = (self.tail + 1) % self.size
      if self.stride > 0 and self.tail == self.head:
        self.stride = self.stride - 1
        self.head = (self.head - pow(2, self.stride)) % self.size

    # Move tail for head-pass logic
    self.tail = (self.tail + pow(2, self.stride)) % self.size

    # Sent packet checks
    mincheck = [i for i in self.buff if i != 0]
    if sorted(sent) == sent and (cuck == True or len(sent) == num) and (len(mincheck) == 0 or max(sent) < min(mincheck)):
      print("Correctly sent:", sent)
    else:
      print("INCORRECTLY sent:", sent)
      print("Something went wrong!")
      self.print()
      exit(0)

  def record(self, num):
    print("Recording", num, "entries")
    recorded=[]
    for n in range(0, round(num/pow(2, self.stride))): # ignore some entries because of increased stride
      if pow(2, self.stride) > self.size/2:
        print("Stride value",pow(2, self.stride), "greater than size", self.size,": ignoring", num-n, "entries!")
        self.iter = self.iter + (num-n)*pow(2, self.stride)
        self.stride = self.stride - 1
        break

      move = False
      if self.buff[self.head] != 0 and self.head == self.tail:
        # Tail entry will be overwritten, so must move
        move = True

      # 'record' packet at head
      recorded.append(self.iter)
      self.buff[self.head] = self.iter
      self.writes[self.head] = self.writes[self.head] + 1
      self.iter = self.iter + pow(2, self.stride)

      # lazy way to check to see if head passes tail 
      inc = False
      for s in range(0, pow(2, self.stride)):
        self.head = (self.head + 1) % self.size
        if self.head == (self.tail - pow(2, self.stride)) % self.size:
          inc = True
#      if move and self.stride != 0:
#        self.tail = (self.tail + pow(2, self.stride-1)) % self.size
      if inc:
        self.stride = self.stride + 1
    print("Recorded:", recorded)

  def print(self):
    try:
      print("Buffer:", self.buff)
      print("Head at:", self.buff[self.head], " ( index", self.head, ")")
      print("Tail at:", self.buff[self.tail], " ( index", self.tail, ")")
      print("Stride:", self.stride)
    except:
      print("Odd types...")
      print("Head:", self.head)
      print("Tail:", self.tail)
      print("Stride:", self.stride)

  def conclude(self):
    maxdiff = 0
    avgdiff = 0
    for i in range(1, len(self.sent)):
      diff = abs(self.sent[i - 1] - self.sent[i]) - 1
      avgdiff = avgdiff + diff
      if diff > maxdiff:
        maxdiff = diff
    avgdiff = avgdiff / len(self.sent)

    print("Maximum consecutively missed blocks:", maxdiff)
    print("Average of consecutively missed blocks:", avgdiff)
    print("Average block writes:", sum(self.writes)/len(self.writes))
    print("Max. of one block's writes:", max(self.writes))
    print("Min. of one block's writes:", min(self.writes))
    

def main():

  print("Please enter a positive, odd integer.")
  buff = FragProdCon(int(input("Size of buffer: ")))

  print("Please enter a positive integer.")
  rec = int(input("Average number of consecutive recordings: "))

  print("Please enter a positive integer.")
  sen = int(input("Average number of consecutive data sends: "))

  print("Please enter a positive integer.")
  dev = int(input("Average variance: "))

  print("Please enter a positive integer.")
  for i in range(0, int(input("Number of record/send iterations: "))):
    print()
    print("ITERATION:", i)

    recs = 0
    while recs < 1:
      recs = abs(rec + rand.randint(-dev, dev))
    sens = 0
    while sens < 1:
      sens = abs(sens + rand.randint(-dev, dev))
    buff.record(recs)
    buff.print()

    print()
    buff.naive_send(sens)
    buff.print()

  # Conclusion
  buff.conclude()

main()


