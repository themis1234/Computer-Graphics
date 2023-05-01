import numpy as np
import matplotlib.pyplot as plt


def interpolate_vectors(p1,p2,V1,V2,xy,dim):
    x1,y1 = p1
    x2,y2 = p2

    if dim ==1:
        x = xy
        l = (x2 - x) / (x2 - x1)
        return l*np.array(V1) +(1-l)*np.array(V2)
    else:
        y = xy
        l = (y2 - y) / (y2 - y1)
        return l*np.array(V1) + (1-l)*np.array(V2)


def bresenham(point1:list, point2:list):

    result = [] 

    x1 = point1[0]
    x2 = point2[0]
    dx = abs(x2 - x1)

    y1 = point1[1]
    y2 = point2[1]
    dy = abs(y2 - y1)

    x, y = x1, y1
    flag = False
    #if slope > 1 then we do the brensenham but for y, so all pixels can be covered
    if dy > dx: 
        dx, dy = dy, dx
        x, y = y, x
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        flag = True

    p = 2 * dy - dx

    if flag:
        result.append([y, x])
    else:
        result.append([x, y])

    for k in range(dx):
        if p > 0:
            y = y + 1 if y < y2 else y - 1
            p = p + 2*(dy - dx)
        else:
            p = p + 2*dy
        x = x + 1 if x < x2 else x - 1
        

        if flag:
            result.append([y, x])
        else:
            result.append([x, y])

    return result

def flat(canvas: list, vetrices:list,vcolors:list):

    e1 = bresenham(vetrices[0], vetrices[1])
    e2 = bresenham(vetrices[1], vetrices[2])
    e3 = bresenham(vetrices[2], vetrices[0])
    
    final_color = [0,0,0]
    #Final color is the average color of the vetrices that make up the 
    final_color[0] = (vcolors[0][0] + vcolors[1][0] + vcolors[2][0])/ 3
    final_color[1] = (vcolors[0][1] + vcolors[1][1] + vcolors[2][1])/ 3
    final_color[2] = (vcolors[0][2] + vcolors[1][2] + vcolors[2][2])/ 3        #b)
    for point in e1:
        canvas[point[1]][point[0]] = list(final_color)
    for point in e2:
        canvas[point[1]][point[0]] = list(final_color)
    for point in e3:
         canvas[point[1]][point[0]] = list(final_color)
    
    mix_x = min(vetrices[:,0]) #Starting x coordinate
    max_x = max(vetrices[:,0]) #Finishing x coordinate

    for x in range(mix_x, max_x + 1):
        inter_points = [] #the two points that the in-between points will be colored of
        for point in e1:
            if point[0] == x:
                inter_points.append(point)
        for point in e2:
            if point[0] == x:
                inter_points.append(point)
        for point in e3:
            if point[0] == x:
                inter_points.append(point)

        #If the points found are the same point
        if len(inter_points) == 1:
            continue
        else:
            inter_points = sorted(inter_points,key = lambda x:x[1])
            min_y = inter_points[0]
            #In case the triange is actually a line, instead of the second element we take the last
            max_y = inter_points[-1] 

            #fill the points inbetween the two points 
            for i in range(min_y + 1, max_y):
                if [i, x] in inter_points:
                    continue
                else:
                    canvas[i][x] = list(final_color)

