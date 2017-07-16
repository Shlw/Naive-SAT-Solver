#include <bits/stdc++.h>

using namespace std;

int n, m;

int main() {
    srand(time(0));
    n = 10;
    m = 30;
    printf("p PP %d %d\n", n, m);
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < rand() % n + 1; ++j) {
            int x = rand() % n + 1;
            if (rand() % 2 == 0) printf("-%d ", x);
            else printf("%d ", x);
        }
        printf("0\n");
    }
}
