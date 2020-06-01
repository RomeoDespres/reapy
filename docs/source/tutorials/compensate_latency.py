import reapy


project = reapy.Project()
for item in project.selected_items:
    item.position -= 0.16
