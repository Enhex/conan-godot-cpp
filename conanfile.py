from conan import ConanFile, tools
from conan.tools.files import copy
from os import cpu_count, path

class GodotcppConan(ConanFile):
    name = "godot-cpp"
    version = "4.4.x"
    license = "MIT"
    author = "Enhex enhex0@gmail.com"
    url = "https://github.com/Enhex/conan-godot-cpp"
    description = "C++ bindings for the Godot script API"
    topics = ("godot")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "SConsDeps"

    scons_options = {}

    def populate_scons_options(self):
        if self.settings.os == "Windows":
            self.scons_options['platform'] = "windows"
        elif self.settings.os == "Linux":
            self.scons_options['platform'] = "linux"
        elif self.settings.os == "Macos":
            self.scons_options['platform'] = "osx"

        self.scons_options['target'] = "template_" + str(self.settings.build_type).lower()

        if self.settings.arch == "x86":
            self.scons_options['bits'] = "32"
        elif self.settings.arch == "x86_64":
            self.scons_options['bits'] = "64"

    def source(self):
        self.run("git clone --single-branch --branch=4.4 --depth=1 --recursive https://github.com/godotengine/godot-cpp.git .")

    def build(self):
        self.populate_scons_options()
        self.run('scons -j{} platform={} target={} bits={}'.format(cpu_count(), self.scons_options['platform'], self.scons_options['target'], self.scons_options['bits']))

    def package(self):
        copy(self, "*.inc",path.join(self.source_folder, "include"),path.join(self.package_folder, "include"))

        copy(self, "*.h",path.join(self.source_folder, "gdextension"),path.join(self.package_folder, "include"))
        copy(self, "*.hpp",path.join(self.source_folder, "gdextension"),path.join(self.package_folder, "include"))
        copy(self, "*.h",path.join(self.source_folder, "include"),path.join(self.package_folder, "include"))
        copy(self, "*.hpp",path.join(self.source_folder, "include"),path.join(self.package_folder, "include"))
        copy(self, "*.h",path.join(self.source_folder, "gen/include"),path.join(self.package_folder, "include"))
        copy(self, "*.hpp",path.join(self.source_folder, "gen/include"),path.join(self.package_folder, "include"))
        copy(self, "*.a", path.join(self.build_folder, "bin"), path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.so", path.join(self.build_folder, "bin"), path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.lib", path.join(self.build_folder, "bin"), path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.dll", path.join(self.build_folder, "bin"), path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, "*.dylib", path.join(self.build_folder, "bin"), path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.populate_scons_options()
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["godot-cpp.{}.{}.x86_{}".format(self.scons_options['platform'], self.scons_options['target'], self.scons_options['bits'])]