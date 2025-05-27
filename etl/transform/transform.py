# The following was adapted into "def load_csv_to_sqlite" within load.py


# def clean_games_csv(input_path, output_path):
#     with open(input_path, encoding='utf-8') as infile, \
#          open(output_path, 'w', newline='', encoding='utf-8') as outfile:
#         reader = csv.reader(infile)
#         writer = csv.writer(outfile)
#         writer.writerow(["app_id", "name", "release_date", "is_free", "type"])  # header

#         next(reader)  # skip input header
#         for i, row in enumerate(reader, start=2):
#             try:
#                 app_id = None
#                 for idx, val in enumerate(row):
#                     if val.isdigit():
#                         app_id = val
#                         app_id_idx = idx
#                         break
#                 if app_id is None:
#                     continue
#                 name = row[app_id_idx + 1]
#                 release_date = row[app_id_idx + 2]
#                 is_free = row[app_id_idx + 3]
#                 is_free = '1' if is_free.strip() == '1' else '0'
#                 type_col = None
#                 for val in row[app_id_idx + 4:]:
#                     if val.strip().lower() in ("game", "demo"):
#                         type_col = val.strip().lower()
#                         break
#                 if type_col is None:
#                     continue
#                 writer.writerow([app_id, name, release_date, is_free, type_col])
#             except Exception:
#                 continue