#define ENABLE_OWN_MODULE_BOOTSEL   (1)

#ifndef BI_AM_ADD

#include "pico/binary_info.h"

#define BI_AM_TAG               BINARY_INFO_MAKE_TAG('A', 'M')
#define BI_AM_ID                0x61F52DA4
#define BI_AM_ADD(nam)          bi_decl(bi_string(BI_AM_TAG, BI_AM_ID, nam))
#define BI_AM_TXT(txt)          bi_decl(bi_program_feature(txt))

bi_decl(bi_program_feature_group_with_flags(
        BI_AM_TAG, BI_AM_ID, "added modules",
        BI_NAMED_GROUP_SEPARATE_COMMAS | BI_NAMED_GROUP_SORT_ALPHA));
#endif
