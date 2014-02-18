# -*- coding: utf-8 -*-
#########################
#       PROJECT         #
#########################


#########################
# IMPORTS               #
#########################
import arrow


#########################
# PRE-DECLARATIONS      #
#########################



#########################
# CLASS                 #
#########################
class Project(object):
        """Definition of a project"""

        def __init__(self, name, description, beginDate):
                """Wait for those parameters:
                name: string
                description: string
                beginDate: arrow date
                """
                self.name = name
                self.description = description
                self.begin = beginDate





        def __str__(self):
                """_year_, _month_, _name_: _description_"""
                return "{0}\t {1}: {2}".format(self.begin.format('YYYY, MMMM', locale='fr_FR'), self.name, self.description)




