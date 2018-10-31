#include <stdio.h>
int main(int argc, char* argv[]) {
    int a, b, c;
    scanf("%d%d%d", &a, &b, &c);
    printf("%d\n", 2*a*b + 2*a*c + 2*b*c);
    return 0;
}
