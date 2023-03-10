# -*- coding: utf-8 -*-
"""
Created On : Thurs Sep 16 2021
Last Modified : Wed Sep 22 2021
Course : MSBD5002 
Assignment : Assignment 01 Question 02 Part (a)

Remarks:
    - this is meant for final submission
    
"""
import pandas as pd

##################################################################
# First Section is to extract the data before Generating the FP Tree #
# - Will Generate the Frequency Table for each Item
# - and deduce the Ordered Frequent Items
print('-'*70)
print('First Section')
print('Extract Data from the CSV File')
print('Generate the Frequency Table' )
print('Deduce the Ordered Frequent Items')
print('-'*70 + '\n')
##################################################################
### Extract the data from DataSetA.csv to a DataFrame
### Extract the data from CSV to DataFrame
df_original = pd.read_csv("DataSetA.csv",sep='\n',header=None, names = ['Items'])
df_work = df_original.copy() # Make a new copy and preserve the old copy 

# df_work variable will be used for forming the Frequency Table and the table for new Ordered Frequent Items
# Remove the ',' and place everything onto a dataframe
# the items are converted to a list
for row in range(0,len(df_work)):
    str_to_list = df_original.loc[row,'Items'].split(',')
    new_item_list = list(filter(None,str_to_list )) # remove all empty entry in the list
    df_work.loc[row,'Items'] = new_item_list


### This Section will Generate the Frequency Table for the Transactions (Item Sets) in DataSetA.csv
#- df_freq_table_1_sorted variable will store the Frequency Table sorted in descending order
# This section will generate the Frequency Table and store in df_freq_table_1_sorted variable
freq_table_1 = [] 
item_recorder = [] 
# Count each transaction item 
for row in range(0,len(df_work)):
    itemset = df_work.loc[row,'Items']
    for item_n in itemset:
        if item_n not in item_recorder: # If the Item isn't in the Frequency table
            # Add a new Item Row to the Frequency Table
            freq_table_1.append([item_n,1])
            item_recorder.append(item_n) # Record in item recorder
        else: # If the Item is in the Frequency Table
            # Add 1 to the current frequency count
            index = item_recorder.index(item_n) # Get the index of the item in the Frequency Table
            freq_table_1[index][1] += 1

# The Frequency Table will be converted to a dataframe
df_freq_table_1 = pd.DataFrame(freq_table_1, columns = ['Item','Frequency'])            
# The Frequency Table is then sorted in descending order
df_freq_table_1_sorted = df_freq_table_1.sort_values(["Frequency"], ascending=False)
df_freq_table_1_sorted.reset_index(drop=True, inplace = True)
print("Frequency Table")
print(df_freq_table_1_sorted) # Print the whole table
print("\n")


### This Section will Generate a table with the original items reordered according to frequency of item
#- the reorder items will be stored under the column titled "(Ordered) Frequent Items" 
#- the original items will be combined with the new (ordered) items in a new table
#- Store in variable "df_table_for_FP_tree" 

# This section will reorder the items in each transaction according to frequency of item
# - Reorder the items in each transaction
# - Combine the Ordered Frequent Items and the Unordered Items into a New Table for FP Tree generation
freq_table_sorted = df_freq_table_1_sorted['Item'].tolist() # Contain a list of each items
# create another copy of the original dataframe but rename the column to '(Ordered) Frequent Items' 
df_work_ordered_frequent_items = df_work.rename(columns={'Items':'(Ordered) Frequent Items'})
for row in range(0,len(df_work)):
    transaction = df_work.loc[row,'Items']
    ordered_entry = []    
    for item in freq_table_sorted:
        if item in transaction:
            ordered_entry.append(item) # Reorder from Most Frequent to Leaset Frequent
        else:
            pass
    df_work_ordered_frequent_items.loc[row,'(Ordered) Frequent Items'] = ordered_entry # Overwrite with Ordered Items

# Combine both original Unordered Items list and new Ordered Frequent Items list into 1 dataframe (1 Table)
df_table_for_FP_tree = pd.concat([df_work['Items'],df_work_ordered_frequent_items['(Ordered) Frequent Items'] ],axis=1)
# print("New Transaction Table with Original Order and (Ordered) Frequent Items")
# print(df_table_for_FP_tree.head(5)) # Print first 5 rows
# print("\n")

