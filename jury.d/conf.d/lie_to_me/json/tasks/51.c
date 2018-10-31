#include <stdio.h>
int main(int argc, char* argv[]) {
    int R, h;
    scanf("%d%d", &R, &h);
    printf("%.2f\n", 2*3.14*R*R + 2*3.14*R*h);
    return 0;
}
