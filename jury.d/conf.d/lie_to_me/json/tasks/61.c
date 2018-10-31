#include <stdio.h>
int main(int argc, char* argv[]) {
    int R, L;
    scanf("%d%d", &R, &L);
    printf("%.2f\n", 3.14*R*R + 3.14*R*L);
    return 0;
}
