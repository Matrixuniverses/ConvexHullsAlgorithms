"""
   Convex Hull Assignment: COSC262 (2018)
   Student Name: Sam Shanand
   Usercode: sjs227
"""


import matplotlib as mtp
import convexhull as cvh
import time
import sys


def validity_test(datasets):
    """ Method to check outputs of algorithms is correct
    """
    
    print('=' * 80)
    print('Dataset\t\tExpected output?\tTime taken')
    print('=' * 80)

    # Loading the verification file
    verify_raw = open('verify.txt')
    verify_lines = verify_raw.readlines()
    verify_raw.close()
    verify_lines = [x.strip() for x in verify_lines]

    for algorithm in [cvh.grahamscan, cvh.giftwrap]:
        print('Algorithm: {0}'.format(algorithm.__name__))
         
        for index, dataset in enumerate(datasets):
            exp_out = verify_lines[index]
            start = time.time()
            act_out = str(algorithm(cvh.readDataPts('Sets/' + dataset + '.dat', int(dataset[2:]))))
            print('{0}\t\t{1}'.format(dataset, exp_out == act_out), end='')
            print('\t\t\t{0:.4f} ms'.format((time.time() - start) * 1e3))
        print()


def grapher(dataset):
    """ Uses matplotlib to graph the times of the algorithms
    """ 
    
    # Loading verification file
    verify

    


def main():
    """ Main method for entry to program
    """
    
    dataset = ['A_3000', 'A_6000', 'A_9000', 'A_12000', 'A_15000', 'A_18000', 'A_21000', 'A_24000', 'A_27000', 'A_30000', 'B_3000', 'B_6000', 'B_9000', 'B_12000', 'B_15000', 'B_18000', 'B_21000', 'B_24000', 'B_27000', 'B_30000']      
    print("Choose option:\n (1) Text output\n (2) Graphical output\n (3) Both")
    sel = input()

    if sel not in ["1","2", "3"]:
        print("Invalid selection, exiting")
        sys.exit(1)
    elif sel == "1":
        validity_test(dataset)
    elif sel == "2":
        print("\tWarning: Graph generation may take some time\n")
        sys.wait(3)
        grapher(dataset)
    else:
        print("\tWarning: Graph generation may take some time\n")
        validity_test(dataset)
        grapher(dataset)



if __name__ == "__main__":
    main()
