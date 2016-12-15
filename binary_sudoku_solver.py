# Binary Sudoku Solver 1.0
# Rafa Rios
# Dec 2016
# Rules:
# Complete the grid with zeros and ones until there are just as many zeros and ones in every row and every column.
# No more than two of the same number can be next to or under each other.
# Rows or columns with exactly the same content are not allowed.
# When the line length has an odd number of cells, the number 1 exceeds the number 0.

class MyException(Exception):
  pass

import sys
import time

nr=0 # number of rows
nc=0 # number of columns

def sum_row(s,p,c):
  s1 = s[(p/nc)*nc:(p/nc)*nc+nc]
  if( (c == '1') and (nc%2 == 1) ):
    return(s1.count(c) > nc/2)
  else:
    return(s1.count(c) >= nc/2)

def sum_col(s,p,c):
  s1=""
  for i in range(nr):
    s1 += s[i*nc+p%nc]
  if( (c == '1') and (nr%2 == 1) ):
    return(s1.count(c) > nr/2)
  else:
    return(s1.count(c) >= nr/2)

def seq_row(s,p,c):
  if( (p%nc > 1) and (s[p-2]==s[p-1] and s[p-1]==c) ):
    return(True)
  if( (p%nc > 0 and p%nc < nc-1) and (s[p-1]==c and s[p+1]==c) ):
    return(True)
  if( (p%nc < nc-3) and (s[p+2]==s[p+1] and s[p+1]==c) ):
    return(True)
  return(False)

def seq_col(s,p,c):
  if( (p/nc > 1) and (s[p-nc*2]==s[p-nc] and s[p-nc]==c) ):
    return(True)
  if( (p/nc > 0 and p/nc < nr-1) and (s[p-nc]==c and s[p+nc]==c) ):
    return(True)
  if( (p/nc < nr-3) and (s[p+nc*2]==s[p+nc] and s[p+nc]==c) ):
    return(True)
  return(False)

def same_row(s,p,c):
  #display(s)
  for i in range(nr):
      #print s[nc*i:nc*i+nc], s[nc*(p/nc):nc*(p/nc)+(p%nc)]+c+s[nc*(p/nc)+(p%nc)+1:nc*(p/nc)+nc]
      #time.sleep(3)
      if( (i != p/nc) and (s[nc*i:nc*i+nc].find('*') == -1) and (s[nc*i:nc*i+nc] == s[nc*(p/nc):nc*(p/nc)+(p%nc)]+c+s[nc*(p/nc)+(p%nc)+1:nc*(p/nc)+nc]) ):
        return(True)
  return(False)

def same_col(s,p,c):
  sp=""
  for i in range(nr):
    if(i == p/nc):
      sp += c
    else:
      sp += s[i*nc + p%nc]
  for j in range(nc):
    if(j != p/nc):
      s1=""
      for i in range(nr):
        s1 += s[i*nc + j]
      if( (sp.find('*') == -1) and (s1 == sp) ):
        return(True)
  return(False)

def r(s):
  p = s.find('*')
  if p == -1:
    raise MyException(s)

  excluded_numbers = set()
  for c in '01':
    #print "p:", p, "c:", c, sum_row(s,p,c), sum_col(s,p,c), seq_row(s,p,c), seq_col(s,p,c), same_row(s,p,c), same_col(s,p,c)
    if sum_row(s,p,c) or sum_col(s,p,c) or seq_row(s,p,c) or seq_col(s,p,c) or same_row(s,p,c) or same_col(s,p,c):
      excluded_numbers.add(c)

  for m in '01':
    if m not in excluded_numbers:
      #print "candidato:", m, "excluded:" , excluded_numbers
      #display(s[:p]+m+s[p+1:])
      #time.sleep(2)
      r(s[:p]+m+s[p+1:])

def display(s):
  c = 1
  for i in s:
    print i,
    if(c % nc == 0):
      print ""
    c += 1

if __name__ == '__main__':
  if len(sys.argv) == 2:
    s=""
    try:
      with open(sys.argv[1], "r") as f:
        for line in f:
          s += line.strip("\n").strip()
          nr += 1
          if (len(s) % nr != 0):
            sys.exit("ERROR: Lenght of lines at input are not the same")
      f.close()
      nc = len(s)/nr
    except (OSError, IOError) as e:
      sys.exit("ERROR: Can't read the file " + sys.argv[1])

    print "nr:", nr, "nc:", nc

    print "\nInput"
    display(s)

    try:
        r(s)
    except MyException as e:
        print "\nSolution"
        display(str(e))
  else:
    print 'Usage: python binary-sudoku-solver.py puzzle'
    print 'where puzzle is matrix with 0s and 1s, read left-to-right, top-to-bottom, and * is a blank'
