#include <stdio.h>
int main(int argc, char* argv[]) {
    int D, h;
    scanf("%d%d", &D, &h);
    printf("%.2f\n", 2*3.14*D*D/4 + 2*3.14*D*h/2);
    return 0;
}
