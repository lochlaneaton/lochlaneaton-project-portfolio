import sys
import math
import string


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X={char: 0 for char in string.ascii_uppercase}
    with open (filename,encoding='utf-8') as f:
        # TODO: add your code here
        for line in f:
            for char in line:
                char = char.upper()
                if char.isalpha() and char in X:
                    if char in X:
                        X[char] += 1

    alphabet_vector = {key: value for key, value in sorted(X.items())}  
              

    return alphabet_vector

# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!

''' Q1: print the list of alphabetic values and their counts'''
def output_shred(filename):
    vector = shred(filename)
    for key in vector:
        print(key, vector[key])

''' Q2: Compute the probability of the first letter in the alphabet vector to make sure you are 
        on the right track for Q3'''

def check_conditional_prob(file):
    prob_list = []
    with open (file, encoding = 'utf-8') as f:
        for line in f:
            prob_list.append(float(line[1:]))
    values_list = list(shred(sys.argv[1]).values())

    print(f'{values_list[0]*math.log(prob_list[0]):.4f}')


''' Q3:  Compute the probability that the letter is either written in English or Spanish 
        given the vector of alphabetic characters from the letter ''' 
def F(vector, file, prior):
    prob_list = []
    values_list = list(vector.values())
    F = math.log(prior)

    with open (file, encoding = 'utf-8') as f:
        for line in f:
            prob_list.append(float(line[1:]))
        for i in range(len(vector)):
            F += values_list[i] * math.log(float(prob_list[i]))
    return f'{F:.4f}'

''' Q4: Compute the probablity that the document is in English given the vector of alphabetic characters.'''
def e_prob(vector, s_prior, e_prior):

    if (float(F(vector, 's.txt', s_prior)) - float(F(vector, 'e.txt', e_prior))) >= 100:
        prob = 0
    elif (float(F(vector, 's.txt', s_prior)) - float(F(vector, 'e.txt', e_prior))) <= -100:
        prob = 1
    else:
        prob = 1 / (1 + math.exp(float(F(vector, 's.txt', s_prior)) - float(F(vector, 'e.txt', e_prior))))

   
    return prob

# Outputs 

print("Q1")
file = sys.argv[1]
vector = shred(filename=file)
q1 = output_shred(filename=file)

print("Q2")
check_conditional_prob('e.txt')
check_conditional_prob('s.txt')

print("Q3")
prior_e = float(sys.argv[2])
q3 = F(vector, 'e.txt', prior_e)
print(q3)

prior_s= float(sys.argv[3])
q3 = F(vector, 's.txt', prior_s)
print(q3)

print("Q4")
e_prior = sys.argv[2]
s_prior = sys.argv[3]
prob = e_prob(vector=vector, e_prior=prior_e, s_prior=prior_s)
print(f'{prob:.4f}')