import read_input as inp
import gurobipy as gp
from gurobipy import GRB
from Dataset.instance_data import num_points

all_points, set1, set2, vehicles, demand, distance, cost, pickup_points, delivery_points, service_time = inp.all_points, inp.set1, inp.set2, inp.vehicles, inp.demand, inp.distance, inp.cost, inp.pickup_points, inp.delivery_points, inp.service_time
maxTime_minutes = 150000
M = 1000000000

print("Multi vehicle DARP")
model = gp.Model("Multi vehicle DARP")
model.reset()
timelimit = maxTime_minutes * 60
model.Params.timelimit = timelimit

x = model.addVars(inp.cost, vtype=GRB.BINARY, name="x")

tmp = {}
for i in all_points:
    for k in vehicles:
        tmp[i,k] = 1
Q = model.addVars(tmp, vtype=GRB.CONTINUOUS, name="Q")
B = model.addVars(tmp, vtype=GRB.CONTINUOUS, name="B")

points_no_depots = inp.pickup_points + inp.delivery_points

# Constraints
model.addConstrs(gp.quicksum(x[i, j, k] for k in inp.vehicles for j in inp.set2 if i != j) == 1 for i in points_no_depots)
model.addConstrs(gp.quicksum(x[inp.depots[0], j, k] for j in pickup_points) == 1 for k in vehicles)
model.addConstrs(gp.quicksum(x[i, inp.depots[1], k] for i in delivery_points) == 1 for k in vehicles)
model.addConstrs(gp.quicksum(x[i, j, k] for i in set1 if i != j) - gp.quicksum(x[j, i, k] for i in set2 if i != j) == 0 for j in points_no_depots for k in vehicles)
model.addConstrs(B[j, k] >= B[i, k] + service_time + cost[i, j, k] - M*(1-x[i, j, k]) for i, j, k in cost)
model.addConstrs(Q[j, k] == Q[i, k] + inp.demand[j] - M*(1-x[i, j, k]) for i, j, k in cost)
model.addConstrs(Q[i, k] >= max(0, demand[i]) for i in all_points for k in vehicles)
model.addConstrs(Q[i, k] <= min(inp.vehicles_df.loc[inp.vehicles_df['id'] == k, 'capacity'].values[0], inp.vehicles_df.loc[inp.vehicles_df['id'] == k, 'capacity'].values[0] + demand[i]) for i in all_points for k in vehicles)
# Vincolo (20) paper non convince
model.addConstrs(gp.quicksum(x[i, j, k] for j in set2 if i != j) - gp.quicksum(x[num_points + i, j, k] for j in set2 if (num_points + i) != j) == 0 for i in pickup_points for k in vehicles)
# Versione mia
# model.addConstrs(gp.quicksum(x[i, j, k] for j in set2 if i != j) - gp.quicksum(x[j, inp.num_points + i, k] for j in set1 if inp.num_points + i != j) == 0 for i in pickup_points for k in vehicles)
model.addConstrs(B[i, k] <= B[num_points + i, k] for i in pickup_points for k in vehicles)
model.addConstrs(B[num_points + i, k] - (B[i, k] + demand[i]) <= inp.max_ride_time_client for i in pickup_points for k in vehicles)

model.write('model.lp')
model.optimize()


# sol = {k: v.X for k, v in x.items() if v.X > 0}
# routes = route(sol)
# print("Routes: ", routes)
# print("Costo della soluzione = ", model.objval)
