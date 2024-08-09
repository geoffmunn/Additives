#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sqlite3

from itertools import combinations

DB_FILE_NAME = 'numbers.db'
LENGTH = 4
TARGET = 100

def main():
    
    


    # Check if the database exists
    #totals_table_exists:bool = True
    # try:
    #     recent_scan = "SELECT * FROM totals LIMIT 1;"
    #     conn        = sqlite3.connect(DB_FILE_NAME)
    #     cursor      = conn.execute(recent_scan)
    #     conn.close()
    # except:
    #     totals_table_exists = False

    # if totals_table_exists == False:
    #     print ('\n 🗄  No totals table found, creating one...')
    #     create_totals_table = "CREATE TABLE totals (ID INTEGER PRIMARY KEY AUTOINCREMENT, total INTEGER NOT NULL);"

    #     conn               = sqlite3.connect(DB_FILE_NAME)
    #     cursor             = conn.execute(create_totals_table)
    #     conn.commit()
    #     conn.close()
    
    delete_totals_table: str = "DROP TABLE IF EXISTS totals;"
    create_totals_table = "CREATE TABLE totals (ID INTEGER PRIMARY KEY AUTOINCREMENT, total INTEGER NOT NULL, total_count INTEGER NOT NULL);"
    create_index = "CREATE UNIQUE INDEX ix_totals ON totals (total);"
    check_total: str = "SELECT total, total_count FROM totals WHERE total=?;"
    insert_total: str  = "INSERT INTO totals (total, total_count) VALUES (?, 1);"
    update_total: str = "UPDATE totals SET total_count=total_count+1 WHERE total=?;"
    delete_totals: str = "DELETE FROM totals WHERE total < ?;"

    conn = sqlite3.connect(DB_FILE_NAME)
    conn.row_factory = sqlite3.Row

    conn.execute(delete_totals_table)
    conn.commit()
    
    conn.execute(create_totals_table)
    conn.execute(create_index)
    conn.commit()

    cursor = conn.cursor()

    # Starting number generation

    current_set: list = []

    for i in range(1, LENGTH + 1):
        current_set.append(i)
    
    totals: dict = {}

    current_number = LENGTH

    # Go through the current set and check if every set of two numbers adds up to a unique number

    # For 2 combos, take the first number and check the others.
    while True:
        
        set_combos = combinations(current_set, LENGTH)
        for line in list(set_combos):
            total = sum(line)

            #cursor = conn.cursor()
            # cursor = conn.execute("SELECT * FROM totals where total=15;")
            # test = cursor.fetchone()
            # print ('test:', test)

            cursor = conn.cursor()
            cursor = conn.execute(check_total, [total])
            
            existing_row = cursor.fetchone()
            if existing_row is None:
                conn.execute(insert_total, [total])
            else:
                conn.execute(update_total, [total])

            conn.commit()
            # for existing_row in cursor.fetchall():
            #     if 
            # if total in totals:
            #     totals[total] += 1
            # else:
            #     totals[total] = 1

        

        # Now go through the numbers to find the next one that doens't have a total of 2

        while True:
            current_number += 1
            # if current_number in totals:
            #     if totals[current_number] < 2:
            #         break
            # else:
            #     break

        
            cursor = conn.cursor()
            cursor = conn.execute(check_total, [current_number])
            existing_row = cursor.fetchone()
            if existing_row is None:
                break
            else:
                if existing_row['total_count'] < 2:
                    break
            

        current_set.append(current_number)

        f = open(f"results/{LENGTH} - {TARGET}.txt", "w")
        f.write(' '.join(str(v) for v in current_set) + "\n\nTotal number: " + len(current_set))
        f.close()

        # Remove all numbers from the total list which are less than the $current_number
        #print ('old totals:', totals)
        #filtered:list = list(filter(lambda num: num > current_number, totals))
        #filtered: dict = dict(filter(lambda item: not (isinstance(item[1], int) and item[1] > current_number), totals.items()))

        #print ('filtered:', filtered)
        # totals = filtered

        conn.execute(delete_totals, [current_number])

        print ('total so far:', len(current_set))
        if len(current_set) >= TARGET:
            break

    # Now find the next number we can add

    print ('final set:', current_set)

    print (' 💯 Done!\n')

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()