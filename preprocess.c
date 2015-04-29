#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <string.h>
#define _GNU_SOURCE


int main() {
    int fd;
    void *content;
    static const int FILESIZE = 1656885703;
    fd = open("EHC_1st_round.log", O_RDONLY);
    content = mmap(0, FILESIZE, PROT_WRITE, MAP_PRIVATE, fd, 0);

    FILE *resultfd;
    resultfd = fopen("preprocess_C.csv", "wb");
    fprintf(resultfd, "pid,sum\n");
    char *p_1;
    char *p_2;
    char *loc = content;
    int filelen = FILESIZE;
    int offset_1;
    int offset_2;
    char plist[3][50];
    char count = 0;
    int i;
    int plist_exist = 0;
    char dot = '.';
    char ret = '\n';

    while (p_1 = memmem(loc, filelen, "act=order", 9)) {
        offset_1 = p_1 - loc;
        loc += offset_1;
        filelen -= offset_1;
        p_2 = memmem(loc, filelen, "plist", 5);
        offset_2 = p_2 - loc;
        loc += offset_2;
        filelen -= offset_2;
        loc += 6;
        i = 0;
        count = 0;
        plist_exist = 0;
        for (;;loc++) {
            if (*loc == ',') {
                plist[count][i] = '\0';
                count++;
                i=0;
                if (count == 3) {
                    fprintf(resultfd, "%s,%d\n", plist[0], atoi(plist[1])*atoi(plist[2]));
                    count = 0;
                }
            } else if (*loc == ';') {
                if (!plist_exist) {break;}
                plist[count][i] = '\0';
                fprintf(resultfd, "%s,%d\n", plist[0], atoi(plist[1])*atoi(plist[2]));
                break;
            } else {
                plist[count][i++] = *loc;
                plist_exist = 1;
            }
        }
    }
  fclose(resultfd);
  return 0;
}