print('Completed First Part')
print('New CSV file was generated "NewDataSetA.csv" '+'\n \n')
### Generate a new CSV file with the new table containing the "(Ordered) Frequent Items" column
### This section is to print the new table into a CSV file.
df_table_for_FP_tree.to_csv('NewDataSetA.csv') # for own record
##################################################################




##################################################################
### Following Section is for Generating the FP Tree ###
print('-'*70)
print('Second Section')
print('Generate the FP Tree Using the Above Data')
print('-'*70 +'\n')
##################################################################
# First determine the Root Nodes for the FP Tree and its respective branches
# Next find the transaction ("(Ordered) Frequent Items") that is the longest length and make it the FP Tree branch
# 

# Variables Used: 
# To store the FP Tree = tree_dict, tree_dict3, tree_dict4
# To store the list of (Ordered) Frequent Items = ordered_frequent_list, ordered_frequent_list3, ordered_frequent_list4
# tree_dict_all = variable will be the final FP tree containing all the possible branches


### Define a Node Class
#- The purpose for this is to record the Node value and the Node Count in the FP-Tree
class Node:
    def __init__(self, value,count=1):
        self.value = value
        self.count = count
        
    def __repr__(self):
        return str(self.value) +":"+ str(self.count)
    
    def all_info(self):
        return [self.value,self.count]

### Create a Function to initialize the Node for each item
def create_new_branch(tree, new_list, branch_num):
    branch = []
    for x in new_list:
        node = Node(x)
        branch.append(node)
    tree['Branch '+str(branch_num)] = branch
    return None



### This Section is to determine the roots for the FP tree
# - find the Roots for the FP Tree and store in "tree_root_tracker_original" variable
ordered_frequent_list = df_work_ordered_frequent_items["(Ordered) Frequent Items"] # Extract only the ordered frequent items
tree_root_tracker_original = [] # This is to record the Nodes that are the Root
branch_num = [] # Records the branch number created (Number of Branches)
branch_count = 0
count = 0
count_list = []
tree_dict = {}
## Find the Root Nodes for the tree by iterating over the "(Ordered) Frequent Items"
for row in ordered_frequent_list:
    # if this is the first branch initialize the Root Node
    if tree_dict == {}:        
        branch_count+=1
        create_new_branch(tree_dict,row,branch_count)
        tree_root_tracker_original.append(tree_dict['Branch 1'][0].value)
        branch_num.append(['Branch 1'])
        count_list.append(count)   
    # if there is no branch with existing Root Nodes, initialize the Root Node
    if row[0] not in tree_root_tracker_original:
        branch_count+=1
        create_new_branch(tree_dict,row,branch_count)
        tree_root_tracker_original.append(tree_dict['Branch '+str(branch_count)][0].value)
        branch_num.append(['Branch '+str(branch_count)])
        count_list.append(count)
    count += 1    


### After determining the Root Nodes
## - find the longest transaction ((Ordered) Frequent Items) that starts with the Root Node
## - add the transaction to the "tree_dict3" to be stored
# Make a copy of the original "(Ordered) Frequent Items"
ordered_frequent_list3 = ordered_frequent_list.copy() 
tree_dict3 = {} 
position_max = [] ## Store the row index that holds the longest length for each Root Node
branch_count = 0
for root in tree_root_tracker_original:
    transaction_count = 0
    max_value = 0
    position_max_value = 0
    for transaction in ordered_frequent_list3:
        if root == transaction[0]:
            # print(root)
            # print(transaction[0])
            if len(transaction)> max_value:
                max_value = len(transaction)
                position_max_value = transaction_count                
        transaction_count +=1
    position_max.append(position_max_value)
    # Update the longest length transaction that starts with the root node
    branch_count+=1
    create_new_branch(tree_dict3, ordered_frequent_list3[position_max_value], branch_count)

## After determining the longest transaction that starts with the Root Nodes
## Remove the longest transaction that was updated to the 'tree_dict3' from 'ordered_frequentlist3' variable
for index in position_max:
    ordered_frequent_list3.drop(index,inplace =True)
ordered_frequent_list3.reset_index(drop = True, inplace = True)

