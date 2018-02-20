#! /usr/bin/env python3

'''
KEY:
    lb = logic board
    pn = player number
    pcs = player colors
    pt = player tokens
    op = other player tokens
    ro = row offset
    v = list of valid moves (either all moves or jumps)
    mj = indicates either moves or jumps
    co = column offset
    e = empty
    cr = number of rows and columns
    r1, c1, r2, c2 = rows and columns in a move
    or1, oc1, or2, oc2 = opponents rows and columns in a move
    jl = jumplist
    l = parallel list of lengths of jumps
    
'''

e = 0
co = [1, -1]
cr = 8
DEBUG=False
VISIBLE=True

import random
import math


def genvalid(lb, pn, pt, op, ro):
    v = {"j":[], "m":[]}
    for r1 in range(cr):
        for c1 in range(cr):                                                                                                  # every single square on board
            if (lb[r1][c1]) in pt:                                                                                            # if correct player
                if lb[r1][c1] == pt[1]:                                                                                       # if king change row offset
                    ro = [1, -1]
                elif ro == [1, -1]:                                                                                           # if not king change row offset back
                    ro = [ro[pn]]
                for i in ro:                                                                                                  # up and/or down
                    for ii in co:                                                                                             # left and right
                        r2 = r1 + 2*i 
                        c2 = c1 + 2*ii
                        if (r1+i in range(cr) and c1+ii in range(cr) and lb[r1+i][c1+ii] == e):                               # check for normal moves
                            v["m"].append(chr(r1+65)+str(c1)+":"+chr(r1+i+65)+str(c1+ii))
                        if (r2 in range(cr) and c2 in range(cr) and                                                           # check for complete jumps
                            lb[r2][c2] == e and lb[r1+i][c1+ii] in op):
                            jl = [chr(r1+65)+str(c1)+":"+chr(r2+65)+str(c2)]
                            prev = []
                            current = jl[:]
                            x = 0
                            while not prev == current:                                                                        # until no change
##                                print(x)
                                for jump in jl:
                                    rj1 = ord(jump[-2])-65                                                                    # new beg
                                    cj1 = int(jump[-1])                                                                       # new beg
                                    for iii in ro:                                                                            # up and/or down
                                        for iv in co:                                                                         # left and right
                                            rj2 = rj1 + 2 * iii                                                               # new end
                                            cj2 = cj1 + 2 * iv                                                                # new end
                                            js = chr(rj2+65)+str(cj2)
                                            if rj2 in range(cr) and cj2 in range(cr):                                         # check for next jumps
                                                if ((lb[rj2][cj2] == e or (js == jump[:2] and js != jump[-5:-3]))
                                                    and lb[rj1+iii][cj1+iv] in op and js not in jump[3:]):
                                                    jl.append(jump+":"+js)
                                                    if jump in jl:                                                            # delete incomplete jump
                                                        jl.remove(jump)
                                mid = current[:]
                                current = jl[:]
                                prev = mid[:]
                                x += 1
                            v["j"] = v["j"] + jl
                        
    if v["j"] != []:
        return v["j"], "j"
    if v["m"] != []:
        return v["m"], "m"
    else:
        return ["END"], "n"
    return v, "n"

def genvalues(pn):
    if pn == 0:
        pt = ["r", "R"]
        op = ["b", "B"]
        ro = 1
    else:
        pt = ["b", "B"]
        op = ["r", "R"]
        ro = -1
    return pt, op, ro

def gendata(move):
##    move = move.split(":")
    r1 = ord(move[0])-65
    c1 = int(move[1])
    r2 = ord(move[-2])-65
    c2 = int(move[-1])
    return r1, c1, r2, c2

def gencom(one, two): # one has priority
    both = []
    for i in one:
        for ii in two:
            if i == ii:
                both.append(i)
    if len(both) > 0:
        return both
    return one

