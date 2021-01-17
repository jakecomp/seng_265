#!/usr/bin/env python3

import argparse
import os
import sys
import csv

order_of_args = []
Master_dict = {}

# A custom action to determine the order of arguments passed via the command line
class customAction(argparse.Action):
    def __call__(self, parser, args, values, option_string = None):

        if(self.dest == "Min_field"):
            if(args.Min_field == None):
                args.Min_field = []
            args.Min_field.append(values)

        if(self.dest == "Max_field"):
            if(args.Max_field == None):
                args.Max_field = []
            args.Max_field.append(values)

        if(self.dest == "Sum_field"):
            if(args.Sum_field == None):
                args.Sum_field = []
            args.Sum_field.append(values)

        if(self.dest == "Mean_field"):
            if(args.Mean_field == None):
                args.Mean_field = []
            args.Mean_field.append(values)

        if(self.dest == "Count"):
            if(args.Count != True):
                args.Count = True
                order_of_args.append(self.dest)

            return

        path_name = self.dest.strip("field")
        order_of_args.append(path_name+values)


def main():

   parser = argparse.ArgumentParser()
   count_list = []
   no_arguments = False
   line = 0
   total_lines = 0
   just_count = 0
   first_min_call = True
   first_mean_call = True
   first_sum_call = True
   first_max_call = True
   non_numeric_flag = False
   value = 0
   other_flag = False


   # Get our command line arguments
   parser.add_argument("--top",dest="Collection",nargs=2,help="Computes the k most occurrences")
   parser.add_argument("--input",dest="Input",required="True",help="input file")
   parser.add_argument("--min",action=customAction,dest="Min_field",help="compute the min value")
   parser.add_argument("--max",action=customAction,dest="Max_field",help="compute the max value")
   parser.add_argument("--mean",action=customAction,dest="Mean_field",help="compute the average value")
   parser.add_argument("--sum",action=customAction,dest="Sum_field",help="compute the sum of specified values")
   parser.add_argument("--count",nargs=0, action=customAction,dest="Count",help="Display number of records")
   parser.add_argument("--group-by",dest="group_by",help="Group via category")

   args = parser.parse_args()


   # Check if file is empty
   #if(os.stat(args.Input).st_size == 0):
       #sys.stderr.write('ERROR: %s is an empty file \n' % args.Input)
       #sys.exit(6)

   # Check if the file intended for input is a valid csv file
   if(args.Input.endswith('.csv') != True):
       sys.stderr.write('ERROR: %s: Input file must be a .csv \n' % args.Input)
       sys.exit(6)
   try:
       data = open(args.Input,mode = 'r',encoding = 'utf-8-sig')
           #data_reader = csv.DictReader(data)
   except:
       sys.stderr.write('ERROR: %s: Input file could not be open or could not be found \n' % args.Input)
       sys.exit(6)
   if(os.stat(args.Input).st_size == 0): #Check if the file is empty
       sys.stderr.write('ERROR: %s is an empty file \n' %args.Input)
       sys.exit(6)
   else:
       data_reader = csv.DictReader(data)
   # If no other arguments where passed just count the records in the file
   if(args.Min_field == None and args.Max_field == None and args.Mean_field == None and args.Sum_field == None and args.group_by == None and args.Collection == None and args.Count == None):
       args.Count = True
       no_arguments = True


   # Get the order of arguments
   args_list = sys.argv

   # Now check to see if there are any invalid field names refrenced by our arguments
   field_names = data_reader.fieldnames
   no_such_field = True
   for i in args_list:
       line+=1
       if(i.startswith('--') and not i.endswith('input') and not i.endswith('--count')):
           if(i == '--top'):
                try:
                   k_value = int(args.Collection[0])
                except:
                   sys.stderr.write('ERROR:argument call --top k field_name: k must be an int \n')
                   sys.exit(6)
                for name in field_names:
                    if(args_list[line+1] == name):
                        no_such_field = False
                        break
                    else:
                        no_such_field = True
                if(no_such_field):
                    sys.stderr.write('ERROR: no such field with name %s found \n' %args_list[line+1])
                    sys.exit(9)
           else:
                for name in field_names:
                    if(args_list[line]==name):
                        no_such_field = False
                        break
                    else:
                        no_such_field = True
                if(no_such_field):
                    sys.stderr.write('ERROR: no such field with name %s found \n' %args_list[line])
                    sys.exit(9)


   # First, if our only argument is our input file, just count the records in the file
   if(no_arguments != False):
       Master_dict["Count"] = {}
       line_num = 0
       for row in data_reader:
           line_num+=1
       Master_dict["Count"] = line_num


   # Check if we are in group-by mode
   elif(args.group_by != None):
       line_count = 0

       group_values = group_by(args.Input,args.group_by) #Get the field we will be grouping by


       # With the exception of group-by and top-k we will only traverse through the input file once
       for row in data_reader:
           line_count+=1

            # Check if --min was called, and if so perfrom the "min" logic
           if(args.Min_field != None):

               if(first_min_call):
                   error_counter = {}
                   first_min_call = False
                   for names in group_values:
                       error_counter[names] = {}
                       for group in args.Min_field:
                           error_counter[names]["Min_"+group] = 0

               for group in args.Min_field:
                   # Check for non-numeric values
                   try:
                       value = float(row[group])
                   except:
                      error_counter[row[args.group_by]]["Min_"+group]+=1
                      sys.stderr.write('ERROR: non-numeric value on line %s in  %s  \n' %(line_count, group))
                      if(error_counter[row[args.group_by]]["Min_"+group]>100):
                          sys.stderr.write('ERROR: cannot compute min: Over 100 non-numeric values in Min_%s \n' %row[args.group_by])
                          sys.exit(7)
                   # Check if we have a record of the min for that group
                   if("Min_"+group in Master_dict[row[args.group_by]]):
                      if(value < Master_dict[row[args.group_by]]["Min_"+group]):
                          Master_dict[row[args.group_by]]["Min_"+group] = value
                   # If no record was found, check if our current group is in our "group" dictionary
                   elif(row[args.group_by] in group_values):
                       Master_dict[row[args.group_by]]["Min_"+group] = value
                   else:
                       #If the group is not in our "group" dictionary check our "_OTHER" dictionary
                       if("min_"+group in Master_dict["_OTHER"]):
                           if(value < Master_dict["_OTHER"]["Min_"+group]):
                               Master_dict["_OTHER"]["Min_"+group] = value
                           else:
                               Master_dict["_OTHER"]["Min_"+group] = value

            # Check if --max was called, and if so perform the "max" logic
           if(args.Max_field != None):

               if(first_max_call != False):
                   error_counter = {}
                   first_max_call = False
                   for names in group_values:
                       error_counter[names] = {}
                       for group in args.Max_field:
                           error_counter[names]["Max_"+group] = 0

               for group in args.Max_field:
                   # Check for any non-numeric values
                   try:
                       value = float(row[group])
                   except:
                       error_counter[row[args.group_by]]["Max_"+group]+=1
                       sys.stderr.write('ERROR: non-numeric value on line %s in %s: \n' %(line_count, group))
                       if(error_counter[row[args.group_by]]["Max_"+group]>100):
                           sys.stderr.write('ERROR: cannot compute max: Over 100 non-numeric values in %s \n' %row[args.group_by])
                           sys.exit(7)
                    # Check to see if we have a record of the max for that group
                   if("Max_"+group in Master_dict[row[args.group_by]]):
                      if(value>Master_dict[row[args.group_by]]["Max_"+group]):
                          Master_dict[row[args.group_by]]["Max_"+group] = value
                   # If no record was found check to see if the current group is in the "group" dictioanry
                   elif(row[args.group_by] in group_values):
                       Master_dict[row[args.group_by]]["Max_"+group] = value
                   else:
                       # If group is not in our "group"dictionary check our "_OTHER" dictioanry
                       if("Max_"+group in Master_dict["_OTHER"]):
                           if(value > Master_dict["_OTHER"]["Max_"+group]):
                               Master_dict["_OTHER"]["Max_"+group] = value
                           else:
                               Master_dict["_OTHER"]["Max_"+group] = value

            # Check if --sum was called, and if so perform the "sum" logic
            # The overall structure is very similar to our "min" and "max"
            # with the exception that we will just append our valid values for each group
           if(args.Sum_field != None):
               if(first_sum_call != False):
                   error_counter = {}
                   first_sum_call = False
                   for names in group_values:
                       error_counter[names] = {}
                       for group in args.Sum_field:
                           error_counter[names]["Sum_"+group] = 0

               for group in args.Sum_field:
                   try:
                       value = float(row[group])
                   except:
                       error_counter[row[args.group_by]]["Sum_"+group]+=1
                       sys.stderr.write('ERROR: non-numeric value on line %s in %s \n' %(line_count,group))
                       if(error_counter[row[args.group_by]]["Sum_"+group]>100):
                           sys.stderr.write('ERROR: cannot compute sum: over 100 non-numeric values in %s \n' %row[args.group_by])
                           sys.exit(7)
                   if("Sum_"+group in Master_dict[row[args.group_by]]):
                       Master_dict[row[args.group_by]]["Sum_"+group]+=value
                   elif(row[args.group_by] in group_values):
                       Master_dict[row[args.group_by]]["Sum_"+group] = value
                   else:
                       if("Sum_"+group in Master_dict["_OTHER"]):
                           Master_dict[row[args.group_by]]["Sum_"+group]+=value

                       else:
                           Master_dict["_OTHER"]["Sum_"+group] = value

           # Check if --mean was called, and if so perform the "mean" logic
           # "Mean" does essentially the same thing as "sum". I tried implementing
           # mean to be computed on the fly, however I got more consistent results once
           # I iterated through the entire file, then simply divide the sum of each required field
           # by the corresponding "Count" for that group
           if(args.Mean_field != None):

               if(first_mean_call != False):
                   error_counter = {}
                   for names in group_values:
                       error_counter[names]={}
                       for group in args.Mean_field:
                           error_counter[names]["Mean_"+group] = 0

               for group in args.Mean_field:
                   try:
                       value = float(row[group])
                   except:
                       error_counter[row[args.group_by]]["Mean_"+group]+=1
                       sys.stderr.write('ERROR: non-numeric value on line %s in %s \n' %(line_count,group))
                       if(error_counter[row[args.group_by]]["Mean_"+group]>100):
                           sys.stderr.write('ERROR: cannot compute mean: over 100 non-numeric values in %s \n' %row[args.group_by])
                           sys.exit(7)
                   if(first_mean_call != False):
                       Master_dict[row[args.group_by]]["Mean_"+group] = value
                       first_mean_call = False
                   elif("Mean_"+group in Master_dict[row[args.group_by]]):
                       Master_dict[row[args.group_by]]["Mean_"+group]+=value
                   elif(row[args.group_by] in group_values):
                       Master_dict[row[args.group_by]]["Mean_"+group] = value
                   else:
                       if("Mean_"+group in Master_dict["_OTHER"]):
                           Master_dict["_OTHER"]["Mean_"+group]+=value
                       else:
                           Master_dict["_OTHER"]["Mean_"+group] = value



        # Once we are done iterating through our file, compute the mean of each group for each of
        # their corresponding "mean" fields
       if(args.Mean_field != None):

           for group in group_values:
               for names in args.Mean_field:
                   Master_dict[group]["Mean_"+names] = (Master_dict[group]["Mean_"+names])/Master_dict[group]["Count"]


        # Check if top-k was called
       if(args.Collection != None):
           top_values = top(args.Input,args.Collection[0],args.Collection[1],group_values)

   # If we are not in "group" mode we will perform the required functions for the entire table
   else:
     Master_dict["TABLE"] = {} #This dictioanry will store all the data of the entire file
     line_count = 0


     # With the exception of top-k, we will traverse through the entire input file once
     for row in data_reader:
         line_count+=1

         # Check if --min was called, and if so perform the "min" logic
         # The structure of the section is very similar to the min in group mode
         # with the exception of just finding the min of the entire field
         if(args.Min_field != None):

             if(first_min_call != False):
                 error_counter = {}
                 first_min_call = False
                 for group in args.Min_field:
                     error_counter["Min_"+group] = 0

             for group in args.Min_field:
                 # Check for non-numeric values
                 try:
                     value = float(row[group])
                 except:
                     error_counter["Min_"+group]+=1
                     sys.stderr.write('ERROR: non-numeric value on line %s in %s \n' %(line_count,group))
                     if(error_counter["Min_"+group]>100):
                         sys.stderr.write('ERROR: cannot compute min: over 100 non-numeric values in %s \n' %group)
                         sys.exit(7)
                 if("Min_"+group in Master_dict["TABLE"]):
                     if(value<Master_dict["TABLE"]["Min_"+group]):
                         Master_dict["TABLE"]["Min_"+group] = value
                 else:
                    Master_dict["TABLE"]["Min_"+group] = value

         # Check if --max was called, and if so perform the "max" logic
         # The structure of the section is very similar to the max in group mode
         # with the exception of just finding the max of the entire field
         if(args.Max_field != None):

             if(first_max_call != False):
                 error_counter = {}
                 first_max_call = False
                 for group in args.Max_field:
                     error_counter["Max_"+group] = 0


             for group in args.Max_field:
                # Check for non-numeric values
                try:
                    value = float(row[group])
                except:
                    error_counter["Max_"+group]+=1
                    sys.stderr.write('ERROR: non-numeric value on line %s in %s \n' %(line_count,group))
                    if(error_counter["Max_"+group]>100):
                        sys.stderr.write('ERROR: cannot compute max: over 100 non-numeric values in %s \n' %group)
                        sys.exit(7)
                if("Max_"+group in Master_dict["TABLE"]):
                    if(value>Master_dict["TABLE"]["Max_"+group]):
                        Master_dict["TABLE"]["Max_"+group] = value
                else:
                   Master_dict["TABLE"]["Max_"+group] = value

         # Check if --sum was called, and if so perform the "sum" logic
         # The structure of the section is very similar to the sum in group mode
         # with the exception of just finding the sum of the entire field
         if(args.Sum_field != None):

             if(first_sum_call != False):
                 error_counter ={}
                 first_sum_call = False
                 for group in args.Sum_field:
                     error_counter["Sum_"+group] = 0

             for group in args.Sum_field:
                # Check for non-numeric values
                try:
                    value = float(row[group])
                except:
                    error_counter["Sum_"+group]+=1
                    sys.stderr.write('ERROR: non-numeric value on line %s in %s \n' %(line_count,group))
                    if(error_counter["Sum_"+group]>100):
                        sys.stderr.write('ERROR: cannot compute sum: over 100 non-numeric values in %s \n' %group)
                        sys.exit(7)
                if("Sum_"+group in Master_dict["TABLE"]):
                    Master_dict["TABLE"]["Sum_"+group]+=value
                else:
                    Master_dict["TABLE"]["Sum_"+group] = value

         # Check if --mean was called, and if so perform the "mean" logic
         # The structure of the section is very similar to the mean in group mode
         # with the exception of just finding the sum of the entire field,
         # then computing the mean of the field once we are done iterating through the input file
         if(args.Mean_field != None):

             if(first_mean_call != False):
                 error_counter = {}
                 first_mean_call = False
                 for group in args.Mean_field:
                     error_counter["Mean_"+group] = 0

             for group in args.Mean_field:
                 # Check for non-numeric values
                 try:
                     value = float(row[group])
                 except:
                     error_counter["Mean_"+group]+=1
                     sys.stderr.write('ERROR: non-numetic value on line %s in %s \n' %(line_count,group))
                     if(error_counter["Mean_"+group]>100):
                         sys.stderr.write('ERROR: cannot compute mean: over 100 non_numeric values in %s \n' %group)
                         sys.exit(7)
                 if("Mean_"+group in Master_dict["TABLE"]):
                    Master_dict["TABLE"]["Mean_"+group]+=value
                 else:
                    Master_dict["TABLE"]["Mean_"+group] = value

     # After iterating through the input file, if --mean was called
     # compute the mean for each mean field
     if(args.Mean_field != None):

         for group in args.Mean_field:
             Master_dict["TABLE"]["Mean_"+group] = Master_dict["TABLE"]["Mean_"+group]/line_count


     # If count was called, append a count key to our "TABLE" dictionary
     # and set the value to the number of records in the input file
     if(args.Count != None):
         Master_dict["TABLE"]["Count"] = line_count
         #print(Master_dict)

     if(args.Collection != None):
         top_values = top(args.Input,args.Collection[0],args.Collection[1])
         #sorted_top_values = sorted(top_values.items(),key=lambda x:x[1],reverse=True)

   # Print our output in the csv file format
   output_writer = csv.writer(sys.stdout)
   headers = []
   if(no_arguments != False):
       row = []
       headers.append("Count")
       row.append(Master_dict["Count"])
       output_writer.writerow(headers)
       output_writer.writerow(row)
   else:
       if(args.group_by != None):
           headers.append(args.group_by)
           headers.append('Count')

       if(args.Collection != None):
           headers.append('top_%s_%s' %(args.Collection[0],args.Collection[1]))

       for record in order_of_args:
          headers.append(record)
       output_writer.writerow(headers)

       for group in Master_dict:
         row =[]
         if(args.group_by != None):
           row.append(group)
           row.append(Master_dict[group]["Count"])

         if(args.Collection != None):
           row.append(top_values)

         for record in order_of_args:
           row.append(Master_dict[group][record])

         output_writer.writerow(row)

