Quick usage
===========
1. Download the [2016
   results](http://er.ncsbe.gov/downloads.html?election_dt=11/08/2016) file
   from the North Carolina State Board of Elections.
2. Unzip the file.
3. Test the relationship between Lieutenant Governor and Governor for the
   Democratics candidates:

```
bash:~$ python ./nc_linear_regress.py resultsPCT20161108.txt \
  DEM 'NC LIEUTENANT GOVERNOR' 'NC GOVERNOR'
Slope=0.9813 Intercept=0.2324 R^2=0.9898 p=0.000000
ALAMANCE:01                        498       474        24     0.0506
[...]
```

This says that there is an incredibly strong relationship between the number of
votest that the Democratics candidates for Lieutenant Governor and Governor
received. The intercept is greater than 0, indicating that Governor generally
received more votes, but the slope is less than 1, meaning that the advantage is
less pronounced in larger precincts.

After the summary is will print per-precinct results. For each precinct it will
print

1. The precinct's name;
2. The actual number of votes the candidate received;
3. The expected number of votes the candidate received;
4. The difference between the two; positive values indicate that the candidate
   overperformed expectations, while negative values show underperformance;
5. The percent by which the prediction was off.

In the example above, based on the performance of the Democratic candidate
for Lieutenant Governor, the Governor received 24 more votes than this simple
model alone would predict, or an overperformance of about 5%.
