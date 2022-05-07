
auto add(auto x, auto y) {
    return x + y;
}

auto x = add(5, 3);

asm {
    OUT %NUMB x;
}
