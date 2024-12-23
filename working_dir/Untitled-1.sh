python3 /Users/suya/Desktop/oscopilot/oscopilot/tool_repository/manager/tool_manager.py --add --tool_name add_new_sheet_to_excel --tool_path /Users/suya/Desktop/oscopilot/FRIDAY-Gizmos/Excel/add_new_sheet_to_excel.py

python3 oscopilot/tool_repository/manager/tool_manager.py --add --tool_name create_excel_horizontal_bar_chart --tool_path oscopilot/FRIDAY-Gizmos/Excel/create_excel_horizontal_bar_chart.py

python3 oscopilot/tool_repository/manager/tool_manager.py --add --tool_name read_excel_sheet --tool_path oscopilot/FRIDAY-Gizmos/Excel/read_excel_sheet.py

python quick_start.py --query "You need to do some tasks related to excel manipulation.\n My sheet records data from an experiment where one hanging block (m2) drags a block (m1=0.75 kg) on a frictionless table via a rope around a frictionless and massless pulley. It has a sheet called Sheet1. \n Your task is: Fill out the rest rows in column B using the formula in B2. Create a horizontal bar chart in Sheet1 with acceleration on the y-axis and the hanging mass on the x-axis. Add the corresponding column headers as the axis labels. \n You should complete the task and save the result directly in this excel file." --query_file_path "working_dir/Dragging.xlsx"

python3 oscopilot/tool_repository/manager/tool_manager.py --add --tool_name add_new_sheet_to_excel --tool_path FRIDAY-Gizmos/Excel/add_new_sheet_to_excel.py

python3 quick_start.py --query "Your task is to add a new worksheet named newsheet" --query_file_path "working_dir/test.xlsx"