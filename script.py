import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):

    name = ''
    num_frames = 1
    vary = False

    for c in commands:
        if c['op'] == 'basename':
            name = c['args'][0]

        elif c['op'] == 'frames':
            num_frames = int(c['args'][0])

        elif c['op'] == 'vary' or c['op'] == 'tween':
            vary = True

    if vary and num_frames == 1:
        print("Vary value found, but not frames. Exiting")
        quit()

    if name == '':
        name = 'default_gif'
        print("No basename given. Using default value of default_gif")


    return (name, num_frames)

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
  # tween
def second_pass( commands, symbols, num_frames ):
    frames = [ {} for i in range(num_frames) ]

    for c in commands:
        if c['op'] == 'vary':
            args = c['args']
            start_frame = int(args[0])
            end_frame = int(args[1])
            knob = c['knob']
            start_knob = float(args[2])
            end_knob = float(args[3])
            d_k = (end_knob - start_knob) / (end_frame - start_frame)
            for i in range(start_frame, end_frame):
                start_knob += d_k
                frames[i][knob] = start_knob
                # tween
        elif c['op'] == 'tween':
            args = c['args']
            start_frame = args[0]
            end_frame = args[1]
            kstart = symbols[c['knob_list0']][1]
            kend = symbols[c['knob_list1']][1]

            for start_knob, end_knob in zip(kstart,kend):
                knob_name = start_knob[0]
                start_value = start_knob[1][1]
                end_value = end_knob[1][1]
                d_k= (end_value - start_value) / (end_frame - start_frame)
                for f in range(num_frames):
                    if f == start_frame:
                        frames[f][knob_name] = start_value
                    elif f >= start_frame and f <= end_frame:
                        start_value += d_k
                        frames[f][knob_name] = start_value

    return frames


def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, symbols, num_frames)


    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []

    count = 0

    for frame in frames:

        print count

        for command in commands:
            c = command['op']
            args = command['args']
            knob_value = 1

            for knob in frame.keys():
                    symbols[knob] = frame[knob]

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                knob = command['knob']

                if knob:
                    tmp = make_translate(args[0]*symbols[knob], args[1]*symbols[knob], args[2]*symbols[knob])
                else:
                    tmp = make_translate(args[0], args[1], args[2])

                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                knob = command['knob']

                if knob:
                    tmp = make_scale(args[0]*symbols[knob], args[1]*symbols[knob], args[2]*symbols[knob])
                else:
                    tmp = make_scale(args[0], args[1], args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                knob = command['knob']

                if knob:
                    theta = args[1] * symbols[knob] * (math.pi/180)
                else:
                    theta = args[1]* (math.pi/180)

                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])

        if(name != 'default_gif' and num_frames != 1):
            diff = len(str(num_frames)) - len(str(count))

            add_string = "0" * diff + str(count)
            save_extension(screen, "./anim/"+ name + add_string)
            tmp = new_matrix()
            ident( tmp )
            stack = [ [x[:] for x in tmp] ]
            screen = new_screen()
            zbuffer = new_zbuffer()
            count += 1

    if(name != 'default_gif' and num_frames != 1):
        make_animation(name)


        # end operation loop
