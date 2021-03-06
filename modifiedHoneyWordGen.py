#! /usr/local/bin/python
# gen.py
# password generation program (intended for generating ``honeywords'')
# Ronald L. Rivest and Ari Juels
# 3/18/13
#
# Usage: python gen.py n f1 f2 ... fk
#        where    n = number of passwords desired [optional; default = 19]
#                 fi = file containing lists of passwords to be used as models, i = 1, 2, ..., k
#                      (if no files given, short internal list used)
#                      passwords separated by whitespace (could be one, or many, per line)
#        The program outputs n passwords, one per line
#
# Example: assuming all password files are in subdirectory "passwords"
#          python gen.py 20 passwords/*
#
# Should run OK with python 2.7 (including pypy) and python 3.3
#
# This version of the program does not implement any password-composition restrictions,
# such as a minimum-length on passwords; this could be easily added.

# Software licence is ``MIT License'':
""" 
Copyright (C) 2013 Ronald L. Rivest and Ari Juels.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

##############################################################################
#### PARAMETERS CONTROLLING PASSWORD GENERATION (aside from password files)

tn = 0.08            # probability that a generated password is a ``tough nut''
                     # (password of length 40 of random chars)
                     # otherwise following parameters apply

# probabilities p1, p2, p3 add up to 1 (heuristically chosen)
p1 = 0.10            # chance of a "random" char at this position (see code)
p2 = 0.40            # chance of a markov-order-1 char at this position (see code)
p3 = 0.50            # choice of continuing copying from same word

q = 0.03             # add 3% noise words to list of passwords

# syntax parameters for a password
nL = 0               # password must have at least nL letters
nD = 0               # password must have at least nD digit
nS = 0               # password must have at least nS special (non-letter non-digit)

#### END OF PARAMETERS CONTROLLING PASSWORD GENERATION
##############################################################################

import random
import sys
import string


# A short list of high-probability passwords that is used to initialize the
# password list in case no password files are provided.
high_probability_passwords = """
123456
1234567
12345678
123asdf
Admin
admin
administrator
asdf123
backup
backupexec
changeme
clustadm
cluster
compaq
default
dell
dmz
domino
exchadm
exchange
ftp
gateway
guest
lotus
money
notes
office
oracle
pass
password
password!
password1
print
qwerty
replicate
seagate
secret
sql
sqlexec
temp
temp!
temp123
test
test!
test123
tivoli
veritas
virus
web
www
KKKKKKK
"""
singLength = False
isWord = False

PATH_TO_FILE = 'words.txt'

def loadWords():
    inFile = open(PATH_TO_FILE, 'r', 0)
    line = inFile.readline()
    wordlist = string.split(line)
    #print "  ", len(wordlist), "words loaded."
    return wordlist

wordList = loadWords()

def read_password_files(filenames):
    """ 
    Return a list of passwords in all the password file(s), plus 
    a proportional (according to parameter q) number of "noise" passwords.
    """
    pw_list = [ ]
    if len(filenames)>0:
        #for filename in filenames:
            #if sys.version_info[0] == 3:
            #    lines = open(filename,"r",errors='ignore').readlines()
            #else:
        lines = open(filenames,"r").readlines()
        for line in lines:
            #words = line.split()[-1]
            #pw_list.extend( words)
            pw_list.extend( line.split() )
    else:
        lines = high_probability_passwords.split()
        for line in lines:
            pw_list.extend( line.split() )
    # add noise passwords
    pw_list.extend( noise_list(int(q*len(pw_list))) )
    return pw_list

def noise_list(n):
    """ 
    Return a list of n ``noise'' passwords, to get better coverage of lengths and character 
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    nchars = len(chars)
    L = [ ]
    for i in range(n):
        w = [ ]
        k = random.randrange(1,18)
        for j in range(k):
            w.append(chars[random.randrange(nchars)])
        w = ''.join(w)
        L.append(w)
    return L