##############
### Remarks for above code: 
# - In Variable ordered_frequentlist3 and tree_dict3:
#   - removed from the list are the longest transaction that was added to the tree_dict3
#   - 11 Transactions was removed from ordered_frequentlist3
#   - 11 Branches was added to the new tree_dict3 
##############


###
### Make a Copy for the following variables for the next program
# - to avoid accidental editing
tree_dict4=tree_dict3.copy()
ordered_frequent_list4 = ordered_frequent_list3.copy()
### This Section will iterate over the remaining (Ordered) Frequent Items (now stored in "ordered_frequent_list4")
# - To check for transactions that has the same items sequence in the 'tree_dict4' variable 
# - but has a transaction length less than or equal to the branches currently in the 'tree_dict4' variable
trans_keep = []   # Stores the transactions ((Ordered) Frequent Items) to be stored into 'tree_dict4'
trans_keep_branchpointer = []  # Stores the new branches name for 'tree_dict4'
trans_keep_index_on_ordered_list = []   # Stores the index position of the transactions ((Ordered) Frequent Items) 
OF_list4_row = 0
for transaction in ordered_frequent_list4:
    branch_num_modify = branch_num.copy()
    for branch in branch_num_modify:       
        check = (len(transaction) <= len(tree_dict4[branch[0]])) and (transaction[0] == tree_dict4[branch[0]][0].value)
        if check:
            item_index = 0
            item_true = []
            for item in transaction:
                if item == tree_dict4[branch[0]][item_index].value:
                    # print(item)
                    item_true.append(True)
                else:
                    item_true.append(False)
                item_index += 1
            if all(item_true) == True:
                trans_keep.append(transaction)
                trans_keep_branchpointer.append(branch[0])
                trans_keep_index_on_ordered_list.append(OF_list4_row)
    OF_list4_row += 1

## This code will update the count for each item in the transaction to the Nodes Count (Item) in tree_dict4 (a copy of tree_dict3)
for x in range(0,len(trans_keep)):
    branch_tree_dict = trans_keep_branchpointer[x]
    transaction_items = trans_keep[x]
    transaction_index = trans_keep_index_on_ordered_list[x]
    for y in range(0,len(transaction_items)):
        tree_dict4[branch_tree_dict][y].count += 1

        
## After Updating the count to the tree dictionary (Variable 'tree_dict4')
## Remove the transaction from  the (Ordered) Frequent Items list (Variable 'ordered_frequent_list4')
for x in range(0,len(trans_keep_index_on_ordered_list)):
    transaction_index = trans_keep_index_on_ordered_list[x]   
    ordered_frequent_list4.drop(transaction_index, inplace = True)
ordered_frequent_list4.reset_index(drop = True, inplace = True)

##############
### Remarks for above code: 
# - In Variable ordered_frequentlist4 and tree_dict4:
#   - removed transactions in the ordered frequent list (Variable ordered_frequent_list4) that was added to the tree dictionary (Variable tree_dict4)
#   - 377 Transactions was removed from ordered_frequentlist4
#   - 377 Transactions was updated to tree_dict4 (a copy of tree_dict3)
##############




### This section will repeatedly iterate over the (Ordered) Frequent Items list (using the While Loop)
# - To do the same as before which is to check for transactions in the (Ordered) Frequent Items list...
# - that has the same items sequence in the branches of the FP tree dictionary (tree_dict_all) but...
# - has a transaction length less than or equal to the branches currently in the tree_dict_all variable 
## Steps Taken: (Using the While Statement)
# - 1. Check if the remaining item sets in the (Ordered) Frequent Items list starts with the Root Node 
# - 2. Determine the next longest length transaction that also starts with the Root Nodes
# - 3. Add the next longest length transaction as a new branch in the tree dictionary
# - 4. After that, iterate over the (Ordered) Frequent Items list
# ...... to check for transactions that has the same items sequence in the tree dictionary
# ...... but has a transaction length less than or equal to the branches currently in the tree dictionary
# - 5. Update the count of each Node (Item) into the tree dictionary
# - 6. Remove the transaction from  the (Ordered) Frequent Items list that was already updated to the tree dictionary
# - 7. Steps are repeated until all of the transactions in the (Ordered) Frequent Items list has been updated to the tree dictionary

