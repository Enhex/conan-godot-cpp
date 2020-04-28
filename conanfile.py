from conans import ConanFile, tools
from pathlib import Path

class GodotcppConan(ConanFile):
    name = "godot-cpp"
    version = "3.2"
    license = "MIT"
    author = "Enhex enhex0@gmail.com"
    url = "https://github.com/Enhex/conan-godot-cpp"
    description = "C++ bindings for the Godot script API"
    topics = ("godot")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "scons"

    scons_options = {}

    def populate_scons_options(self):
        if self.settings.os == "Windows":
            self.scons_options['platform'] = "windows"
        elif self.settings.os == "Linux":
            self.scons_options['platform'] = "linux"
        elif self.settings.os == "Macos":
            self.scons_options['platform'] = "osx"

        self.scons_options['target'] = str(self.settings.build_type).lower()

        if self.settings.arch == "x86":
            self.scons_options['bits'] = "32"
        elif self.settings.arch == "x86_64":
            self.scons_options['bits'] = "64"

    def source(self):
        self.run("git clone --single-branch --branch=3.2 --depth=1 --recursive https://github.com/GodotNativeTools/godot-cpp.git .")

    def build(self):
        self.populate_scons_options()
        self.run('scons -C platform={} generate_bindings=yes target={} bits={}'.format(self.scons_options['platform'], self.scons_options['target'], self.scons_options['bits']))
        # some tools try to remove library file extention, and because the name format uses dots, it ends up removing part of the name.
        # to solve this replace this naming kludge with a single sane name.
        for path in Path('.').rglob('*godot-cpp*.*'):
            prefix = "lib" if self.settings.os != "Windows" else ""
            suffix = path.suffix
            path.replace(str(path.with_name(prefix + 'godot-cpp')) + suffix)

    def package(self):
        self.copy("*.h", dst="include", src="godot_headers")
        self.copy("*.hpp", dst="include", src="godot_headers")
        self.copy("*.h", dst="include", src="include")
        self.copy("*.hpp", dst="include", src="include")

        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.populate_scons_options()
        self.cpp_info.includedirs = ["include", "include/core", "include/gen"]
        self.cpp_info.libs = ["godot-cpp"]

