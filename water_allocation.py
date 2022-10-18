"""
Multi-Objective Optimization for Water Resources

Created:
    March 2022

User input:
    Parameters

Output:
    Prints optimal solution

Users:
HH      households
AGRO    agriculture users
IND     industry users
PG      power generation users

Sources:
GW      groundwater
SW      surface water
DW      saline water
WW      treated wastewater


For model description see:
    xxxxx

"""

from ortools.linear_solver import pywraplp


def runModel(user_param,source_param,budget,unfeasibles = []):
    solver  = pywraplp.Solver.CreateSolver('GLOP')
    users   = list(user_param.keys())
    sources = list(source_param.keys())
    
    # Decision variables
    DWD = {}
    for u in users:
        DWD[u] = solver.NumVar(0.0,solver.infinity(),f'DWD[{u}]')
    
    EWA = {}
    for s in sources:
        EWA[s] = solver.NumVar(0.0,solver.infinity(),f'EWA[{s}]')
    
    Q = {}
    for s in sources:
        for u in users:
            pair = (s,u)
            if pair in unfeasibles:
                Q[pair] = solver.NumVar(0.0,0.0,f'Q[{pair}]')
            else:
                Q[pair] = solver.NumVar(0.0,solver.infinity(),f'Q[{pair}]')
    
    budgetUsed = solver.NumVar(0.0,solver.infinity(),'budgetUsed')
    
    # Objective function
    solver.Minimize(
        solver.Sum([ user_param[u]['weight']    * DWD[u] for u in users   ]) + \
        solver.Sum([ source_param[s]['weight']  * EWA[s] for s in sources ])
        )
    
    # Goal 1
    for u in users:
        solver.Add(
            solver.Sum([ Q[s,u] for s in sources ]) >= user_param[u]['demand'] - DWD[u]
            )
    # Goal 2
    for s in sources:
        solver.Add(
            solver.Sum([ Q[s,u] for u in users   ]) <= source_param[s]['supply'] - EWA[s]
            )
    
    # Water quality concentration
    for u in users:
        solver.Add(
            solver.Sum([ source_param[s]['ppm'] * Q[s,u] for s in sources ]) <= \
            user_param[u]['ppm'] * solver.Sum([ Q[s,u] for s in sources ])
            )
    
    # Budget constraint
    solver.Add(
        solver.Sum([ source_param[s]['extractionCost'] * \
            solver.Sum([ Q[s,u] for u in users]) for s in sources]) <= budgetUsed
        )
    solver.Add(
        solver.Sum([ source_param[s]['extractionCost'] * \
            solver.Sum([ Q[s,u] for u in users]) for s in sources]) >= budgetUsed
        )
    solver.Add(budgetUsed <= budget)
    
    # Solution
    status = solver.Solve()
    
    if status == solver.OPTIMAL or status == solver.FEASIBLE:
        print('--------------------------\nSolution found!')
        print('\nDeficit of water (cubic meter/year):')
        for u in users:
            print(f'User {u}:',DWD[u].solution_value())
        print('\nExceedance in extraction (cubic meter/year):')
        for s in sources:
            print(f'Source {s}:',EWA[s].solution_value())
        print('\nOptimal allocation (cubic meter/year):')
        for s in sources:
            for u in users:
                print(f'From {s} to {u}:',Q[s,u].solution_value())
        print('\nBudget used:',budgetUsed.solution_value())
        print('--------------------------\n')
    return 1


if __name__ == '__main__':
    
    # Units: demand [cubic meter/year], ppm [kg/cubic meter], weight [cost/cubic meter]
    user_param = {
        'HH':   {'demand': 50,  'ppm':0.5, 'weight': 2},
        'AGRO': {'demand': 300, 'ppm':1.0, 'weight': 1},
        'IND':  {'demand': 100, 'ppm':0.7, 'weight': 1},
        'PG':   {'demand': 200, 'ppm':1.0, 'weight': 1}
        }
    
    # Units: supply [cubic meter/year], ppm [kg/cubic meter], weight [cost/cubic meter]
    # extractionCost [$/cubic meter]
    source_param = {
        'GW': {'supply': 75,  'ppm': 0.2, 'weight': 1, 'extractionCost': 5},
        'SW': {'supply': 75,  'ppm': 0.1, 'weight': 1, 'extractionCost': 1},
        'DW': {'supply': 200, 'ppm': 0.7, 'weight': 1, 'extractionCost': 2},
        'WW': {'supply': 300, 'ppm': 1.0, 'weight': 1, 'extractionCost': 3}
        }
    
    budget = 1000.0
    
    # Unfeasible allocations, if all possible set: unfeasibles = []
    unfeasibles = [
        ('GW','PG'),
        ('SW','PG')
        ]
    
    sol = runModel(user_param,source_param,budget,unfeasibles)
    



