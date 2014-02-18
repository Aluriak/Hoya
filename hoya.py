# -*- coding: utf-8 -*-
#########################
#       HOYA            #
#########################


#########################
# IMPORTS               #
#########################
from project import Project
from sys import *
from path import path
import re
import arrow # time management
import pickle  # optimized cPickle charged if possible : 
        # stackoverflow.com/questions/19191859/what-difference-between-pickle-and-pickle-in-python-3






#########################
# PRE-DECLARATIONS      #
#########################
# DEBUG
DEBUG = False
#DEBUG = True
# FILENAMES
HOYA_FILE_SAVE_HOYA = 'data/hoya'
# REGEX
CMD_ADD = re.compile(r"""add( +(.*)|) *""")
CMD_RET = re.compile(r"""ret *""")
CMD_PRINT = re.compile(r"""(ls|print) *""")
CMD_SAVE = re.compile(r""":?([Ww]|save|Save|write) *""")
CMD_QUIT = re.compile(r""":?([Qq]|exit) *""")
CMD_HELP = re.compile(r""":?([Hh]|help!?) *""")
# HELP
HELP = """\tHOYA HELP

add:            add a new project
ret:            retract the last project
print,ls:       print the chronological reversed list of projects
save,w:         save modifications in database
quit,q,exit:    quit Hoya without saving
"""





#########################
# CLASS                 #
#########################
class Hoya(object):
        """Manage project, give to them dates and durations, creat new ones..."""

################ CONSTRUCTOR ################
        def __init__(self):
                """Theses things must be done one single time !"""
                self.nextDate = arrow.utcnow()
                self.nextDate = self.nextDate.replace(day=1)
                self.projects = []
                        



################ ADD PROJECT ################
        def addProject(self, name, description):
                """Add given project with given parameters
                name: string
                description: string"""
                # add project at the begining of projects list
                self.projects.append(Project(name, description, self.nextDate))
                # copy model to project emplacement
                self.__creatProjectTree()
                # Next date is in one month
                self.nextDate = self.nextDate.replace(months=+1, day=1)
                #print("DEBUG: month is now "+self.nextDate.format('YYYY, MMMM', locale='fr_FR'))


################ RET PROJECT ################
        def retProject(self):
                """Retract last project of list"""
                # remove last element of list
                self.projects.pop()
                # Next date is one month ago
                self.nextDate = self.nextDate.replace(months=-1, day=1)
                #print("DEBUG: month is now "+self.nextDate.format('YYYY, MMMM', locale='fr_FR'))


################ CREAT PROJECT TREE ################
        def __creatProjectTree(self):
                """PRIVATE METHOD.
                Creat tree of directory and files from the model to the final project directory of the last project.
                The project directory is named like _monthnumber__year_"""
                # get last project
                prj = self.lastProject()
                # creat substractions
                subs = {
                        'PROJECTNAME': prj.name,
                        'PROJECTDESCRIPTION': prj.description
                }
                # targeted directory
                target = path('./projects') / path(
                        self.nextDate.format('YYYY_MM', locale='fr_FR'))
                # do the copy !
                cptree('model', target, subs)


################ EXTEND PROJECT ################
        def extendProject(self, motive):
                """Extend last project to the next month. Given motive will be given in description"""
                self.addProject("[EXTENDED]", motive)


################ LAST PROJECT ################
        def lastProject(self):
                """return last project (the most recent)"""
                return self.projects[-1]


################ PRINT PROJECTS ################
        def printProjects(self):
                """Print each projects in reversed chronology"""
                for prjct in reversed(self.projects):
                        print(prjct)


################ LOAD ################
        @staticmethod
        def load():
                """Load the Hoya class in hoya file."""
                with open(HOYA_FILE_SAVE_HOYA, 'rb') as f:
                        hoya = pickle.load(f)
                return hoya


################ SAVE ################
        @staticmethod
        def save(hoya):
                """Save given Hoya in hoya file. Erase other data."""
                with open(HOYA_FILE_SAVE_HOYA, 'wb') as f:
                        pickle.dump(hoya, f)








#########################
# FUNCTIONS             #
#########################
################ USER SAID YES ################
def userSaidYes(question):
        """True if user answer yes to given question, else False"""
        REGEX_YES_STR = re.compile(r"""([Yy]|yes|YES|oui|OUI|[Oo]|[1-9]+) *""")
        return REGEX_YES_STR.match(input(question))


################ COPY FILE ################
def copyfile(filename, dest, subs):
        """Copy given file named filename to dest name.
        Use of dict subs for substract key by value in file content"""
        if path(filename).isfile():
                with open(filename, 'r') as fi:
                        with open(dest, 'w') as fd:
                                for l in fi:
                                        for key, val in subs.items():
                                                #print("DEBUG 2: "+key+" "+val)
                                                l = l.replace(key, val)
                                        fd.write(l)
        else:
                assert path(filename).isdir(), "filename not a directory or a file"



################ COPY DIRECTORY ################
def cptree(dirname, dest, subs):
        """Do a recursive copy of dirname directory, named dest, destroy if exist.
        Use of dict subs for substract key by value in each file"""
        # delete and recopy the destination tree
        path(dest).rmtree_p()
        path.copytree(dirname, dest)
        # for each file of source, copy with modification
        for f in path(dirname).walk():
                copyfile(f, path(dest) / f.relpath(dirname), subs)










#########################
# MAIN                  #
#########################
if __name__ == '__main__':
        #DEBUG
        #hoya = Hoya()
        #Hoya.save(hoya)
        #DEBUG

        hoya = Hoya.load()
        finish = False
        while not finish:
                cmd = input("?>")
                # ADDING
                if CMD_ADD.search(cmd):
                        vals = CMD_ADD.findall(cmd)[0]
                        #name, description = CMD_ADD.findall(cmd)[0] # find values under parenthesis in regex
                        print(vals)
                        name = input("name ? ")
                        description = input("description ? ")
                        hoya.addProject(name, description)
                        print("!>"+name+" project added !")

                # RETRACTING
                elif CMD_RET.search(cmd):
                        project = hoya.lastProject()
                        if DEBUG or userSaidYes("!>Delete project "+project.name+" ? "): 
                                hoya.retProject()
                                print(project.name+" project retracted !")

                # PRINTING
                elif CMD_PRINT.search(cmd):
                        hoya.printProjects()

                # SAVING MODIFICATIONS
                elif CMD_SAVE.search(cmd):
                        if DEBUG or userSaidYes("!>Save ? "): Hoya.save(hoya)

                # QUIT WITHOUT SAVING 
                elif CMD_QUIT.search(cmd):
                        if DEBUG or userSaidYes("!>Quit (no saving by this way) ? "): finish = True 
                        
                # HELPING 
                elif CMD_HELP.search(cmd):
                        print(HELP)
                        





