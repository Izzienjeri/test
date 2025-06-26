import random


tissues = 100  
rubbish_bin = 0
empty_threshold = 20

def take_tissue(n):
  global tissues, total_tissues_used
  
  if tissues - n < empty_threshold:
    print("Warning! Tissue box nearly empty.")
  
  if n > tissues:
    print("Not enough tissues left!")
    return


  tissues -= n
  rubbish_bin += n
  
  print(f"{n} tissues taken. {tissues} remaining.")

def refill_box():
  global tissues
  tissues = 100
  print("Tissue box refilled to 100 tissues.")



def generate_decoration():
  decorations = ["flowers", "polka dots", "stripes", "hearts", "plaid"]
  for decoration in decorations:
    if not isinstance(decoration, str):
      print(f"Invalid decoration: {decoration}")
      return  
  return random.choice(decorations)

  
full_box = '[||||||||||]'
empty_box = '[..........]'

def show_capacity():
  if tissues == 0:
    print(empty_box)
  else:
    filled = int(tissues / 10)
    print('[' + (full_box[:filled] + empty_box[filled:]))


print(f"The tissue box has a {generate_decoration()} decoration.")

# Usage
show_capacity() 
# Prints [||||||||||]

take_tissue(50) 
show_capacity()
# Prints [|||||.....]]