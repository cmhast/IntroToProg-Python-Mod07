################################
#
# Assignment 7
# Exceptions and Pickle
#
################################
#
# 2021.5.25 Created (c.hast)
#
################################

import pickle

# Some variables

menu = '''
1) Set input file
2) Set output file
3) Pickle something
4) Unpickle something
5) Do something bad that will cause errors
6) Quit
'''
p_menu = '''
1) An integer
2) A string
3) A list
4) A dictionary
5) Nothing: Return to main menu
6) Nothing: close output file and return to main menu
'''
p_menu_little = '''
1) An integer
2) A string
3) Nothing: that is all
'''
file_in = None
file_out = None
file_in_name = ''
file_out_name = ''
choice = int()

###################################
####### Custom Exceptions #########
###################################

# Admittedly, I'm not really doing anything
# interesting with any of these.

class Error(Exception):
    """A module-specific base class is apparently common practice"""
    pass

class UnknownError(Error):
    """Raised when a built-in exception occurs"""
    pass

class FileModeError(Error):
    """Raised when trying to open a file with the wrong mode"""
    pass
    def __init__(self, type):
        self.bad_type = type

class FileNameError(Error):
    """Raised when trying to open a file without first setting a file name"""
    pass

class FileOpenTwiceError(Error):
    """Raised when trying to open a file that is already open"""
    pass

class RangeError(Error):
    """Raised when a user input falls outside an accepted range"""
    pass

class CloseFile(Error):
    """Not really an error, but I'm tired and want to do it this way"""
    pass

class NotReallyAnError(Error):
    """What it says on the tin"""
    pass

###################################
# Functions to manage user inputs #
###################################

def take_choice(max):
    """Take user input and make it an integer"""
    while True:
        tmp = input().strip()
        try:
            tmp = int(tmp)
            # An input of 0 will go back to the next
            # iteration of the main loop.
            if tmp < 0 or tmp > max:
                raise RangeError
            else:
                return tmp
        except ValueError:
            # A way to escape the loop, just because
            if tmp == 'cancel':
                return 0
            print('Please enter a number')
        except RangeError:
            print('Please enter a number from 1 to {}'.format(str(max)))

def take_yesno_choice():
    """Take user input ("yes" or "no") and make it boolean"""
    while True:
        tmp = input().strip()
        try:
            if tmp == 'yes' or tmp == 'y':
                return True
            elif tmp == 'no' or tmp == 'n':
                return False
            # Not much reason to do it this way.
            # But it uses an exception.
            else:
                raise RangeError
        except RangeError:
            print('Please enter "yes" or "no"')

##########################################################
# Functions to manage files
# Kinda weirdly set up, but whatever
#
# To be clear, I added the second function late,
# After realizing choice 1 and 2 would be basically the same
# exact code, with only minor differences, making a function
# to handle both make more sense when writing it all out twice.
##########################################################

def open_file(name, type):
    """Open a file with some error handling"""
    # Note that *closing* the file isn't handled here.
    # It needs to be done by whatever is using the file.
    if type not in ('rb','wb'):
        raise FileModeError(type)
    if name == '':
        raise FileNameError
    try:
        return open(name,type)
    except FileNotFoundError:
        raise
    except Exception as err:
        raise UnknownError from err

def input_and_output(mode, file, method, other):
    """Manage opening input and output files"""
    if mode == 'input':
        action = 'read from'
#        method = 'rb'
    elif mode == 'output':
        action = 'write to'
#        method = 'wb'
    # I'm not bothering to do any fancy handling here...
    else:
        raise Error
    if file is None:
        file_name = input('What file do you want to {0}? > '.format(action)).strip()
        try:
            if file_name == other:
                raise FileOpenTwiceError
            file = open_file(file_name,method)
            return file, file_name
        except FileModeError as err:
            print('Error: "mode" must be rb or wb, instead it was {1}'.format(method,err.bad_type))
            raise Error
        except FileNameError:
            print('You must enter a file name')
            raise Error
        except FileNotFoundError:
            print('The file you are trying to read from does not exist')
            raise Error
        except FileOpenTwiceError:
            if mode == 'input':
                print('That file is already open for output')
            if mode == 'output':
                print('That file is already open for input')  
            raise Error                
    else:
        print('There is already an {0} file open'.format(mode))
        print('Do you want to close it?')
        if take_yesno_choice():
            raise CloseFile

######################################################

