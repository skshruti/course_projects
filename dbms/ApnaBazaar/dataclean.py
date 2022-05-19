import os
import csv
import sys
table = "accessories.csv"

ids = []
with open("/Users/shrutikumari/Downloads/newproject/data/accessories.csv", "r") as f, open('/Users/shrutikumari/Desktop/sem/dbms/data/accessories.csv', "w+") as csv_file:
    writer = csv.writer(csv_file)
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i==0):
            writer.writerow(line)
        else:
            if(line[20] not in ids):
                writer.writerow(line)
                ids.append(line[20])

with open("/Users/shrutikumari/Downloads/newproject/data/bags.csv", "r") as f, open('/Users/shrutikumari/Desktop/sem/dbms/data/bags.csv', "w+") as csv_file:
    writer = csv.writer(csv_file)
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i==0):
            writer.writerow(line)
        else:
            if(line[20] not in ids):
                writer.writerow(line)
                ids.append(line[20])

with open("/Users/shrutikumari/Downloads/newproject/data/beauty.csv", "r") as f, open('/Users/shrutikumari/Desktop/sem/dbms/data/beauty.csv', "w+") as csv_file:
    writer = csv.writer(csv_file)
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i==0):
            writer.writerow(line)
        else:
            if(line[20] not in ids):
                writer.writerow(line)
                ids.append(line[20])

with open("/Users/shrutikumari/Downloads/newproject/data/house.csv", "r") as f, open('/Users/shrutikumari/Desktop/sem/dbms/data/house.csv', "w+") as csv_file:
    writer = csv.writer(csv_file)
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i==0):
            writer.writerow(line)
        else:
            if(line[20] not in ids):
                writer.writerow(line)
                ids.append(line[20])

with open("/Users/shrutikumari/Downloads/newproject/data/jewelry.csv", "r") as f, open('/Users/shrutikumari/Desktop/sem/dbms/data/jewelry.csv', "w+") as csv_file:
    writer = csv.writer(csv_file)
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i==0):
            writer.writerow(line)
        else:
            if(line[20] not in ids):
                writer.writerow(line)
                ids.append(line[20])

with open("/Users/shrutikumari/Downloads/newproject/data/kids.csv", "r") as f, open('/Users/shrutikumari/Desktop/sem/dbms/data/kids.csv', "w+") as csv_file:
    writer = csv.writer(csv_file)
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i==0):
            writer.writerow(line)
        else:
            if(line[20] not in ids):
                writer.writerow(line)
                ids.append(line[20])

with open("/Users/shrutikumari/Downloads/newproject/data/men.csv", "r") as f, open('/Users/shrutikumari/Desktop/sem/dbms/data/men.csv', "w+") as csv_file:
    writer = csv.writer(csv_file)
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i==0):
            writer.writerow(line)
        else:
            if(line[20] not in ids):
                writer.writerow(line)
                ids.append(line[20])

with open("/Users/shrutikumari/Downloads/newproject/data/shoes.csv", "r") as f, open('/Users/shrutikumari/Desktop/sem/dbms/data/shoes.csv', "w+") as csv_file:
    writer = csv.writer(csv_file)
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i==0):
            writer.writerow(line)
        else:
            if(line[20] not in ids):
                writer.writerow(line)
                ids.append(line[20])

with open("/Users/shrutikumari/Downloads/newproject/data/women.csv", "r") as f, open('/Users/shrutikumari/Desktop/sem/dbms/data/women.csv', "w+") as csv_file:
    writer = csv.writer(csv_file)
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i==0):
            writer.writerow(line)
        else:
            if(line[20] not in ids):
                writer.writerow(line)
                ids.append(line[20])

