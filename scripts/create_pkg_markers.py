import os
for p in ["apps/__init__.py", "apps/api/__init__.py", "apps/api/core/__init__.py"]:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p):
        with open(p, "w") as f:
            f.write("# package marker\n")
