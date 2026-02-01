# Read the file
with open('models.py', 'r') as f:
    lines = f.readlines()

# Find and fix the Task class
new_lines = []
for i, line in enumerate(lines):
    if i == 16:  # This is the line number (0-indexed, so line 17)
        # Skip the unindented line
        continue
    elif i == 15 and 'class Task(SQLModel, table=True):' in line:
        # Add properly indented attributes after class definition
        new_lines.append(line)
        new_lines.append('    priority: str = Field(default="medium")\n')
    else:
        new_lines.append(line)

# Write back
with open('models.py', 'w') as f:
    f.writelines(new_lines)

print("Fixed models.py")