###
### Make a Copy for the following variables for the next program
# - to avoid accidental editing
tree_dict_all = tree_dict4.copy() # This variable will be the final FP tree containing all the possible branches
OF_list = ordered_frequent_list4.copy() # by the end of the While Loop, the (Ordered) Frequent Items list will be empty
tree_root_tracker = tree_root_tracker_original.copy() # This variable was taken from the section at Row 137

## Using While Loop
flag = True # Assuming that not all the (Ordered) Frequent Items list has been updated to the tree dictionary
while flag:
    
    ## This code will check if the remaining item sets in the (Ordered) Frequent Items list starts with the Root Node
    # If no item sets starts with the Root node
    # remove the Root Node from the tree_root_tracker
    for root in tree_root_tracker:
        a = False # Assume Root Item is not in Ordered Frequent List
        for item in OF_list: # Checks if any item sets starts with Root Node in Ordered Frequent List
            if root == item[0]:
                a = True
        if a:
            # No changes required
            pass
        else:
            # Remove the Root Node from the tree_root_tracker
            tree_root_tracker.remove(root)
            # print('Root Node ' + root+ ' Done') # Purpose of print is to monitor progress

    
    ## This code will determine the next longest length transaction that also starts with the Root Nodes in the (Ordered) Frequent Items (OF_list)
    # using the updated tree_root_tracker
    # using the updated branch_num 
    position_max = []
    tree_dict_to_add = {} # this is to store the new branches temporarily before appending to the variable 'tree_dict_all' 
    branch_count = len(branch_num) 
    branch_num2 = [] # this is to store the new branches temporarily before appending to the variable 'branch_num' 
    for root in tree_root_tracker:
        transaction_count = 0
        max_value = 0
        position_max_value = 0
        for transaction in OF_list:
            if root == transaction[0]:
                if len(transaction)> max_value:
                    max_value = len(transaction)
                    position_max_value = transaction_count                
    
            transaction_count +=1
        position_max.append(position_max_value)
        branch_count+=1
        branch_num2.append(['Branch '+ str(branch_count)])
        create_new_branch(tree_dict_to_add, OF_list[position_max_value], branch_count)   

    ## Remove the item sets (transaction) from "OF_list" that was updated to the tree dictionary variable "tree_dict_to_add" 
    for index in position_max:
        OF_list.drop(index,inplace =True)
    OF_list.reset_index(drop = True, inplace = True)


    ## Check if the "OF_list" is empty
    # Check if all of the transactions in the (Ordered) Frequent Items list has been updated to the tree dictionary (tree_dict_all)
    # If not, proceed with the rest of the code
    if len(OF_list) ==0:
        flag = False
        # print('end')
    
    
    ## This Section will iterate over the remaining (Ordered) Frequent Items (OF_list)
    # - To check for transactions that has the same items sequence in the variable "tree_dict_to_add" 
    # - but has a transaction length less than or equal to the branches currently in the variable "tree_dict_to_add" 
    trans_keep = [] # Stores the transactions ((Ordered) Frequent Items) to be stored into 'tree_dict_to_add'
    trans_keep_branchpointer = [] # Stores the new branches name for 'tree_dict_to_add'
    trans_keep_index_on_ordered_list = []  # Stores the index position of the transactions ((Ordered) Frequent Items) 
    OF_list_row = 0
    for transaction in OF_list:
        for branch in branch_num2:        
            check = (len(transaction) <= len(tree_dict_to_add[branch[0]])) and (transaction[0] == tree_dict_to_add[branch[0]][0].value)
            if check:
                item_index = 0
                item_true = []
                for item in transaction:
                    if item == tree_dict_to_add[branch[0]][item_index].value:
                        item_true.append(True)
                    else:
                        item_true.append(False)
                    item_index += 1
                if all(item_true) == True:
                    trans_keep.append(transaction)
                    trans_keep_branchpointer.append(branch[0])
                    trans_keep_index_on_ordered_list.append(OF_list_row)
        OF_list_row += 1
   
    
    ## This code will update the count for each item in the transaction to the Nodes Count (Item) in variable "tree_dict_to_add" 
    for x in range(0,len(trans_keep)):
        branch_tree_dict = trans_keep_branchpointer[x]
        transaction_items = trans_keep[x]
        transaction_index = trans_keep_index_on_ordered_list[x]
        for y in range(0,len(transaction_items)):
            tree_dict_to_add[branch_tree_dict][y].count += 1
    
    # update the variable "tree_dict_all" (containing all the branches created) with the new branches (& Nodes) created in "tree_dict_to_add" 
    tree_dict_all.update(tree_dict_to_add)
    # update the "branch_num" (containing all the branches created) with new branches number created in "branch_num2" 
    branch_num += branch_num2

 
    ## After Updating the count to the tree dictionary (tree_dict_all)
    ## Remove the transaction from  the (Ordered) Frequent Items list (OF_list) 
    for x in range(0,len(trans_keep_index_on_ordered_list)):
        transaction_index = trans_keep_index_on_ordered_list[x]   
        OF_list.drop(transaction_index, inplace = True)
    OF_list.reset_index(drop = True, inplace = True)   


    ## Check if the "OF_list" is empty
    # Check if all of the transactions in the (Ordered) Frequent Items list has been updated to the tree dictionary (tree_dict_all) 
    # If not, proceed with the rest of the code
    if len(OF_list) ==0:
        flag = False
        # print('end')