def tough_nut():
    """
    Return a ``tough nut'' password
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    nchars = len(chars)
    w = [ ]
    k = 40
    for j in range(k):
        w.append(chars[random.randrange(nchars)])
    w = ''.join(w)
    return w

def syntax(p):
    """
    Return True if password p contains at least nL letters, nD digits, and nS specials (others)
    """
    global nL, nD, nS
    L = 0
    D = 0
    S = 0
    for c in p:
        if c in string.ascii_letters:
            L += 1
        elif c in string.digits:
            D += 1
        else:
            S += 1
    if L >= nL and D >= nD and S >= nS:
        return True
    return False
    
def match(iPwd):
    i = -1
    n = ""
    M=[]
    L=[]
    N=[]
    out=[]
    send_out=[]
    for char in iPwd:   
        if char in string.ascii_letters:
            i += 1
            #print char
            continue
        else:
            break
        
    i += 1
    soFar = iPwd[ : i]

    if soFar in wordList:
        isWord = True
        #print isWord
        L = [word for word in wordList if ((len(word) == len(soFar)) and (word != soFar))]

        if len(soFar) < len(iPwd):
            if iPwd[i] in string.digits:
                
                for j in range(10):
                    n=iPwd[i]
                    while (n==iPwd[i]):
                        n = random.choice(string.digits)
                    s=[]
                    s = random.choice(L)
                    s+= n
                    M.append(s)
            else: 
                n = iPwd[i]
                for i in range(10):
                    s=[]
                    s = random.choice(L)
                    s+= n
                    M.append(s)
    
                if len(soFar)+1 < len(iPwd):
                    here = iPwd[i+1: -1]
                    if here in wordList:
                        N = [pw for pw in wordList if ((len(pw) == here) and (pw != here))]
                
                M.append(random.choice(N))
        out = set()
        for word in M:
            if word in out:
                continue
            else:
                out.add(word) 
        
        send_out = list(out)
    return send_out [:(random.randint(0, len(send_out)))/2]
    
    
def make_similar(iPwd, pw_list):
    #randomize later
    #sPwd = random.randrange(0,1)
    sPwd = 0.3
    L = [pw for pw in pw_list if ((len(pw) == len(iPwd)) and (pw != iPwd))]
    nL = len(L)
    L2=[]
    if nL < 10:
        L2 = [pw for pw in wordList if ((len(pw) == len(iPwd)) and (pw != iPwd))]
    while (nL < 10):
        if len(L2) != 0:
            L.append(random.choice(L2))
            nL = len(L)
        else:
            break

    closePwd = []
    choosePwd = int(sPwd * nL)
 
    for i in range(choosePwd):
        here = random.choice(L)
        closePwd.append(here)
    print closePwd
    return closePwd
    

def make_password(pw_list):
    """ 
    make a random password like those in given password list
    """
    #if random.random() < tn:
    #    return tough_nut()
    # start by choosing a random password from the list
    # save its length as k; we'll generate a new password of length k
    k = len(random.choice(pw_list))
    # create list of all passwords of length k; we'll only use those in model
    L = [ pw for pw in pw_list if len(pw) == k ]
    
    nL = len(L)
  
    # start answer with the first char of that random password
    # row = index of random password being used 
    row = random.randrange(nL)
    ans = L[row][:1]                  # copy first char of L[row] 
    j = 1                             # j = len(ans) invariant
    while j < k:                      # build up ans char by char
        p = random.random()           # randomly decide what to do next, based on p
        # here p1 = prob of action 1
        #      p2 = prob of action 2
        #      p3 = prob of action 3
        #      p1 + p2 + p3 = 1.00
        if p<p1:
            action = "action_1"
        elif p<p1+p2:
            action = "action_2"
        else:
            action = "action_3"
        if action == "action_1":
            # add same char that some random word of length k has in this position
            row = random.randrange(nL)
            ans = ans + L[row][j]
            j = j + 1
        elif action == "action_2":
            # take char in this position of random word with same previous char
            LL = [ i for i in range(nL) if L[i][j-1]==ans[-1] ]
            row = random.choice(LL)
            ans = ans + L[row][j]
            j = j + 1
        elif action == "action_3":
            # stick with same row, and copy another character
            ans = ans + L[row][j]
            j = j + 1
    if (nL > 0 or nD > 0 or nS > 0) and not syntax(ans): 
        return make_password(pw_list)
    return ans
    
def generate_passwords( n,pwd, pw_list ):
    """ print n passwords and return list of them """
    ans = [ ]
    ansFin = []
    sim_pw = []


    for t in range( n ):
        pw = make_password(pw_list)
        ans.append( pw )
        pwd1 = list(make_similar(pwd, pw_list))
        sim_pw.extend(pwd1)
        sim_pw.extend(ans[:(random.randint(0, len(ans)))])

    #for i in range(n):
    #    ansFin.append(random.choice(ans))
 
    return sim_pw

def main():
    # get number of passwords desired
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 19
    # read password files
    filenames = sys.argv[2:]           # skip "gen.py" and n   
    pw_list = read_password_files(filenames[0])
    
    # generate passwords
    for p in pw_list:
        nu = []
        final =[]
        new_passwords = generate_passwords(n,p,pw_list)
        other_passwords = list(match(p))

        finalP = new_passwords + other_passwords [:(random.randint(0, len(other_passwords )))/2]
        outfile = sys.argv[3]
        
        for wd in finalP:
            if wd in nu:
                continue
            else:
                nu.append(wd)
              
        random.shuffle(nu)
        for i in range(n):
            if len(nu) > 0:
                x = random.choice(nu)
                j = 0
                while (x in final):
                    j += 1
                    x = random.choice(nu)
                    if j > len(nu)+1:
                        
                        break
                final.append(x)

        
        # shuffle their order
        random.shuffle(final)

        target = open (outfile, 'a')
        target.write(p + ":\n")
        for pw in final:
            if pw == final[-1]:
                target.write(pw + "\n\n")
            else:
                target.write(pw + ", ")
    target.close()

# import cProfile
# cProfile.run("main()")

main()


