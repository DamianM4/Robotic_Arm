import re #re to extract integer constants from strings in text file

class file1:
    def read_file_arm(self):  
        with open('setup.txt', 'r') as F:
            lines = F.read().splitlines()

        l1 = lines[0]
        l1 = int(re.search(r'\d+(?!=)', l1).group())#(?!=) adds integer if it is not succeded by '='

        l2 = lines[1]
        l2 = int(re.search(r'\d+(?!=)', l2).group())

        l3 = lines[2]
        l3 = int(re.search(r'\d+(?!=)', l3).group())

        h = lines[3]
        h = int(re.search(r'\d+(?!=)', h).group())
        #constants extracted and ready to use
        constants = (l1, l2, l3, h)
        return constants