from distutils.core import setup, Extension

thread_affinity = \
Extension(
  "thread_affinity",
  extra_compile_args=["-O3"],
  sources = ["ext/thread_affinity.cc"]
)

setup(
  name = "thread_affinity",
  version = "1.0.0",
  description = "A wrapper to call set & get affinity from python (linux only). Tested on HPC environments.",
  author = "The COMPSs Team",
  author_email = "support-compss@bsc.es",
  url = "https://github.com/bsc-wdc/thread_affinity",
  ext_modules = [thread_affinity]
)
