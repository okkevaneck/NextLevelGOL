import csv


def speedup(r, n, key):
    if n[key] == 0.0:
        return "\\text{NaN}"
    else:
        return f"{r[key]/n[key]:5.2f}"


def printTableSingle(v, d):
    print("\\begin{table}[H]\n    \centering\n    \\begin{tabular}{|c|c|c|} \hline")
    print("        \cellcolor{black!25}\\textbf{Part} & \cellcolor{black!25}\\textbf{Runtime (s)} & \cellcolor{black!25}\\textbf{Fraction (\%)} \\\\ \hline")

    print(f"        Init  & ${d['init:t']:5.3f}$ & ${d['init:p']:5.2f}$ \\\\ \\hline")
    print(f"        Wrap  & ${d['wrap:t']:5.3f}$ & ${d['wrap:p']:5.2f}$ \\\\ \\hline")
    print(f"        Step  & ${d['step:t']:5.3f}$ & ${d['step:p']:5.2f}$ \\\\ \\hline")
    print(f"        Swap  & ${d['swap:t']:5.3f}$ & ${d['swap:p']:5.2f}$ \\\\ \\hline")
    print(f"        GIF   & ${d['gif:t']:5.3f}$ & ${d['gif:p']:5.2f}$ \\\\ \\hline")
    print(f"        Final & ${d['final:t']:5.3f}$ & ${d['final:p']:5.2f}$ \\\\ \\hline")

    print("        \cellcolor{gray!20}\\textbf{Total} & \cellcolor{gray!20}\\textbf{%5.3f} & \cellcolor{gray!20}\\textbf{100} \\\\ \hline" % d['total:t'])
    print("    \end{tabular}\n    \caption{The runtimes of ... (%s).}\n    \label{tab:%s}\n\end{table}" % (v, v))


def printTableDouble(v, d, r):
    print("\\begin{table}[H]\n    \centering\n    \\begin{tabular}{|c|c|c|c|c|} \hline")
    print("        \cellcolor{black!25}\\textbf{Part} & \cellcolor{black!25}\\textbf{Runtime (s)} & \cellcolor{black!25}\\textbf{Fraction (\%)} & \cellcolor{black!25}\\textbf{Speedup (v0)} \\\\ \hline")

    print(f"        Init  & ${d['init:t']:5.3f}$ & ${d['init:p']:5.2f}$ & ${speedup(r, d, 'init:t')}$ \\\\ \\hline")
    print(f"        Wrap  & ${d['wrap:t']:5.3f}$ & ${d['wrap:p']:5.2f}$ & ${speedup(r, d, 'wrap:t')}$ \\\\ \\hline")
    print(f"        Step  & ${d['step:t']:5.3f}$ & ${d['step:p']:5.2f}$ & ${speedup(r, d, 'step:t')}$ \\\\ \\hline")
    print(f"        Swap  & ${d['swap:t']:5.3f}$ & ${d['swap:p']:5.2f}$ & ${speedup(r, d, 'swap:t')}$ \\\\ \\hline")
    print(f"        GIF   & ${d['gif:t']:5.3f}$ & ${d['gif:p']:5.2f}$ & ${speedup(r, d, 'gif:t')}$ \\\\ \\hline")
    print(f"        Final & ${d['final:t']:5.3f}$ & ${d['final:p']:5.2f}$ & ${speedup(r, d, 'final:t')}$ \\\\ \\hline")

    print("        \cellcolor{gray!20}\\textbf{Total} & \cellcolor{gray!20}\\textbf{%5.3f} & \cellcolor{gray!20}\\textbf{100} & \cellcolor{gray!20}\\textbf{%s} \\\\ \hline" % (d['total:t'], speedup(r, d, 'total:t')))
    print("    \end{tabular}\n    \caption{The runtimes of ... (%s).}\n    \label{tab:%s}\n\end{table}" % (v, v))


