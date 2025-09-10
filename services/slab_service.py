import math as ma

def slab_precalc(element_data: dict) -> dict:
    
    lx = float(element_data.get("lx", 0) or 0)
    ly = float(element_data.get("ly", 0) or 0)
    n = float(element_data.get("n", 0) or 1)
    cover = float(element_data.get("cover", 0) or 0)
    diameter = float(element_data.get("diameter", 0) or 0)
    slab_name = str(element_data.get("name"))

    l = min(lx, ly * 0.7)
    d = (2.5 - 0.1 * n) * l / 100
    h = ma.ceil(d + (diameter / 2) + cover)
    return {
        "name" : slab_name,
        "height": h,
    }