print('Completed Generating the FP Tree'+'\n \n')
# ##### Uncomment only if want to print the FP tree CSV file ######
# print('New CSV file containing the FP Tree branches was printed into "FP_Tree.csv" '+'\n \n')
# ### Generate another CSV file containing the branches of the FP-Tree from "tree_dict_all" variable
# tree_dict_all_series = pd.Series(tree_dict_all, name='Branches')
# tree_dict_all_series.to_csv('FP_Tree.csv')
# ##################################################################




##################################################################
### Third Section is to Generate the Frequent Pattern Itemsets from the FP Conditional Tree for each Base Node #
### - Generate the Frequency Table for each FP Conditional Tree for each Base Node #`
### - Generate the Conditional FP Tree for each Node before generating the Frequent Itemsets
print('-'*70)
print('Third Section')
print('<< Generate the Frequent Pattern Itemsets from the FP Conditional Tree for each Base Node >>')
print('- Generate the Frequency Table for each FP Conditional Tree for each Base Node')
print('- Generate the Conditional FP Tree for each Node before generating the Frequent Itemsets')
# print('2 txt files will be generated for better viewing of the results')
# print("""The results will be printed into a txt file titled:
#       "Frequency_Table_and_Conditional_FPTree.txt" - Contain the Frequency Table and Conditional FP Tree for each Node
#       "Frequent_Itemsets_of_each_Base_Node.txt" - Contains the whole set of the Frequent Items for each Node (including those below min threshold)
#       "Frequent_Item_Final.txt" - Contains the Frequent Items for each Node (excluding those below min threshold)""")
print('-'*70)
print('\n')
##################################################################

f = open("Frequency_Table_and_Conditional_FPTree.txt", "w") 
r = open('Frequent_Itemsets_of_each_Base_Node.txt','w')
df_frequentitem_final = [] # this variable will store all the Frequent Itemset and the Support for ALL the Base Node for final print

