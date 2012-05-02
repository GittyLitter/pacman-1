import sys, random, string

# 28 wide
# 15 high

# ghost house at x=[10,15] y=[0,5]

# starting position at x=19 or x=22 preventing starting directions of right or left, respectively.

# piece types:
# - block
# - straight
# - bend
# - cross

class StartBlock:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Map:
    def __init__(self):
        self.cols = 28
        self.rows = 15
        self.tops = [0]*self.cols
        self.tiles = ['_']*self.rows*self.cols

        # insert ghost house
        self.insert_piece(10,0,6,6,'A')

    def get_tile(self,x,y):
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            return '_'
        return self.tiles[x+y*self.cols]

    def set_tile(self,x,y,key):
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            raise "(%d,%d) not a valid index" % (x,y)
        self.tiles[x+y*self.cols] = key

    # writes a rectangle block to the map
    def insert_piece(self,x,y,w,h,key):
        for y0 in xrange(y,y+h):
            for x0 in xrange(x,x+w):
                self.set_tile(x0,y0,key)
                self.tops[x0] = max(self.tops[x0],y0+1)

    # prints the straight tile map
    def print_tiles(self):
        for y in xrange(self.rows):
            for x in xrange(self.cols):
                sys.stdout.write(self.get_tile(x,y))
            print ""

    # prints the tile map with the paths in the grout
    def print_render(self):
        for y in xrange(self.rows):
            for x in xrange(self.cols):
                key = self.get_tile(x,y)
                if (self.get_tile(x-1,y-1) == key and
                    self.get_tile(x,y-1) == key and
                    self.get_tile(x-1,y) == key):
                    sys.stdout.write(key)
                else:
                    sys.stdout.write('.')
            print ""

    # update 'start_blocks' to reflect all valid starting positions for blocks to be created
    def update_next_positions(self):
        self.start_blocks = None

        # start at the lowest level possible
        top = min(self.tops)
        if top > self.rows-3:
            return

        # create a list of contiguous valleys (gaps)
        gaps = []
        curGap = None
        for x in xrange(self.cols):
            if self.tops[x] != top:
                continue
            if curGap and curGap[-1]+1 == x:
                curGap.append(x)
            else:
                curGap = [x]
                gaps.append(curGap)
        
        blocks = []
        for gap in gaps:
            gaplen = len(gap)
            if gaplen < 3:
                raise "gap too small"

            # create a list of nooks (vertical paths that block certain widths)
            nooks = []
            if top > 0:
                key = self.get_tile(gap[0],top-1)
                for x in gap[1:]:
                    newkey = self.get_tile(x,top-1)
                    if newkey != key:
                        if x-gap[0] == 1 or gap[-1] == x:
                            raise "nook right at edge of gap"
                        key = newkey
                        nooks.append(x)

            # get an initial set of possible widths
            def getPossibleWidths():
                widths = range(3,gaplen-2) + [gaplen]
                return set([w for w in widths if w <= 12])

            # final width filter to favor larger widths
            def filterWidths(widths):
                minWidth = 6
                newWidths = [w for w in widths if w >= minWidth]
                if len(newWidths) > 1:
                    return newWidths
                else:
                    return [max(widths)]

            # create block that starts at a left edge
            block = StartBlock(gap[0],top)
            block.dx = 1
            widths = getPossibleWidths()
            for x in nooks:
                # discard widths that come too close to the nooks
                widths.discard(x-1-block.x)
                widths.discard(x+1-block.x)
            block.possibleWidths = filterWidths(list(widths))
            blocks.append(block)

            if gaplen >= 6:
                # create block that starts at a right edge
                block = StartBlock(gap[-1]+1,top)
                block.dx = -1
                widths = getPossibleWidths()
                for x in nooks:
                    # discard widths that come too close to the nooks
                    widths.discard(block.x-(x-1))
                    widths.discard(block.x-(x+1))
                block.possibleWidths = filterWidths(list(widths))
                blocks.append(block)

        self.start_blocks = blocks

if __name__ == "__main__":

    m = Map()
    m.print_tiles()

    i = 1
    try:
        while True:
            m.update_next_positions()
            if not m.start_blocks:
                break
            block = random.choice(m.start_blocks)
            w = random.choice(block.possibleWidths)
            key = string.uppercase[i]
            i += 1
            if block.dx == 1:
                x = block.x
            else:
                x = block.x-w
            m.insert_piece(x,block.y,w,3,key)
            m.print_tiles()
            print ""
    finally:
        m.print_render()