def printTableMulti(v, d, p, r, prev):
    print("\\begin{table}[H]\n    \centering\n    \\begin{tabular}{|c|c|c|c|c|} \hline")
    print("        \cellcolor{black!25}\\textbf{Part} & \cellcolor{black!25}\\textbf{Runtime (s)} & \cellcolor{black!25}\\textbf{Fraction (\%%)} & \cellcolor{black!25}\\textbf{Speedup (v0)} & \cellcolor{black!25}\\textbf{Speedup (%s)} \\\\ \hline" % (prev))

    print(f"        Init  & ${d['init:t']:5.3f}$ & ${d['init:p']:5.2f}$ & ${speedup(r, d, 'init:t')}$ & ${speedup(p, d, 'init:t')}$ \\\\ \\hline")
    print(f"        Wrap  & ${d['wrap:t']:5.3f}$ & ${d['wrap:p']:5.2f}$ & ${speedup(r, d, 'wrap:t')}$ & ${speedup(p, d, 'wrap:t')}$ \\\\ \\hline")
    print(f"        Step  & ${d['step:t']:5.3f}$ & ${d['step:p']:5.2f}$ & ${speedup(r, d, 'step:t')}$ & ${speedup(p, d, 'step:t')}$ \\\\ \\hline")
    print(f"        Swap  & ${d['swap:t']:5.3f}$ & ${d['swap:p']:5.2f}$ & ${speedup(r, d, 'swap:t')}$ & ${speedup(p, d, 'swap:t')}$ \\\\ \\hline")
    print(f"        GIF   & ${d['gif:t']:5.3f}$ & ${d['gif:p']:5.2f}$ & ${speedup(r, d, 'gif:t')}$ & ${speedup(p, d, 'gif:t')}$ \\\\ \\hline")
    print(f"        Final & ${d['final:t']:5.3f}$ & ${d['final:p']:5.2f}$ & ${speedup(r, d, 'final:t')}$ & ${speedup(p, d, 'final:t')}$ \\\\ \\hline")

    print("        \cellcolor{gray!20}\\textbf{Total} & \cellcolor{gray!20}\\textbf{%5.3f} & \cellcolor{gray!20}\\textbf{100} & \cellcolor{gray!20}\\textbf{%s} & \cellcolor{gray!20}\\textbf{%s} \\\\ \hline" % (d['total:t'], speedup(r, d, 'total:t'), speedup(p, d, 'total:t')))
    print("    \end{tabular}\n    \caption{The runtimes of ... (%s).}\n    \label{tab:%s}\n\end{table}" % (v, v))


def printTable(v, d, p, r, prev):
    if r == None:
        printTableSingle(v, d)
    elif p == None:
        printTableDouble(v, d, r)
    else:
        printTableMulti(v, d, p, r, prev)

data = {}

with open('means.csv', mode='r') as file:
    meansFile = csv.reader(file)
    for l in meansFile:
        if (l[0] == 'version'):
            continue
        v = data[l[0]] = {}
        v['init:t']     = float(l[8])
        v['wrap:t']     = float(l[7])
        v['step:t']     = float(l[6])
        v['swap:t']     = float(l[5])
        v['gif:t']      = float(l[4])
        v['final:t']    = float(l[3])
        v['total:t']    = float(l[2])
        v['throughput'] = float(l[1])

with open('percentages.csv', mode='r') as file:
    percentagesFile = csv.reader(file)
    for l in percentagesFile:
        if (l[0] == 'version'):
            continue
        v = data[l[0]]
        v['init:p']     = float(l[8])
        v['wrap:p']     = float(l[7])
        v['step:p']     = float(l[6])
        v['swap:p']     = float(l[5])
        v['gif:p']      = float(l[4])
        v['final:p']    = float(l[3])
        v['total:p']    = float(l[2])


keys = [key for key in data.keys()]
for i in range(len(keys)):
    key = keys[i]
    prev = keys[i-1] if i > 1 else None
    if key == 'v6.0':
        prev = 'v4'
    if key == 'v7.0':
        prev = 'v7.1'
    if key == 'v7.1':
        prev = 'v6.1'

    d = data[keys[i]]
    p = data[prev] if i > 1 else None
    r = data[keys[0]] if i > 0 else None
    
    
    print(f"\n\nTABLE FOR {keys[i]}, throughput: {d['throughput']/1000000:.0f}M")
    print(f"prev={prev}\n")
    printTable(keys[i], d, p, r, prev)
