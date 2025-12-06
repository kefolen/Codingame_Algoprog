# import sys
import math
import heapq
import random
import time

eps = 1e-8
inf = 10 ** 9


def inp():
    astronauts = 0
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
                astronauts += 1
            ans.sort(key=lambda x: x[0], reverse=True)
            buildings[new_b[1]].append(ans)

    return resources, new_buildings, astronauts


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
    anss = []

    visited = set()
    for color in target.keys():
        ans = [inf, -1, 0, inf]
        for u in dsu_v[color]:
            cnt = 0
            if u in visited: continue
            visited.add(u)

            for i in target.keys():
                if leader(u) in dsu_v[i]:
                    cnt += target[i]

            if tp[v] == False and tp[u] == False and ans[0] == inf and cnt > ans[2]:
                ans = [inf, u, cnt, 5000 / cnt]

            pu = (buildings[u][1], buildings[u][2])

            if (math.floor(distance(pu, pv) * 10) + 1000) / cnt < ans[-1]:
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
                for e in edges.keys():
                    if edges[e] == 0: continue
                    pe1 = (buildings[e[0]][1], buildings[e[0]][2])
                    pe2 = (buildings[e[1]][1], buildings[e[1]][2])
                    if segment_intersect(pe1, pe2, pv, pu):
                        intersect = True
                        break

                if not intersect:
                    ans = [(math.floor(distance(pu, pv) * 10) + 1000), u, cnt,
                           (math.floor(distance(pu, pv) * 10) + 1000) / cnt]
        anss.append(ans)

    anss.sort(key=lambda x: x[-1])
    return anss


def deikstra(d, p, visited, start, color):
    q = []
    for i in start:
        d[color][i] = 0
        q.append([0, i])

    heapq.heapify(q)
    while q:
        x = heapq.heappop(q)[1]
        for i in graph[x]:
            if visited[color][i[0]]: continue
            if d[color][i[0]] > d[color][x] + 1 * (i[1] != 0):
                d[color][i[0]] = d[color][x] + 1 * (i[1] != 0)
                p[color][i[0]] = x
                heapq.heappush(q, [d[color][x], x])
            visited[color][x] = 1

    return d, p, visited


def pos_upgrades(colors):
    dist = [[inf for i in range(150)] for j in range(21)]
    parent = [[-1 for i in range(150)] for j in range(21)]
    visited = [[0 for i in range(150)] for j in range(21)]
    flow = {e: [edges[e], 0] for e in edges.keys()}
    upgrades = []
    for i in range(1, 21):
        if len(colors[i]) == 0: continue
        dist, parent, visited = deikstra(dist, parent, visited, colors[i], i)

        for b in land:
            for color in buildings[b][-1]:
                if dist[color[1]][b] == inf: continue
                cnt = color[0]
                cur = b
                p = parent[color[1]]
                while p[cur] != -1:
                    if (cur, p[cur]) in flow:
                        flow[(cur, p[cur])][1] += cnt
                    else:
                        flow[(p[cur], cur)][1] += cnt
                    cur = p[cur]

    for edge in flow.keys():
        if flow[edge][0] == 0 or flow[edge][0] * 10 >= flow[edge][1]: continue
        pv = (buildings[edge[0]][1], buildings[edge[0]][2])
        pu = (buildings[edge[1]][1], buildings[edge[1]][2])
        cost = (flow[edge][0] + 1) * math.floor(distance(pu, pv) * 10) + 1000
        score = cost / (flow[edge][1]) * flow[edge][0]
        upgrades.append((score, edge, cost))

    return upgrades


graph = {}
edges = {}
pods = {}
buildings = {}
free_id = set(list(range(1, 501)))
land = set()
dsu_p = [-1 for i in range(150)]
dsu_s = [0 for j in range(150)]
dsu_v = {i: set() for i in range(1, 21)}
tp = [False for i in range(150)]
destinations = [list() for i in range(21)]
astronauts = 0
# game loop
tl = 0.40
distribution = 0.1
qlimit = 500
for _ in range(20):

    start_time = time.time()

    out = []
    planned = []
    heapq.heapify(planned)
    resources, new, astronauts = inp()
    old_resources = resources
    for i in new:
        dsu_s[i] = 1
        dsu_p[i] = i
        if buildings[i][0] != 0:
            dsu_v[buildings[i][0]].add(i)
            destinations[buildings[i][0]].append(i)
        else:
            land.add(i)

    for b in land:
        # if time.time() - start_time > tl:
        # break
        target = {}
        for i in buildings[b][-1]:
            if not leader(b) in dsu_v[i[1]]:
                target[i[1]] = i[0]
        if target:

            possible = closest_reachable(b, target)
            for i in range(len(possible)):
                if qlimit < len(land) * i: break
                cost, dest, cnt, score = possible[i]
                if cost != inf:
                    if len(free_id) == 0:
                        continue
                    cur_id = free_id.pop()
                    heapq.heappush(planned, [score, (b, dest, cur_id), 'TUBE ' + str(b) + ' ' + str(dest) +
                                             ';POD ' + str(cur_id) + 10 * (' ' + str(b) + ' ' + str(dest)), cost])
                elif dest != -1:
                    cost = 5000
                    heapq.heappush(planned, [score, (b, dest, -1), 'TELEPORT ' + str(b) + ' ' + str(dest), cost])

    while planned:
        action = heapq.heappop(planned)
        if resources - action[-1] < distribution * old_resources:
            if action[1][2] != -1:
                free_id.add(action[1][2])
            continue

        if action[1][2] != -1:
            if leader(action[1][0]) == leader(action[1][1]):
                continue
            if len(graph[action[1][0]]) == 5:
                free_id.add(action[1][2])
                continue
            if len(graph[action[1][1]]) == 5:
                free_id.add(action[1][2])
                continue
            if (action[1][0], action[1][1]) in edges.keys():
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
            for e in edges.keys():
                if edges[e] == 0: continue
                pe1 = (buildings[e[0]][1], buildings[e[0]][2])
                pe2 = (buildings[e[1]][1], buildings[e[1]][2])
                if segment_intersect(pe1, pe2, pv, pu):
                    intersect = True
                    break

            if intersect:
                free_id.add(action[1][2])
                continue
            graph[action[1][0]].append([action[1][1], 1])
            graph[action[1][1]].append([action[1][0], 1])
            pods[action[1][2]] = [action[1][0], action[1][1], 1]
            edges[(action[1][0], action[1][1])] = 1

        else:
            if tp[action[1][0]] == True or tp[action[1][1]] == True:
                continue
            graph[action[1][0]].append([action[1][1], 0])
            edges[(action[1][0], action[1][1])] = 0
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

    up_planned = pos_upgrades(destinations)
    heapq.heapify(up_planned)

    while up_planned:
        action = heapq.heappop(up_planned)
        if resources - action[-1] < 0:
            break

        cur_id = free_id.pop()
        text1 = "UPGRADE " + str(action[1][0]) + ' ' + str(action[1][1])
        text2 = "POD " + str(cur_id) + 10 * (' ' + str(action[1][0]) + ' ' + str(action[1][1]))
        out.append(text1)
        out.append(text2)
        edges[(action[1][0], action[1][1])] += 1
        resources -= action[-1]

    if out:
        print(*out, sep=';', end='\n')
    else:
        print('WAIT')

    # Wr55 ite an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    # print("TUBE 0 1;TUBE 0 2;POD 42 0 1 0 2 0 1 0 2")
