from conans import ConanFile, CMake, tools
import os


class LibZipConan(ConanFile):
    name = "libzip"
    description = "A C library for reading, creating, and modifying zip archives"
    version = "2008.11.18"
    url = "https://github.com/bincrafters/conan-libzip"
    homepage = "https://github.com/nih-at/libzip"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "BSD"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_bzip2": [True, False],
        "with_openssl": [True, False]
    }
    default_options = {'shared': False, 'fPIC': True, 'with_bzip2': True, 'with_openssl': True}
    requires = "zlib/1.2.11"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def requirements(self):
        if self.options.with_bzip2:
            self.requires.add("bzip2/1.0.6")

        if self.options.with_openssl:
            self.requires.add("openssl/1.0.2t")

    def source(self):
        source_url = "https://libzip.org/download"
        tools.get("{0}/{1}-{2}.tar.gz".format(source_url, self.name, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_OPENSSL"] = self.options.with_openssl
        cmake.configure()
        return cmake

    def exclude_targets(self):
        cmake_file = os.path.join(self._source_subfolder, "CMakeLists.txt")
        excluded_targets = ["regress", "examples", "man"]
        for target in excluded_targets:
            tools.replace_in_file(cmake_file, "ADD_SUBDIRECTORY(%s)" % target, "")
        if self.options.with_openssl:
            tools.replace_in_file(cmake_file, "OPENSSL_LIBRARIES", "CONAN_LIBS_OPENSSL")

    def build(self):
        self.exclude_targets()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
