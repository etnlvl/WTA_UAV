from ortools.linear_solver import pywraplp

class MIP_Assignment:
    def __init__(self, probabilities, weapons, targets):
        self.probabilities = probabilities
        self.weapons = weapons
        self.targets = targets
        self.num_weapons = len(weapons)
        self.num_targets = len(targets)
        self.assignement = []
        self.test = self.optimizeMIP()

    def optimizeMIP(self):
        # Solver
        # Create the mip solver with the SCIP backend.
        solver = pywraplp.Solver.CreateSolver("SCIP")

        if not solver:
            return

        # Variables
        # x[i, j] is an array of 0-1 variables, which will be 1
        # if worker i is assigned to task j.
        x = {}
        for i in range(self.num_weapons):
            for j in range(self.num_targets):
                x[i, j] = solver.IntVar(0, 1, "")

        # Constraints
        # Each weapon is assigned to at most 1 target .
        for i in range(self.num_weapons):
            solver.Add(solver.Sum([x[i, j] for j in range(self.num_targets)]) <= 1)

        # Each target is assigned to one or less  weapon
        for j in range(self.num_targets):
            solver.Add(solver.Sum([x[i, j] for i in range(self.num_weapons)]) <= 1)

        # Objective
        objective_terms = []
        for i in range(self.num_weapons):
            for j in range(self.num_targets):
                objective_terms.append(self.probabilities[i][j] * x[i, j])
        solver.Minimize(-solver.Sum(objective_terms))        # Here we want the global probability of hit to be maximized, costs must be maximized and not minimize.

        # Solve
        print(f"Solving with {solver.SolverVersion()}")
        status = solver.Solve()

        # Print solution.
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print(f"Total cost = {solver.Objective().Value()}\n")
            for i in range(self.num_weapons):
                for j in range(self.num_targets):
                    # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                    if x[i, j].solution_value() > 0.5:
                        print(f" {self.weapons[i].name} assigned to drone {self.targets[j].idx}." + f" Cost: {self.probabilities[i][j]}")
                        self.assignement.append((i,j))
            return self.assignement

        else:
            return "No solution found."

    if __name__ == "__optimize__":
        optimizeMIP()


