#include <archive.h>
#include <archive_entry.h>
#include <stdio.h>
#include <inttypes.h>

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

	arnum = archive_read_open_filename(ar, argv[1], 16384);
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
	puts("==> Stage 2: Displaying");

	ar = archive_read_new();
	archive_read_support_filter_all(ar);
	archive_read_support_format_all(ar);

	arnum = archive_read_open_filename(ar, argv[1], 16384);
	if(arnum != ARCHIVE_OK){
		fprintf(stderr, "%s: %s: %s\n",
			argv[0], argv[1], archive_error_string(ar));
		return 2;
	}

	while(archive_read_next_header(ar, &aren) == ARCHIVE_OK){
		printf("<<< %s >>>\n", archive_entry_pathname(aren));
		for(;;){
			size_t size;
			off_t  offset;
			const void* buffer;
			switch(archive_read_data_block(ar, &buffer, &size, &offset)){
				case ARCHIVE_OK:
					puts(":: Block reading succeeded");
					fwrite(buffer, size, 1, stdout);
					break;
				case ARCHIVE_WARN:
					puts(":: Block reading succeeded, warning exists");
					fwrite(buffer, size, 1, stdout);
					break;
				case ARCHIVE_EOF:
					goto loop_outside;
				case ARCHIVE_RETRY:
					puts(":: Block reading failed, retrying");
					break;
				case ARCHIVE_FATAL:
					puts(":: Fatal error! STOP!");
					return 2;
			}
		}
loop_outside:
		puts("@@ Extract OK @@");
	}

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
