Arginine is a relatively unabbundant amino acid, but proteins rich in arginine may very well be related to neurodegenerative diseases. Since hyperphosphorylated tau protein binds to arginine tRNA at orders of magnitude higher than other proteins, and because of arginine rich peptides perceived ability to penetrate the brain, it is of interest to analyze the human proteome for arginine abundance, and detect proteins whos translation may be halted in alzheimers brain and whos partially translated forms may spread to other cells.

CountArgs is a program for calculating the number of arginine amino acids present in a given protein. It works on a CSV of the human proteome, but you can also add your mass-spec data for further analysis. The output file is in CSV format as well, so as not to overcrowd your terminal.

The calculated values are: the amount of arginines, the number of amino acids, and the percent of arginines out of total amino acids

It's important to note that I'm running this on only about 45% of the human proteome data, because I can't upload a file greater than 25MB to github. To do this I used a program that's included `shorten_proteom.py`. Also, FASTA data is usually not in CSV format. For this conversion I have another program which can convert the .FASTA to .CSV, it's a precursor program, since the requirements for the assignment is .CSV.
