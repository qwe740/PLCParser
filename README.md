# PLCParser
Python parser for pulling PIPESIM .plc file results into a Pandas DataFrame

## How to use:

1. Create NetworkSimulationProfile Object and Extract the Results
```
directory = r'C:\users\you\folderwithPLCs'
myPLCObject = NetworkSimulationProfile(directory)

#Extract Results
myPLCObject.extractResults()
```

2. The object has a property `results` where the data is stored in this data structure:
```
{ plc1 : dataframe1, #no .plc at the end of the plc1 filename
  plc2 : dataframe2,
  .
  .
  .
  plcn : dataframen
}
```
3. Each dataframe has columns of all the variables and each row corresponds to a point along the profile
![Markdown Image](https://user-images.githubusercontent.com/30243166/115302596-38e18680-a128-11eb-9aa1-942cd6661776.PNG)

4. The names of all the columns can be found by accessing this property of the PLCObject:
```
print(myPLCObject.varnames[plcfile]) #Note the .plc from the end of the filename is omitted
```

5. The names of all the plc files can be found by accessing the keys of the results object:
```
print(myPLCObject.results.keys()
```
6. That's it! Happy Coding!
