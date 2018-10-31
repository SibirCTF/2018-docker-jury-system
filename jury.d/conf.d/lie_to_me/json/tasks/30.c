#include <stdio.h>
int main(int argc, char* argv[]) {
    int a, b, c;
    scanf("%d%d%d", &a, &b, &c);
    printf("%d\n", (a + b + c)/2*((a + b + c)/2 - a)*((a + b + c)/2 - b)*((a + b + c)/2 - c));
    return 0;
}
