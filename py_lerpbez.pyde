ELLIPSE_SIZE = 5
#allows the enabling drawing of sub-paths - hardcoded as it probably turns the complexity into some degree of superexponential. Use at own risk.
ENABLE_SUBPATHS = False

def genLerps(points, t):
    if len(points) >= 2:
        lerps = [(lerp(x1, x2, t), lerp(y1, y2, t))
                 for (x1, y1), (x2, y2) in getAdjacents(points)]
        return [lerps] + genLerps(lerps, t)
    else:
        return [points]

def reset_path():
    global point_path, complete, t
    if ENABLE_SUBPATHS:
        point_path = [[i] for i in sum(genLerps(points, 0), [])]
    else:
        point_path = [points[0][:]]
    complete = False
    t = 0

def setup():
    global points, t_delta, animate, display_guides, rainbow_lerps, draw_subpaths
    size(1000, 800)
    background(0)
    points = [[50, 50], [350, 500], [650, 500], [950, 50]]
    t_delta = 0.001
    animate = True
    display_guides = True
    rainbow_lerps = False
    draw_subpaths = False
    reset_path()

def mousePressed():
    global t
    reset_path()
    min(points, key=lambda (a, b): dist(a, b, mouseX, mouseY))[:] = mouseX, mouseY

mouseDragged = mousePressed

def getAdjacents(l):
    return (l[i:i + 2] for i in range(len(l) - 1))

def keyPressed():
    global animate, t_delta, display_guides, rainbow_lerps, draw_subpaths
    if keyCode == ord("I"):
        animate = not animate
        print("animation is now {}".format(animate))
    elif keyCode == ord(" "):
        points.append([mouseX, mouseY])
        reset_path()
        print("new point added at {}".format(points[-1]))
    elif keyCode == ord("A"):
        t_delta /= 1.1
        print("delta is now {}".format(t_delta))
    elif keyCode == ord("D"):
        t_delta *= 1.1
        print("delta is now {}".format(t_delta))
    elif keyCode in [ENTER, RETURN, ord("\n")]:
        display_guides = not display_guides
        print("display_guides is now {}".format(display_guides))
    elif keyCode == ord("R"):
        setup()
        print("reset")
    elif keyCode == ord("P"):
        reset_path()
        print("path has been reset")
    elif keyCode in [UP, DOWN, LEFT, RIGHT]:
        action = {
            UP: (0, -10), DOWN: (0, 10), LEFT: (-10, 0), RIGHT: (10, 0)}[keyCode]
        for p in points + point_path:
            p[:] = map(sum, zip(p, action))
        print("grid transformed by {}".format(action))
    elif keyCode == ord("X"):
        rainbow_lerps = not rainbow_lerps
        print("rainbow_lerps is now {}".format(rainbow_lerps))
    elif keyCode == ord("Z"):
        draw_subpaths = not draw_subpaths
        print("draw_subpaths is now {}".format(draw_subpaths))
    elif keyCode in [BACKSPACE, DELETE, ord("\b")]:
        if len(points) > 1:
            p = points.pop()
            reset_path()
            print("popped point at {}".format(p))
        else:
            print("too few points")
    elif keyCode == ord("F"):
        print("frame rate is {}".format(frameRate))

def draw():
    global t, complete
    if animate:
        t += t_delta
        if t > 1:
            complete = True
            t -= 1
    background(0)
    fill(255)
    stroke(255)
    strokeWeight(1)
    lerps = [points] + genLerps(points, t)

    if rainbow_lerps:
        colorMode(HSB, 120, 120, 120)
    to_draw = (lerps[:-1] if display_guides else [points])
    for ind, pl in enumerate(to_draw):
        if rainbow_lerps:
            clr = (map(ind, 0, len(to_draw), 20, 120), 120, 120)
            stroke(*clr)
            fill(*clr)
        for (x1, y1), (x2, y2) in getAdjacents(pl):
            ellipse(x1, y1, ELLIPSE_SIZE, ELLIPSE_SIZE)
            line(x1, y1, x2, y2)
        x, y = pl[-1]
        ellipse(x, y, ELLIPSE_SIZE, ELLIPSE_SIZE)
    colorMode(RGB, 255, 255, 255)

    (bx, by), = lerps[-1]
    fill(255, 0, 0)
    stroke(255, 0, 0)
    ellipse(bx, by, 10, 10)
    if not complete:
        if ENABLE_SUBPATHS:
            point_path[:] = [
                a + b for a, b in zip(point_path, [[i] for i in sum(lerps[1:], [])])]
        else:
            point_path.append([bx, by])

    strokeWeight(1.2)
    if rainbow_lerps:
        colorMode(HSB, 120, 120, 120)
    else:
        stroke(255)
        
    if not ENABLE_SUBPATHS:
        to_draw = [point_path]
    else:
        to_draw = (point_path if draw_subpaths else [point_path[-1]])

    for ind, path in enumerate(to_draw):
        if rainbow_lerps:
            if ind == len(to_draw) - 1:
                clr = (120, 120, 120)
            else:
                clr = (map(ind, 0, len(to_draw), 20, 120), 120, 120)
            stroke(*clr)
        elif ind == len(to_draw) - 1:
            stroke(255, 0, 0)
        for (x1, y1), (x2, y2) in getAdjacents(path):
            line(x1, y1, x2, y2)