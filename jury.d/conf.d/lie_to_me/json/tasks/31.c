#include <stdio.h>
int main(int argc, char* argv[]) {
    int a, b, h;
    scanf("%d%d%d", &a, &b, &h);
    printf("%.1f\n", (a+b)*h*0.5);
    return 0;
}
