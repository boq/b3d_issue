import struct
import sys
from StringIO import StringIO

def nop(stream, level):
    pass

def bb3d(stream, level):
    rp(stream, level, "version", "<i")

    while True:
        chunk = read_chunk(stream, level)
        if not chunk: break

def texs(stream, level):
    while True:
        c = rc(stream, level, "file")
        if c is None: break
        rp(stream, level, "flags", "<I")
        rp(stream, level, "blend", "<I")
        rp(stream, level, "pos", "<ff")
        rp(stream, level, "scale", "<ff")
        rp(stream, level, "rotation", "<f")


def brus(stream, level):
    texs = rp(stream, level, "n_texs", "<I")

    while True:
        c = rc(stream, level, "name")
        if c is None: break
        rp(stream, level, "color", "<ffff")
        rp(stream, level, "shininess", "<f")
        rp(stream, level, "blend", "<I")
        rp(stream, level, "fx", "<I")

        for i in range(texs):
            rp(stream, level, "tex[%d]" % i, "<I")

def node(stream, level):
    rc(stream, level, "name")
    rp(stream, level, "pos", "<fff")
    rp(stream, level, "scale", "<fff")
    rp(stream, level, "rot", "<ffff")

    while True:
        chunk = read_chunk(stream, level)
        if not chunk: break

def bone(stream, level):
    while True:
        id = rf(stream, level, "weight[%d] = %f", "<If")
        if id is None: break

def keys(stream, level):
    flags = rp(stream, level, "flags", "<I")
    while True:
        frame = rp(stream, level, "frame", "<I")
        if frame is None: break
        if (flags & 1) != 0:
            rp(stream, level + 1, "pos", "<fff")
        if (flags & 2) != 0:
            rp(stream, level + 1, "scale", "<fff")
        if (flags & 4) != 0:
            rp(stream, level + 1, "rot", "<ffff")

def anim(stream, level):
    rp(stream, level, "flags", "<I")
    rp(stream, level, "frames", "<I")
    rp(stream, level, "fps", "<f")

def mesh(stream, level):
    rp(stream, level, "brush_id", "<i")
    while True:
        chunk = read_chunk(stream, level)
        if not chunk: break

def vrts(stream, level):
    flags = rp(stream, level, "flags", "<I")
    tex_sets = rp(stream, level, "tex_coord_sets", "<I")
    tex_coord_set_size = rp(stream, level, "tex_coord_set_size", "<I")

    while True:
        pos = rp(stream, level + 1, "pos", "<fff")
        if pos is None: break
        if (flags & 1) != 0:
            rp(stream, level + 1, "normal", "<fff")
        if (flags & 2) != 0:
            rp(stream, level + 1, "color", "<ffff")
        for set_i in range(tex_sets):
            for i in range(tex_coord_set_size):
                rp(stream, level + 2, "tex_coords[%d][%d]" % (set_i, i), "<f")

def tris(stream, level):
    rp(stream, level, "brush_id", "<i")
    id = 0
    while True:
        x = rp(stream, level + 1, "[%s]" % id, "<III")
        if x is None: break
        id += 1

METHODS = {
    "BB3D" : bb3d,
    "TEXS" : texs,
    "BRUS" : brus,
    "NODE" : node,
    "BONE" : bone,
    "KEYS" : keys,
    "ANIM" : anim,
    "MESH" : mesh,
    "VRTS" : vrts,
    "TRIS" : tris,
}

def unpack(stream, fmt):
    size = struct.calcsize(fmt)
    buf = stream.read(size)
    if len(buf) == 0: return None
    return struct.unpack(fmt, buf)

def pa(level, value):
    print "  " * level + value

def rp(stream, level, label, fmt):
    value = unpack(stream, fmt)
    if value is None: return None
    if len(value) == 1: value = value[0]
    pa(level, label + " = " + str(value))
    return value

def rf(stream, level, format, fmt):
    value = unpack(stream, fmt)
    if value is None: return None
    if len(value) == 1: value = value[0]
    pa(level, format % value)
    return value

def read_cstr(stream):
    result = ""
    while True:
        ch = stream.read(1)
        if len(ch) == 0:
            assert len(result) == 0
            return None
        if ord(ch) == 0: break
        result += ch

    return result

def rc(stream, level, label):
    value = read_cstr(stream)
    if value is None: return None
    pa(level, label + " = " + str(value))
    return value

def read_chunk(stream, level):
    id = stream.read(4)
    if len(id) == 0: return False
    pa(level, "CHUNK " + id)
    length = rp(stream, level + 1, "length", "<I")
    contents = StringIO(stream.read(length))

    METHODS.get(id, nop)(contents, level + 1)
    return True

for f in sys.argv[1:]:
    print "Processing " + f
    with open(f, "rb") as i:
        read_chunk(i, 0)

 