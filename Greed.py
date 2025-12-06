import sys
import math
import heapq
import random

eps = 1e-8
inf = 10 ** 9


def inp():
    resources = int(input())
    num_travel_routes = int(input())
    for i in range(num_travel_routes):
        building_id_1, building_id_2, capacity = [int(j) for j in input().split()]
    num_pods = int(input())

    for i in range(num_pods):
        pod_properties = input()

    cnt_new_b = int(input())
    new_buildings = []
    for i in range(cnt_new_b):
        new_b = list(map(int, input().split()))
        new_buildings.append(new_b[1])
        graph[new_b[1]] = []
        buildings[new_b[1]] = [new_b[0]] + new_b[2:]

    return resources, new_buildings


def orientation(p1, p2, p3):
    sign = (p3[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    if sign == 0:
        return 0
    elif sign > 0:
        return 1
    else:
        return -1


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def segment_intersect(A, B, C, D):
    return ((orientation(A, B, C) * orientation(A, B, D) < 0) and
            (orientation(C, D, A) * orientation(C, D, B) < 0))


def point_intersect(A, B, c):
    return (((distance(B, c) + distance(A, c) - distance(A, B)) > -eps) and (
            (distance(B, c) + distance(A, c) - distance(A, B)) < eps))


def closest_reachable(v):
    pv = (buildings[v][1], buildings[v][2])
    ans = [inf, -1]
    for u in connected:
        if  buildings[u][0] != 0 and buildings[v][0] != 0:
            continue
        pu = (buildings[u][1], buildings[u][2])

        if distance(pu, pv) < ans[0]:
            intersect = False

            # intersection with other modules
            for p in buildings:
                if p == v or p == u:
                    continue
                pp = (buildings[p][1], buildings[p][2])
                if point_intersect(pu, pv, pp):
                    intersect = True
                    break

            # intersection with other tubes
            for e in edges:
                pe1 = (buildings[e[0]][1], buildings[e[0]][2])
                pe2 = (buildings[e[1]][1], buildings[e[1]][2])
                if segment_intersect(pe1, pe2, pv, pu):
                    intersect = True
                    break

            if not intersect:
                ans = [distance(pu, pv), u]

    return ans


graph = {}
edges = []
pods = {}
buildings = {}
connected = set()
not_connected = set()
free_id = set(list(range(1, 501)))

# game loop
for _ in range(20):
    planned = []
    heapq.heapify(planned)
    resources, new = inp()
    out = []
    if len(connected) == 0:
        connected.add(new[-1])
        new.pop()

    for i in new:
        not_connected.add(i)

    for b in not_connected:
        cost, dest = closest_reachable(b)
        if len(free_id) == 0:
            continue
        cur_id = random.choice(list(free_id))
        free_id.remove(cur_id)
        heapq.heappush(planned, [math.floor(cost * 10) + 1000, (b, dest, cur_id), 'TUBE ' + str(b) + ' ' + str(dest) +
                                 ';POD ' + str(cur_id) + 10 * (' ' + str(b) + ' ' + str(dest))])

    # print(planned[0][0], file=sys.stderr, flush=True)
    while planned:
        if resources - planned[0][0] < 0:
            free_id = set(list(range(1, 501)))
            for id in pods.keys():
                free_id.remove(id)
            break
        action = heapq.heappop(planned)
        if len(graph[action[1][0]]) == 5:
            connected.discard(action[1][0])
            free_id.add(action[1][2])
            continue
        if len(graph[action[1][1]]) == 5:
            connected.discard(action[1][1])
            free_id.add(action[1][2])
            continue

        intersect = False
        v, u = action[1][0], action[1][1]
        pv = (buildings[v][1], buildings[v][2])
        pu = (buildings[u][1], buildings[u][2])
        # intersection with other modules
        for p in buildings:
            if p == v or p == u:
                continue
            pp = (buildings[p][1], buildings[p][2])
            if point_intersect(pu, pv, pp):
                intersect = True
                break

        # intersection with other tubes
        for e in edges:
            pe1 = (buildings[e[0]][1], buildings[e[0]][2])
            pe2 = (buildings[e[1]][1], buildings[e[1]][2])
            if segment_intersect(pe1, pe2, pv, pu):
                intersect = True
                break

        if intersect:
            free_id.add(action[1][2])
            continue
        graph[action[1][0]].append(action[1][1])
        graph[action[1][1]].append(action[1][0])
        pods[action[1][2]] = (action[1][0], action[1][1])
        edges.append((action[1][0], action[1][1]))
        connected.add(action[1][1])
        not_connected.discard(action[1][1])
        connected.add(action[1][0])
        not_connected.discard(action[1][0])
        out.append(action[2])
        resources -= action[0]

    if out:
        print(*out, sep=';', end='\n')
    else:
        print('WAIT')

    # Wr55 ite an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    # print("TUBE 0 1;TUBE 0 2;POD 42 0 1 0 2 0 1 0 2")
