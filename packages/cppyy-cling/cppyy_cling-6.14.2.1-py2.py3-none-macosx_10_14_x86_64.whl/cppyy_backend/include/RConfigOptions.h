#ifndef ROOT_RConfigOptions
#define ROOT_RConfigOptions

#define R__CONFIGUREOPTIONS   "LZ4_INCLUDE_DIR=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/lz4 LZ4_INCLUDE_DIRS=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/lz4 LZ4_LIBRARIES=LZ4::LZ4 LZ4_LIBRARY=$<TARGET_FILE:lz4> ZLIB_INCLUDE_DIR=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/zlib ZLIB_INCLUDE_DIRS=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/zlib ZLIB_LIBRARIES=ZLIB::ZLIB ZLIB_LIBRARY=$<TARGET_FILE:ZLIB> xxHash_INCLUDE_DIR=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/xxhash xxHash_INCLUDE_DIRS=/Users/wlav/wheelie/cppyy-backend/cling/src/builtins/xxhash xxHash_LIBRARIES=xxHash::xxHash xxHash_LIBRARY=$<TARGET_FILE:xxhash> "
#define R__CONFIGUREFEATURES  " builtin_freetype builtin_llvm builtin_clang builtin_lzma builtin_lz4 builtin_pcre builtin_xxhash builtin_zlib cling cxx14 explicitlink libcxx thread"

#endif
