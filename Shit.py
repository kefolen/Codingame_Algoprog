import sys
import math
import heapq
import random

eps = 1e-8
inf = 10 ** 9


def leader(v):
    if dsu_p[v] == v:
        return v
    dsu_p[v] = leader(dsu_p[v])
    return dsu_p[v]


def unite(a, b):
    a = leader(a)
    b = leader(b)
    if dsu_s[a] > dsu_s[b]:
        a, b = b, a
    dsu_s[b] += dsu_s[a]
    dsu_p[a] = b
    # for i in dsu_v[a]:
    # dsu_v[b].add(i)


def representative(a):
    ans = set()
    for i in range(1, 21):
        if a in dsu_v[i]:
            ans.add(i)
    return ans


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
        buildings[new_b[1]] = [new_b[0]] + new_b[2:4]
        if new_b[0] == 0:
            cnt = {}
            ans = []
            for j in range(new_b[4]):
                if new_b[5 + j] in cnt:
                    cnt[new_b[5 + j]] += 1
                else:
                    cnt[new_b[5 + j]] = 1

            for j in cnt:
                ans.append([cnt[j], j])
            ans.sort(key=lambda x: x[0], reverse=True)
            buildings[new_b[1]].append(ans)

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


def closest_reachable(v, target):
    pv = (buildings[v][1], buildings[v][2])
    ans = [inf, -1]
    for u in dsu_v[target]:
        if tp[v] == False and tp[u] == False and ans[0] == inf:
            ans[-1] = u
        pu = (buildings[u][1], buildings[u][2])

        if distance(pu, pv) < ans[0]:
            intersect = False

            # intersection with other modules
            for p in buildings.keys():
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
free_id = set(list(range(1, 501)))
land = set()
dsu_p = [-1 for i in range(150)]
dsu_s = [0 for j in range(150)]
dsu_v = {i: set() for i in range(1, 21)}
tp = [False for i in range(150)]
# game loop


for _ in range(20):
    planned = []
    heapq.heapify(planned)
    resources, new = inp()
    out = []

    for i in new:
        dsu_s[i] = 1
        dsu_p[i] = i
        if buildings[i][0] != 0:
            dsu_v[buildings[i][0]].add(i)
        else:
            land.add(i)

    delayed = []
    for b in land:
        target = -1
        cnt = -1
        for i in buildings[b][-1]:
            if leader(b) in dsu_v[i[1]]:
                continue
            target = i[1]
            cnt = i[0]

            cost, dest = closest_reachable(b, target)
            if cost != inf:
                if len(free_id) == 0:
                    continue
                cur_id = random.choice(list(free_id))
                free_id.remove(cur_id)
                heapq.heappush(planned,
                               [(math.floor(cost * 10) + 1000) / cnt, (b, dest, cur_id),
                                'TUBE ' + str(b) + ' ' + str(dest) +
                                ';POD ' + str(cur_id) + 10 * (' ' + str(b) + ' ' + str(dest)),
                                math.floor(cost * 10) + 1000])
            elif dest != -1:
                heapq.heappush(planned, [5000 / cnt, (b, dest, -1), 'TELEPORT ' + str(b) + ' ' + str(dest), 5000])

        if target == -1:
            delayed.append(b)
            break

    for i in delayed:
        land.discard(i)

    # print(planned[0][0], file=sys.stderr, flush=True)
    while planned:
        action = heapq.heappop(planned)
        if resources - action[-1] < 0:
            if action[1][2] != -1:
                free_id.add(action[1][2])
            continue

        if leader(action[1][0]) == leader(action[1][1]):
            continue

        if action[1][2] != -1:
            if len(graph[action[1][0]]) == 5:
                free_id.add(action[1][2])
                continue
            if len(graph[action[1][1]]) == 5:
                free_id.add(action[1][2])
                continue
            if (action[1][0], action[1][1]) in edges:
                free_id.add(action[1][2])
                continue
            intersect = False
            v, u = action[1][0], action[1][1]
            pv = (buildings[v][1], buildings[v][2])
            pu = (buildings[u][1], buildings[u][2])
            # intersection with other modules
            for p in buildings.keys():
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
        else:
            if tp[action[1][0]] == False or tp[action[1][1]] == False:
                continue
            tp[action[1][0]] = True
            tp[action[1][1]] = True

        r1 = representative(action[1][1])
        if dsu_s[leader(action[1][0])] == 1:
            for x in r1:
                dsu_v[x].add(action[1][0])
        else:
            r2 = representative(action[1][0]).union(r1)
            spam = set()
            for x in r2:
                spam = spam.union(dsu_v[x])

            for x in r2:
                dsu_v[x] = spam.copy()

        unite(action[1][0], action[1][1])

        out.append(action[2])
        resources -= action[-1]

    if out:
        print(*out, sep=';', end='\n')
    else:
        print('WAIT')

    # Wr55 ite an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    # print("TUBE 0 1;TUBE 0 2;POD 42 0 1 0 2 0 1 0 2")
