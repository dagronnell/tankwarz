# Credits ChatGPT
def _project_polygon(axis, polygon):
    # Projicerar polygonens hörn på axeln och returnerar minsta och största värde
    min_proj = max_proj = None
    for point in polygon:
        proj = point[0] * axis[0] + point[1] * axis[1]
        if min_proj is None or proj < min_proj:
            min_proj = proj
        if max_proj is None or proj > max_proj:
            max_proj = proj
    return min_proj, max_proj


def _is_separating_axis(axis, polygon1, polygon2):
    # Kontrollerar om en axel är en separerande axel
    min_proj1, max_proj1 = _project_polygon(axis, polygon1)
    min_proj2, max_proj2 = _project_polygon(axis, polygon2)
    if max_proj1 < min_proj2 or max_proj2 < min_proj1:
        return True  # Det finns ett gap
    return False


def polygons_collide(poly1, poly2):
    # Huvudfunktionen för kollisionsdetektering

    for i in range(len(poly1)):
        # Skapa en kant och dess normal (perpendikulär)
        edge = (poly1[i][0] - poly1[i - 1][0], poly1[i][1] - poly1[i - 1][1])
        axis = (-edge[1], edge[0])
        if _is_separating_axis(axis, poly1, poly2):
            return False  # Det finns en separerande axel, ingen kollision
    # Upprepa för den andra polygonen
    for i in range(len(poly2)):
        edge = (poly2[i][0] - poly2[i - 1][0], poly2[i][1] - poly2[i - 1][1])
        axis = (-edge[1], edge[0])
        if _is_separating_axis(axis, poly1, poly2):
            return False
    return True  # Ingen separerande axel hittades, polygonerna kolliderar


def line_intersects_with(line_start, line_end, rect):
    # Funktion för att kontrollera om två linjesegment korsar varandra
    def segments_intersect(a1, a2, b1, b2):
        def ccw(p1, p2, p3):
            return (p3[1] - p1[1]) * (p2[0] - p1[0]) > (p2[1] - p1[1]) * (p3[0] - p1[0])

        return ccw(a1, b1, b2) != ccw(a2, b1, b2) and ccw(a1, a2, b1) != ccw(a1, a2, b2)

    # Skapa linjesegment för väggens kanter
    top_left = rect.topleft
    top_right = rect.topright
    bottom_left = rect.bottomleft
    bottom_right = rect.bottomright

    # Kontrollera om någon av väggens kanter korsar linjen från tanken till spelaren
    return (segments_intersect(line_start, line_end, top_left, top_right) or
            segments_intersect(line_start, line_end, top_right, bottom_right) or
            segments_intersect(line_start, line_end, bottom_right, bottom_left) or
            segments_intersect(line_start, line_end, bottom_left, top_left))
