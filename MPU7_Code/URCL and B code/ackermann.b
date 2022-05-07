
auto ack(auto m, auto n) {
    if (m == 0) {
        return n + 1;
    }
    if (n == 0) {
        return ack(m - 1, 1);
    }
    return ack(m - 1, ack(m, n - 1));
}

asm {
    OUT %TEXT 'a';
    OUT %TEXT 'c';
    OUT %TEXT 'k';
    OUT %TEXT '(';
    OUT %TEXT '3';
    OUT %TEXT ',';
    OUT %TEXT '1';
    OUT %TEXT ')';
    OUT %TEXT ':';
}

auto x = ack(3, 1);

asm {
    OUT %NUMB x;
}
