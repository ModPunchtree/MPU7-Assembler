
auto recursiveFibonacci(auto x) {
    if (x < 2) {
        return x;
    }
    return recursiveFibonacci(x - 1) + recursiveFibonacci(x - 2);
}

auto x = -1;
while (1) {
    x += 1;
    asm {
        OUT %TEXT '\n';
        OUT %TEXT 'f';
        OUT %TEXT 'i';
        OUT %TEXT 'b';
        OUT %TEXT '(';
        OUT %TEXT x;
        OUT %TEXT ')';
    }
    auto answer = recursiveFibonacci(x);
    asm {
        OUT %NUMB answer;
    }
}