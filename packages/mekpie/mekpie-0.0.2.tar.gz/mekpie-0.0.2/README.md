![](/resources/logo.svg)

# Make Building C as Simple as Pie

Mekpie is an opinionated build system for small scale C projects. The core premise of Mekpie is that you should not be spending time worrying about Make files, compiler arguments, or build times, when working on a small C projects. By enforcing a simple directory structure and always providing a clean build, Mekpie saves you time and effort. For added convenience Mekpie takes notes from tools like [Rust's cargo](https://doc.rust-lang.org/cargo/guide/index.html) and [Node's npm](https://www.npmjs.com/) and provides options for building, running, cleaning, and testing your current project.

Mekpie is a small scale project and is not supposed to replace tools like [CMake](https://cmake.org/) or provide any sort of package management capabilities. Use Mekpie when the alternative is a shoddy Make file or manually compiling.

## Installing

*Coming soon*

Mekpie is a python package. Use pip to install it!
```bash
$ pip install mekpie
```

## Getting Started

Create a new project by running
```bash
$ mekpie new "project-name"
project-name created succesfully!
```

Then navigate to the project directory and run
```bash
$ mekpie run
Project succesfully cleaned.
Project succesfully built.
Hello, World!
```

That's it!

## [Read More](https://ejrbuss.net/mekpie)

## Contact

Feel free to send be bug reports or feature requests. If you are interested in my other work, checkout my [website](https://ejrbuss.net).

Email ejrbuss@gmail.com