### Make a Copy for the following variables for the next program
# - to avoid accidental editing
freq_table_4_cond = df_freq_table_1_sorted.copy() # this variable is from row 62 (to store Freq Table for each Conditional Pattern Node)
freq_table_items = freq_table_4_cond['Item'].tolist() # Extract the list of Items in the Frequency Table for the Conditional Pattern Base
# Start from the last Node (Item) in the Frequency Table (Bottom Upwards)
# The variable "end_root_item" represent the Base Node of interest at each iteration
for item_x in range(len(freq_table_items)-1, -1, -1):
    end_root_item = freq_table_items[item_x]
    print(end_root_item, file=f)
    # print('Working on: '+ end_root_item+ '\n...') # Purpose of print is to monitor progress


    ###filename = 'output_'+str(end_root_item)+'.txt' ###txt file contain Base Node info###
    ###fff = open(filename, 'w') ###txt file contain Base Node info###
    ###print(end_root_item, file=fff) ###txt file contain Base Node info###


    ## This Section will iterate over the tree dictionary "tree_dict_all"
    # to find the branches that contains the Base Node in variable "end_root_item"
    # all the combination of item sets will be stored in variable "cond_pattern_base" 
    cond_pattern_base = [] ### for used throughout the code
    cond_pattern_base_store = [] #### for storing all duplicate but not dropping any items
    cond_pattern_base_store_drop = [] #### for storing duplicate and later drop the items below threshold
    for branch_TD in tree_dict_all:
        # Extract the Node Value (Item) from each Branch in tree dictionary
        branch_TD_list_value = [] # Node Value (Item) from each Branch stored here
        for item_in_branch in tree_dict_all[branch_TD]:
            branch_TD_list_value.append(item_in_branch.value)
        # Next, compare the Node Value (Item) with the Base Node of interest ("end_root_item")
        combo = [] # some combination of item set stored here before adding to "cond_pattern_base"
        if end_root_item in branch_TD_list_value:
            # extract the index position of the Base Node in the branch
            item_index = branch_TD_list_value.index(end_root_item)
            # extract the count of the Base Node in the branch
            item_count = tree_dict_all[branch_TD][item_index].count
            # find all the combination of item sets that end with the Base Node
            # add all the duplicate combination into the following variable
            combo1 = branch_TD_list_value[0:item_index+1]
            combo2 = branch_TD_list_value[0:item_index+1]
            combo3 = branch_TD_list_value[0:item_index+1]            
            for num in range(0,item_count):
                cond_pattern_base.append(combo1)
                cond_pattern_base_store.append(combo2)
                cond_pattern_base_store_drop.append(combo3)                


    ## Remove the duplicate item sets from the Conditional FP Tree for each Node
    ###print('Conditional FP Tree with no repeat', file=fff) ###txt file contain Base Node info###
    cond_pattern_base_norepeat = []
    for itemset in cond_pattern_base:
        if itemset not in cond_pattern_base_norepeat:
            cond_pattern_base_norepeat.append(itemset)
            ###print(itemset, file=fff) ###txt file contain Base Node info###
    ###print('\n', file=fff) ###txt file contain Base Node info###
    

    ## This Section will determine the Frequency Table for the Conditional Pattern Base Node of interest
    # the Frequency Table will be stored in this variable "freq_table_4_cond"
    # freq_table_4_cond is a copy of the original Frequency Table
    # First, Set the frequency for all items in the table to 0 before start counting
    for x in range(0,len(freq_table_4_cond)):
        freq_table_4_cond.iloc[x,1] = 0
    

    ## Count each item in the item sets in variable "cond_pattern_base" 
    # add the count amount to the Frequency Table for the Conditional Pattern Base Node of interest
    # which is variable "freq_table_4_cond"
    for row in range(0,len(cond_pattern_base)):
        itemset = cond_pattern_base[row]
        for item_n in itemset:
            item_index_count = freq_table_items.index(item_n)
            freq_table_4_cond.iloc[item_index_count,1] += 1
    
    
    ######
    print('Frequency Table (Complete)',file=f) #######################
    print(freq_table_4_cond, file=f) ####################### 
    print('\n', file=f) #######################
    ######
    
    ###print('Frequency Table (Complete)',file=fff) ###txt file contain Base Node info###
    ###print(freq_table_4_cond, file=fff) ###txt file contain Base Node info###
    ###print('\n', file=fff) ###txt file contain Base Node info###
    
   
    ## Find the items in the variable "freq_table_4_cond" that are below the minimum support threshold 2500
    index_row_to_be_dropped = [] # store the index position of the items to be dropped from the frequency table
    item_dropped = [] # This variable stores the Items to be dropped because it is below the min support threshold
    # Make a Copy
    freq_table_4_cond_drop = freq_table_4_cond.copy() # This copy will contain dropped items below min threshold
    for row in range(0, len(freq_table_4_cond_drop)):
        if freq_table_4_cond_drop.iloc[row,1] < 2500:
            item_dropped.append(freq_table_4_cond_drop.iloc[row,0])            
            index_row_to_be_dropped.append(row)        
    ## Finally Remove the items that are below the minimum support threshold
    for index in index_row_to_be_dropped:
        freq_table_4_cond_drop.drop(index,inplace =True)
    freq_table_4_cond_drop.reset_index(drop = True, inplace = True)
    # print('Frequency Table for Base Node '+ end_root_item+ ' Done') # Purpose of print is to monitor progress

   
    print('Frequency Table (After Dropping Items below Threshold)',file=f) #######################
    print(freq_table_4_cond_drop, file=f) #######################    
    print('\n', file=f) #######################

    
    ###print('Frequency Table (After Dropping Items below Threshold)',file=fff) ###txt file contain Base Node info###
    ###print(freq_table_4_cond_drop, file=fff) ###txt file contain Base Node info###
    ###print('\n', file=fff) ###txt file contain Base Node info###

    
    ## This section is for displaying the Frequent Itemsets (Part A)
    # Using the "cond_pattern_base_norepeat" variable (contains the conditional fp tree itemsets that has no repeat)
    # This section will drop the items below the min threshold
    cond_pattern_base_norepeat_dropped = cond_pattern_base_norepeat.copy()
    for itemdrop in item_dropped:
        for itemset in cond_pattern_base_norepeat_dropped:
            if itemdrop in itemset:
                itemset.remove(itemdrop)
    ## This section is for displaying the Frequent Itemsets (Part B)
    # Using the "cond_pattern_base_norepeat_dropped" variable from the previous program
    # This section will drop any Frequent Itemset that are duplicates
    print('Conditional FP Tree final output (Unsorted)', file=f) #######################
    ###print('Conditional FP Tree final output', file=fff) ###txt file contain Base Node info###
    cond_pattern_base_final = []
    for itemset in cond_pattern_base_norepeat_dropped:
        if itemset not in cond_pattern_base_final:
            cond_pattern_base_final.append(itemset)
            print(itemset, file =f) #######################
            ###print(itemset, file =fff) #######################
    print('\n', file=f) #######################
    ###print('\n', file=fff) ###txt file contain Base Node info###



    ## This section is for determining the Support for the Frequent Itemsets (Part A)   
    # Using the "cond_pattern_base_store_drop" variable (contains the duplicate conditional fp tree itemsets)
    # This section will drop the items below the min threshold    
    # By the end of this code, the variable will contain the duplicate itemsets but with the items in it (below min threshold) dropped
    for itemdrop in item_dropped:
        for itemset in cond_pattern_base_store_drop:
            if itemdrop in itemset:
                itemset.remove(itemdrop)

    
    ## This section is for displaying the Frequent Itemsets (Part C)
    # This section sorts the Frequent Itemset in ascending order of the length of the Itemsets
    print('Conditional FP Tree final output (sorted)', file=f) #######################
    ###print('Conditional FP Tree final output (sorted)', file=fff) ###txt file contain Base Node info###  
    s_cond_pb_final = cond_pattern_base_final.copy()
    # s_cond_pattern_base = cond_pattern_base_store_drop.copy()
    sorted_cond_pf_final = sorted(s_cond_pb_final, key = len)
    for i in sorted_cond_pf_final:
        print(i, file =f) #######################
        ###print(i, file =fff) ###txt file contain Base Node info###
          
    print('\n', file=f) #######################
    print('-'*70, file=f) #######################
    ###print('\n', file=fff) ###txt file contain Base Node info###
    ###print('-'*70, file=fff) ###txt file contain Base Node info###


    ###########################################################################
    ##### The following section will determine the Frequent Itemsets #####
    # print('Next - Generate the Frequent Itemset'+'\n'+'...') # Purpose of print is to monitor progress
    ## This section is for determining the Support for the Frequent Itemsets (Part B) 
    # the Support will be counted here using the variable "cond_pattern_base_store_drop" (from Row 598)
    # "df_frequentitem_full_base" variable will store all the Frequent Itemset and the Support for the Base Node of interest
    # "df_frequentitem_final" variable will store all the Frequent Itemset and the Support for ALL the Base Node
    # "df_frequentitem_final" variable will be required at the end of the For Loop for printing the final results
    df_frequentitem_full_base = []    
    for s_item in sorted_cond_pf_final:
        counts = 0
        for d_item in cond_pattern_base_store_drop:
            if set(s_item).issubset(set(d_item)):
                counts+=1        
        df_frequentitem_full_base.append([s_item,counts])
        df_frequentitem_final.append([s_item,counts])
    ## This section is for determining the Support for the Frequent Itemsets (Part C) 
    # The Frequent Itemset with Support below the threshold will be removed
    # "df_frequentitem_full_base" variable will store all the Frequent Itemset and the Support for the Base Node of interest 
    # "df_frequentitem_full_base" variable will be converted into a dataframe beforehand
    df_frequentitem_full_base = pd.DataFrame(df_frequentitem_full_base, columns=['Frequent Item', 'Support'])
    index = [] # store the position index for the Frequent Itemset to be dropped
    for index_i in range(0, len(df_frequentitem_full_base)):
        if df_frequentitem_full_base.iloc[index_i,1] < 2500:
            index.append(index_i)   
    # "df_frequentitem_full_base_drop" variable will store all the Frequent Itemset and the Support for the Base Node of interest
    # ... but without the Frequent Itemsets below min threshold 
    df_frequentitem_full_base_drop = df_frequentitem_full_base.copy()
    for i in index:
        df_frequentitem_full_base_drop.drop(axis=0, index = i, inplace=True)
       
    ####fff.close() ###txt file contain Base Node info###
    
    # print('Generate the frequent itemset for '+ end_root_item+ ' Done' +'\n'*2) # Purpose of print is to monitor progress
    print(end_root_item, file=r)
    print('\n', file=r)
    print(df_frequentitem_full_base, file=r)
    print('\n', file=r)
    print(df_frequentitem_full_base_drop, file=r)
    print('\n', file=r)
    print('-'*70, file=r)
    print('\n', file=r)

