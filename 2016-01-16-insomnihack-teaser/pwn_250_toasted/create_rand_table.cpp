#include <cstdlib>
#include <cstdio>

int main(){
	for(int i=0;i<(1<<10);i++){
		srand(i);
		for(int j=0;j<260;j++){
			printf("%d ", rand());
		}
		printf("\n");
	}
}
