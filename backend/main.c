#include <stdio.h>
int main() {
    int a[] = {50, 25, 75, 100};
    int n = sizeof(a)/sizeof(a[0]);
    printf("[");
    for (int i = 0; i < n; i++) {
        printf("%d", a[i]);
        if (i < n - 1) printf(", ");
    }
    printf("]");
    return 0;
}