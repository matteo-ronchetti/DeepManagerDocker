import os
import jinja2
import glob
import shutil

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
dockerfiles_dir = os.path.join(os.path.dirname(__file__), "dockerfiles")

templates_glob_expr = os.path.join(templates_dir, "**", "*.jinja")

jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))

shutil.rmtree(dockerfiles_dir)

for src_path in glob.iglob(templates_glob_expr):
    dst_path = os.path.join(dockerfiles_dir, src_path[len(templates_dir) + 1:-6])
    print("Rendering", src_path, "to", dst_path)

    dst_dir = os.path.dirname(dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    with open(src_path) as f:
        template = jinja.from_string(f.read())

    with open(dst_path, "w") as f:
        f.write(template.render())


# base = jinja.get_template("Dockerfile.jinja")
# 
# with open("Dockerfile", "w") as f:
#     f.write(base.render())

# class DockerFile:
#     def __init__(self, src_img):
#         self.lines = ["FROM %s" % src_img, ""]
# 
#     def write(self, path):
#         with open(path, "w") as f:
#             f.write("\n".join(self.lines))
# 
#     def apt_install(self, libraries):
#         libraries = list(set(libraries))
# 
#         self.lines.append("RUN apt-get update \\")
#         self.lines.append("    && apt-get install -y --no-install-recommends \\")
#         self.lines.append("    " + " ".join(libraries) + " \\")
#         self.lines.append("    && apt-get clean \\")
#         self.lines.append("    && apt-get autoremove \\")
#         self.lines.append("    && rm -rf /var/lib/apt/lists/* \\")
#         self.lines.append("    && rm -rf /var/cache/apt/archives/*")
#         self.lines.append("")
# 
#     def install_python(self, version="3.6.3"):
#         self.lines.append("# Install python %s from source" % version)
#         self.lines.append(
#             "RUN wget https://www.python.org/ftp/python/{version}/Python-{version}.tgz \\".format(version=version))
#         self.lines.append("    && tar -xvf Python-{version}.tgz \\".format(version=version))
#         self.lines.append("    && cd Python-{version} \\".format(version=version))
#         self.lines.append("    && ./configure \\")
#         self.lines.append("    && make -j$(nproc) \\")
#         self.lines.append("    && make install \\")
#         self.lines.append("    && ldconfig \\")
#         self.lines.append("    && pip3 install --upgrade pip \\")
#         self.lines.append("    && cd .. && rm -r Python-{version}".format(version=version))
# 
#     def pip_install(self, libraries):
#         libraries = list(set(libraries))
# 
#         self.lines.append("RUN pip --no-cache-dir install \\")
#         self.lines.append("    " + " ".join(libraries) + " \\")
#         self.lines.append("    && rm -rf /tmp/* /var/tmp/*")
# 
# 
# base = DockerFile("nvidia/cuda:9.1-cudnn7-devel-ubuntu16.04")
# 
# python_requirements = "build-essential libpq-dev libssl-dev openssl libffi-dev zlib1g-dev tcl tk wget tar".split(" ")
# python_libraries = "numpy sklearn scipy ".split(" ")
# 
# base.apt_install(python_requirements)
# base.install_python()
# base.pip_install(python_libraries)
# 
# base.write("Dockerfile")
