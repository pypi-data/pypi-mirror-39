#ifndef ROOT_RConfigure
#define ROOT_RConfigure

/* Configurations file for macosx64 */
#ifdef R__HAVE_CONFIG
#define ROOTPREFIX    "$(ROOTSYS)"
#define ROOTBINDIR    "$(ROOTSYS)/bin"
#define ROOTLIBDIR    "$(ROOTSYS)/lib"
#define ROOTINCDIR    "$(ROOTSYS)/include"
#define ROOTETCDIR    "$(ROOTSYS)/etc"
#define ROOTDATADIR   "$(ROOTSYS)/."
#define ROOTDOCDIR    "$(ROOTSYS)/."
#define ROOTMACRODIR  "$(ROOTSYS)/macros"
#define ROOTTUTDIR    "$(ROOTSYS)/tutorials"
#define ROOTSRCDIR    "$(ROOTSYS)/src"
#define ROOTICONPATH  "$(ROOTSYS)/icons"
#define TTFFONTDIR    "$(ROOTSYS)/fonts"
#endif

#define EXTRAICONPATH ""

#undef R__HAS_SETRESUID   /**/
#undef R__HAS_MATHMORE   /**/
#define R__HAS_PTHREAD    /**/
#undef R__HAS_XFT    /**/
#undef R__HAS_COCOA    /**/
#undef R__HAS_VC    /**/
#undef R__HAS_VDT    /**/
#undef R__HAS_VECCORE    /**/
#undef R__USE_CXX11    /**/
#define R__USE_CXX14    /**/
#undef R__USE_CXX17    /**/
#undef R__USE_CXXMODULES   /**/
#define R__USE_LIBCXX    /**/
#define R__HAS_STD_STRING_VIEW   /**/
#define R__HAS_STD_EXPERIMENTAL_STRING_VIEW   /**/
#undef R__HAS_STOD_STRING_VIEW /**/
#undef R__HAS_STD_APPLY /**/
#undef R__HAS_STD_INVOKE /**/
#define R__HAS_STD_INDEX_SEQUENCE /**/
#define R__HAS_ATTRIBUTE_ALWAYS_INLINE /**/
#undef R__EXTERN_LLVMDIR /**/
#undef R__USE_IMT   /**/
#undef R__COMPLETE_MEM_TERMINATION /**/
#undef R__HAS_CEFWEB  /**/
#undef R__HAS_QT5WEB  /**/

#if defined(R__HAS_VECCORE) && defined(R__HAS_VC)
#ifndef VECCORE_ENABLE_VC
#define VECCORE_ENABLE_VC
#endif
#endif

#define R__HAS_DEFAULT_LZ4  /**/
#undef R__HAS_DEFAULT_ZLIB  /**/
#undef R__HAS_DEFAULT_LZMA  /**/

#undef R__HAS_TMVACPU /**/
#undef R__HAS_TMVAGPU /**/

#endif