def genloc(lb, pt, op):
    ploc = []
    oloc = []
    for row in range(cr):
        for col in range(cr):
            if lb[row][col] in pt:
                ploc.append((row, col))
            if lb[row][col] in op:
                oloc.append((row, col))
    plen = len(ploc)
    olen = len(oloc)
    rtot = 0
    ctot = 0
    for i in range(olen):
        rtot += oloc[i][0]
        ctot += oloc[i][1]
    ravg = rtot / olen
    cavg = ctot / olen
    return ploc, oloc, ravg, cavg

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    HEURISTICS:
        old:
            1. PICK A JUMP THAT WILL NOT BE JUMPED (safejump)  
            2. PICK A JUMP INTO THE KING ROW if not already king (kingjump) 
            3. PICK A JUMP TO PREVENT / BLOCK AN OPPONENT'S JUMP (blockjump) 
            4. PICK A JUMP INTO A SIDE COLUMN (sidejump) 
            5. PICK A MOVE INTO THE KING ROW if not already king (kingmove)
            6. PICK A MOVE THAT WILL NOT BE JUMPED (safemove) 
            7. PICK A MOVE TO EVADE / GET OUT OF AN OPPONENT'S JUMP (dodgemove) 
            8. PICK A MOVE TO PREVENT / BLOCK AN OPPONENT'S JUMP (blockmove)
            9. PICK A MOVE THAT WILL NOT VACATE THE HOME ROW (homemove)
           10. PICK THE LONGEST CHAIN OF JUMPS (longjump)
           11. PICK A JUMP TO EVADE / GET OUT OF AN OPPONENT'S JUMP (dodgejump)

        new:
           12. PICK A MOVE THAT DOESN'T UNBLOCK
           13. PICK A JUMP THAT DOESN'T UNBLOCK
           14. PICK A MOVE THAT CHASES THE AVERAGE OPPONENT CHECKER

    FUTURE HEURISTICS (not written yet):
    keep diagonal
    if non king in between back off and lie in wait
    go towards (pick shortest distance)
    stay in safety
    bait
    count num checkers on board
    jump for future jump
    corner
    overwhelm (if more checkers than other player, come from both sides)
    if opponent in corner, force them out
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

### 5
### HEURISTIC NUMBER FIVE 
### PICK A MOVE INTO THE KING ROW if not already king 
def kingmove(lb, pn, pt, v):
    king = []
    for move in v: 
        r1, c1, r2, c2 = gendata(move)
        if ((pn == 0 and r2 == 7 and lb[r1][c1] == pt[0]) or
            (pn == 1 and r2 == 0 and lb[r1][c1] == pt[0])):
            king.append(move)
    return king

def sidemove(v): # move to side col (disabled)
    side = []
    for move in v: 
        r1, c1, r2, c2 = gendata(move)
        if (c2 == 7) or (c2 == 0):
            side.append(move)
    return side

def kingmoveking(lb, pt, v): # move to king row if king (disabled)
    kking = []
    for move in v: 
        r1, c1, r2, c2 = gendata(move)
        if ((r2 == 7 and lb[r1][c1] == pt[1]) or
            (r2 == 0 and lb[r1][c1] == pt[1])):
            kking.append(move)
    return kking

### 6
### HEURISTIC NUMBER SIX 
### PICK A MOVE THAT WILL NOT BE JUMPED 
def safemove(lb, pn, pt, op, ro, v):
    king = kingmove(lb, pn, pt, v)
    side = sidemove(v)
    kking = kingmoveking(lb, pt, v)
    safe = king + side + kking
    for move in v: 
        if move not in safe:
            r1, c1, r2, c2 = gendata(move)
            dr = int(r2 - r1)
            dc = int(c2 - c1)
            a = lb[r2+dr][c2-dc]
            b = lb[r2+dr][c2+dc]
            ab = int((r2)-(r2+dr))
            c = lb[r2-dr][c2+dc]
            cd = int((r2)-(r2-dr))
            if not ((a == op[0] and c == e and ab == ro * -1) or
                    (b == op[0] and ab == ro * -1) or
                    (c == op[0] and a == e and cd == ro * -1) or
                    (a == op[1] and c == e) or
                    (b == op[1]) or
                    (c == op[1] and a == e)):
                safe.append(move)
    return safe

