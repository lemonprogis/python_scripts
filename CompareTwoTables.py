#-------------------------------------------------------------------------------
# Name:        CompareTwoTables
# Purpose:     Compare two identical datasets for data differences
#
# Author:      kristen
#
# Created:     17/09/2014
#
# Edits: 
#              Ed - 22/07/2015
#-------------------------------------------------------------------------------

import arcpy, os
from itertools import chain

def reportUnmatched(tbl1, fields):
    #get count of selected records
    result = arcpy.GetCount_management(tbl1)
    count = int(result.getOutput(0))
    print str(count) + " records different"

    #prep reporting
    message = "Unmatching records: \n"
    fieldCount = len(fields)

    #if there are different records, loop through for reporting
    if count > 0:

        #report all unmatching records
        with arcpy.da.SearchCursor(tbl1, fields) as cursor:
            for row in cursor:
                #set up field iteration
                i = 0
                while i < fieldCount:
                    message = message + str(row[i]) + ", "
                    #if you want to do something else with the unmatched results, here is where to add it
                    #####################################
                    i += 1

                message = message[0:-2] + "\n"

        print message

    #if no different records, tell the user
    else:
        print "All records matched in this join"

def removeSHP(name):
    #take out .shp of file name
    if ".shp" in name: 
        return name.replace(".shp", "")
    return name

def getCommonFieldNames(table1, table2):

    #list fields of table1
    fieldNames1 = [str(f.name) for f in arcpy.ListFields(table1)]

    #list fields of table2
    fieldNames2 = [str(f.name) for f in arcpy.ListFields(table2)]

    #convert lists to sets
    set1 = set(fieldNames1)
    set2 = set(fieldNames2)

    #see which fields aren't the same
    unmatchingFields = list(set1 ^ set2)

    #report unmatching fields
    print unmatchingFields

    #get the set of fields that are the same
    matchingFields = list(set1 & set2)

    #report matching fields
    print matchingFields

    return matchingFields

def compareTables(table1, joinField1, table2, joinField2):

    #get matching fields
    matchingFields = getCommonFieldNames(table1, table2)

    #make table views
    tbl1 = "tbl1"
    tbl2 = "tbl2"

    arcpy.MakeTableView_management(table1, tbl1)
    arcpy.MakeTableView_management(table2, tbl2)

    #join tables: tbl1 as left
    arcpy.AddJoin_management(tbl1, joinField1, tbl2, joinField2)

    #remove shp if it exists in either table name
    name1 = removeSHP(os.path.basename(table1))
    name2 = removeSHP(os.path.basename(table2))

    #create list of full matching field names
    fullMatchingFields = list(chain.from_iterable((name1 + field, name2 + field) for field in matchingFields))
    where_clauses = ["{}.{} <> {}.{}".format(name1, field, name2, field) for field in matchingFields]

    wc1 = " OR ".join(where_clauses)
    print wc1

    #Run query: tbl1
    lyr1 = "lyr1"
    arcpy.MakeTableView_management(tbl1, lyr1, wc1)

    #report unmatched records
    reportUnmatched(lyr1, fullMatchingFields)
    arcpy.Delete_management(lyr1)

    #remove join
    arcpy.RemoveJoin_management(tbl1)

    #join tables the other direction: tbl2 as left
    arcpy.AddJoin_management(tbl2, joinField2, tbl1, joinField1)

    #just want records where records in tbl1 aren't in tbl2
    wc2 = "{}.{} IS NULL".format(name1, joinField1)
##    print wc2

    #Run query: tbl2
    lyr2 = "lyr2"
    arcpy.MakeTableView_management(tbl2, lyr2, wc2)

    #report unmatching records
    reportUnmatched(lyr2, fullMatchingFields)
    arcpy.Delete_management(lyr2)

    #remove join
    arcpy.RemoveJoin_management(tbl2)
