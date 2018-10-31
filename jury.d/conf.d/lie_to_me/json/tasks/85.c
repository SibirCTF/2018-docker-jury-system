#include <stdio.h>
int main(int argc, char* argv[]) {
    int m, h1, h2;
    scanf("%d%d%d", &m, &h1, &h2);
    printf("%d\n", m*10*(h2-h1));
    return 0;
} 
