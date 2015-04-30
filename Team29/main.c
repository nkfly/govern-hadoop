#include <archive.h>
#include <archive_entry.h>
#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>
#include <unistd.h>
#define _GNU_SOURCE
int main(int argc, char* argv[]){
	struct archive* ar;
	struct archive_entry* aren;
	int arnum;

	if(argc < 3){
		fprintf(stderr, "Usage: %s infile outfile\n", argv[0]);
		return 255;
	}

#ifdef ENABLE_STAGE_1
	puts("==> Stage 1: Listing");

	ar = archive_read_new();
	archive_read_support_filter_all(ar);
	archive_read_support_format_all(ar);

	arnum = archive_read_open_filename(ar, argv[1], 1656885703);
	if(arnum != ARCHIVE_OK){
		fprintf(stderr, "%s: %s: %s\n", 
				argv[0], argv[1], archive_error_string(ar));
		return 1;
	}

	while(archive_read_next_header(ar, &aren) == ARCHIVE_OK){
		const char *hardlink, *symlink;
		printf("%s format: %s, pathname: %s, size: %"PRId64", links: %d,"
				"username: %s, uid: %d", 
				argv[1], archive_format_name(ar), archive_entry_pathname(aren),
				archive_entry_size(aren), archive_entry_nlink(aren),
				archive_entry_uname(aren), archive_entry_uid(aren));
		hardlink = archive_entry_hardlink(aren);
		symlink = archive_entry_symlink(aren);
		if(hardlink != NULL){
			printf(", hardlink: %s", hardlink);
		}
		if(symlink != NULL){
			printf(", symlink: %s", symlink);
		}
		putchar('\n');
	}

	archive_read_close(ar);
	archive_read_free(ar);
#endif

#ifdef ENABLE_STAGE_2
	//puts("==> Stage 2: Displaying");

	ar = archive_read_new();
	archive_read_support_filter_all(ar);
	archive_read_support_format_all(ar);

	arnum = archive_read_open_filename(ar, argv[1], 1656885703);
	if(arnum != ARCHIVE_OK){
		fprintf(stderr, "%s: %s: %s\n",
				argv[0], argv[1], archive_error_string(ar));
		return 2;
	}
	//int jj = 0;
	size_t now=0;
	void* bigmap;
	bigmap = malloc(sizeof(char) * 1656885703);
	while(archive_read_next_header(ar, &aren) == ARCHIVE_OK){
		//printf("<<< %s >>>\n", archive_entry_pathname(aren));
		for(;;){
			size_t size;
			off_t  offset;
			const void* buffer;
			switch(archive_read_data_block(ar, &buffer, &size, &offset)){
				case ARCHIVE_OK:
					//puts(":: Block reading succeeded");
					memcpy(bigmap+now, buffer, size);
					now += size;
					//fwrite(buffer, size, 1, stdout);
					break;
				case ARCHIVE_WARN:
					memcpy(bigmap+now, buffer, size);
					now += size;
					//puts(":: Block reading succeeded, warning exists");
					//fwrite(buffer, size, 1, stdout);
					break;
				case ARCHIVE_EOF:
					//break;
					goto loop_outside;
				case ARCHIVE_RETRY:
					//puts(":: Block reading failed, retrying");
					break;
				case ARCHIVE_FATAL:
					//puts(":: Fatal error! STOP!");
					return 2;
			}
			//printf("size = %d\n", size);
			//jj++;
		}
loop_outside:
		break;
		//puts("@@ Extract OK @@");
	}
	pid_t pid;
	pid = fork();
	if(pid<0){
		fprintf(stderr, "Fork Failed");
		exit(-1);
	}
	else if(pid==0){
		#if 0
		//FILE *fp = fopen(argv[2], "w");
		//fputs(bigmap, fp);
		//fclose(fp);
		if(execl("/usr/bin/hadoop", "/usr/bin/hadoop", "fs", "-put", "EHC_1st_round.log", ".", (char *)0) <0 )
			fprintf(stderr, "hadoop error");
		#endif
		//if( execl("/usr/bin/hadoop", "/usr/bin/hadoop", "fs", "-mkdir", "hdfs://master/tmp/Team29", (char *)0) < 0)
		//	fprintf(stderr, "hadoop mkdir error");
		FILE *ff = popen("/usr/bin/hadoop fs -put - hdfs://master/tmp/Team29/EHC_1st_round.log", "w");
		int fno = fileno(ff);
		//fwrite(bigmap, sizeof(char), 1656885703, ff);
		write(fno, bigmap, 1656885703);
		fclose(ff);
		//write(STDOUT_FILENO, "hadoop", 6);
	}
	else{
		void *content;
		static const int FILESIZE = 1656885703;
		content = bigmap;
		FILE *resultfd;
		resultfd = fopen("preprocess.csv", "w");
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
		
		pid_t forR;
		forR = fork();
		if(forR < 0)
			fprintf(stderr, "fork R error");
		else if(forR == 0){
			execl("/usr/bin/R", "/usr/bin/R", "CMD", "BATCH",  "--no-save",  "--no-restore",  "cal_sales.r", (char *)0 );
			//write(STDOUT_FILENO, "R", 1);
		}
		else{
			wait(NULL);
			//write(STDOUT_FILENO, "R", 1);
		}
		wait(NULL);
		//write(STDOUT_FILENO, "W", 1);
	}
	//printf("%d\n", jj);
	//free(bigmap);
	archive_read_close(ar);
	archive_read_free(ar);
#endif

#ifdef ENABLE_STAGE_3
	puts("==> Stage 3: Extracting");

	struct archive* arext;

	ar = archive_read_new();
	archive_read_support_format_all(ar);
	archive_read_support_filter_all(ar);

	arext = archive_write_disk_new();
	archive_write_disk_set_options(arext,
			ARCHIVE_EXTRACT_PERM | ARCHIVE_EXTRACT_TIME | ARCHIVE_EXTRACT_ACL | 
			ARCHIVE_EXTRACT_FFLAGS | ARCHIVE_EXTRACT_XATTR );
	archive_write_disk_set_standard_lookup(arext);

	if(archive_read_open_filename(ar, argv[1], 16384)){
		fprintf(stderr, "%s: %s: %s\n",
				argv[0], argv[1], archive_error_string(ar));
		return 3;
	}

	while((arnum = archive_read_next_header(ar, &aren)) == ARCHIVE_OK){
		int filesize, accsize;
		printf("<<< %s >>>\n", archive_entry_pathname(aren));
		if(archive_write_header(arext, aren) != ARCHIVE_OK){
			puts(":: Write header not OK ...");
		}else if((filesize = archive_entry_size(aren)) > 0){
			accsize = 0;
			for(;;){
				size_t size;
				off_t  offset;
				const void* buffer;
				arnum = archive_read_data_block(ar, &buffer, &size, &offset);
				if(arnum != ARCHIVE_OK){
					break;
				}
				arnum = archive_write_data(arext, buffer, size);
				if(arnum >= 0){
					accsize += arnum;
					printf(":: %d of %d bytes written\n", accsize, filesize);
				}
			}
		}

		if(archive_write_finish_entry(arext) != ARCHIVE_OK){
			return 3;
		}
	}

	archive_read_close(ar);
	archive_read_free(ar);
	archive_write_close(arext);
	archive_write_free(arext);
#endif


	return 0;
}