def input_to_pickle(nested):
    """Ask user for type then take input"""
    print('What would you like to pickle?')
    # Not allowing nesting. Because I don't want to deal with it.
    if nested:
        tmp_max = 3
        print(p_menu_little)
    else:
        print(p_menu)
        tmp_max = 6
    choice = take_choice(tmp_max)
    if choice == 0:
        raise NotReallyAnError
    elif choice == 1:
        try:
            tmp = int(input('What integer? > ').strip())
            return tmp
        except ValueError:
            print('That is not an integer...')
            raise NotReallyAnError
    elif choice == 2:
        return input('What string? > ').strip()
    elif choice == 3 and not nested:
        tmp_list = []
        while True:
            print('For the next item on the list:')
            try:
                tmp = input_to_pickle(True)
            except NotReallyAnError:
                continue
            if tmp is None:
                break
            if tmp == '':
                print('Do you want to add an empty string to the list?')
                if not take_yesno_choice():
                    break
            tmp_list.append(tmp)
        return tmp_list
    elif choice == 4:
        tmp_dic = {}
        while True:
            print('What is the next key?')
            tmp_k = input('(Enter nothing to finish) > ').strip()
            if tmp_k == '':
                break
            print('For the value of {0}:'.format(tmp_k))
            try:
                tmp_v = input_to_pickle(True)
            except NotReallyAnError:
                print('{0} is not going to be added to the dictionary'.format(tmp_k))
                print('You will have to re-enter it if you want it to be added.')
                tmp_k = ''
                continue
            if tmp_v is None:
                print('Ok, but that does mean{0} will not be added'.format(tmp_k))
                break
            # Does not check for the key already being in the dictionary,
            # Simply overwrites.
            tmp_dic[tmp_k]=tmp_v
        return tmp_dic
    elif choice == 5:
        return None
    elif choice == 3 and nested:
        return None
    elif choice == 6:
        raise CloseFile


###################################
############# Main ################
###################################

while True:
    print(menu)
    choice = take_choice(6)
    
    # Cycle through again
    if choice == 0:
        continue
    # Open input file
    elif choice == 1:
        try:
            file_in, file_in_name = input_and_output('input',file_in,'rb',file_out_name)
        except CloseFile:
            file_in.close()
            file_in = None
            file_in_name = ''
        except Error:
            continue
    # Open output file
    elif choice == 2:
        try:
            file_out, file_out_name = input_and_output('output',file_out,'wb',file_in_name)
        except CloseFile:
            file_out.close()
            file_out = None
            file_out_name = ''
        except Error:
            continue
    # Pickle something
    elif choice == 3:
        if file_out is None:
            print('There must be an output file')
            continue
        while True:
            try:
                tmp = input_to_pickle(False)
            except CloseFile:
                file_out.close()
                file_out = None
                file_out_name = ''
                break
            except NotReallyAnError:
                continue
            if tmp is None:
                del tmp
                break
            pickle.dump(tmp,file_out)
    # Unpickle something
    elif choice == 4:
        if file_in is None:
            print('There must be an input file open')
            continue
        while True:
            try:
                tmp = pickle.load(file_in)
                if type(tmp) == int:
                    print('The next unpickled object is an integer')
                    print('It\'s value is:',tmp)
                if type(tmp) == str:
                    print('The next unpickled object is a string')
                    print('It\'s value is:',tmp)
                if type(tmp) == list:
                    print('The next unpickled object is a list')
                    print('It\'s values are:')
                    for i in tmp:
                        print(i)
                if type(tmp) == dict:
                    print('The next unpickled object is a dictionary')
                    print('It\'s entries are:')
                    for i in tmp.keys():
                        print(i, ': ', tmp[i], sep='')
            except EOFError:
                print('That\'s all in that file')
                break
            except pickle.UnpicklingError:
                print('There was a problem unpickling the file.')
                break
        file_in.close()
        file_in = None
        file_in_name = ''
    # Something intended purely to raise an exception
    elif choice == 5:
        try:
            file_in = input_and_output('input',file_in,'r', file_out_name)
        except CloseFile:
            file_in.close()
            file_in = None
            file_in_name = ''
            print('That was less dramatic than expected.')
        except Error:
            print('Hooray! Something bad happened!')
            print('Do you want to see something cool?')
            if take_yesno_choice():
                raise SystemExit
    # Quit
    elif choice == 6:
        print('Goodbye!')
        if not file_in is None:
            file_in.close()
        if not file_out is None:
            file_out.close()
        break
    else:
        print('I honestly have no idea how you got here')
        print('Any invalid choice should have been filtered out')
        print('Congratulations: you broke my script')







    