### 7
### HEURISTIC NUMBER SEVEN 
### PICK A MOVE TO EVADE / GET OUT OF AN OPPONENT'S JUMP (including multiple jumps)
def dodgemove(lb, pn, v):
    opn = 1 - pn
    opt, oop, oro = genvalues(opn)
    ov, omj = genvalid(lb, opn, opt, oop, [oro])
    dodge = []
    if omj != "j":
        ov = []
    for omove in ov:  #jumps to dodge
        mid = []
        for i in range((len(omove)-2)//3):
            or1, oc1, or2, oc2 = gendata(omove[(0+i*3):(5+i*3)])
            orj = (or1 + or2) // 2
            ocj = (oc1 + oc2) // 2
            mid.append(chr(orj+65)+str(ocj))
        for pmove in v:
            beg = pmove[:2]
            if beg in mid:
                dodge.append(pmove)
                break
    return dodge

### 8
### HEURISTIC NUMBER EIGHT 
### PICK A MOVE TO PREVENT / BLOCK AN OPPONENT'S JUMP
def blockmove(lb, pn, v):
    opn = 1 - pn
    opt, oop, oro = genvalues(opn)
    ov, omj = genvalid(lb, opn, opt, oop, [oro])
    block = []
    if omj != "j":
        ov = []
    for omove in ov:  #jumps to block
        for pmove in v:
            if omove[-2:] == pmove[-2:]:
                block.append(pmove)
    return block

### 9
### HEURISTIC NUMBER NINE 
### PICK A MOVE THAT WILL NOT VACATE THE HOME ROW
def homemove(lb, pn, pt, v):
    nothome = []
    for move in v:
        r1, c1, r2, c2 = gendata(move)
        if not ((lb[r1][c1] == pt[0] and ((r1 == 0 and pn == 0) or (r1 == 7 and pn == 1)))):
            nothome.append(move)
    return nothome

def closemove(lb, pn, v):
    pass

### 12
### HEURISTIC NUMBER TWELVE
### PICK A MOVE THAT DOESN'T UNBLOCK
def staymove(lb, pt, op, ro, v):
    stay = []
    bad = []
    for move in v: 
        r1, c1, r2, c2 = gendata(move)
        for ri in [-1, 1]:
            for ci in [-1, 1]:
                rii = ri * 2
                cii = ci * 2
                dr = ri - r1
                if r1+rii in range(cr) and c1+cii in range(cr):
                    if lb[r1+ri][c1+ci] in pt and ((lb[r1+rii][c1+cii] == op[0] and dr == ro * -1) or lb[r1+rii][c1+cii] == op[1]):
                        bad.append(move)
    for move in v:
        if move not in bad:
            stay.append(move)
    return stay

### 14
### HEURISTIC NUMBER FOURTEEN
### PICK A MOVE THAT CHASES THE AVERAGE OPPONENT CHECKER
def directmove(lb, pt, op, v):
    direct = []
    ploc, oloc, oravg, ocavg = genloc(lb, pt, op)
    if len(oloc) <= 6:
        for move in v:
            r1, c1, r2, c2 = gendata(move)
            fr = abs(math.sqrt((oravg - r1) ** 2 + (ocavg - c1) ** 2))
            to = abs(math.sqrt((oravg - r2) ** 2 + (ocavg - c2) ** 2))
            if to < fr:
                direct.append(move)
    return direct




### 10
### HEURISTIC NUMBER TEN 
### PICK THE LONGEST CHAIN OF JUMPS
def longjump(v):
    l = []
    long = []
    for jump in v:
        l.append(len(jump))
    mx = max(l)
    if mx <= 5:
        return v
    ct = l.count(mx)
    idx = 0
    for i in range(ct):
        long.append(v[l.index(mx, idx)])
        idx = (l.index(mx, idx)) + 1
    return long

### 2
### HEURISTIC NUMBER TWO 
### PICK A JUMP INTO THE KING ROW if not already king 
def kingjump(lb, pn, pt, v):
    king = []
    for jump in v: 
        r1, c1, r2, c2 = gendata(jump)
        if ((pn == 0 and r2 == 7 and lb[r1][c1] == pt[0]) or
            (pn == 1 and r2 == 0 and lb[r1][c1] == pt[0])):
            king.append(jump)
    return king

### 4
### HEURISTIC NUMBER FOUR 
### PICK A JUMP INTO THE SIDE COLUMN
def sidejump(v): # jumps to side column
    side = []
    for jump in v: 
        r1, c1, r2, c2 = gendata(jump)
        if (c2 == 7) or (c2 == 0):
            side.append(jump)
    return side

def kingjumpking(lb, pt, v): # jumps to king row if king (disabled)
    kking = []
    for jump in v:
        r1, c1, r2, c2 = gendata(jump)
        if ((r2 == 7 and lb[r1][c1] == pt[1]) or
            (r2 == 0 and lb[r1][c1] == pt[1])):
            kking.append(jump)
    return kking

### 1
### HEURISTIC NUMBER ONE 
### PICK A JUMP THAT WILL NOT BE JUMPED 
def safejump(lb, pn, pt, op, ro, v):
    king = kingjump(lb, pn, pt, v)
    side = sidejump(v)
    kking = kingjumpking(lb, pt, v)
    safe = king + side + kking
    for jump in v:
        if jump not in safe:
            r1, c1, r2, c2 = gendata(jump[-5:])
            dr = int((r2 - r1)/2)
            dc = int((c2 - c1)/2)
            a = lb[r2+dr][c2-dc]
            b = lb[r2+dr][c2+dc]
            ab = int((r2)-(r2+dr))
            c = lb[r2-dr][c2+dc]
            cd = int((r2)-(r2-dr))
            if not ((a == op[0] and c == e and ab == ro * -1) or
                    (b == op[0] and ab == ro * -1) or
                    (c == op[0] and a == e and cd == ro * -1) or
                    (a == op[1] and c == e) or
                    (b == op[1]) or
                    (c == op[1] and a == e)):
                safe.append(jump)
    return safe

### 11
### HEURISTIC NUMBER ELEVEN 
### PICK A JUMP TO EVADE / GET OUT OF AN OPPONENT'S JUMP (including multiple jumps)
def dodgejump(lb, pn, v):
    opn = 1 - pn
    opt, oop, oro = genvalues(opn)
    ov, omj = genvalid(lb, opn, opt, oop, [oro])
    dodge = []
    if omj != "j":
        ov = []
    for omove in ov:  #jumps to dodge
        mid = []
        for i in range((len(omove)-2)//3):
            or1, oc1, or2, oc2 = gendata(omove[(0+i*3):(5+i*3)])
            orj = (or1 + or2) // 2
            ocj = (oc1 + oc2) // 2
            mid.append(chr(orj+65)+str(ocj))
        for pmove in v:
            beg = pmove[:2]
            if beg in mid:
                dodge.append(pmove)
                break
    return dodge

### 3
### HEURISTIC NUMBER THREE 
### PICK A JUMP TO PREVENT / BLOCK AN OPPONENT'S JUMP
def blockjump(lb, pn, v):
    opn = 1 - pn
    opt, oop, oro = genvalues(opn)
    ov, omj = genvalid(lb, opn, opt, oop, [oro])
    block = []
    if omj != "j":
        ov = []
    for omove in ov:  #jumps to block
        for pmove in v:
            if omove[-2:] == pmove[-2:]:
                block.append(pmove)
    return block

### 13
### HEURISTIC NUMBER THIRTEEN
### PICK A JUMP THAT DOESN'T UNBLOCK
def stayjump(lb, pt, op, ro, v):
    stay = []
    bad = []
    for jump in v: 
        r1, c1, r2, c2 = gendata(jump)
        for ri in [-1, 1]:
            for ci in [-1, 1]:
                rii = ri * 2
                cii = ci * 2
                dr = ri - r1
                if r1+rii in range(cr) and c1+cii in range(cr):
                    if lb[r1+ri][c1+ci] in pt and ((lb[r1+rii][c1+cii] == op[0] and dr == ro * -1) or lb[r1+rii][c1+cii] == op[1]):
                        bad.append(jump)
    for jump in v:
        if jump not in bad:
            stay.append(jump)
    return stay


def pickmove(lb, pn, pt, op, ro, v, mj):
    genloc(lb, pt, op)
    if mj == "n": # if no options
        return []
    if len(v) == 1: # if only one option
        return v[0]
    if mj == "m": # if moves
        nothome = homemove(lb, pn, pt, v)
        king = kingmove(lb, pn, pt, v)
        safe = safemove(lb, pn, pt, op, ro, v)
        dodge = dodgemove(lb, pn, v)
        block = blockmove(lb, pn, v)
        stay = staymove(lb, pt, op, ro, v)
        direct = directmove(lb, pt, op, v)
        best = gencom(gencom(gencom(gencom(gencom(gencom(gencom(v,safe),nothome),king),dodge),block),stay),direct)
        return best[random.randrange(0, len(best))]
    if mj == "j": # if jumps
        long = longjump(v)
        king = kingjump(lb, pn, pt, v)
        side = sidejump(v)
        safe = safejump(lb, pn, pt, op, ro, v)
        dodge = dodgemove(lb, pn, v)
        block = blockjump(lb, pn, v)
        stay = stayjump(lb, pt, op, ro, v)
        best = gencom(gencom(gencom(gencom(gencom(gencom(gencom(v,long),king),side),safe),dodge),block),stay)
        return best[random.randrange(0, len(best))]
    return v[random.randrange(0, len(v))]

def getManualMove(validMoves,validJumps, pn, pcs):
    move=input("Enter a move " + pcs[pn] + ": ")
    if move=="exit":
        return move
    if len(validJumps)>0:
        while move not in validJumps:
            print("You must take the jump!")
            print(validJumps)
            move=input("Enter a jump " + pcs[pn] + ": ")
        return move
    while move not in validMoves:
        print(move, "is invalid!  Please try again from the following:")
        print(validMoves)
        move=input("Enter a move " + pcs[pn] + ": ")
    return move

def getMove(lb, pn, pcs, pt, op, ro):
    v, mj = genvalid(lb, pn, pt, op, [ro])
    move = pickmove(lb, pn, pt, op, ro, v, mj)
    return move
