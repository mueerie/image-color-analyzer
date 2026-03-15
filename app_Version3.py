pantone_data = pd.read_csv("pantone-list_Version2.csv", delimiter="\t")
pantone_data.columns = pantone_data.columns.str.strip()

def closest_pantone(rgb, pantone_list):
    min_dist = float('inf')
    closest = None
    for col in ["RED", "GREEN", "BLUE"]:
        if col not in pantone_list.columns:
            st.error(f"CSV未找到列：{col}，请检查表头为PANTONENAME, UNIQUECODE, RED, GREEN, BLUE，并且用Tab作为分隔符。")
            st.stop()
    for idx, row in pantone_list.iterrows():
        dist = np.linalg.norm(np.array(rgb) - np.array(row[["RED", "GREEN", "BLUE"]]))
        if dist < min_dist:
            min_dist = dist
            closest = row["PANTONENAME"]
    return closest