import read_input as inp
import gurobipy as gp
from gurobipy import GRB
from Dataset.instance_data import num_points

all_points, set1, set2, vehicles, demand, distance, cost, pickup_points, delivery_points, service_time = inp.all_points, inp.set1, inp.set2, inp.vehicles, inp.demand, inp.distance, inp.cost, inp.pickup_points, inp.delivery_points, inp.service_time
maxTime_minutes = 30000000
M = 10000000

print("n = ", num_points)
print("Multi vehicle DARP")
model = gp.Model("Multi vehicle DARP")
model.reset()
timelimit = maxTime_minutes * 60
model.Params.timelimit = timelimit

x = model.addVars(inp.cost, vtype=GRB.BINARY, name="x")
# y = model.addVars(inp.cost, vtype=gp.GRB.BINARY, name='y')

tmp = {}
for i in all_points:
    for k in vehicles:
        tmp[i,k] = 1

# Q[i,k] = load of vehicle k when leaving vertex i
Q = model.addVars(tmp, lb = 0, vtype=GRB.CONTINUOUS, name="Q")
# B[i,k] = beginning of service of vehicle k at vertex i
B = model.addVars(tmp, lb = 0, vtype=GRB.CONTINUOUS, name="B")

# Objective function
model.setObjective(x.prod(cost), GRB.MINIMIZE)

# Constraints
points_no_depots = inp.pickup_points + inp.delivery_points
model.addConstrs((gp.quicksum(x[i, j, k] for k in vehicles for j in set2 if i != j) == 1 for i in points_no_depots)) #ogni client attraversato da un solo veicolo
model.addConstrs(gp.quicksum(x[inp.depots[0], j, k] for j in set2) == 1 for k in vehicles) # un solo arco uscente dal dep
model.addConstrs(gp.quicksum(x[i, inp.depots[1], k] for i in set1) == 1 for k in vehicles) # un solo arco entrante nel dep
model.addConstrs(gp.quicksum(x[i, j, k] for i in set1 if i != j) - gp.quicksum(x[j, i, k] for i in set2 if i != j) == 0 for j in points_no_depots for k in vehicles) #flusso clients = 0
model.addConstrs(B[j, k] >= B[i, k] + service_time + cost[i, j, k] - M*(1 - x[i, j, k]) for i, j, k in cost) # se arco (i,j) usato, allora istante di passaggio in j è successivo a i

# VINCOLO CHE CRiEA PROBLEMI. nel paper è posta l'uguaglianza
# model.addConstrs(Q[j, k] <= M * x[i, j, k] for i, j, k in cost)
# model.addConstrs(Q[j, k] <= Q[i, k] + demand[j] for i, j, k in cost)
model.addConstrs(Q[j, k] >= Q[i, k] + demand[j] - M * (1 - x[i, j, k]) for i, j, k in cost)

model.addConstrs(Q[i, k] >= max(0, demand[i]) for i in all_points for k in vehicles)
model.addConstrs(Q[i, k] <= min(inp.vehicles_df.loc[inp.vehicles_df['id'] == k, 'capacity'].values[0], inp.vehicles_df.loc[inp.vehicles_df['id'] == k, 'capacity'].values[0] + demand[i]) for i in all_points for k in vehicles)
# Associazione vertic
model.addConstrs(gp.quicksum(x[i, j, k] for j in set2 if i != j) - gp.quicksum(x[num_points + i, j, k] for j in set2 if (num_points + i) != j) == 0 for i in pickup_points for k in vehicles)
model.addConstrs(B[i, k] <= B[num_points + i, k] for i in pickup_points for k in vehicles)
model.addConstrs(B[num_points + i, k] - (B[i, k] + demand[i]) <= inp.max_ride_time_client for i in pickup_points for k in vehicles)
# ADD TIME WINDOWS CONSTRAINTS

# EXTRA ADDED BY ME
# model.addConstrs(Q["Source", k] == 0 for k in vehicles)
# model.addConstrs(B["Source", k] == 0 for k in vehicles)

model.write('model.lp')
model.optimize()

sol = {k: v.X for k, v in x.items() if v.X > 0}
print(sol)
# # Create a dictionary for the results
k_lists = {}
route = {}
# Divide 'sol' items into lists based on the k index
for (i, j, k), value in sol.items():
    if k not in k_lists:  # Check if 'k' exists in the dictionary
        k_lists[k] = []  # Create a new list if it doesn't
    k_lists[k].append((i, j))
# Print the lists for each k
for k, values in k_lists.items():
    print(f"List for k={k}: {values}")
    # route[k] = route(values)
#
# def extract_routes(k_lists):
#     routes = []
#
#     for k, values in k_lists.items():
#         route = ["Source"]
#
#         # Filter the arcs to those matching the vehicle index
#         for (i, j, vehicle_k), value in sol.items():
#             if value > 0 and vehicle_k == k:
#                 route.append(i)
#                 route.append(j)
#
#         route.append("Sink")
#         routes.append(f"Vehicle {k}: {route}")
#
#     return routes