# The group by method
def group_by(input_file,field_name):

    with open(input_file, mode = 'r', encoding = 'utf-8-sig') as data:
     data_reader = csv.DictReader(data)
     dictionary={}
     line = 0
     unique_counter = 0
     error_counter = 0
     count = 0
     over_flow_flag = False

     for row in data_reader:
      if(unique_counter>20):
          # Check if there is more than 20 unqiue groups and handle approproatley
          if(over_flow_flag != True):
              sys.stderr.write('WARNING:Groups in %s have been capped to 20 unique values' %field_name)
              Master_dict["_OTHER"] = {}
              Master_dict["_OTHER"]["Count"] = 1
              over_flow_flag = True
          elif(unique_counter>100):
              sys.stderr.write('ERROR: %s has a high cardinality, cannot perform a meaningful grouping method\n' %field_name)
              sys.exit(9)
          else:
              Master_dict["_OTHER"]["Count"]+=1
      elif(row[field_name] not in Master_dict):
       dictionary[row[field_name]] = 1
       Master_dict[row[field_name]] = {}
       Master_dict[row[field_name]]["Count"] = 1
       unique_counter = unique_counter+1
      else:
          Master_dict[row[field_name]]["Count"]+=1

    return dictionary

# My implementation of top-k, unfortunatley I could not get it working with the group-by function
def top(input_file,k_value,field_name,group_values = None):

 with open(input_file,mode = 'r',encoding = 'utf-8-sig') as data:
     data_reader = csv.DictReader(data)
     line = 0
     unique_counter=0
     dictionary={}
     dup_dictionary={}
     error_counter=0
     over_flow_flag = False # I made these flags as I wanted to only print the error messages once
     high_card = False
     if(group_values == None):
         for row in data_reader:
             if(over_flow_flag != True and unique_counter>20):
                 sys.stderr.write("WARNING: top for %s has been capped to 20 distinct values \n" %field_name)
                 over_flow_flag = True
                 other_flag = True
             elif(unique_counter>100 and high_card != True):
                 sys.stderr.write("WARNING: top for %s has high cardinality\n" %field_name)
                 high_card = True
             else:
                 line = line+1
                 if(row[field_name] not in dictionary):
	                 dictionary[(row[field_name])]= 0
	                 unique_counter = unique_counter+1
                 if(row[field_name] in dictionary):
	                 dictionary[(row[field_name])]+=1

         # Check if the k value exceeds the number of unique groups
         if(int(k_value) > unique_counter):
             sys.stderr.write('ERROR: No %s unique values for top: only %s unique values in %s \n' %(k_value,unique_counter,field_name))
             sys.exit(6)
         # Get the top k values for the field as requested
         for num in range(int(k_value)):
             max_key = max(dictionary,key=dictionary.get)
             dup_dictionary.update({max_key:dictionary[max_key]})
             delete_max_key = max(dictionary, key=lambda k: dictionary[k])
             del dictionary[delete_max_key]
     else:
         #My attempt at top-k when the group-by function is called
         for group in group_values:
             dictionary[group] = {}
             for row in data_reader:
                 if('Top_'+field_name not in dictionary[group]):
                     dictionary[group]['Top_'+field_name] = {}
                 if(row[field_name] not in dictionary[group]['Top_'+field_name]):
                     dictionary[group]['Top_'+field_name][row[field_name]] = 1
                 else:
                     dictionary[group]['Top_'+field_name][row[field_name]]+=1
         for row in data_reader:
            for group in group_values:
                keys = list(dictionary[group]['Top_'+field_name].keys())
                values = list(dictionary[group]['Top_'+field_name].values())
                dictionary[group]['Top_'+field_name] = {}
                for num in range(int(k_value)):
                    max_key = max(dictionary[group]['Top_'+field_name][row[field_name]],key=dictionary[group]['Top_'+field_name][row[field_name]].get)
                    dup_dictionary.update({max_key:dictionary[group]['Top_'+field_name][max_key]})
                    delete_max_key = max(dictionary[group]['Top_'+field_name][row[field_name]], key=lambda k: dictionary[group]['Top_'+field_name][k])
                    del dictionary[group]['Top_'+field_name][delete_max_key]


 return dup_dictionary


if __name__ == '__main__':
     main()
