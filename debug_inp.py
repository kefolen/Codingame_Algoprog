def inp():
    astronauts = 0
    resources = int(input())
    print(resources, file=sys.stderr, flush=True)
    num_travel_routes = int(input())
    print(num_travel_routes, file=sys.stderr, flush=True)
    for i in range(num_travel_routes):
        building_id_1, building_id_2, capacity = [int(j) for j in input().split()]
        print(building_id_1, building_id_2, capacity, file=sys.stderr, flush=True)
    num_pods = int(input())
    print(num_pods, file=sys.stderr, flush=True)

    for i in range(num_pods):
        pod_properties = input()
        print(pod_properties, file=sys.stderr, flush=True)


    cnt_new_b = int(input())
    print(cnt_new_b, file=sys.stderr, flush=True)
    new_buildings = []
    for i in range(cnt_new_b):
        new_b = list(map(int, input().split()))
        print(*new_b, file=sys.stderr, flush=True)
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