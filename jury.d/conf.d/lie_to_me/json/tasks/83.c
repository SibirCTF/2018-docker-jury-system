#include <stdio.h>
int main(int argc, char* argv[]) {
    int x0, v0, t, a;
    scanf("%d%d%d%d", &x0, &v0, &t, &a);
    printf("%d\n", x0+v0*t+a*t*t/2);
    return 0;
}

