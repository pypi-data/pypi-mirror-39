# pop_projection

Projection of a population of a retirement plan consisting of :
- employees (actives and retirees)
- their spouses
- thier childrens


Given such population at the end of year 0, we compute, for each following year (year 1, year 2, ..., year 100, and at the end of that year), the number of individuals, that survived, died and quit the company (actives only)  and those that retired (actives only). In addition to that, new spouses, new children, and new actives are also generated using given laws.

The laws governing suchs movements are :

- law of mortality (mortality tables)
- law of quitting
- law of retirement (this one is in fact deterministic : retirement at some age , 60 for example)
- law of marriage
- law of birth
- law of replacement


Law of quitting, law of retirement, law of marriage and law of birth are functions that are passed to the main function (simulerEffectif) as tuples : (law, [list of parameters]). The list of parameters must exist in the list of columns of the corresponding input data :
- law of quitting --> parameters names are in the list of columns of employees.
- law of retirement --> parameters names are in the list of columns of employees.
- law of marriage --> parameters names are in the list of columns of employees.
- law of birth --> parameters names are in the list of columns of spouses.
- law of replacement has two parameters :
    - a list of departures by group 
    - the year of this departures (1 or 2 or ...)

This laws, except law of replacement, return a number between 0 and 1 representing a probability of occurence of the event in the year :
- law of quitting --> probablity that the employee will quit before the end of the next year.
- law of retirement --> probablity that the employee will retire before the end of the next year.
- law of marriage --> probablity that the employee will marry before the end of the next year.
- law of birth --> probablity that the spouse (if female) or his wife will give birth before the end of the next year.

law of replacement returns a list of new employees to add to the population of employees.

# Installation
```
pip install pop-projection
```
# Usage example

```
import pop_projection.Effectifs as eff
import pandas as pd


# Define law of retirement
def law_ret1(age, year_emp):
    if year_emp < 2002:
        if age+1 >= 55:
            return True
        else:
            return False
    if year_emp >= 2002:
        if age+1 >= 60:
            return True
        else:
            return False

# Define law of reignation
def law_resignation_1(age, sexe):
    if age+1 >= 50 :
        return 0
    if sexe == 'female':
        if age+1 <= 30:
            return 0.02
        else:
            return 0.01
    if sexe == 'male':
        if age+1 <= 30:
            return 0.02
        else:
            return 0.01
    


# Define law of marriage
def law_mar1(age, sexe, typeAgent):
    """
    Return the probability of getting maried  during the following year at a given age for a given sex

    """
    if sexe == 'male':
        if typeAgent=='active':
            if age >= 25 and age <= 54:
                return 0.095
            else :
                return 0
        else:
            return 0
    
    if sexe == 'female':
        if typeAgent=='active':
            if age >= 25 and age <= 54:
                return 0.15
            else :
                return 0
        else:
            return 0

# Define law of replacement   
def law_replacement1(departures_, year_):
    
    '''
        assumes departures_ is a dic storing number of departures by group of the year year_
        returns a list of dics having keys : sex, age, number and group
        
    '''
    new_employees = []

    for g in departures_:
        temp = {'sex':'male', 'age' : 30, 'number':departures_[g],'group':g}
        new_employees.append(temp)
    
    return new_employees

# Path for input data
path ="./data/"

# Number of years to project
MAX_ANNEES = 50

# Loading data
employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

# Projection of population
numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, (law_ret1, ['age', 'Year_employment']), 
                    (law_resignation_1, ['age', 'sex']), (law_mar1, ['age', 'sex','type']), law_replacement_ = None)

# Global numbers
Effectifs = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

Effectifs.to_csv('Effectifs_python.csv', sep = ';', index=False, decimal=',')

#Number of actives leaving population : deaths, resignations, and new retired
Leaving = eff.leavingNumbers(numbers_[0], numbers_[4], MAX_ANNEES)

Leaving.to_csv('Sortants_python.csv', sep = ';', index=False, decimal=',')


#export projected employees
pd.DataFrame.from_dict(numbers_[0]).to_csv('employees_proj.csv', sep = ';', index=False, decimal=',')

#export projected spouses
pd.DataFrame.from_dict(numbers_[1]).to_csv('spouses_proj.csv', sep = ';', index=False, decimal=',')

#export projected children
pd.DataFrame.from_dict(numbers_[2]).to_csv('children_proj.csv', sep = ';', index=False, decimal=',')
```