def Gourauds(canvas: list, vetrices: list, vcolors: list):

    e1 = bresenham(vetrices[0], vetrices[1])
    e2 = bresenham(vetrices[1], vetrices[2])
    e3 = bresenham(vetrices[2], vetrices[0])
    
    #We exclude the first and last point of each line because they are the points
    #that we use to color the rest
    for i in range(1,len(e1)-1):

        dim = 0
        point = e1[i]
        coo = point[1]
        #If slope > 1 we shade as of y and not x so that the shading is more precise
        if abs(vetrices[0][0] - vetrices[1][0]) > abs(vetrices[0][1] - vetrices[1][1]):
            dim = 1
            coo = point[0]
        canvas[point[1]][point[0]] = interpolate_vectors(vetrices[0], vetrices[1], vcolors[0], vcolors[1],coo,dim)
 
    for i in range(1,len(e2)-1):
    
        dim = 0
        point = e2[i]
        coo = point[1]

        if abs(vetrices[1][0] - vetrices[2][0]) > abs(vetrices[1][1] - vetrices[2][1]):
            dim = 1
            coo = point[0]
        canvas[point[1]][point[0]] = interpolate_vectors(vetrices[1], vetrices[2], vcolors[1], vcolors[2],coo,dim)

    for i in range(1,len(e3)-1):
        
        dim = 0
        point = e3[i]
        coo = point[1]
        if abs(vetrices[2][0] - vetrices[0][0]) > abs(vetrices[2][1] - vetrices[0][1]):
            dim = 1 
            coo = point[0]
        canvas[point[1]][point[0]] = interpolate_vectors(vetrices[2], vetrices[0], vcolors[2], vcolors[0],coo,dim)
   
    #Here we color the start and end of each line
    for i in range(len(vetrices)):
        point = vetrices[i]
        canvas[point[1]][point[0]] = vcolors[i]

    
    mix_x = min(vetrices[:,0])  
    max_x = max(vetrices[:,0])

    for x in range(mix_x, max_x + 1):
        inter_points = [] 
        for point in e1:
            if point[0] == x:
                inter_points.append(point)
                break
        for point in e2:
            if point[0] == x:
                inter_points.append(point)
                break
        for point in e3:
            if point[0] == x:
                inter_points.append(point)
                break

        if len(inter_points) == 1:
            continue
        else:
            inter_points = sorted(inter_points,key = lambda x:x[1])
            min_y = inter_points[0]
            max_y = inter_points[-1] 
            
            for i in range(min_y[1] + 1, max_y[1]):
                if [i, x] in inter_points:
                    continue
                else:    
                    canvas[i][x] = interpolate_vectors(min_y, max_y, canvas[min_y[1]][x], canvas[max_y[1]][x],i,2)
                    

def render(vetrices: list, faces: list, vcolors: list, depth: list, shade_t):
    m = 512
    n = 512
    canvas = [[[1.0 for i in range(3)] for j in range(m)] for k in range(n)]

    triangle_colors = []
    average_depth = []
    for i in range(len(faces)):
        triangle = faces[i]
        #We will subsitute the values of faces with the actuall coordinates of the triangle
        faces[i] = [vetrices[triangle[0]], vetrices[triangle[1]], vetrices[triangle[2]]]

        #Triangle depth is the average depth of its points that make it
        new_depth = (depth[triangle[0]] + depth[triangle[1]] + depth[triangle[2]]) / 3
        triangle_colors.append([vcolors[triangle[0]], vcolors[triangle[1]], vcolors[triangle[2]]])
        average_depth.append(new_depth)

    #We sort the arrays based on depths
    order = np.argsort(average_depth)
    faces = np.array(faces)
    faces = faces[order]
    triangle_colors = np.array(triangle_colors)
    triangle_colors = triangle_colors[order]
    if shade_t == 'gourauds':
        for i in range(len(faces)):
            Gourauds(canvas, faces[i], triangle_colors[i])
    elif shade_t == 'flat':
        for i in range(len(faces)):
            flat(canvas,faces[i],triangle_colors[i])
    else:
        print("Wrong shading option, choose bewteen gourauds and flat")
    return canvas

data = np.load('h1.npy', allow_pickle=True)
vcolors = data[()]['vcolors'].tolist()
faces = data[()]['faces'].tolist()
depth = data[()]['depth'].tolist()
vetrices = data[()]['verts2d'].astype(int).tolist()

canvas = render(vetrices, faces, vcolors, depth,'gourauds')
plt.imshow(canvas, interpolation='nearest')
plt.title('Gourauds')
plt.show()
