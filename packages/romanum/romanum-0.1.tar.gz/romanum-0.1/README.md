# Roman numeral conversion tools

The scripts (and functions) r2n and n2r will convert roman numerals to integers and natural numbers to roman numerals, respectively. Error handling is nonexistent. 

## Works: 

* Conversion to/from integers in standard form with absolute value of 1-4999 or 0, when represented with 'nulla' 
* Conversion to/from integers, when the overline in vinculus forms is replaced with parentheses groups. 

## Doesn't work: 

* Input validation: **Use -f** and input clean inputs or face errors. 
* Decoding some rarer "nonstandard" forms. 

## TODO: 

* Decoding vinculus forms to/from LaTeX etc.. 
* Nice errors handling / warnings. 
* Proper packaging: verify that pip works & register to PyPi 

