# Python Programming - Sections 1811
# Programming Assignment 4
# Instructor: Dr. Scott Bishop
# Student: Vladimir Palenov
# Assignment 5 "COVID-19 Genomic Data Wrangling"

# Program 1:  Creating codon dictionary
# def create_codon_dictionary(filename):
# This function takes in a file name as an argument
# and returns a  new  codon dictionary where:
# key = codon_triplet (e.g. AAA , AUG , etc.)
# value = [amino_acid_abbr1 ,amino_acid_abbr2 , full_name]
def create_codon_dictionary(filename):
    dna_codons = open(filename)
    codon_dictionary = {}
    #key is codon, list is abbr, fullname, amino 3 letter code
    for line in dna_codons:
        line_list = line.strip().split(',')
        if(line_list[0] not in codon_dictionary):
            codon_key = line_list[0]
            codon_dictionary[codon_key] = line_list[1:]#append list [abbr,letter,full-name]
    dna_codons.close()
    return codon_dictionary




# Program 2:  Creating abbreviation dictionary
# def create_abbreviation_dictionary(codon_dictionary):
# This function takes in a codon dictionary as an argument
# and returns a  new  abbreviation dictionary where:
# key = amino_acid_abbr2 (i.e.  the single letter abbreviation)
# value = [amino_acid_abbr1 , full_name]
def create_abbreviation_dictionary(codon_dictionary):
    abbreviation_dictionary = {}
    for elem in codon_dictionary:
        abbreviation_dictionary[codon_dictionary[elem][1]] = [codon_dictionary[elem][0],codon_dictionary[elem][2]]
    return abbreviation_dictionary


# Program 3:  Fasta file to string
# def fasta_to_string(filename):
# This function takes in a filename as an argument
# and returns a  string of genomic sequence
def fasta_to_string(filename):
    fastaString = ""
    with open(filename, 'r') as file:
        file.readline()
        temp = file.read()
        for char in temp:
            if 65 <= ord(char) <= 90:
                fastaString = fastaString + char
    return fastaString


# Program 4:  Translate
# def translate(genome,codon_dictionary,start_seq,stop_seq):
# This function takes in a genome string, codone dictionary, start
# sequence string and stop sequence string as arguments
# and returns a translated string of single letter amino acid abbreviations
def translate(genome,codon_dictionary,start_seq,stop_seq):
    result = ""
    for item in range (len(start_seq), genome.find(stop_seq), 3):
        abbrev = genome[item : item + 3]
        result = result + codon_dictionary[abbrev][1]
    return result

# Program 5:  Counter
# def count (char, string):
# counter function takes in a character and a string as arguments
# and counts how many times the character occurs in the string
# returns an integer number of occurences
def count (char, string):
    count = 0
    for item in string:
        if item == char:
            count = count + 1
    return count

#done:step 1 read in the fasta file
filename = "NC_045512.fasta"
genome = fasta_to_string(filename)

#done: step 2 create codon dictionary
filename = "codon_to_amino.csv"
codon_dictionary = create_codon_dictionary(filename)


#done: step 3 create abbreviation to full name dictionary
abbr_amino_dictionary = create_abbreviation_dictionary(codon_dictionary)


#done: step 4 Translate the Sequence from FASTA to coded
start_seq = genome[0:265]     #5' UTR Start Sequence 1..265
stop_seq = genome[29674:29903]#3'UTR stop sequence  29675..29903
encoded_genome = translate(genome, codon_dictionary, start_seq, stop_seq)


#done: step 5 get glycoprotein substring from encoded_genome
surf_start = 7099
surf_end = 8372
glycoprotein = encoded_genome[surf_start:surf_end]


#done: step 6 print out table using abbr_amino_dictionary
for item in abbr_amino_dictionary:
    print(item, abbr_amino_dictionary[item][0], "\t", abbr_amino_dictionary[item][1])


#done: step 7 user command line interface
while True:
    answer = input("\nTo view the translated surface glycoprotein enter 1\n"\
    "To view the sars-cov-2 genome enter 2\n"\
    "Or enter in a protein abbreviation to check if in the Spike Glycoprotein (3 to exit):\n")
    if (answer == '1'):
        print("Translated surface glycoprotein: \n",glycoprotein)
    elif (answer == '2'):
        print("SARS_COV-2 genome: \n", genome)
    elif (answer == '3'):
        print("Thank you!")
        break
    elif (not answer):
        print("Empty input. Please try again.\n")
    else:
        if(answer in abbr_amino_dictionary):
            if (answer not in glycoprotein):
                print(abbr_amino_dictionary[answer][1], "(", answer, ") is not in the spike protein")
            else:
                print(abbr_amino_dictionary[answer][1], "(", answer, ") is in the spike protein and is coded for ", count(answer, glycoprotein)," times\n")
        else:
            print("Wrong input. Please try again.\n")