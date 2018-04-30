import random as rand

class FragProdCon:

  def __init__(self, siz):
    self.debug = 0
    self.iter = 1
    self.size = siz
    self.buff = [0] * self.size
    self.writes = [0] * self.size
    self.sent = []
    self.head = 0
    self.tail = 0
    self.stride = 0

  def send(self, num):
    sent=[]
    tosend = [i for i in self.buff if i != 0]
    if self.debug > 0:
      print("Sending", num)
    cuck = False
    while len(sent) != num:
      if len(tosend) == 0:
        cuck = True
        if self.debug > 0:
          print("No more to send after", len(sent))
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
      if self.debug > 0:
        self.print()
    else:
      print("INCORRECTLY sent:", sent)
      print("Something went wrong!")
      self.print()
      exit(0)

  def record(self, num):
    recorded=[]
    for n in range(0, round(num/pow(2, self.stride))): # ignore some entries because of increased stride
      move = False
      if self.buff[self.head] != 0 and self.head == self.tail:
        # Tail entry will be overwritten, so must move
        move = True

      # 'record' packet at head
      recorded.append(self.iter)
      self.buff[self.head] = self.iter
      self.writes[self.head] = self.writes[self.head] + 1
      self.iter = self.iter + 1

      # lazy way to check to see if head passes tail 
      inc = False
      for s in range(0, pow(2, self.stride)):
        self.head = (self.head + 1) % self.size
        if self.head == (self.tail - pow(2, self.stride)) % self.size:
          inc = True
      if inc:
        self.stride = self.stride + 1

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
    print("Packet iter:", self.iter)
    print("Maximum consecutively missed blocks:", maxdiff)
    print("Average of consecutively missed blocks:", avgdiff)
    print("Average block writes:", sum(self.writes)/len(self.writes))
    print("Max. of one block's writes:", max(self.writes))
    print("Min. of one block's writes:", min(self.writes))


class NaiveProdCon:

  def __init__(self, siz):
    self.debug = 0
    self.iter = 1
    self.size = siz
    self.buff = [0] * self.size
    self.writes = [0] * self.size
    self.sent = []
    self.head = 0
    self.tail = 0

  def send(self, num):
    if self.debug > 0:
      print("Sending", num)
    sent=[]
    tosend = [i for i in self.buff if i != 0]
    cuck = False
    while len(sent) != num:
      if len(tosend) == 0:
        if self.debug > 0:
          print("No more packets to send after", len(sent))
        cuck = True
        break
      if self.buff[self.tail] == min(tosend):
        sent.append(self.buff[self.tail])
        self.sent.append(self.buff[self.tail])
        tosend.remove(self.buff[self.tail])
        self.buff[self.tail] = 0
      
      self.tail = (self.tail + 1) % self.size

    # Sent packet checks
    mincheck = [i for i in self.buff if i != 0]
    if sorted(sent) == sent and (cuck == True or len(sent) == num) and (len(mincheck) == 0 or max(sent) < min(mincheck)):
      if self.debug > 0:
        self.print()
    else:
      print("INCORRECTLY sent:", sent)
      print("Something went wrong!")
      self.print()
      exit(0)

  def record(self, num):
    if self.debug > 0:
      print("Recording", num)
    recorded=[]
    for n in range(0, num):
      # 'record' packet at head
      recorded.append(self.iter)
      self.buff[self.head] = self.iter
      self.writes[self.head] = self.writes[self.head] + 1
      self.iter = self.iter + 1
      self.head = (self.head + 1) % self.size

  def print(self):
    try:
      print("Buffer:", self.buff)
      print("Head at:", self.buff[self.head], " ( index", self.head, ")")
      print("Tail at:", self.buff[self.tail], " ( index", self.tail, ")")
    except:
      print("Odd types...")
      print("Head:", self.head)
      print("Tail:", self.tail)

  def conclude(self):
    maxdiff = 0
    avgdiff = 0
    for i in range(1, len(self.sent)):
      diff = abs(self.sent[i - 1] - self.sent[i]) - 1
      avgdiff = avgdiff + diff
      if diff > maxdiff:
        maxdiff = diff
    avgdiff = avgdiff / len(self.sent)
    print("Packet iter:", self.iter)
    print("Maximum consecutively missed blocks:", maxdiff)
    print("Average of consecutively missed blocks:", avgdiff)
    print("Average block writes:", sum(self.writes)/len(self.writes))
    print("Max. of one block's writes:", max(self.writes))
    print("Min. of one block's writes:", min(self.writes))
    
    

def main():

  print("Please enter a positive, odd integer.")
  size = int(input("Size of buffer: "))
  frag_buff = FragProdCon(size)
  naive_buff = NaiveProdCon(size)

  print("Please enter a positive integer.")
  rec = int(input("Average number of consecutive recordings: "))

  print("Please enter a positive integer.")
  sen = int(input("Average number of consecutive data sends: "))

  print("Please enter a positive integer.")
  dev = int(input("Average variance: "))

  print("Please enter a positive integer.")
  num = int(input("Number of packets to send: "))

  debug = int(input("Debug? (0=no, 1=yes)"))
  frag_buff.debug = debug
  naive_buff.debug = debug

  while frag_buff.iter < num or naive_buff.iter < num:
    recs = 0
    while recs < 1:
      recs = rec + rand.randint(-dev, dev)
    sens = 0
    while sens < 1:
      sens = sen + rand.randint(-dev, dev)
  # FRAG BUFF
    if frag_buff.iter < num:
      frag_buff.record(recs)
      frag_buff.send(sens)
  # NAIVE BUFF
    if naive_buff.iter < num:
      naive_buff.record(recs)
      naive_buff.send(sens)

  print()
  print("FRAGMENTED LOSS BUFFER:")
  frag_buff.conclude()
  print()
  print("NAIVE LOSS BUFFER:")
  naive_buff.conclude()

main()


