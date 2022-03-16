
auto x1 = 1;
auto y1 = 6;
auto x2 = 3;
auto y2 = 1;

auto dx = x2 - x1;
auto sx = 1;
if (x1 > x2) {
    sx = -sx;
    dx = x1 - x2;
}

auto dy = y1 - y2;
auto sy = 1;
if (y1 > y2) {
    sy = -sy;
    dy = y2 - y1;
}

auto error = dx + dy;
dx += 128;
dy += 128;

auto e2;
while (1) {
    asm {
        OUT %X x1;
        OUT %Y y1;
        OUT %COLOR 7;
    };
    e2 = error << 1;
    e2 += 128;
    if (e2 >= dy) {
        if (x1 == x2) {
            asm {
                HLT;
            };
        }
        error += dy + 128;
        x1 += sx;
    }
    if (e2 <= dx) {
        if (y1 == y2) {
            asm {
                HLT;
            };
        }
        error += dx + 128;
        y1 += sy;
    }
}
