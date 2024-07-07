import pygame as pg
from cheeze import *

pg.init()

def draw_rect_alpha(surface, color, rect):
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def lighten(color, v):
    return (min(255, color[0] + v), min(255, color[1] + v), min(255, color[2] + v))

# Pygame utility functions for representation
def draw_dashed_line_pg(surf, color, p1: tuple[int, int], p2: tuple[int, int], division: int = 10):
    divsize = 0.3

    solidfill_parts = divsize/division
    nonsolidfill = (1-divsize)/(division-1)  # The number of empty divisions is always less!

    xdist = p2[0] - p1[0]
    ydist = p2[1] - p1[1]

    for x in range(division):
        position = (solidfill_parts*x + nonsolidfill*x)
        start = (p1[0] + position*xdist, p1[1] + position*ydist)
        end = (start[0] + solidfill_parts*xdist, start[1] + solidfill_parts*ydist)

        pg.draw.line(surf, color, start, end)

def intify(s):  # Convert sequences of floats to the int form
    return type(s)(map(int, s))


def draw_dashed_rect_pg(surf, color, r: pg.Rect, division: int = 10):
    # r.top -= 1
    # r.left -= 1
    # r.w += 1
    # r.h += 1

    r.w -= 1
    r.h -= 1
    draw_dashed_line_pg(surf, color, r.topleft, r.topright, division)
    draw_dashed_line_pg(surf, color, r.topright, r.bottomright, division)
    draw_dashed_line_pg(surf, color, r.topleft, r.bottomleft, division)
    draw_dashed_line_pg(surf, color, r.bottomleft, r.bottomright, division)


def draw_boxes(boxes: list[tuple[pg.Rect, pg.Rect, str, pg.Color]], font: pg.font.FontType, surf: pg.Surface):
    """
    The outer rect is rendered rect of the shader bound
    the inner rect is the dotted line that is the provided rect box
    
    str is the label
    """
    for (outer, dashed, label, color) in boxes:
        labelsurf = font.render(label, True, color)
        r = labelsurf.get_rect()
        r_outer = pg.Rect(outer)
        r.centerx = r_outer.centerx
        r.top = r_outer.top + 4

        pg.draw.rect(surf, color, outer, 1)
        draw_dashed_rect_pg(surf, lighten(color, 200), pg.Rect(dashed))
        surf.blit(labelsurf, r)


def show_shaderbounds(shaderbounds: ShaderBounds):
    """
    Display and check the reshading area interactively
    Drag with the mouse to automatically check all the widgets and areas to be reshaded!
    Dotted rectangle denotes the original boundary
    Solid rectangle denotes the rendered boundary
    Shaded region means the area to be reshaded.
    """
    fsize = 12  # Font Size
    linecount = 20
    w, h = intify(shaderbounds.size)
    h += fsize*linecount

    surf = pg.display.set_mode((w, h))
    pg.display.set_caption("ShaderBounds Interactive View")
    font = pg.font.SysFont("Consolas", fsize)

    clock = pg.time.Clock()

    childrens = shaderbounds.get_children()
    running = True

    mpos = None
    hoverpos = (0, 0)

    reshades: list[tuple[ShaderBounds, list[tuple[float, float, float, float]]]] = []
    shader_area_coverage = 0

    while running:
        clock.tick(60)
        for evt in pg.event.get():
            match evt.type:
                case pg.QUIT:
                    pg.display.quit()
                    pg.display.init()
                    return
                
                case pg.MOUSEBUTTONDOWN:
                    # Check for drawing a selection radius
                    mpos = evt.pos  # If we didn't have a previous click
                
                case pg.MOUSEBUTTONUP:
                    r = pg.Rect(*mpos, evt.pos[0]-mpos[0], evt.pos[1]-mpos[1])
                    r.normalize()

                    rect = (*r.topleft, *r.size)
                    reshades = shaderbounds.check_reshade(rect)

                    mpos = None
                
                case pg.MOUSEMOTION:
                    hoverpos = evt.pos
        
        
        surf.fill((255, 255, 255))

        # Put drawing functions here

        # The text box black colored
        textrect = surf.get_rect()
        textrect.top = textrect.bottom - linecount*fsize
        textrect.height = linecount*fsize
        surf.fill((0, 0, 0), textrect)

        boxes = []

        text = [
            f"Mouse Coordinates: {hoverpos}", "",
            f"Reshades ({round(shader_area_coverage*100/(w*h), 3)}%)",
        ]

        shader_area_coverage = 0

        for shaderbound in childrens:
            if shaderbound.drawable:
                color = (255, 0, 0)
            else:
                color = (100, 100, 100)

            boxes.append((
                shaderbound.rendered.as_int(),
                intify((*shaderbound.pos, *shaderbound.size)),
                shaderbound.parent,
                color
            ))
    
        draw_boxes(boxes, font, surf)

        for shaderbound, regions in reshades:
            stat = "full" if regions is None else "part"
            if regions is None:
                regions = [shaderbound.get_shadable_rect().as_int()]

            for x in regions:
                text.append(f"{shaderbound.parent}: {stat} {intify(x)}")
                draw_rect_alpha(surf, (255, 0, 0, 10), pg.Rect(*x))
                shader_area_coverage += x[2]*x[3]
                
        for (i, t) in enumerate(text):
            status_text = font.render(t, True, (255, 255, 255))
            surf.blit(status_text, (0, textrect.top + i*fsize))

        # Overlay mouse
        if mpos is not None:
            r = pg.Rect(*mpos, hoverpos[0]-mpos[0], hoverpos[1]-mpos[1])
            r.normalize()
            draw_rect_alpha(surf, (0, 255, 0, 100), r)

        pg.display.flip()
        