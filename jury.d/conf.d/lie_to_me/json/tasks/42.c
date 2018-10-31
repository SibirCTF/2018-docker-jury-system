#include <stdio.h>
int main(int argc, char* argv[]) {
    int a, b, c, R;
    scanf("%d%d%d%d", &a, &b, &c, &R);
    printf("%d\n", (a*b*c)/(4*R));
    return 0;
}
