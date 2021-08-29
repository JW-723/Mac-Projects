
def physical_function(students,turns,neighbor):
    assert students >= neighbor
    turn_flag = True
    even_flag = True if students % 2 == 0 else False
    students = [x for x in range(1,students+1)]

    while turns != 0:
        if turn_flag:
            start = students[0]
            switches = len(students)//2 * 2
            count = 0
            while count < switches:
                students[count],students[count+1] = students[count+1],students[count]
                count += 2
            turn_flag = not turn_flag
            
            
        else:
            start = students[-1]
            switches = len(students)//2
            swaps = 0
            count = 0 if even_flag else -1
            while swaps < switches:
                students[count],students[count-1] = students[count-1],students[count]
                count -= 2
                swaps += 1

            turn_flag = not turn_flag

        turns -= 1
    
    location = students.index(neighbor)
    if location == len(students)-1:
        print(students[0], students[location-1])
    else:
        print(students[location+1], students[location-1])

x = input()
val = x.split()
val = [int(x) for x in val]

physical_function(val[0],val[1],val[2])