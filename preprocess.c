#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <string.h>
int main() {
  int fd;
  char *content;
  static const FILESIZE = 1656885703;
  fd = open("EHC_1st_round.log", O_RDONLY);
  content = mmap(0, FILESIZE, PROT_WRITE, MAP_PRIVATE, fd, 0);

  FILE *resultfd;
  resultfd = fopen("preprocess.csv", "w");
  fprintf(resultfd, "pid,sum\n");
  char line[10000];
  char *check;
  char *tok[50];
  char *pid_tok[50];
  char *pid_list_tok[500];
  char *line_ptr = NULL;
  char *tok_ptr = NULL;
  char *pid_tok_ptr = NULL;
  char *pid_list_tok_ptr = NULL;
  int i, j;
  int pivot = 0;
  int count = 0;
  for (i=0 ; i<FILESIZE ; i++) {
    line[pivot] = *(content+i);
    if (line[pivot] == '\n') {
      line[pivot+1] = '\0';
      pivot = 0;
      check = strstr(line, "act=order");
      if (check == NULL) {
        continue;
      } else {
        count = 0;
        line_ptr = line;
        while ((tok[count] = strtok_r(line_ptr, ";", &tok_ptr)) != NULL) {
          count++;
          line_ptr = NULL;
        }
        count = 0;
        while ((pid_tok[count] = strtok_r(tok[3], "=", &pid_tok_ptr)) != NULL) {
          count++;
          tok[3] = NULL;
        }
        if (count <= 1) {
          continue;
        }
        count = 0;
        while ((pid_list_tok[count] = strtok_r(pid_tok[1], ",", &pid_list_tok_ptr)) != NULL) {
          count++;
          pid_tok[1] = NULL;
        }
        for (j=0 ; j<count ; j+=3) {
          fprintf(resultfd, "%s,%d\n", pid_list_tok[j], atoi(pid_list_tok[j+1])*atoi(pid_list_tok[j+2]));
        }
      }
    } else {
      pivot++;
    }
  }
  fclose(resultfd);
  return 0;
}
