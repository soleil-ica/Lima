from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps


# Windows 32 bits + MSVC18
def rule_win32_msvc18(settings):
    return [
        "simulator",
        "andor",
        "perkinelmer",
        "roperscientific",
        "uview"
    ]


# Windows 64 bits + MSVC18
def rule_win64_msvc18(settings):
    return [
        "simulator",
        "dhyana",
        "hamamatsu",
        "perkinelmer",
        "pco",
        "spectrumone",
        "rixs"
    ]


# CentOS 6 32 bits + GCC 4.4
def rule_linux32_gcc44(settings):
    return [
        "simulator",
        "imxpad",
        "marccd",
        "merlin",
        "pilatus",
        "xpad"
    ]


# CentOS 6 64 bits + GCC 4.4
def rule_linux64_gcc44(settings):
    return [
        "simulator",
        "eiger",
        "imxpad",
        "marccd",
        "merlin",
        "slseiger",
        "slsjungfrau",
        "spectralinstrument",
        "ufxc"
    ]


# CentOS 7 64 bits + GCC 4.8
def rule_linux64_gcc48(settings):
    return [
        "simulator",
        "basler",
        "lambda",
        "rixs",
        "fitgaussian"
    ]


# CentOS 7 64 bits + GCC 11
def rules_linux64_gcc11(settings):
    return [
        "simulator",
        "rixs"
    ]


# Camera rules based on platform and compiler
CAM_RULES = [
    # Windows 32 bits + MSVC18
    (lambda s: s.os == "Windows"
        and s.arch == "x86"
        and s.compiler == "msvc"
        and str(s.compiler.version).startswith("195"),
        rule_win32_msvc18),

    # Windows 64 bits + MSVC18
    (lambda s: s.os == "Windows"
        and s.arch == "x86_64"
        and s.compiler == "msvc"
        and str(s.compiler.version).startswith("195"),
        rule_win64_msvc18),

    # CentOS 6 32 bits + GCC 4.4
    (lambda s: s.os == "Linux"
        and s.arch == "x86"
        and s.compiler == "gcc"
        and str(s.compiler.version).startswith("4.4"),
        rule_linux32_gcc44),

    # CentOS 6 64 bits + GCC 4.4
    (lambda s: s.os == "Linux"
        and s.arch == "x86_64"
        and s.compiler == "gcc"
        and str(s.compiler.version).startswith("4.4"),
        rule_linux64_gcc44),

    # CentOS 7 64 bits + GCC 4.8
    (lambda s: s.os == "Linux"
        and s.arch == "x86_64"
        and s.compiler == "gcc"
        and str(s.compiler.version).startswith("4.8"),
        rule_linux64_gcc48),

    # CentOS 7 64 bits + GCC 11
    (lambda s: s.os == "Linux"
        and s.arch == "x86_64"
        and s.compiler == "gcc"
        and str(s.compiler.version).startswith("11"),
        rules_linux64_gcc11),
]


class LimaDetectorConan(ConanFile):
    name = "limadetector"
    executable = "ds_LimaDetector"
    version = "1.14.0"
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
        # Camera options
        "with_andor": [True, False, "auto"],
        "with_basler": [True, False, "auto"],
        "with_dhyana": [True, False, "auto"],
        "with_eiger": [True, False, "auto"],
        "with_hamamatsu": [True, False, "auto"],
        "with_imxpad": [True, False, "auto"],
        "with_lambda": [True, False, "auto"],
        "with_marccd": [True, False, "auto"],
        "with_merlin": [True, False, "auto"],
        "with_pco": [True, False, "auto"],
        "with_perkinelmer": [True, False, "auto"],
        "with_pilatus": [True, False, "auto"],
        "with_roperscientific": [True, False, "auto"],
        "with_simulator": [True, False, "auto"],
        "with_slseiger": [True, False, "auto"],
        "with_slsjungfrau": [True, False, "auto"],
        "with_spectralinstrument": [True, False, "auto"],
        "with_spectrumone": [True, False, "auto"],
        "with_ufxc": [True, False, "auto"],
        "with_uview": [True, False, "auto"],
        "with_xpad": [True, False, "auto"],
        # Other options
        "with_rixs": [True, False, "auto"],
        "with_fitgaussian": [True, False, "auto"]
    }

    default_options = {
        # Camera options
        "with_andor": "auto",
        "with_basler": "auto",
        "with_dhyana": "auto",
        "with_eiger": "auto",
        "with_hamamatsu": "auto",
        "with_imxpad": "auto",
        "with_lambda": "auto",
        "with_marccd": "auto",
        "with_merlin": "auto",
        "with_pco": "auto",
        "with_perkinelmer": "auto",
        "with_pilatus": "auto",
        "with_roperscientific": "auto",
        "with_simulator": "auto",
        "with_slseiger": "auto",
        "with_slsjungfrau": "auto",
        "with_spectralinstrument": "auto",
        "with_spectrumone": "auto",
        "with_ufxc": "auto",
        "with_uview": "auto",
        "with_xpad": "auto",
        # Other options
        "with_rixs": "auto",
        "with_fitgaussian": "auto"
    }

    def config_options(self):
        # First collect active cameras based on rules
        active = []
        for cond, fn in CAM_RULES:
            if cond(self.settings):
                active = fn(self.settings)
                break

        # Set auto → True/False
        for opt, val in self.options.items():
            if val == "auto":
                setattr(self.options, opt, opt.replace("with_", "") in active)

        self.output.info("=== CAMERA OPTIONS AFTER RESOLUTION ===")
        for opt, val in self.options.items():
            self.output.info(f"{opt} = {val}")

    def requirements(self):
        self.requires("yat4tango/[>=1.0]@soleil/stable")
        self.requires("nexuscpp/[>=4]@soleil/stable")
        if self.options.get_safe("with_andor"):
            self.requires("atmcd/2.83.3@soleil/stable")
        if self.options.get_safe("with_basler"):
            self.requires("pylon/6.3.0@soleil/stable")
        if self.options.get_safe("with_eiger"):
            self.requires("eigerapi/1.0.9@soleil/stable")
            self.requires("lz4/1.9.4")
        if self.options.get_safe("with_lambda"):
            self.requires("xsp/2.1.0@soleil/stable")
        if (self.options.get_safe("with_perkinelmer") and
                self.settings.arch == "x86"):
            self.requires("xisl/4.0@soleil/stable")
        if self.options.get_safe("with_pilatus"):
            self.requires("libtiff/4.0.3@soleil/stable")
        if self.options.get_safe("with_roperscientific"):
            self.requires("pvcam/2.7.5@soleil/stable")
        if self.options.get_safe("with_ufxc"):
            self.requires("ufxclib/[>=1.0]@soleil/stable")
        if self.options.get_safe("with_xpad"):
            self.requires("xpix/2.1.7-soleil@soleil/stable")

        if self.options.get_safe("with_rixs") or self.options.get_safe("with_fitgaussian"):
            self.requires("opencv/3.4.20@soleil/stable")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        for opt, val in self.options.items():
            cm_name = f"{opt.upper()}"
            tc.variables[cm_name] = val

        self.set_cmake_variables(tc)
        tc.generate()