r.close()#######################
f.close()#######################
print('Completed Generating Frequent Itemsets and the Support')
print('New txt file generated containing the Frequency Table and Conditional FP Tree for each Node printed into "Frequency_Table_and_Conditional_FPTree.txt"')
print('New txt file generated containing the whole set of the Frequent Items for each Node (including those below min threshold) printed into "Frequent_Itemsets_of_each_Base_Node.txt" '+'\n \n')
##################################################################



##################################################################
### Final Section is to Print the Frequent Itemsets and its Support Count #
print('-'*70)
print('Final Section is to Print the Frequent Itemsets and its Support Count')
print('-'*70)
print('\n')
##################################################################
# "df_frequentitem_final" variable is from the previous For Loop program
# "df_frequentitem_final" variable stores all the Frequent Itemset and the Support for ALL the Base Node
# In this program it will be converted into a DataFrame
# Before removing the Frequent Itemsets below minimum threshold and then sort it according to the Support Count in descending order
# A txt file will be generated to store the Table with Frequent Itemsets and its Support before and after Sorting

rrr = open('Frequent_Itemsets_Final.txt','w')
## Convert into a DataFrame
df_frequentitem_final = pd.DataFrame(df_frequentitem_final, columns=['Frequent Item', 'Support'])
## Determine the position index of the Frequent Itemsets below the minimum threshold
index = []
for index_i in range(0, len(df_frequentitem_final)):
    if df_frequentitem_final.iloc[index_i,1] < 2500:
        index.append(index_i)
