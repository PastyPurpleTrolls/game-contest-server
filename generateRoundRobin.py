import random

outFile = open("fixed-table.html", "w")
outFile.write('<div id="fixed-table-container-1" class="fixed-table-container">\n')
outFile.write("    <table>\n")
outFile.write("        <thead>\n")
outFile.write("            <tr><th>-</th><th>Rank</th><th>Wins</th>")
numRowsCols = 26
for col in range(numRowsCols):
    outFile.write("<th>Player %s</th>" % col)
outFile.write("</tr>\n")
outFile.write("        </thead>\n")

outFile.write("        <tbody>\n")
for row in range(numRowsCols):
    rank = random.randint(1, numRowsCols)
    wins = random.randint(0, 100)
    outFile.write("            <tr><td><%%= link_to 'Player %s', '#' %%> (John Luscombe)</td><td>%s</td><td>%s</td>" % (row, rank, wins))
    for col in range(numRowsCols):
        numWins1 = random.randint(0, 100)
        numWins2 = 100 - numWins1
        if row == col:
            outFile.write("<td>--</td>")
        else:
            outFile.write("<td>%s-%s</td>" % (numWins1, numWins2))
    outFile.write("            </tr>\n")
outFile.write("        </tbody>\n")
outFile.write("    </table>\n")
outFile.write("</div>")
