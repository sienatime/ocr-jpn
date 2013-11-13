from PIL import Image

def check_neighbors(color, counter, up, left, eq, final_ctr):
    #check the values of the pixels up and to the left. if either of those pixels is the same color, make the value of the current pixel the same. 
    if up and color in up:
        if left and color in left and up != left:
            #if BOTH up and left are the same color but different values (e.g. black2 and black4, we have found a new equality and we need to add to our counter and put the equality in the right bucket.
            final_ctr = add_to_equalities(eq, up, left, final_ctr)
        return up, final_ctr
    elif left and color in left:
        return left, final_ctr
    else:
        return None, final_ctr

def search_equalities(eq, val):
    #return the index of the value if it exists in the equalities list
    for i in range(len(eq)):
        if val in eq[i]:
            return i
    return None

def add_to_equalities(eq, val1, val2, final_ctr):
    #this function adds to the equality buckets if appropriate. there should be no duplicates in the buckets.

    #first, see if either of these values are already in the buckets.
    val1_i = search_equalities(eq, val1)
    val2_i = search_equalities(eq, val2)

    #if both of the values are already in SEPARATE buckets, we need to join those buckets.
    #note: Python counts 0 as False, so we have to check explicitly if the values are None.
    if val1_i != val2_i and val1_i != None and val2_i != None:
        join = eq[val1_i] + eq[val2_i]
        eq[val1_i] = join
        del eq[val2_i]
        final_ctr += 1
        return final_ctr
    #otherwise if one of the values is in a bucket but not the other, add the other to that bucket.
    elif val1_i != None and val2_i == None:
        eq[val1_i].append(val2)
        final_ctr += 1
        return final_ctr
    elif val2_i != None and val1_i == None:   
        eq[val2_i].append(val1)
        final_ctr += 1
        return final_ctr
    #if neither of the values are in a bucket yet, make a new bucket.
    elif val1_i == None and val2_i == None:
        final_ctr += 1
        eq.append([val1, val2])

    #final_ctr keeps track of the number of equalities found so far. every time we find one, we add to it.
    return final_ctr

def find_islands(im):
    #This function counts the number of black and white "islands" (isolated spaces) in a thresholded image.
    im_x, im_y = im.size

    #these will increment every time we find a new island. however, we will also have to assign equalities between islands and we traverse down the image so this is not our final island countself.
    black = 0
    white = 0
    #the equalities are lists of lists that contain all the black or white pixels that should be treated as one island
    bl_equalities = []
    wh_equalities = []
    #these are the number of equalities found.
    bl_eq_ctr = 0
    wh_eq_ctr = 0

    #an empty matrix the same size as the image. this will get populated with values like black1 white1 black2 etc
    islands = [[None for x in xrange(im_y)] for x in xrange(im_x)] 

    #traverse the image and build out islands and equalities
    for i in range(im_y):
        for j in range(im_x):
            val = im.getpixel((j,i))
            
            #to avoid index out of bounds errors, we simply assign up or left to None if it doesn't exist.
            try:
                up = islands[j][i-1]
            except(IndexError):
                up = None

            try:
                left = islands[j-1][i]
            except(IndexError):
                left = None

            #for black or white, check the neighboring up and/or left pixels to see if we are part of an island of the same color
            if val == 0:
                put_val, bl_eq_ctr = check_neighbors("black", black, up, left, bl_equalities, bl_eq_ctr)
                # check_neighbors will return None if we are in a new island
                if put_val:
                    islands[j][i] = put_val
                else:
                    #if we have found a new island, increment the counter and put that new value into islands
                    black += 1
                    islands[j][i] = "black" + str(black)
            elif val == 255:
                put_val, wh_eq_ctr = check_neighbors("white", white, up, left, wh_equalities, wh_eq_ctr)
                if put_val:
                    islands[j][i] = put_val
                else:
                    white += 1
                    islands[j][i] = "white" + str(white)
            else:
                raise TypeError("Non black or white pixel found.")

    debug = False
    if debug:
        for column in range(im_y):
            for elt in range(im_x):
                print islands[elt][column],
            print "\n"

        print black
        print bl_equalities
        print white
        print wh_equalities

    #the final number of islands is the counter minus the number of equalities found.
    return (black-bl_eq_ctr,white-wh_eq_ctr)