from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMakeToolchain, CMakeDeps


class LimaConan(ConanFile):
    name = "lima"
    executable = "ds_LimaDetector"
    version = "1.13.1"
    package_type = "application"
    user = "soleil"
    python_requires = "base/[>=1.0]@soleil/stable"
    python_requires_extend = "base.Device"

    license = "GPL-3.0-or-later"
    author = "Arafat Noureddine, Florent Langlois"
    url = "https://github.com/soleil-ica/Lima"
    description = "LimaDetector device"
    topics = ("control-system", "tango", "device", "lima")

    settings = "os", "compiler", "build_type", "arch"

    exports_sources = \
        "CMakeLists.txt", \
        "cmake/*", \
        "third-party/**", \
        "common/**", \
        "control/**", \
        "hardware/**", \
        "camera/**", \
        "applications/**", \
        "VERSION"

    options = {
        "with_andor": [True, False],
        "with_basler": [True, False],
        "with_dhyana": [True, False],
        "with_eiger": [True, False],
        "with_hamamatsu": [True, False],
        "with_imxpad": [True, False],
        "with_lambda": [True, False],
        "with_marccd": [True, False],
        "with_merlin": [True, False],
        "with_pco": [True, False],
        "with_perkinelmer": [True, False],
        "with_pilatus": [True, False],
        "with_roperscientific": [True, False],
        "with_simulator": [True, False],
        "with_slseiger": [True, False],
        "with_slsjungfrau": [True, False],
        "with_spectralinstrument": [True, False],
        "with_spectrumone": [True, False],
        "with_ufxc": [True, False],
        "with_uview": [True, False],
        "with_xpad": [True, False]
    }

    default_options = {
        "with_andor": True,
        "with_basler": True,
        "with_dhyana": True,
        "with_eiger": True,
        "with_hamamatsu": True,
        "with_imxpad": True,
        "with_lambda": True,
        "with_marccd": True,
        "with_merlin": True,
        "with_pco": True,
        "with_perkinelmer": True,
        "with_pilatus": True,
        "with_roperscientific": True,
        "with_simulator": True,
        "with_slseiger": True,
        "with_slsjungfrau": True,
        "with_spectralinstrument": True,
        "with_spectrumone": True,
        "with_ufxc": True,
        "with_uview": True,
        "with_xpad": True
    }

    def requirements(self):
        self.requires("yat4tango/[>=1.0]@soleil/stable")
        self.requires("nexuscpp/[>=4]@soleil/stable")
        if self.settings.os == "Windows":
            if self.settings.arch == "x86":
                # Windows 32 bits
                if self.settings.compiler.version == "190":
                    # Windows 32 bits with VS2015 (MSVC 14)
                    self.requires("atmcd/2.83.3@soleil/stable")
                    self.requires("xisl/4.0@soleil/stable")
                    self.requires("pvcam/2.7.5@soleil/stable")
                else:
                    # Other Windows 32 bits compilers
                    pass
            elif self.settings.arch == "x86_64":
                # Windows 64 bits
                if self.settings.compiler.version == "190":
                    # Windows 64 bits with VS2015 (MSVC 14)
                    self.requires("opencv_world/[~3.0.0]@soleil/stable")
                else:
                    # Other Windows 64 bits compilers
                    pass
        elif self.settings.os == "Linux":
            if self.settings.arch == "x86":
                # Linux 32 bits
                if (
                    self.settings.compiler == "gcc"
                    and self.settings.compiler.version == "4.4"
                ):
                    # CentOS 6 32 bits with GCC 4.4
                    self.requires("tiff/4.0.3@soleil/stable")
                    self.requires("xpix/2.1.7-soleil@soleil/stable")
                else:
                    # Other Linux 32 bits compilers
                    pass
            elif self.settings.arch == "x86_64":
                # Linux 64 bits
                if (
                    self.settings.compiler == "gcc"
                    and self.settings.compiler.version == "4.4"
                ):
                    # CentOS 6 64 bits with GCC 4.4
                    self.requires("eigerapi/1.0.9@soleil/stable")
                    self.requires("lz4/1.9.4")
                    self.requires("ufxclib/[>=1.0]@soleil/stable")
                elif (
                    self.settings.compiler == "gcc"
                    and self.settings.compiler.version == "4.8"
                ):
                    # CentOS 7 64 bits with GCC 4.8
                    self.requires("pylon/6.3.0@soleil/stable")
                    self.requires("xsp/2.1.0@soleil/stable")
                else:
                    # Other Linux 64 bits compilers
                    pass

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.variables["WITH_ANDOR"] = self.options.with_andor
        tc.variables["WITH_BASLER"] = self.options.with_basler
        tc.variables["WITH_DHYANA"] = self.options.with_dhyana
        tc.variables["WITH_EIGER"] = self.options.with_eiger
        tc.variables["WITH_HAMAMATSU"] = self.options.with_hamamatsu
        tc.variables["WITH_IMXPAD"] = self.options.with_imxpad
        tc.variables["WITH_LAMBDA"] = self.options.with_lambda
        tc.variables["WITH_MARCCD"] = self.options.with_marccd
        tc.variables["WITH_MERLIN"] = self.options.with_merlin
        tc.variables["WITH_PCO"] = self.options.with_pco
        tc.variables["WITH_PERKINELMER"] = self.options.with_perkinelmer
        tc.variables["WITH_PILATUS"] = self.options.with_pilatus
        tc.variables["WITH_ROPERSCIENTIFIC"] = self.options.with_roperscientific
        tc.variables["WITH_SIMULATOR"] = self.options.with_simulator
        tc.variables["WITH_SLSEIGER"] = self.options.with_slseiger
        tc.variables["WITH_SLSJUNGFRAU"] = self.options.with_slsjungfrau
        tc.variables["WITH_SPECTRALINSTRUMENT"] = self.options.with_spectralinstrument
        tc.variables["WITH_SPECTRUMONE"] = self.options.with_spectrumone
        tc.variables["WITH_UFXC"] = self.options.with_ufxc
        tc.variables["WITH_UVIEW"] = self.options.with_uview
        tc.variables["WITH_XPAD"] = self.options.with_xpad
        self.set_cmake_variables(tc)
        tc.generate()
