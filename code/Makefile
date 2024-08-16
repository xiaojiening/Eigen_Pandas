# Define environment and compiler settings
PYTHON = /disk2/home/xiaojiening/miniconda3/envs/py3.12.0/bin/python
CPP_COMPILER = g++
CPP_FLAGS = -std=c++11 -O3 -march=native -fopenmp
CPP_SOURCE = process.cpp
CPP_EXE = process
DATA_DIR = ../data

# Default target: run all necessary steps
all: preprocess compile_cpp process_cpp process_py run_analysis

# Pre-process data with Python
preprocess:
	@echo "Pre-Processing... This may take around 3 minutes..."
	@$(PYTHON) preprocess.py

# Compile C++ source code
compile_cpp: $(CPP_SOURCE)
	@echo "Compiling C++ source..."
	@$(CPP_COMPILER) $(CPP_FLAGS) -o $(CPP_EXE) $(CPP_SOURCE)

# Process data using C++ executable
process_cpp: compile_cpp
	@echo "Processing with C++ (Eigen Version)..."
	@./$(CPP_EXE)

# Process data using Python script
process_py:
	@echo "Processing with Python (Pandas Version)..."
	@$(PYTHON) process.py

# Run the final analysis
run_analysis: process_cpp process_py
	@echo "Running analysis..."
	@$(PYTHON) analysis.py
	@echo "Analysis Done!"

# Clean up generated files
clean:
	@echo "Cleaning up..."
	@rm -f $(CPP_EXE)
	@rm -rf $(DATA_DIR)/*

# Declare phony targets to avoid conflicts with file names
.PHONY: all preprocess compile_cpp process_cpp process_py run_analysis clean
