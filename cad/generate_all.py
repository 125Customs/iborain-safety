#!/usr/bin/env python3
"""
Iborain Safety — Master Unified 3D CAD Production Suite Generator
Compiles the Master Universal Autonomous Solar Sentry CAD Assembly and Slicing Plates.
"""
import os
import sys
import shell_universal_sentry

def main():
    print("=================================================================")
    print(" 🛡️ Iborain Safety — Compiling Master Unified Sentry CAD Models")
    print("=================================================================")
    shell_universal_sentry.generate_all()

if __name__ == "__main__":
    main()