## Remove the Frequent Itemsets below the minimum threshold 
df_frequentitem_final_drop = df_frequentitem_final.copy()
for i in index:
    df_frequentitem_final_drop.drop(axis=0, index = i, inplace=True)
df_frequentitem_final_drop.reset_index(drop = True, inplace=True)
print('Frequent Itemsets Final Output (Unsorted)', file=rrr) # print to txt file
print(df_frequentitem_final_drop, file=rrr)  # print to txt file
print('\n', file=rrr) # print to txt file

## Sort the Frequent Itemsets according to the Support Count in Descending Order
print('Frequent Itemsets Final Output (Sorted Descending)', file=rrr) # print to txt file
df_frequentitem_final_sorted = df_frequentitem_final_drop.sort_values(['Support'], ascending=False)
df_frequentitem_final_sorted.reset_index(drop = True, inplace=True)
print(df_frequentitem_final_sorted, file=rrr) # print to txt file
rrr.close()
print('\n')
print('Completed Generating Frequent Itemsets and the Support')
print("Another txt file was generated to store the Table with Frequent Itemsets and its Support before and after Sorting")
print("refer to 'Frequent_Itemsets_Final.txt'"+'\n'+'\n')
##################################################################



##################################################################
### Display the Frequent Pattern from the Conditional Pattern Base
##################################################################
print('Final Output')
for i in range(0, len(df_frequentitem_final_sorted)):
    frequent_items_a = str(df_frequentitem_final_sorted.iloc[i][0])
    supportcount_a = str(df_frequentitem_final_sorted.iloc[i][1])
    print(' : '.join([frequent_items_a,supportcount_a]))
##################################################################

print('\n'+'END OF THE CODE')



