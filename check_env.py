import os, pprint

print("SECRET_KEY env =", repr(os.environ.get("SECRET_KEY")))
print("\nENV keys containing SECRET_KEY:")
print({k:repr(v) for k,v in os.environ.items() if "SECRET_KEY" in k})
