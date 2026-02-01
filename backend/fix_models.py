import re

with open('models.py', 'r') as f:
    lines = f.readlines()

# Fix line 16-17
if len(lines) > 16 and 'class Task(SQLModel, table=True):' in lines[15]:
    # Insert proper indentation
    lines.insert(16, '    priority: str = Field(default="medium")\n')
    # Remove the old line if it exists
    if len(lines) > 17 and 'priority: str = Field(default="medium")' in lines[16]:
        lines.pop(16)

with open('models.py', 'w') as f:
    f.writelines(lines)

print("Fixed models.py indentation")
